import pytest
import json

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    # Initialize the test database with some test data
    with app.app_context():
        cursor = app.db.cursor()
        
        # Create a test group
        cursor.execute('INSERT INTO groups (name) VALUES (?)', ('Test Group',))
        group_id = cursor.lastrowid
        
        # Create a test activity
        cursor.execute('INSERT INTO study_activities (name, url) VALUES (?, ?)', 
                      ('Test Activity', 'http://test.com'))
        activity_id = cursor.lastrowid
        
        # Create a test word with parts as JSON string
        cursor.execute('''
            INSERT INTO words (kanji, romaji, english, parts) 
            VALUES (?, ?, ?, ?)''',
            ('テスト', 'tesuto', 'test', json.dumps(['テス', 'ト']))
        )
        word_id = cursor.lastrowid
        
        # Associate word with group
        cursor.execute('INSERT INTO word_groups (word_id, group_id) VALUES (?, ?)',
                      (word_id, group_id))
        
        app.db.commit()
        
        yield {'group_id': group_id, 'activity_id': activity_id, 'word_id': word_id}
        
        # Clean up
        cursor.execute('DELETE FROM word_groups')
        cursor.execute('DELETE FROM words')
        cursor.execute('DELETE FROM groups')
        cursor.execute('DELETE FROM study_activities')
        app.db.commit()

def test_get_group_words_raw(client, init_database):
    # Test getting words from existing group
    response = client.get(f'/groups/{init_database["group_id"]}/words/raw')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'words' in data
    assert isinstance(data['words'], list)
    assert len(data['words']) > 0
    
    # Test non-existent group
    response = client.get('/groups/9999/words/raw')
    assert response.status_code == 404

def test_create_study_session(client, init_database):
    # Test successful creation
    response = client.post('/api/study-sessions',
        json={
            'group_id': init_database['group_id'],
            'study_activity_id': init_database['activity_id']
        })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'session_id' in data
    assert 'created_at' in data
    
    # Test missing fields
    response = client.post('/api/study-sessions', 
        json={'group_id': init_database['group_id']})
    assert response.status_code == 400
    
    # Test non-existent group
    response = client.post('/api/study-sessions', 
        json={
            'group_id': 9999,
            'study_activity_id': init_database['activity_id']
        })
    assert response.status_code == 404

def test_create_session_review(client, init_database):
    # First create a session
    response = client.post('/api/study-sessions',
        json={
            'group_id': init_database['group_id'],
            'study_activity_id': init_database['activity_id']
        })
    session_data = json.loads(response.data)
    session_id = session_data['session_id']
    
    # Test successful review submission
    response = client.post(f'/api/study-sessions/{session_id}/review', 
        json={
            'word_id': init_database['word_id'],
            'correct': True
        })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'review_id' in data
    assert 'created_at' in data
    
    # Test word not in group
    response = client.post(f'/api/study-sessions/{session_id}/review', 
        json={'word_id': 9999, 'correct': True})
    assert response.status_code == 403
    
    # Test non-existent session
    response = client.post('/api/study-sessions/9999/review', 
        json={'word_id': init_database['word_id'], 'correct': True})
    assert response.status_code == 404

def test_complete_study_flow(client, init_database):
    # 1. Get words from a group
    response = client.get(f'/groups/{init_database["group_id"]}/words/raw')
    assert response.status_code == 200
    words_data = json.loads(response.data)
    assert len(words_data['words']) > 0
    
    # 2. Create a study session
    response = client.post('/api/study-sessions',
        json={
            'group_id': init_database['group_id'],
            'study_activity_id': init_database['activity_id']
        })
    assert response.status_code == 201
    session_data = json.loads(response.data)
    session_id = session_data['session_id']
    
    # 3. Submit reviews for words
    word_id = init_database['word_id']
    response = client.post(f'/api/study-sessions/{session_id}/review', 
        json={'word_id': word_id, 'correct': True})
    assert response.status_code == 201
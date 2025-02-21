import os
import sys
import tempfile
import pytest

# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def init_db(app):
    with app.app_context():
        cursor = app.db.cursor()
        
        # Read and execute all SQL setup files
        sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'setup')
        
        # Order matters due to foreign key constraints
        setup_files = [
            'create_table_groups.sql',
            'create_table_words.sql',
            'create_table_word_groups.sql',
            'create_table_study_activities.sql',
            'create_table_study_sessions.sql',
            'create_table_word_review_items.sql'
        ]
        
        for filename in setup_files:
            with open(os.path.join(sql_dir, filename), 'r') as f:
                cursor.executescript(f.read())
        
        app.db.commit()

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    test_config = {
        'TESTING': True,
        'DATABASE': db_path  # Use the temporary database file
    }
    
    from app import create_app
    app = create_app(test_config)
    
    # Initialize the database with tables
    init_db(app)
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)
# API Documentation for New Endpoints

## GET /groups/:id/words/raw
Retrieves a raw list of words for a specific group, used by learning applications.

### Parameters
- `id` (path parameter): The ID of the group to fetch words from

### Response (200 OK)
```json
{
  "words": [
    {
      "id": number,
      "kanji": string,
      "romaji": string,
      "english": string
    }
  ]
}
```

### Errors
- 404: Group not found
- 500: Server error

## POST /study-sessions
Creates a new study session for a specific group and activity.

### Request Body
```json
{
  "group_id": number,
  "study_activity_id": number
}
```

### Response (201 Created)
```json
{
  "session_id": number,
  "created_at": string (ISO timestamp)
}
```

### Errors
- 400: Missing required fields
- 404: Group or activity not found
- 500: Server error

## POST /study-sessions/:id/review
Records a word review result for an ongoing study session.

### Parameters
- `id` (path parameter): The ID of the study session

### Request Body
```json
{
  "word_id": number,
  "correct": boolean
}
```

### Response (201 Created)
```json
{
  "review_id": number,
  "created_at": string (ISO timestamp)
}
```

### Errors
- 400: Missing required fields
- 403: Word does not belong to session's group
- 404: Study session not found
- 500: Server error


# Testing Guide

## Manual Testing Commands

### Get Raw Words
```bash
curl -X GET http://localhost:5000/groups/1/words/raw
```

### Create Study Session
```bash
curl -X POST http://localhost:5000/study-sessions \
  -H "Content-Type: application/json" \
  -d '{"group_id": 1, "study_activity_id": 1}'
```

### Submit Review
```bash
curl -X POST http://localhost:5000/study-sessions/1/review \
  -H "Content-Type: application/json" \
  -d '{"word_id": 1, "correct": true}'
```
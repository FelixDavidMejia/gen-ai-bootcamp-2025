# Role
 - Your role is Backend developer


# Introduction
This @backend-flask folder holds the source code for a simple backend API using Flask. The API is built using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/). This backend API is a prototype of learning portal for a language learning school. This app will act as three things:
 - Inventory of possible vocabulary that can be learned
 - Act as a Learning Record Store (LRS), providing correct and wrong score on practice vocabulary
 - A unified launchpad to launch different learning apps

# Your Mission
Your mission is to implement the missing endpoints. You will be helping me to find out which endpoints are missing, and to implement those missing endpoints.

# Clue of which endpoints are missing:

## GET /groups/:id/words/raw

This endpoint is responsible for providing a payload to the language app, that has to know the vocabulary to be used in the current session. All this endpoint does is to return a very specific structure of JSON data. The structure will be expected by the frontend. Consulting the structure expected by the frontend, we can find the structure we must use for this endpoint.

## POST /study_sessions

This endpoint actually creates a study session in the DB so the app can track the review words that are being studied.
   
## POST /study_sessions/:id/review

This endpoint is what the learning app reports back to submit whether an answer got right or wrong.

# Other Considerations and Tips

 - In order to know the expected structure of the JSON payload, we can check what is expected or returned by the frontend.
 - The Frontend application is located in the `frontend-react` folder.
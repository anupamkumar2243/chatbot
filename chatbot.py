from flask import Flask, request
from google.cloud import dialogflow
import os
import twilio
from twilio.twiml.messaging_response import MessagingResponse
import uuid

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_incoming_message():
    # Get the incoming message from Twilio
    incoming_message = request.values.get("Body", "")

    # Use the Dialogflow API to process the incoming message
    project_id = os.getenv("dining-out-ufhe")
    session_id = str(uuid.uuid1())
    language_code = "en-US"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=incoming_message, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    # Get the response from Dialogflow
    reply = response.query_result.fulfillment_text

    # Send the response back to Twilio
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

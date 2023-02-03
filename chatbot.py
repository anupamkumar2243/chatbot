from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# Your Twilio account SID and Auth Token
account_sid = 'ACee517d6a707743d96d48aab9ee5f2034'
auth_token = 'b71741aec4a3af0ed5673116ad4b85db'

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# The Twilio Sandbox number
from_ = 'whatsapp:+14155238886'

@app.route('/', methods=['POST'])
def handle_request():
    # Get the request data from Dialogflow
    req = request.get_json(silent=True, force=True)
    
    # Extract the action and parameters from the request
    action = req['queryResult']['action']
    parameters = req['queryResult']['parameters']
    
    # Send a message to WhatsApp using Twilio
    if action == 'send_message':
        to = parameters['+91 63517 28234']
        message = parameters['message']
        client.messages.create(
            from_=from_,
            body=message,
            to=f'whatsapp:{to}'
        )
        response = "Message sent."
    else:
        response = "Action not supported."
    
    # Return the response to Dialogflow
    return {
        "fulfillmentText": response
    }

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)))

import os
from flask import Flask, render_template, request
from twilio.rest import Client

app = Flask(__name__)

# Fetch keys from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    number = request.form.get('phone')
    results = None
    try:
        # Twilio Lookup V2 API
        fetch_info = client.lookups.v2.phone_numbers(number).fetch(fields='caller_name,line_type_intelligence')
        
        results = {
            "Number": fetch_info.phone_number,
            "Carrier": fetch_info.line_type_intelligence.get('carrier_name', 'Unknown'),
            "Name": fetch_info.caller_name.get('caller_name') if fetch_info.caller_name else "Not Found",
            "Type": fetch_info.line_type_intelligence.get('type', 'Mobile')
        }
    except Exception as e:
        results = {"Name": "Error", "Carrier": str(e), "Type": "N/A"}
    
    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)


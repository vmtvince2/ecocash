from flask import Flask, jsonify, request
import http.client
import json
import uuid

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def payment():
    try:
        # Generate a UUID for the sourceReference
        source_reference = str(uuid.uuid4())
        
        # Get data from the request
        data = request.json
        phone = data.get('phone')
        amount = data.get('amount')
        currency = data.get('currency')     # Default currency for testing

        # Prepare the payload
        payload = json.dumps({
            "customerMsisdn": phone,
            "amount": amount,
            "reason": "Payment",
            "currency": "USD",
            "sourceReference": source_reference
        })

        # Set the headers
        headers = {
            'X-API-KEY': 'yfsGMcWVQHFKphbASvhmexrox3FPyNky',  # Your API key
            'Content-Type': 'application/json'                 # Content type
        }

        # Create a connection to the EcoCash API
        conn = http.client.HTTPSConnection("developers.ecocash.co.zw")

        # Make the POST request
        conn.request("POST", "/api/ecocash_pay/api/v2/payment/instant/c2b/sandbox", payload, headers)

        # Get the response
        res = conn.getresponse()
        data = res.read()

        # Close the connection
        conn.close()

        # Return the response from the EcoCash API
        return jsonify(json.loads(data.decode("utf-8"))), res.status

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode

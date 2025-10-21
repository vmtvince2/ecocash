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
        currency = data.get('currency') 
        game = data.get('game')# Default currency for testing

        if not phone or not amount or not currency:
            return jsonify({"error": "Missing required fields."}), 400

        # Ensure phone number is formatted as 263 followed by the number
        if not phone.startswith("263"):
            if phone.startswith("0"):
                phone = "263" + phone[1:]  # Remove leading zero and prepend 263
            else:
                phone = "263" + phone  # Prepend 263 if no leading zero

        # Prepare the payload for EcoCash
        payload = json.dumps({
            "customerMsisdn": phone,
            "amount": amount,
            "reason": "Payment",
            "currency": "USD",
            "sourceReference": source_reference
        })

        # Set the headers for EcoCash
        headers = {
            'X-API-KEY': 'yfsGMcWVQHFKphbASvhmexrox3FPyNky',  # Your API key
            'Content-Type': 'application/json'                 # Content type
        }

        # Create a connection to the EcoCash API
        conn = http.client.HTTPSConnection("developers.ecocash.co.zw")

        # Make the POST request to EcoCash
        conn.request("POST", "/api/ecocash_pay/api/v2/payment/instant/c2b/sandbox", payload, headers)

        # Get the response from EcoCash
        res = conn.getresponse()
        eco_response = res.read()
        conn.close()

        # Send the sourceReference and phone number to the specified endpoint
        callback_payload = json.dumps({
            "sourceReference": source_reference,
            "phone": phone,
            "game": game
        })

        # Set headers for the callback request
        callback_headers = {
            'Content-Type': 'application/json'  # Content type for the callback
        }

        # Create a connection to the callback URL
        callback_conn = http.client.HTTPSConnection("zimbabwe.mchezoradio.com")

        # Make the POST request to the callback URL
        callback_conn.request("POST", "/transaction/process", callback_payload, callback_headers)

        # Get the response from the callback
        callback_res = callback_conn.getresponse()
        callback_data = callback_res.read()
        callback_conn.close()

        # Log the response from the callback for debugging
        print("Callback response:", callback_data.decode("utf-8"))

        # Return the response from the EcoCash API
        return jsonify(json.loads(eco_response.decode("utf-8"))), res.status

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode

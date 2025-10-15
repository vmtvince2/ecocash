
import requests
import json
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/payment', methods=['POST'])
def payment():
    try:
        new_reference = str(uuid.uuid4())
        data = request.json
        phone = data.get('phone')
        amount = data.get('amount')
        currency = data.get('currency')

        if not phone or not amount or not currency:
            return jsonify({"error": "Missing required fields."}), 400

        # Ensure phone number is formatted as 263 followed by the number
        if not phone.startswith("263"):
            if phone.startswith("0"):
                phone = "263" + phone[1:]  # Remove leading zero and prepend 263
            else:
                phone = "263" + phone  # Prepend 263 if no leading zero

        url = "https://developers.ecocash.co.zw/api/ecocash_pay/api/v2/payment/instant/c2b/sandbox"

        payload = json.dumps({
            "customerMsisdn": phone,
            "amount": amount,
            "reason": "Payment",
           # "currency": currency,
            "sourceReference": new_reference
        })

        headers = {
            'X-API-KEY': 'yfsGMcWVQHFKphbASvhmexrox3FPyNky',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            return jsonify({
                "status": response.status_code,
                "response": response.json()
            })
        else:
            return jsonify({
                "status": response.status_code,
                "error": "Error from external API.",
                "details": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run()


import requests
import json
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def payment():

    new_reference = str(uuid.uuid4())
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount')
    currency = data.get('currency')



    url = "https://developers.ecocash.co.zw/api/ecocash_pay/api/v2/payment/instant/c2b/sandbox"

    payload = json.dumps({
        "customerMsisdn": phone,
        "amount": amount,
        "reason": "Payment",
        "currency": "USD",
        "sourceReference": new_reference
    })

    headers = {
        'X-API-KEY': 'yfsGMcWVQHFKphbASvhmexrox3FPyNky',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    return jsonify({
        "status": response.status_code,
        "response": response.json()
    })

if __name__ == '__main__':
    app.run()

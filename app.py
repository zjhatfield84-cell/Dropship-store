from flask import Flask, jsonify, request
import os
import stripe
from datetime import datetime

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Summer Vibes Dropshipping Store</h1>
    <p>Live on Render with Stripe!</p>
    <p><a href='/test-payment'>Test Payment</a></p>
    """

@app.route('/test-payment')
def test_payment():
    return """
    <h1>Test Stripe Payment</h1>
    <button onclick="startPayment()">Pay $29.99</button>
    <script>
    function startPayment() {
        fetch('/create-checkout-session', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({items: [{name: 'Turbo Fan', price: 29.99}]})
        }).then(r => r.json()).then(data => {
            if (data.url) window.location.href = data.url;
        });
    }
    </script>
    """

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': data['items'][0]['name']},
                    'unit_amount': int(data['items'][0]['price'] * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://the-collective-bn46.onrender.com/success',
            cancel_url='https://the-collective-bn46.onrender.com/',
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/success')
def success():
    return "<h1>✅ Payment Successful! Thank you.</h1><p>Your dropshipping order is processing.</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

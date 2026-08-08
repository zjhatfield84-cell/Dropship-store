from flask import Flask, jsonify, request
import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Summer Vibes Store</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 40px; background: #f0f0f0; }
            button { background: #28a745; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; }
            button:active { background: #218838; }
        </style>
    </head>
    <body>
        <h1>🌞 Summer Vibes Dropshipping Store</h1>
        <p>Test Product: Rechargeable Turbo Fan</p>
        <p><strong>$29.99</strong></p>
        <button onclick="pay()">Buy Now - Pay $29.99</button>

        <script>
        async function pay() {
            try {
                const response = await fetch('/create-checkout-session', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        items: [{ name: "Rechargeable Turbo Fan", price: 29.99 }]
                    })
                });
                const data = await response.json();
                if (data.url) {
                    window.location.href = data.url;
                } else {
                    alert("Error: " + (data.error || "Something went wrong"));
                }
            } catch (err) {
                alert("Error: " + err.message);
            }
        }
        </script>
    </body>
    </html>
    '''

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
    return '''
    <h1 style="text-align:center; color:green;">✅ Payment Successful!</h1>
    <p style="text-align:center;">Thank you for your order. Your product will ship soon.</p>
    <p style="text-align:center;"><a href="/">Back to Store</a></p>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

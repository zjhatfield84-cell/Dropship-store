from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_YOUR_KEY_HERE")  # Change later

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Rechargeable Handheld Turbo Fan", "price": 29.99, "original_price": 49.99, "description": "Powerful portable fan for summer heat.", "image": "fan.jpg", "category": "Cooling"},
    {"id": 2, "name": "Self-Cooling Pet Mat", "price": 34.99, "original_price": 59.99, "description": "Keeps pets cool in hot weather.", "image": "petmat.jpg", "category": "Pet"},
    {"id": 3, "name": "Waterproof Floating Phone Pouch", "price": 19.99, "original_price": 29.99, "description": "Protect your phone at beach/pool.", "image": "pouch.jpg", "category": "Travel"},
    {"id": 4, "name": "Sand-Free Beach Blanket", "price": 39.99, "original_price": 59.99, "description": "Lightweight beach blanket.", "image": "blanket.jpg", "category": "Beach"},
    {"id": 5, "name": "Portable Neck Fan", "price": 27.99, "original_price": 44.99, "description": "Hands-free personal cooling.", "image": "neckfan.jpg", "category": "Cooling"},
    {"id": 6, "name": "Posture Corrector Brace", "price": 24.99, "original_price": 39.99, "description": "Improves posture instantly.", "image": "posture.jpg", "category": "Wellness"}
]

orders = []

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Not found", 404
    return render_template('product.html', product=product)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        items = data.get('items', [])
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item['name']},
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': 1,
            })
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://your-render-url/success',
            cancel_url='https://your-render-url/',
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

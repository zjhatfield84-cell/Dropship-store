from flask import Flask, jsonify, request
import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

PRODUCTS = [
    {
        "id": 1,
        "name": "Astronaut Neck Fan",
        "price": 26.00,
        "desc": "Cute astronaut design, hands-free portable neck fan. Perfect for outdoor use.",
        "image": "https://m.media-amazon.com/images/I/61pZ8Y8Y8YL._AC_SL1500_.jpg"
    },
    {
        "id": 2,
        "name": "Refrigeration Handheld Turbo Fan",
        "price": 30.00,
        "desc": "Powerful high-speed turbo fan with strong airflow. USB rechargeable.",
        "image": "https://m.media-amazon.com/images/I/71kdcW5h+wL._AC_SL1500_.jpg"
    },
    {
        "id": 3,
        "name": "Portable Neck Fan Handheld Mini Fan",
        "price": 27.00,
        "desc": "Versatile 2-in-1 neck & handheld mini fan. Quiet and lightweight.",
        "image": "https://m.media-amazon.com/images/I/71ecgG1ixBL._AC_SL1500_.jpg"
    },
    {
        "id": 4,
        "name": "Waterproof Phone Pouch for Swimming",
        "price": 17.00,
        "desc": "Touchscreen waterproof phone pouch. Protects your phone at the beach or pool.",
        "image": "https://m.media-amazon.com/images/I/71Rynapac.jpg"
    },
]

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Summer Vibes Store</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }
            .container { max-width: 480px; margin: 0 auto; }
            h1 { text-align: center; color: #1a1a1a; margin-bottom: 5px; }
            .subtitle { text-align: center; color: #666; margin-bottom: 25px; }
            .product {
                background: white;
                border-radius: 16px;
                padding: 18px;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                text-align: center;
            }
            .product img {
                width: 100%;
                max-height: 220px;
                object-fit: contain;
                border-radius: 12px;
                background: #f8f8f8;
                margin-bottom: 12px;
            }
            .product h3 { margin: 8px 0 6px; font-size: 18px; color: #222; }
            .product p { color: #555; font-size: 14px; margin: 0 0 12px; line-height: 1.4; }
            .price { font-size: 24px; font-weight: bold; color: #16a34a; margin-bottom: 14px; }
            button {
                background: #16a34a;
                color: white;
                border: none;
                padding: 14px;
                font-size: 16px;
                border-radius: 10px;
                width: 100%;
                font-weight: 600;
                cursor: pointer;
            }
            button:active { background: #15803d; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌞 Summer Vibes Store</h1>
            <p class="subtitle">Cool products • Fast shipping</p>
    '''

    for p in PRODUCTS:
        html += f'''
            <div class="product">
                <img src="{p["image"]}" alt="{p["name"]}" 
                     onerror="this.src='https://placehold.co/400x300/e2e8f0/64748b?text={p["name"].replace(" ", "+")}'">
                <h3>{p["name"]}</h3>
                <p>{p["desc"]}</p>
                <div class="price">${p["price"]:.2f}</div>
                <button onclick="buy('{p["name"]}', {p["price"]})">Buy Now</button>
            </div>
        '''

    html += '''
        </div>
        <script>
        async function buy(name, price) {
            try {
                const response = await fetch('/create-checkout-session', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ items: [{ name: name, price: price }] })
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
    return html

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': data['items'][0]['name']
                    },
                    'unit_amount': int(data['items'][0]['price'] * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            shipping_address_collection={
                'allowed_countries': ['US'],
            },
            success_url='https://the-collective-bn46.onrender.com/success',
            cancel_url='https://the-collective-bn46.onrender.com/',
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/success')
def success():
    return '''
    <div style="text-align:center; padding:50px; font-family:Arial;">
        <h1 style="color:green;">✅ Payment Successful!</h1>
        <p>Thank you for your order. Your product will ship soon.</p>
        <p>We will email you the tracking number once it ships.</p>
        <a href="/">Back to Store</a>
    </div>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

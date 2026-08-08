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
        "image": "https://m.media-amazon.com/images/I/61+5+5+5+5L._AC_SL1500_.jpg"
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
        "image": "https://m.media-amazon.com/images/I/71+5+5+5+5L._AC_SL1500_.jpg"
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
            body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
            .container { max-width: 500px; margin: 0 auto; }
            h1 { text-align: center; color: #333; }
            .product { border: 1px solid #ddd; border-radius: 12px; padding: 20px; margin: 15px 0; background: white; text-align: center; }
            .product img { max-width: 100%; height: 180px; object-fit: contain; border-radius: 8px; margin-bottom: 10px; }
            button { background: #28a745; color: white; border: none; padding: 14px 25px; font-size: 16px; border-radius: 8px; width: 100%; font-weight: bold; }
            .price { font-size: 22px; font-weight: bold; color: #28a745; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌞 Summer Vibes Store</h1>
            <p style="text-align:center; color:#666;">Top summer products • Fast shipping</p>
    '''

    for p in PRODUCTS:
        html += f'''
            <div class="product">
                <img src="{p["image"]}" alt="{p["name"]}" onerror="this.src='https://via.placeholder.com/300x180?text=Product'">
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

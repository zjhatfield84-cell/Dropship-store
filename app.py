from flask import Flask, jsonify, request
import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Rechargeable Handheld Turbo Fan", "price": 29.99, "desc": "Powerful portable fan for summer heat. USB rechargeable."},
    {"id": 2, "name": "Self-Cooling Pet Mat", "price": 34.99, "desc": "Keeps dogs and cats cool. No electricity needed."},
    {"id": 3, "name": "Waterproof Phone Pouch", "price": 19.99, "desc": "Floats and protects your phone at the beach or pool."},
    {"id": 4, "name": "Sand-Free Beach Blanket", "price": 39.99, "desc": "Lightweight, sand-repellent, perfect for summer."},
    {"id": 5, "name": "Portable Neck Fan", "price": 27.99, "desc": "Hands-free personal cooling fan."},
    {"id": 6, "name": "Posture Corrector Brace", "price": 24.99, "desc": "Improves posture instantly. Adjustable & breathable."},
]

@app.route('/')
def home():
    products_html = ""
    for p in PRODUCTS:
        products_html += f'''
        <div style="border:1px solid #ddd; border-radius:12px; padding:20px; margin:15px 0; background:white;">
            <h3>{p["name"]}</h3>
            <p>{p["desc"]}</p>
            <p style="font-size:20px; font-weight:bold; color:#28a745;">${p["price"]}</p>
            <button onclick="buy({p['id']}, '{p["name"]}', {p["price"]})" 
                style="background:#28a745; color:white; border:none; padding:12px 25px; font-size:16px; border-radius:8px; width:100%;">
                Buy Now
            </button>
        </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Summer Vibes Dropshipping Store</title>
        <style>
            body {{ font-family: Arial, sans-serif; background:#f5f5f5; margin:0; padding:20px; }}
            h1 {{ text-align:center; color:#333; }}
            .container {{ max-width:500px; margin:0 auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌞 Summer Vibes Store</h1>
            <p style="text-align:center;">Top selling products • Fast shipping</p>
            {products_html}
        </div>

        <script>
        async function buy(id, name, price) {{
            try {{
                const response = await fetch('/create-checkout-session', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ items: [{{ name: name, price: price }}] }})
                }});
                const data = await response.json();
                if (data.url) {{
                    window.location.href = data.url;
                }} else {{
                    alert("Error: " + (data.error || "Something went wrong"));
                }}
            }} catch (err) {{
                alert("Error: " + err.message);
            }}
        }}
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
            line_items=[{{
                'price_data': {{
                    'currency': 'usd',
                    'product_data': {{'name': data['items'][0]['name']}},
                    'unit_amount': int(data['items'][0]['price'] * 100),
                }},
                'quantity': 1,
            }}],
            mode='payment',
            success_url='https://the-collective-bn46.onrender.com/success',
            cancel_url='https://the-collective-bn46.onrender.com/',
        )
        return jsonify({{'url': session.url}})
    except Exception as e:
        return jsonify({{'error': str(e)}}), 400

@app.route('/success')
def success():
    return '''
    <div style="text-align:center; padding:50px; font-family:Arial;">
        <h1 style="color:green;">✅ Payment Successful!</h1>
        <p>Thank you for your order. Your product will ship soon.</p>
        <a href="/">Back to Store</a>
    </div>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

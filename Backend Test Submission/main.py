from flask import Flask, request, jsonify, redirect
from middleware import logging_middleware
from util import generate_shortcode, is_valid_shortcode
from store import add_url, get_url, shortcode_exists

app = Flask(__name__)
app.wsgi_app = logging_middleware(app.wsgi_app)

@app.route("/shorturls", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    validity = int(data.get("validity", 30)) 
    custom_code = data.get("custom_code")

    if not long_url or not isinstance(long_url, str):
        return jsonify({"error": "Invalid or missing URL"}), 400

    if custom_code:
        if not is_valid_shortcode(custom_code):
            return jsonify({"error": "Invalid custom shortcode"}), 400
        if shortcode_exists(custom_code):
            return jsonify({"error": "Custom shortcode already exists"}), 409
        shortcode = custom_code
    else:
        
        for _ in range(5):  
            shortcode = generate_shortcode()
            if not shortcode_exists(shortcode):
                break
        else:
            return jsonify({"error": "Unable to generate unique shortcode"}), 500

    add_url(shortcode, long_url, validity)
    return jsonify({
        "short_url": f"http://localhost:5000/{shortcode}",
        "valid_for_minutes": validity
    }), 201

@app.route("/<string:code>")
def redirect_url(code):
    long_url, error = get_url(code)
    if error == "Not Found":
        return jsonify({"error": "Shortcode does not exist"}), 404
    if error == "Expired":
        return jsonify({"error": "Shortcode has expired"}), 410
    return redirect(long_url, code=302)

if __name__ == "__main__":
    app.run(debug=True)



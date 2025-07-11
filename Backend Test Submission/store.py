from datetime import datetime, timedelta

url_store = {}  # key = shortcode, value = {url, expiry_time}

def add_url(shortcode, long_url, validity_minutes):
    expiry = datetime.now() + timedelta(minutes=validity_minutes)
    url_store[shortcode] = {"url": long_url, "expiry": expiry}

def get_url(shortcode):
    data = url_store.get(shortcode)
    if not data:
        return None, "Not Found"
    if datetime.now() > data["expiry"]:
        return None, "Expired"
    return data["url"], None

def shortcode_exists(shortcode):
    return shortcode in url_store

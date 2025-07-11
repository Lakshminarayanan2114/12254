import random
import string

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_shortcode(code):
    return code.isalnum() and 3 <= len(code) <= 10

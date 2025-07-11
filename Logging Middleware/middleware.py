from datetime import datetime
from flask import request

def logging_middleware(app):
    def middleware(environ, start_response):
        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        method = environ.get('REQUEST_METHOD')
        path = environ.get('PATH_INFO')
        ip = environ.get('REMOTE_ADDR')
        log_line = f"[{request_time}] {ip} {method} {path}"
        with open("requests.log", "a") as log_file:
            log_file.write(log_line + "\n")
        return app(environ, start_response)
    return middleware

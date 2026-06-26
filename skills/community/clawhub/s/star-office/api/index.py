from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "service": "star-office-ui",
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "path": self.path
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.do_GET()

# Also provide Flask-like interface for local dev
try:
    from flask import Flask, jsonify, request
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return jsonify({
            "service": "star-office-ui",
            "status": "ok", 
            "timestamp": datetime.now().isoformat()
        })

    @app.route("/")
    def index():
        return jsonify({
            "service": "Star Office UI",
            "status": "running on Vercel",
            "endpoints": ["/health"]
        })

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 19000)))
except ImportError:
    pass  # Flask not available in serverless env
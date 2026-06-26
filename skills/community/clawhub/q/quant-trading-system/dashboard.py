#!/usr/bin/env python3
"""Simple Dashboard Server"""
import json
import http.server
import socketserver
from urllib.parse import urlparse

PORT = 5000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {"capital": 10000, "return": 0, "positions": 0, "strategies": 10}
            self.wfile.write(json.dumps(data).encode())
        elif self.path == "/strategies":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = ["momentum", "mean_reversion", "breakout", "macd_cross", "supertrend", "rsi_extreme", "bollinger_bounce", "trend_following", "volatility_breakout", "ai_hybrid"]
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
            <html><head><title>Quant Trading System V3</title></head>
            <body>
            <h1>📈 Quant Trading System V3</h1>
            <ul>
            <li><a href="/status">Status</a></li>
            <li><a href="/strategies">Strategies</a></li>
            </ul>
            </body></html>
            """
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        pass  # Suppress logs

print(f"Starting dashboard on http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()

#!/usr/bin/env python3
"""Simple webhook receiver for SMS gateway."""
import os
import sys
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

# OpenClaw webhook endpoint (set via env or default)
OPENCLAW_URL = os.environ.get('OPENCLAW_WEBHOOK_URL', 'http://localhost:8080/webhook')

class SMSWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            print(f"📥 Incoming SMS webhook received")
            print(f"   Event: {self.path}")
            print(f"   Data: {json.dumps(data, indent=2)}")
            
            # Forward to OpenClaw if configured
            if OPENCLAW_URL != 'disabled':
                try:
                    req = urllib.request.Request(
                        OPENCLAW_URL,
                        data=body,
                        headers={'Content-Type': 'application/json'},
                        method='POST'
                    )
                    urllib.request.urlopen(req, timeout=5)
                except Exception as e:
                    print(f"   ⚠️ Could not forward to OpenClaw: {e}")
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"invalid json"}')
    
    def do_GET(self):
        # Health check
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"sms-webhook-receiver"}')
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    
    server = HTTPServer(('0.0.0.0', port), SMSWebhookHandler)
    print(f"🌐 SMS Webhook Receiver running on http://0.0.0.0:{port}")
    print(f"   Forward to OpenClaw: {OPENCLAW_URL}")
    print(f"\nConfigure sms-gate.app webhook:")
    print(f"   URL: http://<this-mac-ip>:{port}/sms-received")
    print(f"   Event: sms:received")
    print(f"\nOr with ngrok: https://xxxx.ngrok.io/sms-received")
    print(f"\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        server.shutdown()

if __name__ == '__main__':
    main()

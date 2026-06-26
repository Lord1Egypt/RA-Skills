#!/usr/bin/env python3
"""Minimal webhook server with HMAC verification and routing."""
import http.server
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure your secrets here (or via env vars)
_config_path = Path(__file__).parent.parent / "config" / "webhook_secret.txt"
WEBHOOK_SECRET = _config_path.read_text().strip() if _config_path.exists() else os.environ.get("WEBHOOK_SECRET", "")

# Route table: event_type -> handler_function_name
ROUTES = {}

def verify_signature(payload_bytes: bytes, signature: str, secret: str = WEBHOOK_SECRET) -> bool:
    """Verify HMAC-SHA256 signature from provider."""
    if not secret:
        return True  # Skip verification if no secret configured
    expected = hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

def route_event(event_type: str, payload: dict) -> dict:
    """Route event to appropriate handler."""
    handler_name = ROUTES.get(event_type, "handle_default")
    handler = globals().get(handler_name)
    if handler:
        return handler(payload)
    return {"status": "no_handler", "event": event_type}

def handle_default(payload: dict) -> dict:
    """Default handler for unknown events."""
    logger.info(f"Default handler received: {payload}")
    return {"status": "processed"}

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            signature = self.headers.get("X-Hub-Signature-256", "") or \
                        self.headers.get("X-Signature-256", "") or \
                        self.headers.get("X-Slack-Signature", "")

            if signature and not verify_signature(body, signature, WEBHOOK_SECRET):
                logger.warning("Invalid signature — rejecting request")
                self.send_response(401)
                self.end_headers()
                return

            try:
                payload = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                self.send_response(400)
                self.end_headers()
                return

            event_type = self.headers.get("X-GitHub-Event") or \
                        self.headers.get("X-Slack-Event-Type") or \
                        payload.get("type", "") or \
                        "unknown"

            result = route_event(event_type, payload)
            logger.info(f"Routed {event_type} -> {result}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            logger.exception(f"Webhook error: {e}")
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        logger.info(format % args)

def run(port=8443):
    server = http.server.HTTPServer(("0.0.0.0", port), WebhookHandler)
    logger.info(f"Webhook server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8443
    run(port)
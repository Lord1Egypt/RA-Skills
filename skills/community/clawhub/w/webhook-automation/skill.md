---
name: webhook-automation
description: "Event-driven webhook workflows with HMAC verification, retry logic, and multi-provider patterns. Use when: (1) receiving webhooks from GitHub, Stripe, Slack, or any provider, (2) building automated pipelines that react to external events, (3) validating webhook signatures and filtering spoofed requests, (4) retrying failed deliveries with exponential backoff, (5) routing webhook payloads to different handlers based on event type. Triggers on: webhook, endpoint, HMAC, signature, GitHub webhook, Stripe webhook, Slack events, webhooks, receive webhook, verify signature, retry failed."
---

# Webhook Automation

Build reliable webhook endpoints that verify signatures, parse payloads, route events, retry failures, and integrate with any service.

## Why This Matters

Webhooks are how the outside world talks to your agent. But raw webhooks are dangerous — anyone can POST fake events. This skill teaches you to:
1. **Verify authenticity** — HMAC signatures prove the sender is real
2. **Parse reliably** — handle JSON, form data, and edge cases
3. **Route smartly** — different event types go to different handlers
4. **Retry gracefully** — failed work gets retried, not lost

## Quick Start

### 1. Create the Webhook Server

Save as `scripts/webhook_server.py`:

```python
#!/usr/bin/env python3
"""Minimal webhook server with HMAC verification and routing."""
import http.server
import hashlib
import hmac
import json
import logging
from urllib.parse import parse_qs
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure your secrets here (or via env vars)
WEBHOOK_SECRET = Path("config/webhook_secret.txt").read_text().strip() if Path("config/webhook_secret.txt").exists() else ""

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
            # Read raw body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            # Get signature header (varies by provider)
            signature = self.headers.get("X-Hub-Signature-256", "") or \
                        self.headers.get("X-Signature-256", "") or \
                        self.headers.get("X-Slack-Signature", "")

            # Verify signature
            if signature and not verify_signature(body, signature, WEBHOOK_SECRET):
                logger.warning("Invalid signature — rejecting request")
                self.send_response(401)
                self.end_headers()
                return

            # Parse JSON
            try:
                payload = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                self.send_response(400)
                self.end_headers()
                return

            # Extract event type
            event_type = self.headers.get("X-GitHub-Event") or \
                        self.headers.get("X-Slack-Event-Type") or \
                        payload.get("type", "") or \
                        "unknown"

            # Route and respond
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
    run()
```

### 2. Create Event Handlers

Save as `scripts/handlers.py`:

```python
"""Webhook event handlers — add your logic here."""
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# --- GitHub Handlers ---

def handle_github_push(payload: dict) -> dict:
    """Handle GitHub push event."""
    repo = payload.get("repository", {}).get("full_name", "")
    branch = payload.get("ref", "").split("/")[-1]
    commits = payload.get("commits", [])
    logger.info(f"GitHub push to {repo}/{branch}: {len(commits)} commits")
    return {"status": "ok", "repo": repo, "branch": branch, "commits": len(commits)}

def handle_github_pull_request(payload: dict) -> dict:
    """Handle GitHub PR event."""
    action = payload.get("action", "")
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {}).get("full_name", "")
    logger.info(f"GitHub PR {action} on {repo}: #{pr.get('number')} {pr.get('title', '')}")
    return {"status": "ok", "action": action, "pr": pr.get("number"), "title": pr.get("title")}

def handle_github_issue(payload: dict) -> dict:
    """Handle GitHub issue event."""
    action = payload.get("action", "")
    issue = payload.get("issue", {})
    logger.info(f"GitHub issue {action}: #{issue.get('number')} {issue.get('title', '')}")
    return {"status": "ok", "action": action, "issue": issue.get("number")}

# --- Slack Handlers ---

def handle_slack_event(payload: dict) -> dict:
    """Handle Slack event callback."""
    event = payload.get("event", {})
    event_type = event.get("type", "")
    logger.info(f"Slack event: {event_type}")
    return {"status": "ok", "event_type": event_type}

def handle_slack_url_verification(payload: dict) -> dict:
    """Respond to Slack URL verification challenge."""
    return {"challenge": payload.get("challenge", "")}

# --- Stripe Handlers ---

def handle_stripe_webhook(payload: dict) -> dict:
    """Handle Stripe webhook."""
    event_type = payload.get("type", "")
    logger.info(f"Stripe event: {event_type}")
    # Add your Stripe logic here (invoices, payments, subscriptions, etc.)
    return {"status": "ok", "event_type": event_type}

# --- Generic Handlers ---

def handle_default(payload: dict) -> dict:
    """Catch-all for unhandled events."""
    logger.info(f"Default handler: {json.dumps(payload)[:200]}")
    return {"status": "processed"}
```

### 3. Wire Up Routes

After `handlers.py`, add to `webhook_server.py`:

```python
# In webhook_server.py, import handlers and set routes:
from scripts.handlers import (
    handle_github_push, handle_github_pull_request, handle_github_issue,
    handle_slack_event, handle_slack_url_verification,
    handle_stripe_webhook, handle_default
)

ROUTES = {
    # GitHub
    "push": "handle_github_push",
    "pull_request": "handle_github_pull_request",
    "issues": "handle_github_issue",
    # Slack
    "event_callback": "handle_slack_event",
    "url_verification": "handle_slack_url_verification",
    # Stripe
    "invoice.paid": "handle_stripe_webhook",
    "customer.subscription.deleted": "handle_stripe_webhook",
    # Default
    "unknown": "handle_default"
}
```

## Recipes

### Recipe 1: GitHub Webhook → Discord Notification

Schedule an agent task that polls for GitHub events and posts to Discord:

```json
cron_add(
  name="GitHub webhook relay",
  schedule={"kind": "cron", "expr": "*/5 * * * *", "tz": "UTC"},
  payload={
    "kind": "agentTurn",
    "message": "Run: python scripts/check_github_events.py. For each new push/PR, format as: **[REPO]** [BRANCH] — N commits. Post to Discord #github channel."
  },
  delivery={"mode": "announce"},
  sessionTarget="isolated"
)
```

### Recipe 2: Stripe → Notion (Payment Recording)

When Stripe sends an `invoice.paid` event:

```python
def handle_stripe_invoice_paid(payload: dict) -> dict:
    """Record paid invoice to Notion database."""
    invoice_id = payload.get("data", {}).get("object", {}).get("id", "")
    amount = payload.get("data", {}).get("object", {}).get("amount_paid", 0) / 100
    customer = payload.get("data", {}).get("object", {}).get("customer_email", "")
    date = payload.get("created", 0)

    # Create Notion page (requires notion-integration skill)
    create_notion_page(
        database_id="YOUR_DATABASE_ID",
        properties={
            "Invoice ID": invoice_id,
            "Amount": amount,
            "Customer": customer,
            "Date": datetime.fromtimestamp(date).isoformat()
        },
        content=f"Invoice {invoice_id} paid: ${amount}"
    )
    return {"status": "recorded"}
```

### Recipe 3: Retry Queue for Failed Deliveries

```python
import time
from pathlib import Path

RETRY_FILE = Path("data/failed_webhooks.json")
MAX_RETRIES = 5

def record_failure(event: dict, error: str):
    failures = json.loads(RETRY_FILE.read_text()) if RETRY_FILE.exists() else []
    failures.append({"event": event, "error": error, "attempt": 0, "next_retry": time.time() + 300})
    RETRY_FILE.write_text(json.dumps(failures, indent=2))

def process_retries():
    if not RETRY_FILE.exists():
        return
    failures = json.loads(RETRY_FILE.read_text())
    remaining = []
    for f in failures:
        if f["attempt"] >= MAX_RETRIES:
            logger.error(f"Max retries reached for: {f['event']}")
            continue
        if time.time() < f["next_retry"]:
            remaining.append(f)
            continue
        # Retry
        result = deliver_webhook(f["event"])
        if result.get("success"):
            logger.info(f"Retry succeeded for: {f['event']}")
        else:
            f["attempt"] += 1
            f["next_retry"] = time.time() + (2 ** f["attempt"]) * 60
            remaining.append(f)
    RETRY_FILE.write_text(json.dumps(remaining, indent=2))
```

### Recipe 4: Webhook Signature Verification (GitHub-Style)

```python
import hmac
import hashlib

def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub's HMAC-SHA256 webhook signature."""
    if not signature.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

def verify_slack_signature(payload: bytes, timestamp: str, signature: str, secret: str) -> bool:
    """Verify Slack's signing secret."""
    base = f"v0:{timestamp}:{payload.decode()}".encode()
    expected = "v0=" + hmac.new(secret.encode(), base, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def verify_stripe_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """Verify Stripe webhook signature."""
    elements = dict(item.split("=") for item in signature_header.split(","))
    timestamp = elements.get("t", "")
    expected_sig = elements.get("v1", "")
    payload_with_ts = f"{timestamp}.".encode() + payload
    computed = hmac.new(secret.encode(), payload_with_ts, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, expected_sig)
```

### Recipe 5: Webhook → Agent Task (Event-Driven Automation)

```python
def route_to_agent(event_type: str, payload: dict):
    """Convert webhook payload into an agent task message."""
    messages = {
        "push": f"New GitHub push: {payload.get('repository', {}).get('full_name', '')} on {payload.get('ref', '')}. Check for breaking changes and report.",
        "pull_request": f"PR opened: {payload.get('pull_request', {}).get('title', '')}. Review the diff and post findings to #pr-review channel.",
        "invoice.paid": f"Payment received: ${payload.get('data', {}).get('object', {}).get('amount_paid', 0) / 100} from {payload.get('data', {}).get('object', {}).get('customer_email', '')}. Record to Notion."
    }
    return messages.get(event_type, f"Webhook event: {event_type}")
```

## Provider-Specific Notes

### GitHub
- Set `Content-Type: application/json` in webhook config
- Secret is set per-webhook in GitHub settings
- Signature header: `X-Hub-Signature-256` (format: `sha256=<hex>`)
- Event type header: `X-GitHub-Event`

### Slack
- Requires URL verification challenge response
- Signature: `X-Slack-Signature` header, verified against `X-Slack-Request-Timestamp`
- Events need to respond within 3 seconds — use the handler to queue work for later

### Stripe
- Signature: `Stripe-Signature` header (format: `t=<timestamp>,v1=<sig>`)
- Always use the Stripe SDK for signature verification
- 90-day retention of webhook payload for replay

### Discord Webhooks
- Incoming webhooks are POST-only, no signature verification
- Use Discord's own bot for verified event handling instead

## Testing Your Webhook

```bash
# Send a test payload
curl -X POST http://localhost:8443/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{"repository": {"full_name": "test/repo"}, "ref": "refs/heads/main", "commits": [{"message": "test"}]}'

# Test with signature (requires secret configured)
SIGNATURE=$(echo -n '{"test": true}' | openssl dgst -sha256 -hmac "your-secret" | sed 's/^.* //')
curl -X POST http://localhost:8443/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=$SIGNATURE" \
  -d '{"test": true}'
```

## Deployment Checklist

- [ ] Set `WEBHOOK_SECRET` (never hardcode in source)
- [ ] Use HTTPS in production (never raw HTTP for webhooks)
- [ ] Return 200 quickly — queue long work for later
- [ ] Log all received events with timestamp
- [ ] Set up retry queue for failed deliveries
- [ ] Monitor `/health` endpoint for uptime checks

## See Also

- `fuzzy-cron-scheduler` skill — for polling-based webhook alternatives
- `fuzzy-browser-automation` skill — for web scraping triggered by events
- `notion-integration` skill — for recording webhook events to Notion
- `discord` skill — for routing webhook alerts to Discord channels
- `rss-aggregator` skill — for feed-based event monitoring
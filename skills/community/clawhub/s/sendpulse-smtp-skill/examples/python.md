# Python examples

Official SDK: https://github.com/sendpulse/sendpulse-rest-api-python. Below: a
clean `requests`-based client (recommended for new code). For classic SMTP relay
via `smtplib` see [../references/smtp-relay.md](../references/smtp-relay.md).

## Minimal client with token caching

```python
import base64
import os
import time

import requests

API_BASE = "https://api.sendpulse.com"
_token_cache = {"token": None, "expires_at": 0}


def get_token() -> str:
    if _token_cache["token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["token"]

    resp = requests.post(f"{API_BASE}/oauth/access_token", json={
        "grant_type": "client_credentials",
        "client_id": os.environ["SENDPULSE_API_ID"],
        "client_secret": os.environ["SENDPULSE_API_SECRET"],
    }, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data["expires_in"] - 60
    return _token_cache["token"]


def api(method: str, path: str, **kwargs) -> dict:
    resp = requests.request(
        method, f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {get_token()}"},
        timeout=30, **kwargs,
    )
    if resp.status_code == 401:            # token expired mid-flight — refresh once
        _token_cache["token"] = None
        resp = requests.request(
            method, f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {get_token()}"},
            timeout=30, **kwargs,
        )
    resp.raise_for_status()
    return resp.json()


def send_email(subject: str, from_name: str, from_email: str,
               to_email: str, html: str, text: str,
               to_name: str = "") -> str:
    """Returns the SendPulse message id."""
    result = api("POST", "/smtp/emails", json={"email": {
        "subject": subject,
        "from": {"name": from_name, "email": from_email},
        "to": [{"name": to_name, "email": to_email}],
        "html": base64.b64encode(html.encode()).decode(),  # html MUST be base64
        "text": text,
    }})
    if not result.get("result"):
        raise RuntimeError(f"SendPulse rejected the email: {result}")
    return result["id"]


msg_id = send_email(
    subject="Order confirmed",
    from_name="My Shop", from_email="noreply@myshop.com",   # verified sender!
    to_email="jane@example.com", to_name="Jane",
    html="<h1>Hello!</h1><p>Your order #1234 is confirmed.</p>",
    text="Hello! Your order #1234 is confirmed.",
)
print("Message id:", msg_id)
```

## Template with variables & attachment

```python
with open("invoice.pdf", "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode()

api("POST", "/smtp/emails", json={"email": {
    "subject": "Your invoice",
    "from": {"name": "My Shop", "email": "billing@myshop.com"},
    "to": [{"email": "jane@example.com"}],
    "template": {"id": 12345, "variables": {"name": "Jane", "order_id": "1234"}},
    "attachments_binary": {"invoice.pdf": pdf_b64},
}})
```

## Hygiene: blocklist check, status, bounces

```python
# 1. Never send to unsubscribed addresses
info = api("GET", "/smtp/unsubscribe/search", params={"email": "jane@example.com"})

# 2. Delivery status of a sent message
status = api("GET", f"/smtp/emails/{msg_id}")

# 3. Daily cron: pull bounces, purge hard bounces from your own database
bounces = api("GET", "/smtp/bounces/day")
for b in bounces:
    ...  # mark b["email"] as undeliverable in your DB

# 4. User opted out in your app -> mirror it to SendPulse
api("POST", "/smtp/unsubscribe",
    json={"emails": [{"email": "jane@example.com", "comment": "opted out in app"}]})
```

## Notes

- On HTTP 429 (rate limit) retry with exponential backoff
  (`time.sleep(2 ** attempt)`), max ~5 attempts. Do not retry 4xx validation errors.
- Bulk status for many messages: `api("POST", "/smtp/emails/info", json={"emails": [...]})`
  — up to 500 ids per call, far cheaper than per-id GETs.

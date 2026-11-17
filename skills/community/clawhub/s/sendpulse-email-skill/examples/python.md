# Python examples

Official SDK: https://github.com/sendpulse/sendpulse-rest-api-python. Below: plain
`requests` with a Single API Key — no token refresh needed.

## Minimal client

```python
import base64
import os

import requests

API = "https://api.sendpulse.com"
HEADERS = {"Authorization": f"Bearer {os.environ['SENDPULSE_API_KEY']}"}


def api(method: str, path: str, **kwargs) -> dict | list:
    resp = requests.request(method, f"{API}{path}", headers=HEADERS, timeout=30, **kwargs)
    if resp.status_code == 429:
        raise RuntimeError("Rate limited — retry with exponential backoff")
    resp.raise_for_status()
    return resp.json()
```

## Book → subscribers → campaign

```python
# 1. Create an address book
book_id = api("POST", "/addressbooks", json={"bookName": "Newsletter"})["id"]

# 2. Add subscribers (upsert: re-adding updates variables; dates YYYY-MM-DD)
api("POST", f"/addressbooks/{book_id}/emails", json={
    "emails": [
        {"email": "jane@example.com",
         "variables": {"name": "Jane", "city": "Berlin", "signup_date": "2026-07-01"}},
        {"email": "john@example.com",
         "variables": {"name": "John", "city": "Kyiv", "signup_date": "2026-07-02"}},
    ],
})

# 3. Pre-flight
senders = api("GET", "/senders")          # sender_email below must be here & active
cost = api("GET", f"/addressbooks/{book_id}/cost")

# 4. Create the campaign (body MUST be Base64; or pass "template_id")
html = "<h1>Hello {{name}}!</h1><p>Our July digest...</p>"
campaign = api("POST", "/campaigns", json={
    "name": "July digest",
    "sender_name": "My Shop",
    "sender_email": "news@myshop.com",
    "subject": "Your July digest is here",
    "body": base64.b64encode(html.encode()).decode(),
    "list_id": book_id,
    "send_date": "2026-07-10 10:00:00",   # omit to send ASAP
    "stats": {"opens": True, "clicks": True, "utm_campaign": "july_digest"},
})
campaign_id = campaign["id"]

# 5. Status — campaign may sit in review first (normal for new accounts).
#    Prefer the task_status_update webhook over polling.
info = api("GET", f"/campaigns/{campaign_id}")
```

## Analytics after sending

```python
stats = api("GET", f"/campaigns/{campaign_id}")
countries = api("GET", f"/campaigns/{campaign_id}/countries")
links = api("GET", f"/campaigns/{campaign_id}/referrals")       # clicks per link
one = api("GET", f"/campaigns/{campaign_id}/email/jane@example.com")
history = api("GET", "/emails/jane@example.com/campaigns")      # address across campaigns
```

## Opt-out mirroring & suppression

```python
# Unsubscribe from one book
api("POST", f"/addressbooks/{book_id}/emails/unsubscribe",
    json={"emails": ["jane@example.com"]})

# Account-wide blacklist — NOTE: Base64 of a comma-separated STRING, not an array!
api("POST", "/blacklist", json={
    "emails": base64.b64encode(b"jane@example.com,spam@example.com").decode(),
    "comment": "opted out in app",
})
```

## Webhook receiver sketch (Flask)

```python
@app.post("/hooks/sendpulse/<secret>")
def sendpulse_hook(secret):
    if secret != os.environ["SP_HOOK_SECRET"]:
        return "", 403
    events = request.get_json(force=True)
    for event in events if isinstance(events, list) else [events]:
        queue.enqueue(handle_event, event)   # process async; stay fast
    return "", 200
```

## OAuth variant (if not using an API key)

```python
tok = requests.post(f"{API}/oauth/access_token", json={
    "grant_type": "client_credentials",
    "client_id": os.environ["SENDPULSE_API_ID"],
    "client_secret": os.environ["SENDPULSE_API_SECRET"],
}, timeout=30).json()  # access_token, expires_in=3600 — cache ~55 min, refresh on 401
```

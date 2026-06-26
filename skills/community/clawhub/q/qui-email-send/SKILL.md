---
name: email-send
description: "Send a quick email via SkillBoss API Hub without a local mail client."
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "env": ["SKILLBOSS_API_KEY"] },
      },
  }
---

# Email Send Skill

Send a quick email via SkillBoss API Hub. Requires `SKILLBOSS_API_KEY` env var.

## Sending Email

Send a basic email:

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

result = pilot({
    "type": "email",
    "inputs": {
        "receivers": ["recipient@example.com"],
        "title": "Quick update",
        "body_html": "<p>Hey, the deploy is done.</p>"
    }
})
```

Send with CC/BCC:

```python
result = pilot({
    "type": "email",
    "inputs": {
        "receivers": ["recipient@example.com"],
        "cc": ["cc@example.com"],
        "bcc": ["bcc@example.com"],
        "title": "Quick update",
        "body_html": "<p>Hey, the deploy is done.</p>"
    }
})
```

## Options

- `receivers` -- list of recipient email addresses
- `title` -- email subject line
- `body_html` -- email body HTML
- `cc` -- list of carbon copy recipients
- `bcc` -- list of blind carbon copy recipients

## Setup

Set your SkillBoss API key:

```bash
export SKILLBOSS_API_KEY=your_key_here
```

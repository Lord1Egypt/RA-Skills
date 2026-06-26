---
name: telegram-notifier
description: Send any agent report, alert, or message to a Telegram chat using your bot token. Use when you want to deliver findings, briefings, security alerts, or task completions via Telegram. Supports plain text and Markdown. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment. No external services except Telegram's own API.
---

# Telegram Notifier

Send structured messages from any agent to Telegram.

One skill. One job. Works with any agent, any report, any workflow.

---

## Prerequisites

You need a Telegram bot token and a chat ID in your environment:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**Get a bot token:** Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` → copy the token.

**Get your chat ID:** Message [@userinfobot](https://t.me/userinfobot) on Telegram → it replies with your ID.

---

## Sending a message

### Basic send (plain text)

```python
import os, requests

requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    json={
        "chat_id": os.environ['TELEGRAM_CHAT_ID'],
        "text": "Your message here"
    },
    timeout=10
)
```

### Markdown formatted message

```python
import os, requests

def send_telegram(text: str, parse_mode: str = "Markdown") -> bool:
    """Send a message to Telegram. Returns True on success."""
    r = requests.post(
        f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
        json={
            "chat_id": os.environ['TELEGRAM_CHAT_ID'],
            "text": text,
            "parse_mode": parse_mode,
        },
        timeout=10,
    )
    return r.status_code == 200

# Example: send an agent report
send_telegram("*SECURITY REPORT*\n\n✅ No threats detected.\nNext scan: 04:00")
```

### Send with agent prefix (recommended format)

```python
from datetime import datetime

def agent_report(agent_name: str, body: str) -> None:
    timestamp = datetime.now().strftime("%H:%M")
    message = f"📡 *{agent_name}* — {timestamp}\n\n{body}"
    send_telegram(message)

agent_report("Alpha", "Network scan complete. 2 new devices detected.")
```

---

## Common use cases

### 1. Deliver a briefing

```python
report = """
🌅 *MORNING BRIEFING*

🔴 Security: 1 warning — config perms
🖥️ Infra: All containers healthy
💰 Cashflow: 0 new installs
"""
send_telegram(report)
```

### 2. Send an alert

```python
def send_alert(title: str, detail: str, severity: str = "WARN") -> None:
    icons = {"CRITICAL": "🚨", "WARN": "⚠️", "INFO": "ℹ️"}
    icon = icons.get(severity, "⚠️")
    send_telegram(f"{icon} *{severity}: {title}*\n\n{detail}")

send_alert("Disk usage at 91%", "Root partition: 91% full. Free up space.", "WARN")
```

### 3. Confirm task completion

```python
send_telegram("✅ *Task complete:* Suricata rules updated. 49,892 rules active.")
```

### 4. Send on cron schedule

```bash
openclaw cron add \
  --name "telegram-notifier:daily-check" \
  --cron "0 8 * * *" \
  --prompt "Run a system health check and send the results via the telegram-notifier skill."
```

---

## Error handling

```python
import os, requests

def send_telegram(text: str) -> dict:
    """Returns {"ok": True} or {"ok": False, "error": "..."}"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set"}

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text[:4096]},  # Telegram limit: 4096 chars
            timeout=10,
        )
        data = r.json()
        if data.get("ok"):
            return {"ok": True}
        return {"ok": False, "error": data.get("description", "unknown error")}
    except requests.Timeout:
        return {"ok": False, "error": "Request timed out"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
```

---

## Limitations

- Telegram message limit: 4096 characters. Truncate or split long reports.
- Rate limit: 30 messages/second per bot (you will never hit this in normal use).
- parse_mode `"Markdown"` requires escaping special chars: `_ * [ ] ( ) ~ > # + - = | { } . !`
  Use `"HTML"` if your messages contain special characters.
- This skill only sends messages. For receiving messages or building interactive bots, use a dedicated bot framework.

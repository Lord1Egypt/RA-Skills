---
name: unanswered-messages
description: Track and find unanswered messages using a local file-based inbox. No DB required. Use when asked to find unanswered messages, missed messages, people waiting for a response, or to log a new incoming message.
---

# Unanswered Messages (File-Based)

Tracks messages sent to Heleni that haven't been replied to yet.
**No DB required** — uses `/opt/ocana/openclaw/workspace/inbox/pending.json`.

---

## File Structure

`/opt/ocana/openclaw/workspace/inbox/pending.json`:

```json
{
  "version": 1,
  "messages": [
    {
      "id": "MSG_ID",
      "ts": "2026-04-01T14:30:00Z",
      "chat_id": "+972XXXXXXXXX",
      "chat_name": "Netanel",
      "chat_type": "direct",
      "sender_name": "Netanel",
      "sender_phone": "+972XXXXXXXXX",
      "body": "message text...",
      "answered": false,
      "answered_at": null
    }
  ]
}
```

---

## 1. Log an Incoming Message

When a message arrives that needs a response, add it to the file:

```python
import json, datetime

INBOX = "/opt/ocana/openclaw/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

data["messages"].append({
    "id": "<message_id>",
    "ts": datetime.datetime.utcnow().isoformat() + "Z",
    "chat_id": "<chat_id>",
    "chat_name": "<chat_name>",
    "chat_type": "direct",  # or "group"
    "sender_name": "<sender_name>",
    "sender_phone": "<sender_phone>",
    "body": "<message body, max 300 chars>",
    "answered": False,
    "answered_at": None
})

with open(INBOX, "w") as f:
    json.dump(data, f, indent=2)
```

---

## 2. Mark a Message as Answered

After replying, mark it done:

```python
import json, datetime

INBOX = "/opt/ocana/openclaw/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

for msg in data["messages"]:
    if msg["id"] == "<message_id>":
        msg["answered"] = True
        msg["answered_at"] = datetime.datetime.utcnow().isoformat() + "Z"

with open(INBOX, "w") as f:
    json.dump(data, f, indent=2)
```

---

## 3. Find Unanswered Messages

```python
import json
from datetime import datetime, timedelta, timezone

INBOX = "/opt/ocana/openclaw/workspace/inbox/pending.json"
MAX_AGE_HOURS = 24  # ignore very old messages

with open(INBOX) as f:
    data = json.load(f)

cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_AGE_HOURS)
unanswered = [
    m for m in data["messages"]
    if not m["answered"]
    and datetime.fromisoformat(m["ts"].replace("Z", "+00:00")) > cutoff
]

for m in sorted(unanswered, key=lambda x: x["ts"]):
    ts = datetime.fromisoformat(m["ts"].replace("Z", "+00:00")).strftime("%d/%m %H:%M")
    print(f"📩 {m['sender_name']} | {m['chat_name']} | {ts}")
    print(f"   > {m['body'][:100]}")
    print(f"   Message ID: {m['id']}")
```

---

## 4. Cleanup — Remove Old Answered Messages

Run periodically (e.g. weekly via heartbeat) to keep the file small:

```python
import json
from datetime import datetime, timedelta, timezone

INBOX = "/opt/ocana/openclaw/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

cutoff = datetime.now(timezone.utc) - timedelta(days=7)
data["messages"] = [
    m for m in data["messages"]
    if not m["answered"]
    or datetime.fromisoformat(m["ts"].replace("Z", "+00:00")) > cutoff
]

with open(INBOX, "w") as f:
    json.dump(data, f, indent=2)

print(f"Kept {len(data['messages'])} messages")
```

---

## Heartbeat Integration

During heartbeat, check for unanswered messages from the last 2 hours:

```python
import json
from datetime import datetime, timedelta, timezone

INBOX = "/opt/ocana/openclaw/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

cutoff = datetime.now(timezone.utc) - timedelta(hours=2)
unanswered = [
    m for m in data["messages"]
    if not m["answered"]
    and datetime.fromisoformat(m["ts"].replace("Z", "+00:00")) > cutoff
]

if unanswered:
    # Alert Netanel or handle inline
    for m in unanswered:
        print(f"⚠️ לא ענינו ל-{m['sender_name']}: {m['body'][:80]}")
```

Add this check to `HEARTBEAT.md` under "Heartbeat Checks".

---

## Output Format

Report unanswered messages as:
- 📩 **[sender_name]** | [chat_name] | [DD/MM HH:MM]
  > [body preview, max 100 chars]
  > Message ID: [message_id]

Group by chat if multiple from same conversation.

---

## Notes

- ❌ No DB, no tunnel, no psql — pure file I/O
- ✅ Works offline, works on AWS without Mac tunnel
- Inbox file: `/opt/ocana/openclaw/workspace/inbox/pending.json`
- Currently: messages are logged manually when Heleni decides to track them
- Future: hook into inbound message handler to auto-log

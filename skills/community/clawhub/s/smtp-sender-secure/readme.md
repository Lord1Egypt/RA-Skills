# Zero‑Exposure SMTP Mail Sender (MGC Secure Edition)

A secure SMTP email‑sending MCP server that prevents credential exposure by using **MGC Blackbox** for local encrypted storage.  
Your AI can send emails — **but never sees your SMTP password**.

---

## ✨ Features

- **Zero‑Exposure:** SMTP password never leaves your machine  
- **Local encryption:** Powered by MGC Blackbox secure vault  
- **Safe for AI automation:** Credentials are never passed to the model  
- **Simple API:** One MCP tool — `send_email`  
- **Compatible with all SMTP providers**  

---

## 📦 Installation

Install MGC Blackbox:

```bash
pip install mgc-blackbox
mgc
```

Clone this skill:

```bash
git clone https://github.com/zkeviny/MGC-Blackbox
cd MGC-Blackbox/mgc_skill/zero_exposure_smtp_sender
```

Run the MCP server:

```bash
python mcp_server.py
```

---

## 🔐 MGC Blackbox Setup

Create a JSON file containing your SMTP credentials:

```json
{
  "address": "your@email.com",
  "password": "auth_code",
  "smtp_server": "smtp.email.com",
  "smtp_port": 587
}
```

Store it securely:

```bash
mgc_save info_type=config info_owner=your_email < config.json
```

> `info_type` and `info_owner` are identifiers you choose when saving credentials.

---

## 🛠 MCP Tool: `send_email`

This MCP server exposes one tool:

### **send_email**

| Parameter     | Type   | Description |
|---------------|--------|-------------|
| `to`          | string | Recipient email |
| `subject`     | string | Email subject |
| `body`        | string | Plain‑text body |
| `info_type`   | string | MGC credential type |
| `info_owner`  | string | MGC credential owner |

---

## 📤 Example (Python)

```python
from mcp import MCPClient

client = MCPClient("http://localhost:57219")

client.call_tool("send_email", {
    "to": "to@example.com",
    "subject": "Hello",
    "body": "This is a secure email.",
    "info_type": "config",
    "info_owner": "your_email"
})
```

---

## 💬 Trigger Phrases (for AI clients)

- “send an email”
- “send via SMTP”
- “email this to someone”

---

## ⚠ Limitations

- Plain‑text emails only  
- No attachments  
- No HTML email support  

> For attachments or HTML templates, you can extend this skill using MGC’s secure local execution.

---

## 👤 Author

**MirginCipher**  
MIT License  
Part of the **MGC Secure / Zero‑Exposure** skill series.

```

---
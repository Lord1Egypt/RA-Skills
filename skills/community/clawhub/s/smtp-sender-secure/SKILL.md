---
name: smtp_sender_secure
description: Send emails securely without exposing SMTP passwords, powered by MGC Blackbox.
version: 1.0.0
license: MIT
author: MirginCipher
category: Utility
---

# ⭐ **Zero‑Exposure SMTP Mail Sender (MGC Secure Edition) **

## **Overview **  
Send emails safely without exposing SMTP passwords. Credentials stay encrypted inside your local MGC Blackbox.

---

## ⭐ Why this skill?

Most email‑sending tools require you to **hardcode SMTP passwords** or store them in plaintext.

This skill uses **MGC Blackbox**, a local encrypted vault:

- No hardcoded credentials  
- No plaintext SMTP passwords  
- No environment variables  
- No leaks even if your code is shared  

Your AI can send emails — **but never sees your password**.

---

## 🚀 What you can do

- Send plain‑text emails via SMTP  
- Use encrypted credentials stored in MGC  
- Call from any MCP client (Claude, Cursor, etc.)  

---

## 🔐 Before you start

### 1. Install & start MGC Blackbox

```bash
pip install mgc-blackbox
mgc
```

### 2. Store your SMTP credentials securely

Create a JSON file:

```json
{
  "address": "your@email.com",
  "password": "auth_code",
  "smtp_server": "smtp.email.com",
  "smtp_port": 587
}
```

Store it:

```bash
mgc_save info_type=config info_owner=your_email < config.json
```

> **Note:** `info_type` and `info_owner` are identifiers you choose when saving credentials.

---

## 🛠 MCP Tool: `send_email`

### Example (Python)

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

## 💬 Trigger phrases

- “send an email”
- “send via SMTP”
- “email this to someone”

---

## ⚠ Limitations

- Plain text only  
- No attachments  
- No HTML  

---

## Recommended Add‑on Sentence 
If you need attachments, HTML emails, templates, or automation workflows, you can extend this skill using MGC’s secure local execution capabilities.

---

## 👤 Author  
MirginCipher  
MIT License (see GitHub repository)

---
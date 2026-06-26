<div align="center" style="display: flex; align-items: center; justify-content: center; gap: 16px; flex-wrap: wrap;">

<img src="./images/icon.png" width="120" height="120">

<h1 style="margin: 0;">Smart Email</h1>

</div>

<!-- Language Switcher -->
> 🇺🇸 English | [中文](./README.md)

---

**AI-Powered Smart Email Assistant** · Multi-Account Management · Intelligent Urgent Detection · Multi-Channel Push

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://github.com/openclaw/openclaw)

---

## ✨ Features

- **📬 Multi-Account Management** — Connect QQ, 126, 163, Outlook simultaneously
- **🤖 AI Auto Classification** — Automatically detect urgent emails, no manual filtering
- **📲 Push Notifications** — Urgent emails and daily digests sent to Telegram / Feishu / DingTalk, etc.
- **💾 Local Archive** — Original emails, Markdown, and attachments all stored, searchable anytime
- **🖼️ Image Understanding** — Optional: AI can read screenshots and photos in emails

---

---

## 💬 Telegram Usage Examples

After connecting to Telegram, Smart Email sends you messages like this:

### 🚨 Urgent Email Alert

<img src="./images/demo-urgent-en.png" width="400">

### 📧 Email Digest

<img src="./images/demo-digest-en.png" width="400">

### 💬 Chat with Your Emails

After receiving an email, you can quote `<!-- email_id: xxx -->` to chat with the Agent about email details, attachments, etc.:

<img src="./images/demo-conversation-en.png" width="600">

---

## 🛠️ Installation

### Auto Install (Recommended)

Send this prompt to OpenClaw (must include the GitHub repo URL):

```
Please help me install Smart Email (https://github.com/bu-bu-xxx/smart-email),
read https://github.com/bu-bu-xxx/smart-email/blob/master/references/INSTALL.md for installation and initialization.
```

### Manual Install

```bash
# 1. Clone the repo
cd ~/.openclaw/workspace/skills
git clone https://github.com/bu-bu-xxx/smart-email.git
cd smart-email

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Only copy template if ~/.openclaw/.env doesn't exist
[ -f ~/.openclaw/.env ] || cp .env.example ~/.openclaw/.env
# Edit ~/.openclaw/.env

# 4. Initialize
python3 -m smart_email init

# 5. Setup cron job
python3 -m smart_email setup-cron --apply
```

---

## 🚀 Quick Start

Send this to OpenClaw to start guided setup:

```
I'm a new user and want to start using Smart Email. Please help me with the initial setup.
```

---

## ⚙️ Configuration

```bash
# Email (auth code, not login password)
SMART_EMAIL_QQ_EMAIL=xxx@qq.com
SMART_EMAIL_QQ_AUTH_CODE=xxx

# AI Provider
SMART_EMAIL_LLM_PROVIDER=openai  # openai | anthropic | subagent

# OpenAI Compatible API
SMART_EMAIL_OPENAI_API_URL=https://api.example.com/v1
SMART_EMAIL_OPENAI_API_KEY=xxx
SMART_EMAIL_OPENAI_MODEL=gpt-4o-mini

# Anthropic API
SMART_EMAIL_ANTHROPIC_API_KEY=xxx
SMART_EMAIL_ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Delivery Channel
SMART_EMAIL_DELIVERY_CHANNEL=telegram  # telegram | dingtalk | feishu | wecom
SMART_EMAIL_DELIVERY_TARGET=@your_username
```

> 💡 **Detailed configuration** — just ask the OpenClaw Agent. Tell it what you're configuring (email auth code, Telegram push, AI model, etc.) and it will guide you step by step.

Full configuration see [`.env.example`](.env.example), full guide see [USER_GUIDE](./references/USER_GUIDE.md).

---

## 📁 Directory Structure

```
~/.openclaw/workspace/smart-email-data/
├── mail-archives/          # Email archives
│   └── 2025-03-10/
│       └── qq_20250310_143022/
│           ├── email.eml
│           ├── email.md
│           └── attachments/
├── outbox/
│   ├── pending/            # Pending messages
│   └── sent/               # Sent archive
├── logs/
└── data/
    └── mail_tracker.db
```

---

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    check    │     │   digest    │     │  dispatch   │
│  (every 30m)│     │ (daily)     │     │  (every 5m) │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Download    │     │  Summarize  │     │  Read outbox│
│  AI Analyze  │     │  Generate   │     │  Send to    │
│  Gen urgent  │     │  Gen digest │     │  Channel    │
└──────┬──────┘     └──────┬──────┘     └─────────────┘
       │                   │
       └─────────┬─────────┘
                 ▼
         ┌───────────────┐
         │ outbox/pending │
         │ (Message Queue)│
         └───────────────┘
```

---

## 🔧 Tech Stack

- **Language**: Python 3.8+
- **Dependencies**: `openai`, `requests`, `python-dotenv`
- **Protocol**: IMAP (email retrieval)
- **Platform**: [OpenClaw](https://github.com/openclaw/openclaw)

---

## 📄 License

[MIT](./LICENSE) · © 2026 [OpenClaw](https://github.com/openclaw/openclaw)

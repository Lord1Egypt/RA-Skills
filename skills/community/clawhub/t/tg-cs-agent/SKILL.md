---
name: tg-cs-agent
description: Deploy and manage a Telegram customer service bot powered by Claude + RAG. Use when setting up a new CS bot, adding knowledge base docs, managing the bot lifecycle (start/stop/restart), or troubleshooting bot issues. Triggers on "customer service bot", "CS bot", "客服机器人", "telegram bot", "knowledge base".
---

# Telegram Customer Service Agent

RAG-powered Telegram customer service bot using Claude + Telethon + ChromaDB.

## Architecture

- **Telegram**: Telethon userbot (not Bot API) — appears as a real user
- **AI**: Claude via Anthropic API with RAG context from local markdown docs
- **Knowledge Base**: ChromaDB + multilingual sentence-transformers embeddings
- **Handoff**: Auto-escalation to human agent when AI can't help

## Prerequisites

- Python 3.11+
- Telegram account with API credentials (get from https://my.telegram.org)
- Anthropic API key
- Telethon session (logged in via `tgctl-telethon login` or manual auth)

## Setup New Bot

### 1. Create project

```bash
mkdir -p ~/tg-cs-bot && cd ~/tg-cs-bot
cp -r <skill_dir>/scripts/*.py .
pip install anthropic chromadb sentence-transformers python-dotenv telethon
```

### 2. Configure environment

Create `.env`:
```
ANTHROPIC_API_KEY=<key>
ANTHROPIC_BASE_URL=https://api.anthropic.com
TELEGRAM_API_ID=<id>
TELEGRAM_API_HASH=<hash>
TELEGRAM_PROFILE=default
MODEL=claude-sonnet-4-20250514
KNOWLEDGE_DIR=docs
MAX_HISTORY=20
HANDOFF_CHAT_ID=<admin_telegram_id_or_username>
```

### 3. Add knowledge base

Put markdown files in `docs/` directory. The bot splits by `##` headers and vectorizes with `paraphrase-multilingual-MiniLM-L12-v2` for multilingual support.

### 4. Login to Telegram (first time only)

```bash
python3 -c "
from telethon import TelegramClient
import asyncio
async def login():
    c = TelegramClient('~/.tgctl-telethon/default/session', API_ID, 'API_HASH')
    await c.start()
    print('Logged in:', (await c.get_me()).first_name)
asyncio.run(login())
"
```

### 5. Run

```bash
python3 main.py
```

## Managing the Bot

- **Start**: `python3 main.py` (or use the start.sh script)
- **Stop**: Ctrl+C or kill the process
- **Add knowledge**: Drop `.md` files in `docs/`, restart bot
- **Clear user history**: User sends `/clear`
- **Request human**: User sends `/human`

## Customization

### System Prompt

Edit `config.py` → `__post_init__` → `self.system_prompt` to change:
- Bot personality and tone
- Language rules
- Handoff trigger conditions
- Platform-specific instructions

### Embedding Model

In `knowledge.py`, change `model_name` for different language support:
- `paraphrase-multilingual-MiniLM-L12-v2` — multilingual (recommended)
- `all-MiniLM-L6-v2` — English only, faster
- `shibing624/text2vec-base-chinese` — Chinese optimized

### Handoff Behavior

The bot adds `[HANDOFF]` to responses when it can't help. This triggers:
1. Notification to `HANDOFF_CHAT_ID` with user info
2. A message to the user that human support is coming

## File Structure

```
tg-cs-bot/
├── main.py              # Entry point, message routing
├── config.py            # Config + system prompt
├── agent.py             # Claude RAG agent
├── knowledge.py         # ChromaDB knowledge base
├── telegram_client.py   # Telethon wrapper
├── .env                 # Secrets (not committed)
├── docs/                # Knowledge base markdown files
│   ├── platform.md
│   ├── faq.md
│   └── ...
└── requirements.txt
```

## Troubleshooting

- **database is locked**: Kill all Python processes, delete `session.session-journal`, rebuild session with sqlite dump/restore
- **Not logged in**: Run the login step again
- **Poor RAG results**: Check embedding model matches your docs language, use multilingual model for mixed content
- **Bot not responding**: Check `[READY] Listening for messages...` in logs, verify Telegram connection

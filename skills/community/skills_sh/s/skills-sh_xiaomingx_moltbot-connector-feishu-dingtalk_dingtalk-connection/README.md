# DingTalk x Moltbot Bridge

Connect a DingTalk bot to a local Clawdbot (Moltbot) Gateway using an outgoing webhook.

## How it works

```
DingTalk user -> DingTalk cloud -> webhook (this bridge) -> Clawdbot Gateway -> AI agent
```

This bridge exposes an HTTP endpoint for DingTalk's outgoing webhook. When a message arrives,
it forwards the text to the local Clawdbot Gateway over WebSocket and sends the reply back to
the DingTalk session webhook.

## Setup

Prereqs: Python 3.11 + uv.

### 1) Create a DingTalk bot (outgoing webhook)

- Create a DingTalk custom bot or internal app bot that supports outgoing webhooks.
- Configure the callback URL to your public endpoint (e.g. `https://example.com/dingtalk`).
- Set a signing secret and keep it safe.

> Note: DingTalk must reach your webhook over the public internet. Use a reverse proxy or
> tunnel if you are running locally.

### 2) Install dependencies

```bash
cd <skill-dir>/dingtalk-connection
uv sync
```

### 3) Configure env

```bash
cp .env.example .env
```

Set at least:

- `DINGTALK_SIGNING_SECRET` (matches the DingTalk bot secret)
- `DINGTALK_PORT` / `DINGTALK_PATH` (server listen settings)

### 4) Run

```bash
uv run python bridge.py
```

## Group chat behavior

In group chats, the bridge replies only when the bot is mentioned or when the message looks
like a request (question mark, common verbs, or bot name). Customize the logic in
`bridge.py` -> `should_respond_in_group()`.

## Files

```
<skill-dir>/dingtalk-connection/
├── bridge.py
├── setup_service.py
├── pyproject.toml
└── README.md
```

---
name: qwen-web-agent
description: "Browser automation for 通义千问 (Qwen) web interface at qianwen.com. Use when the agent needs to ask questions to Qwen AI and get back responses via browser automation. Supports single-turn and multi-turn conversations. Launches a real Chromium browser (headed mode) via Playwright, handles login persistence, sends queries, and captures complete AI replies. Best for: (1) Getting AI answers from Qwen's web platform, (2) Automating Qwen queries from other agents/skills, (3) Integrating Qwen responses into automated workflows."
---

# Qwen Web Agent

Browser automation for 通义千问 (qianwen.com) using Playwright. Login session persists at `~/.qwen_session/`.

## Quick Start

### Single-turn
```bash
python scripts/qwen_agent.py "你的问题"
echo "你的问题" | python scripts/qwen_agent.py
```

### Multi-turn
```bash
printf "问题1\n问题2\n关闭" | python scripts/qwen_multi_agent.py
```

## First Run (Manual Login Required)

The first launch opens a Chromium window — complete login in the browser, then the script continues automatically. Subsequent runs reuse the saved session.

## Scripts

### `scripts/qwen_agent.py`
Single-turn Q&A. Sends one query, waits for the streaming response to stabilize, saves to `last_output.md`, then cleans up the conversation.

**Parameters:**
- `--timeout N`: Override timeout in seconds (default 120)

### `scripts/qwen_multi_agent.py`
Multi-turn conversation. Reads queries from stdin line by line, maintains conversation context, writes all turns to `qwen_session_history.md`.

**Exit commands:** `关闭`, `exit`, `quit`, or EOF

## Environment Requirements

- Python 3.x
- `pip install playwright python-dotenv`
- `playwright install chromium`
- Display server (X11/Wayland) or Xvfb for headed mode

## Architecture

Both scripts use Playwright async API with a persistent browser context. The response capture logic polls DOM selectors (`#qk-markdown-react`, `.chat-answers-card-wrap`, etc.) until the text stabilizes (streaming detection). Multi-turn additionally tracks response element count to distinguish new responses from cached ones.

## References

See `references/使用说明.md` for detailed usage documentation.

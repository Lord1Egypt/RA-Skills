---
name: web-chat
description: Use when the user wants to interact with Google Gemini or ChatGPT via browser automation. Triggers on phrases like "ask Gemini", "ask ChatGPT", "ask GPT", "让 Gemini", "让 ChatGPT", "问一下 Gemini", "问一下 ChatGPT", "用 Gemini 查", "用 GPT 查". Sends the user's query to the target chatbot and returns the response verbatim.
version: 1.0.0
metadata:
  openclaw:
    emoji: "\u2728"
    category: "ai-tools"
    tags: ["gemini", "google", "chatgpt", "openai", "gpt", "browser-automation", "playwright", "ai-chat"]
    # NOTE: OpenClaw reports the host OS as "darwin" on macOS.
    os: [linux, darwin]
    requires:
      bins: ["python3"]
---

# Web Chat

Send messages to AI chatbots (Gemini, ChatGPT) via Playwright browser automation and return responses with citations.

| Chatbot | Script | Website |
|---------|--------|---------|
| Google Gemini | `scripts/ask_gemini.py` | gemini.google.com |
| ChatGPT | `scripts/ask_chatgpt.py` | chatgpt.com |

## Workflow

### Step 1: Ensure Chrome is Running with CDP

If the script fails to connect (Chrome not running or no `--remote-debugging-port`), start Chrome:

```bash
{baseDir}/scripts/start_chrome.sh
```

The start script has built-in locking and CDP detection to handle concurrent starts safely. It launches Chrome with `--remote-debugging-port=9222` and `--user-data-dir=~/.openclaw/workspace/chrome_profile`. Login sessions persist across restarts.

### Step 2: Choose Chatbot and Extract Query

**Choose chatbot**: Use the one the user names ("ask Gemini", "用 ChatGPT 查"). "GPT" means ChatGPT. Default to Gemini if unspecified.

**Extract query**: Strip only the trigger prefix. Do NOT rephrase, translate, summarize, or add context. Pass the rest verbatim:

| User says | Extracted query |
|-----------|----------------|
| "ask Gemini what is MCP protocol" | "what is MCP protocol" |
| "问一下 ChatGPT，transformer 的注意力机制怎么工作" | "transformer 的注意力机制怎么工作" |
| "用 GPT 查一下 React 19 有什么新特性" | "React 19 有什么新特性" |

### Step 3: Send the Query

```bash
# Gemini
{baseDir}/.venv/bin/python3 {baseDir}/scripts/ask_gemini.py "extracted query"

# ChatGPT
{baseDir}/.venv/bin/python3 {baseDir}/scripts/ask_chatgpt.py "extracted query"
```

| Flag | Description | Default |
|------|-------------|---------|
| `--port PORT` | Chrome CDP port | `9222` |
| `--timeout SECS` | Max wait for response | `120` |
| `--new-chat` | Force new chat session | `false` |
| `--json` | JSON output | `false` |

Return the script output to the user VERBATIM. Do NOT summarize, rephrase, translate, or otherwise alter the response. Present the full, unmodified text exactly as the script printed it.

## Error Handling

| Error | Action |
|-------|--------|
| "Cannot connect to Chrome on port 9222" | Run `{baseDir}/scripts/start_chrome.sh` (has built-in lock and CDP check), wait 5 seconds, retry. Do NOT kill Chrome manually. |
| "You are not logged in" | Inform user to log in manually in the Chrome window |
| "Could not find input field" | Selectors may be outdated; inform user the script may need updating |
| Response timeout | Retry with `--timeout 300` |

## Rebuilding .venv

```bash
cd {baseDir} && rm -rf .venv && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

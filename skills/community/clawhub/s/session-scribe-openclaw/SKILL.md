---
name: session-scribe
description: Automatically summarize active OpenClaw session transcripts into daily memory files using a cheap LLM. Run as a system cron job — reads new transcript entries since last run, summarizes them via OpenAI or Anthropic API, and appends bullet-point notes to a daily memory file. No gateway involvement, no context bloat. Designed to pair with the supermemory skill for full memory pipeline automation. Use when you want session context preserved without relying on agent self-reporting.
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["node"]
      env: ["OPENAI_API_KEY"]
    primaryEnv: "OPENAI_API_KEY"
---

# session-scribe

Reads OpenClaw session transcripts and writes summarized bullet points to a daily memory file — automatically, via system cron.

No gateway involvement. No context bloat. Just cheap, reliable scribing.

## ⚠️ Privacy notice

This skill sends conversation transcript content to an external LLM (OpenAI or Anthropic). If your sessions contain secrets, API keys, PII, or sensitive data — be aware that content will be sent to the provider for summarization. Use a dedicated low-privilege API key with spend limits, and consider running `--dry-run` first to see exactly what gets sent.

## How it works

1. Reads `<sessions-dir>/<session-id>.jsonl` for new entries since last run
2. Extracts user + assistant turns (skips tool calls, system events)
3. Sends to OpenAI or Anthropic API for summarization (`gpt-4o-mini` by default — cheap)
4. Appends bullet-point summary to `<memory-dir>/YYYY-MM-DD.md` (date auto-generated)
5. Saves progress in `.scribe-state.json` so next run only processes new entries

## Setup

```bash
# Install dependencies (one-time, in the skill directory)
cd /path/to/skills/session-scribe && npm install

# Set your API key — OpenAI or Anthropic both work
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Find your session ID
python3 -c "
import json, os
sessions = json.load(open(os.path.expanduser('~/.openclaw/agents/main/sessions/sessions.json')))
for k, v in sessions.items():
    print(k, '->', v.get('sessionId'))
"

# Test run (dry-run, prints summary without writing)
node scripts/scribe.js \
  --sessions ~/.openclaw/agents/main/sessions \
  --session-id <your-session-id> \
  --memory-dir ~/.openclaw/workspace/memory \
  --dry-run

# Or auto-resolve session by key suffix (e.g. your Discord channel ID)
node scripts/scribe.js \
  --sessions ~/.openclaw/agents/main/sessions \
  --auto-session "discord:channel:YOUR_CHANNEL_ID" \
  --memory-dir ~/.openclaw/workspace/memory \
  --dry-run
```

> **Note:** OpenClaw's internal `oat` tokens cannot be used for direct API calls. Use a standard API key from platform.openai.com or console.anthropic.com.

## System cron setup

Add to crontab (`crontab -e`) to run every hour:

```bash
# Store your key in a protected file (do NOT inline secrets in crontab)
echo "sk-your-key" > ~/.openclaw/secrets/scribe-key
chmod 600 ~/.openclaw/secrets/scribe-key

# Single session (via key file)
0 * * * * node /path/to/session-scribe/scripts/scribe.js \
  --sessions ~/.openclaw/agents/main/sessions \
  --auto-session "discord:channel:YOUR_CHANNEL_ID" \
  --memory-dir ~/.openclaw/workspace/memory \
  --api-key-file ~/.openclaw/secrets/scribe-key \
  >> /tmp/scribe.log 2>&1

# All sessions across all agents
0 * * * * node /path/to/session-scribe/scripts/scribe.js \
  --agents-dir ~/.openclaw/agents \
  --all-sessions \
  --memory-dir ~/.openclaw/workspace/memory \
  --api-key-file ~/.openclaw/secrets/scribe-key \
  >> /tmp/scribe.log 2>&1
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--sessions <dir>` | Path to OpenClaw sessions directory | required |
| `--session-id <id>` | Specific session UUID to scribe | — |
| `--auto-session <key>` | Auto-resolve session ID from sessions.json key suffix | — |
| `--memory-dir <dir>` | Directory to write daily memory files | required |
| `--provider <name>` | LLM provider: `openai` or `anthropic` | auto-detected from env |
| `--model <model>` | Model to use | `gpt-4o-mini` |
| `--api-key <key>` | API key (alternative to env var) | — |
| `--api-key-file <path>` | Read API key from file | — |
| `--agent <id>` | Agent label shown in memory file headers | `agent` |
| `--dry-run` | Print summary without writing to disk | false |
| `--min-turns <n>` | Minimum new turns before scribing | `3` |
| `--active-within-hours <n>` | Only scribe sessions active within this window (--all-sessions mode) | `1` |

## Pairing with supermemory

For a full automated memory pipeline:

1. **session-scribe** runs hourly → appends to `memory/YYYY-MM-DD.md`
2. **supermemory ingest** runs every 2h → syncs changed files to Supermemory
3. **supermemory recall** at session start → enriched context from past sessions

## References

- [references/transcript-format.md](references/transcript-format.md) — OpenClaw JSONL transcript structure and sessions.json format

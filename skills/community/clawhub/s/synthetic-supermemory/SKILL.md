---
name: synthetic-supermemory
description: Full automated memory pipeline for OpenClaw agents. Scribe session transcripts into structured daily memory files, ingest them into Supermemory for semantic recall, and retrieve enriched context at session startup. Use when you want persistent memory across sessions without agent self-reporting. Triggers on requests like "set up memory", "remember sessions", "recall context", "ingest memory files", "search memories", or any task requiring long-term agent memory. Requires SUPERMEMORY_API_KEY and OPENAI_API_KEY (or ANTHROPIC_API_KEY).
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["node"]
      env: ["SUPERMEMORY_API_KEY", "OPENAI_API_KEY"]
    primaryEnv: "SUPERMEMORY_API_KEY"
---

# synthetic-supermemory

Full memory pipeline for OpenClaw agents. Three components that work together:

```
session transcripts
      ↓ scribe.js (hourly system cron)
memory/YYYY-MM-DD.md
      ↓ ingest.js (every 2h system cron)
Supermemory (containerTag per agent)
      ↓ recall.js (session startup)
enriched context
```

No gateway involvement. No context bloat. Fully automated.

## ⚠️ Privacy notice

`scribe.js` sends conversation transcript content to an external LLM (OpenAI or Anthropic) for summarization. If your sessions contain secrets, API keys, or PII — be aware that content will be sent to the provider. Use a dedicated low-privilege API key with spend limits.

## Quick setup

```bash
# Install dependencies
cd /path/to/skills/synthetic-supermemory && npm install

# Store keys securely (do NOT put secrets in crontab)
mkdir -p ~/.openclaw/secrets
echo "sk-your-openai-key" > ~/.openclaw/secrets/scribe-key && chmod 600 ~/.openclaw/secrets/scribe-key
echo "sm-your-supermemory-key" > ~/.openclaw/secrets/supermemory-key && chmod 600 ~/.openclaw/secrets/supermemory-key

# Test scribe (dry-run)
SUPERMEMORY_API_KEY=$(cat ~/.openclaw/secrets/supermemory-key) \
node scripts/scribe.js \
  --agents-dir ~/.openclaw/agents \
  --all-sessions \
  --memory-dir ~/.openclaw/workspace/memory \
  --api-key-file ~/.openclaw/secrets/scribe-key \
  --dry-run

# Test recall
SUPERMEMORY_API_KEY=$(cat ~/.openclaw/secrets/supermemory-key) \
node scripts/recall.js --container my-agent
```

## Cron setup (add via `crontab -e`)

```bash
# Scribe active sessions hourly
0 * * * * SUPERMEMORY_API_KEY=$(cat ~/.openclaw/secrets/supermemory-key) node /path/to/synthetic-supermemory/scripts/scribe.js --agents-dir ~/.openclaw/agents --all-sessions --memory-dir ~/.openclaw/workspace/memory --api-key-file ~/.openclaw/secrets/scribe-key >> /tmp/scribe.log 2>&1

# Ingest changed memory files into Supermemory every 2 hours
0 */2 * * * SUPERMEMORY_API_KEY=$(cat ~/.openclaw/secrets/supermemory-key) node /path/to/synthetic-supermemory/scripts/ingest.js --dir ~/.openclaw/workspace/memory --container my-agent >> /tmp/ingest.log 2>&1
```

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scribe.js` | Summarize session transcripts → daily memory files + Supermemory | Hourly cron |
| `ingest.js` | Ingest changed memory files → Supermemory (upsert, change-tracked) | Every 2h cron |
| `recall.js` | Retrieve context at session startup | Session start |
| `add.js` | Add a single memory from CLI or stdin | On demand |
| `search.js` | Semantic search across memories | On demand |

## scribe.js options

| Flag | Description | Default |
|------|-------------|---------|
| `--agents-dir <dir>` | OpenClaw agents directory | — |
| `--all-sessions` | Scribe all recently active sessions | — |
| `--sessions <dir>` | Single agent sessions directory | — |
| `--session-id <id>` | Specific session UUID | — |
| `--auto-session <key>` | Auto-resolve session by key suffix | — |
| `--memory-dir <dir>` | Directory for daily memory files | required |
| `--provider <name>` | LLM provider: `openai` or `anthropic` | auto-detected |
| `--model <model>` | Summarization model | `gpt-4o-mini` |
| `--api-key-file <path>` | LLM API key file (600 permissions) | — |
| `--sm-container <tag>` | Supermemory container override | `--agent` value |
| `--agent <id>` | Agent label for memory headers | `agent` |
| `--active-within-hours <n>` | Only scribe sessions active within window | `1` |
| `--min-turns <n>` | Minimum new turns before scribing | `3` |
| `--dry-run` | Print without writing | false |

## ingest.js / recall.js / search.js / add.js options

All take `--container <tag>` to namespace memories per agent.

```bash
# Ingest a directory
node scripts/ingest.js --dir ~/.openclaw/workspace/memory --container sapphire

# Recall context at session start
node scripts/recall.js --container sapphire --query "recent projects and identity"

# Add a one-off memory
node scripts/add.js --container sapphire --content "Kitsune prefers dark mode"

# Search
node scripts/search.js --container sapphire --query "TokTeam deployment"
```

## References

- [references/api.md](references/api.md) — Full Supermemory API reference (batch add, delete, container management)
- [references/transcript-format.md](references/transcript-format.md) — OpenClaw session transcript JSONL structure

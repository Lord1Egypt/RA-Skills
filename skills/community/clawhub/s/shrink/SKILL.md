---
name: shrink
description: >-
  Replace base64 images in session history with context-aware text descriptions,
  reducing image token cost by 96-99%. Use when: (1) user says /shrink, /shrink,
  shrink images, compress images, reduce context, image bloat, shrink session,
  context too large, (2) session is approaching context limits and contains images,
  (3) user wants to optimize token usage across sessions. Supports single session,
  all sessions, per-agent targeting, dedup detection, cost estimates, and automatic
  auth failover.
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
    credentials:
      - name: ANTHROPIC_API_KEY
        description: >-
          Anthropic API key for vision model calls. If not set, the script reads
          keys from ~/.openclaw/agents/<agentId>/agent/auth-profiles.json (the
          targeted agent only when --agent is specified, or all agents when
          auto-discovering keys). Images and surrounding conversation context
          (up to 10 preceding messages) are sent to the Anthropic vision API
          for description generation.
        required: false
    permissions:
      - reads session JSONL files (~/.openclaw/agents/<id>/sessions/*.jsonl)
      - reads auth-profiles.json for Anthropic API keys
      - writes modified JSONL files (replaces image blocks with text)
      - creates .bak backup files before writing
      - sends images + conversation context to Anthropic vision API (api.anthropic.com)
      - optionally restarts the OpenClaw gateway (user-initiated only)
      - optionally redacts PII/secrets during extraction (--redact flag, data never written to disk)
---

# 🦐 Shrink — Multimodal Context Optimizer

Replace base64 image blocks in session JSONL with concise, context-aware text descriptions.
Images consuming 15,000–25,000+ tokens become ~100 token descriptions — a 99%+ reduction.
OpenClaw's built-in pruning explicitly skips images. This is the only tool that solves this.

## Interactive Flow

When triggered, present an interactive menu using inline buttons (Telegram/Discord).

### Step 1: Scan & Present

Run a dry-run first to show the user what's available:

```bash
python3 <skill_dir>/scripts/shrink.py --agent <agentId> --dry-run --json
```

Parse the JSON output and present:

```
🔍 Context Scan Complete

📊 Found {images_found} images in this session
   • {images_deduped} duplicates detected
   • Est. savings: ~{tokens_saved:,} tokens ({savings_percent}%)
   • Est. cost: ~${estimated_cost_usd:.3f}
```

Then offer buttons:
- **🚀 Shrink Now** → run without --dry-run
- **🔎 Details** → show per-image breakdown from the dry-run
- **⚙️ Options** → show configurable settings

If no images found: "✅ No unprocessed images found. Session is already optimized!"

### Step 2: Execute

On "Shrink Now", run live and keep the user informed with progress updates.

For large runs (10+ images), send a progress message and update it as images complete:
```
🖼️ Shrinking Wayne (36 images)...
✅ 1/36 — Quicknode dashboard (23K tokens saved)
✅ 2/36 — ♻️ Duplicate (reused)
✅ 3/36 — Wagyu portfolio (21K tokens saved)
...running total: 68K saved
```

```bash
python3 <skill_dir>/scripts/shrink.py --agent <agentId>
```

Report the full summary stats when complete.

### Step 2b: Apply Changes

After shrinking completes, inform the user that changes are saved to disk but agents
still hold old context in memory. Offer to apply immediately:

```
⚠️ Changes saved to disk. Agents are still using old context in memory.
```

Present buttons:
- **⚡ Apply Now** → run `openclaw gateway restart` (~5 sec downtime, all agents reload clean)
- **⏰ Apply Later** → changes take effect at next session load (daily reset, /compact, or /reset)

If user chooses "Apply Now", run:
```bash
openclaw gateway restart
```
Then confirm: "✅ Gateway restarted. All agents now running on shrunk sessions."

**Important:** Warn that "Apply Now" causes ~5 seconds of downtime for ALL agents, not just the shrunk one.

### Step 3: Options (if requested)

Show current settings and let the user adjust:
- **Model**: auto (detects key type), claude-sonnet-4-6, claude-haiku-4-5
- **Context depth**: 1-10 preceding messages (default: 5)
- **Min tokens**: skip images below threshold (default: 500)
- **Scope**: this session only, or all sessions

Present buttons:
- **📊 All Sessions** → `--all-sessions`
- **🎯 This Session** → single session (default)

## Variant: `/shrink all`

When user says "shrink all", "shrink all sessions", or "shrink everything":

```bash
python3 <skill_dir>/scripts/shrink.py --agent <agentId> --all-sessions --dry-run --json
```

Present totals across all sessions, then confirm before running live.

## Script Reference

```bash
# Basic: current session dry-run
python3 scripts/shrink.py --agent main --dry-run

# Live shrink with all defaults
python3 scripts/shrink.py --agent main

# All sessions for an agent
python3 scripts/shrink.py --agent main --all-sessions

# Specific session file
python3 scripts/shrink.py --session-file path/to/session.jsonl

# Budget-conscious: limit images and use cheaper model
python3 scripts/shrink.py --agent main --max-images 5 --model claude-haiku-4-5

# JSON output for programmatic use
python3 scripts/shrink.py --agent main --all-sessions --json
```

## All Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--session-file` | — | Path to specific JSONL file |
| `--agent <id>` | — | Target agent's sessions directory |
| `--all-sessions` | off | Process all JSONL files for the agent |
| `--dry-run` | off | Preview without modifying |
| `--model` | auto | Vision model (auto-detects from auth type) |
| `--max-images N` | all | Limit to first N images |
| `--min-tokens N` | 500 | Skip images below token threshold |
| `--context-depth N` | 5 | Preceding messages for context-aware descriptions |
| `--no-backup` | off | Skip .bak backup creation |
| `--json` | off | JSON output (suppresses pretty-print) |
| `--no-verbose` | off | Suppress per-image details |

## Key Behaviors

- **Idempotent** — re-runs skip already-deflated images (marker: `[🖼️ Image deflated:`)
- **Dedup** — identical images get one API call, description reused for copies
- **Context-aware** — reads preceding messages + user text + agent response for rich descriptions
- **Auth failover** — tries API key first (Sonnet), falls back to OAuth (Haiku) automatically
- **Safe** — creates .bak backup before writing, gracefully skips failed images
- **Redaction** — `--redact pii|keys|all` strips sensitive data during extraction for compliance

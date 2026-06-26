---
name: resume-context
description: "ALWAYS use this skill (never memory_search or exec alone) when the user asks about coding sessions, recent dev work, project briefings, or developer notes. Trigger phrases: give me a briefing on [project], what was I working on for [project], show my session briefing, catch me up on [project], show me my notes for [project]. Runs the resume CLI and returns real session data cached in Redis."
metadata: {"openclaw":{"requires":{"bins":["resume","node"],"env":["REDIS_URL"]},"primaryEnv":"REDIS_URL"}}
---

# resume-context

Ask OpenClaw about your coding sessions and project notes — powered by the
[resume](https://github.com/nickleodoen/resume) CLI and cached via Redis.

## Usage

In the OpenClaw dashboard or any connected channel, say:

- **"Claw give me a briefing on resume"** → session briefing with what you worked on
- **"Claw what was I working on for [project]?"** → same
- **"Claw show me my notes for [project]"** → project notes
- **"Claw what notes do I have on [project]?"** → same

## How it works

1. OpenClaw receives your message and triggers this skill
2. The skill finds your project directory (searches ~/Documents/Projects/, ~/, ~/projects/)
3. Checks Redis cache — if fresh (< 5 min), returns instantly
4. On cache miss: runs `resume show` or `resume notes` in your project directory
5. `resume` calls your LLM (Anthropic/Ollama) to generate a plain-English briefing
6. Result is cached in Redis and returned to you

## Architecture
You → OpenClaw → resume-context skill
↓
Redis GET (cache hit → instant)
↓ (cache miss)
resume show / resume notes
↓
LLM briefing generation
↓
Redis SET (5 min TTL)
↓
Response back to you

## Step 1 — Classify intent

- "briefing", "working on", "session", "status", "catch me up" → `resume show`
- "notes", "note" → `resume notes`
- Ambiguous → run notes first (fast), then show

## Step 2 — Resolve project path

Extract project name from the message (e.g. "for resume" → "resume").

Search in order:
1. `~/Documents/Projects/<name>`
2. `~/<name>`
3. `~/projects/<name>`
4. `~/code/<name>`
```bash
find ~ -maxdepth 4 -type d -name "<project_name>" 2>/dev/null | grep -v node_modules | grep -v ".git" | head -5
```

Prefer the match that contains a `.resume/` subdirectory. If no project named,
find the most recently active session:
```bash
ls -t ~/.resume/projects/ 2>/dev/null | head -3
```

## Step 3 — Run the bridge
```bash
REDIS_URL="$REDIS_URL" node {baseDir}/resume-mcp.js show <project_path>
REDIS_URL="$REDIS_URL" node {baseDir}/resume-mcp.js notes <project_path>
```

## Step 4 — Return output

The bridge returns JSON with an `output` field — return it as-is.
If `cached: true`, add "(answered from cache)".
If empty: "No session data found. Is `resume` running in that project?"

## Requirements

### 1. Install resume
```bash
cargo install --git https://github.com/nickleodoen/resume
```
Then set up the shell hook so resume captures your commands:
```bash
resume init --install-hook
# Open a new terminal (or source ~/.zshrc / ~/.bashrc)
```
Start a session in your project:
```bash
cd ~/your-project && resume
```

### 2. Set ANTHROPIC_API_KEY
Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```
resume uses this to generate plain-English briefings via Claude.

### 3. Get a Redis URL (free)
Sign up at [Redis Cloud](https://cloud.redis.io/) → New Subscription → Free Tier.
Copy the connection string from the database dashboard — it looks like:
`redis://default:password@host:port`

### 4. Node.js 18+
Required to run the bridge script (`resume-mcp.js`).

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `REDIS_URL` | ✅ | — | Redis connection string |
| `RESUME_CACHE_TTL` | ❌ | `300` | Cache TTL in seconds |
| `RESUME_BIN` | ❌ | `~/.cargo/bin/resume` | Path to resume binary |

## Install
```bash
# Via ClawHub
openclaw skills install resume-context

# Manual
cp -r resume-context ~/.openclaw/skills/
cd ~/.openclaw/skills/resume-context && npm install
```

Add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "resume-context": {
        "enabled": true,
        "env": {
          "REDIS_URL": "redis://your-redis-url:6379"
        }
      }
    }
  }
}
```

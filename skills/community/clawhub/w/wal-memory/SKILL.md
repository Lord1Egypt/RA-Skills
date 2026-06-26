---
name: wal-memory
description: Session crash and compaction recovery using a two-file WAL (Write-Ahead Log) system. Use when setting up persistent memory for an OpenClaw agent that needs to survive session rollovers, gateway disconnects, Anthropic outages, or context compaction. Installs state-log.js + GOALS.md structure + cold boot recovery hook. Eliminates agent amnesia between sessions.
metadata:
  requires: "Node.js (node binary must be available in PATH)"
---

# WAL Memory

Two-file system for session crash recovery. Survives gateway disconnects, provider outages, and context compaction. Co-designed with Gemini.

## The Problem

OpenClaw agents lose state in two ways:
1. **Compaction** — context window fills, gets summarized, detail lost
2. **Session rollover** — session dies (crash/disconnect/overload), new session starts cold with zero history

## The Two Files

- **`memory/GOALS.md`** — The "why": current milestone, sprint tasks, architecture decisions. Updated manually at major milestones or end of session.
- **`STATE.log`** — The "what just happened": append-only WAL, auto-timestamped. Never edit manually. Written via `state-log.js`.

## Setup

### 1. Install the logger script

Copy `scripts/state-log.js` to `~/clawd/scripts/state-log.js`.

Test it:
```bash
node ~/clawd/scripts/state-log.js "STARTUP" "WAL memory system initialized"
# Should print: Logged: STARTUP
# STATE.log should appear in ~/clawd/
```

### 2. Create GOALS.md

Copy `assets/GOALS.template.md` to `~/clawd/memory/GOALS.md`. Fill in your current objective, sprint tasks, and key decisions. Keep it under 30 lines — this is the "why", not the "what".

### 3. Update AGENTS.md — Cold Boot Recovery Hook

Add this to your "Every Session" startup sequence:

```markdown
## Every Session — Cold Boot Recovery Hook
1. Read `memory/GOALS.md` — current mission and what's in flight
2. Run `tail -n 20 ~/clawd/STATE.log` — last 20 actions, tells you where we left off
3. Read today's `memory/YYYY-MM-DD.md` for recent context
```

### 4. Update HEARTBEAT.md — Safety Net Flush

Add this as the first step of every heartbeat:

```bash
node ~/clawd/scripts/state-log.js "HEARTBEAT" "Interval reached $(date '+%Y-%m-%d %H:%M')"
```

This guarantees STATE.log has a timestamp even if the session crashes immediately after — you'll always know exactly when things flatlined.

## The Logging Rule

After any meaningful action, run:

```bash
node ~/clawd/scripts/state-log.js "CATEGORY" "What you just did"
```

**Categories:**
- `ACTION` — file created, code edited, config changed
- `DEPLOY` — pushed to production, service restarted
- `AGENT` — dispatched or agent task completed
- `TASK` — milestone completed
- `FIX` — bug or system fix applied
- `STARTUP` — cold boot (always log this first)
- `HEARTBEAT` — interval ping
- `ERROR` — something failed

**Examples:**
```bash
node ~/clawd/scripts/state-log.js "AGENT" "Dispatched Owsley to build auth system"
node ~/clawd/scripts/state-log.js "DEPLOY" "FF ElasticSearch secured, 6027 docs indexed"
node ~/clawd/scripts/state-log.js "FIX" "Cron syntax fixed — was using session spawn, now uses agent --deliver"
```

**Do NOT log:** reads, searches, minor tool calls. Signal only.
**Never log:** passwords, API keys, tokens, or sensitive payloads — STATE.log is plaintext.

## Recovery Protocol

On cold boot or post-compaction, first action is always:

```bash
# 1. Read the why
cat ~/clawd/memory/GOALS.md

# 2. Read what just happened
tail -n 20 ~/clawd/STATE.log

# 3. Resume from last log entry
```

## File Details

- `STATE.log` lives at `~/clawd/STATE.log`
- Auto-rotates at 5MB (renames to `STATE.log.old`, starts fresh)
- Format: `[2026-03-03T09:00:00.000Z] [CATEGORY] Message`
- **Add `STATE.log` to `.gitignore`** — it may contain sensitive action descriptions, credentials referenced in log messages, or private task details. Do not commit it to source control unless you have reviewed its contents and are certain it contains no sensitive data.

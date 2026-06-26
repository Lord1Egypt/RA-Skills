---
name: self-healing-agent
description: Self-recovery and auto-repair system for OpenClaw agents. Monitors agent health, detects failures (crashed cron jobs, broken skills, config corruption, memory bloat, session timeouts), automatically diagnoses root causes, and applies fixes. Inspired by Hermes agent's self-recovery capabilities. Use when asked to "make my agent self-healing", "auto-repair", "self-recovery", "agent health monitoring", "fix broken cron jobs automatically", "auto-diagnose failures", "resilient agent", "fault tolerance", "watchdog", "heartbeat monitor", or when agents repeatedly fail and need automated recovery. Also use to set up continuous health monitoring via cron.
---

# Self-Healing Agent

Automated failure detection, diagnosis, and recovery for OpenClaw agents. The watchdog that keeps your agent running.

## Quick Start

```bash
# Full health check — scan all systems, diagnose issues, suggest fixes
python3 scripts/self-healing-agent.py check

# Auto-heal — detect and fix what it can automatically
python3 scripts/self-healing-agent.py heal

# Monitor mode — run continuously, fix issues as they appear
python3 scripts/self-healing-agent.py monitor --interval 300

# Check specific subsystem
python3 scripts/self-healing-agent.py check --target cron
python3 scripts/self-healing-agent.py check --target memory
python3 scripts/self-healing-agent.py check --target config
python3 scripts/self-healing-agent.py check --target sessions
```

## Commands

### `check` — Health Check
Runs diagnostic suite:
- **Cron health** — Failed jobs, consecutive errors, stuck jobs, timeout patterns
- **Memory health** — File sizes, bloated sessions, orphaned files, growth rate
- **Config health** — Valid JSON, required fields present, deprecated settings
- **Session health** — Active sessions, zombie processes, memory usage
- **Skill health** — Broken scripts, missing dependencies, syntax errors
- **Network health** — API endpoint reachability, DNS resolution, SSL cert validity

Options: `--target <subsystem>` to check one area, `--json` for machine output.

### `heal` — Auto-Repair
For each detected issue, applies the safest fix:
- Restarts failed cron jobs (after diagnosing root cause)
- Clears bloated session files (with backup)
- Fixes JSON syntax errors in config (common trailing comma, etc.)
- Removes orphaned process files
- Restores corrupted memory files from git history
- Rotates oversized log files

Options: `--dry-run` to preview, `--aggressive` for riskier fixes.

### `monitor` — Continuous Watchdog
Runs in a loop, checking health every N seconds:
- Logs findings to `memory/self-healing-log.json`
- Auto-heals fixable issues
- Escalates unfixable issues to the agent's main session
- Tracks MTTR (mean time to recovery) and failure patterns

Options: `--interval <seconds>` (default: 300), `--max-heals <n>` per cycle.

### `report` — Health Report
Generates a markdown health report covering:
- Last 24h failure count and types
- MTTR statistics
- Most common failure modes
- Recommendations for prevention

## What It Monitors

| Subsystem | Checks | Auto-Heals |
|-----------|--------|------------|
| Cron | Failed runs, timeouts, consecutive errors | Restart jobs, clear error state |
| Memory | File sizes >1MB, growth rate, duplicates | Archive old files, compact |
| Config | JSON validity, required fields, deprecated keys | Fix syntax, add defaults |
| Sessions | Zombie processes, bloated contexts | Kill zombies, archive contexts |
| Skills | Syntax errors, missing deps, broken imports | Log issue, skip broken skill |
| Network | API endpoints, DNS, SSL certs | Retry with backoff, switch endpoints |

## Healing Log

All actions are logged to `memory/self-healing-log.json`:
```json
{
  "timestamp": "2026-04-05T06:00:00Z",
  "issue": "cron job 'daily-intel' failed 3 consecutive times",
  "diagnosis": "Script timeout — API rate limit hit",
  "action": "Reset error count, added 30s backoff, restarted",
  "result": "success",
  "mttr_seconds": 12
}
```

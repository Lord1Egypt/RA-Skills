---
name: skill-insight
version: 1.0.0
description: "Understand what your AI agent's skills are actually being used for — with usage reports, success/failure tracking, and unused-skill recommendations. Part of the Hal Stack 🦞"
author: halthelobster
changelog: "v1.0.8 - Complete rewrite: honest scope, setup guide for users. v1.0.7 - Category translated + outcome tracking. v1.0.6 - Period labels translated. v1.0.5 - Full i18n. v1.0.0 - Initial release."
---

# Skill Insight 🦞

**By Hal Labs** — Part of the Hal Stack

> **What it does**: Analyzes skill usage data you already have. Generates reports, tracks success/failure, identifies dead weight. **It does not automatically collect data for you.**

## The Honest Scope

This skill is a **data analysis and reporting tool**. It assumes usage data already exists. If you don't collect any, the reports will be empty.

**What it CAN do well:**
- Generate readable usage reports (daily/weekly/monthly)
- Track success vs failure rates per skill
- Recommend which zero-use skills to uninstall
- Work fully automatically for `script`-type skills (cron scan)

**What it CANNOT do automatically:**
- Detect `route`-type skill calls — these happen inside the AI's reasoning, never appearing in session text
- Know which skills you actually use without you telling it

**Setup is required.** See the section below.

## Quick Setup (3 steps)

### Step 1 — Add skills to your registry

```bash
# Start with your installed skills:
bash scripts/add_skill.sh <skill-name> <category> <description>
# Example: bash scripts/add_skill.sh fullstack-dev development "Backend architecture"
```

### Step 2 — Choose a data collection method

This is the critical part. Pick one that matches your workflow:

**Option A: For `script`-type skills only (easiest, automatic)**
```bash
# Add to crontab -e:
0 9 * * * cd ~/.openclaw/workspace/skills/skill-insight && bash scripts/cron_wrapper.sh >> ~/.local/log/skill-insight.log 2>&1
```
This runs daily and scans your session history for skill scripts that were executed via `exec` commands. Works for `script` access_type skills. **Will NOT detect `route`-type skills.**

**Option B: For `route`-type skills (requires agent cooperation)**

Add to your agent's `HEARTBEAT.md` or equivalent:
```bash
# After any skill executes successfully:
bash scripts/record.sh <skill-name> "<what you used it for>" --lang en

# If it failed:
bash scripts/record_outcome.sh --skill <skill-name> --scene "<what>" failed "<reason>" --lang en
```

**Option C: Manual (lowest effort, most incomplete)**
```bash
# After any skill call, run:
bash scripts/record.sh <skill-name> "<scene>"
```

### Step 3 — Generate reports

```bash
bash scripts/report.sh --period week --lang zh   # Chinese
bash scripts/report.sh --period week --lang en   # English
bash scripts/analyze.sh --period 7               # Unused skill analysis
```

## How Data Collection Works

Understanding `access_type` helps you know what's covered:

| access_type | Example | Auto-scan works? | Manual record needed? |
|-------------|---------|-----------------|----------------------|
| `script` | `bash meeting.sh`, `bash ai_news_cron.sh` | ✅ Yes (cron scan) | ✅ Appreciated |
| `route` | Skill triggered by description match | ❌ No | ✅ **Required** |
| `tool` | MCP tool, built-in tool | ❌ No | ❌ Not applicable |

**If most of your skills are `route`-type** (most OpenClaw skills), Option B is the only way to get meaningful data.

## Setting Up Auto-Record for Route-Type Skills

If your agent supports `HEARTBEAT.md` or similar periodic scripts, add this:

```
### Skill Usage Tracking
- After any skill is used: `bash scripts/record.sh <skill-name> "<scene>" --lang en`
- If skill failed: `bash scripts/record_outcome.sh --skill <skill-name> --scene "<scene>" failed --lang en`
- Daily: `bash scripts/report.sh --period today --lang en`
```

For OpenClaw agents with proactive agent protocols (WAL/Working Buffer), the record call can be inserted after the WAL write step.

## Commands Reference

```bash
# Record a skill invocation
bash scripts/record.sh <skill> <scene>              # success by default
bash scripts/record.sh <skill> <scene> skipped     # explicitly skipped

# Update outcome
bash scripts/record_outcome.sh <id> failed <reason>
bash scripts/record_outcome.sh --skill <name> --scene <pattern> failed <reason>

# Reports
bash scripts/report.sh --period today|week|month|all [--lang en|zh]
bash scripts/analyze.sh --period 7|30 [--lang en|zh]

# Registry
bash scripts/add_skill.sh <name> <category> <description> [installed]

# Session scan (script-type only)
bash scripts/scan_sessions.py [--lang en|zh]
```

## Output Language

Use `--lang en` for English, `--lang zh` for Chinese. Falls back to English if unset.

## Architecture

```
skill-insight/
├── scripts/
│   ├── record.sh / .py        # Record an invocation
│   ├── record_outcome.sh / .py   # Update outcome
│   ├── report.sh / .py        # Usage report
│   ├── analyze.sh / .py       # Unused skill analysis
│   ├── scan_sessions.sh / .py # Session scanner (script-type only)
│   ├── add_skill.sh / .py    # Add to registry
│   ├── cron_wrapper.sh        # Daily cron wrapper
│   ├── i18n.py               # Translations
│   └── path_utils.py          # Path resolution
├── data/                      # ← Your data (NOT published)
│   ├── skill_registry.json
│   └── usage.json
├── sample/                    # Example data
└── SKILL.md
```

## Philosophy

You can't optimize what you don't measure.

This skill answers: which skills am I actually using? Which ones are dead weight? Is this skill reliable?

The goal isn't to use every skill — it's to know which ones earn their place.

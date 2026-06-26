---
name: skill-radar
description: Scan, analyze, and optimize your AI skill ecosystem. Diagnose skill usage, discover capability gaps, and check version updates in one command. Trigger on "skill check", "skill radar", "skill management", "skill diagnostics", "skill optimization", "check skill", "skill usage".
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: ["python3", "openclaw"]
---

# Skill Radar 📡

> Your AI Skill Manager — Make every installed Skill count

## Core Philosophy

**Make Skill management simpler and more efficient.**

- **Simpler** — See the full picture with one command, no more getting lost in 100+ Skills
- **More Efficient** — Precisely identify idle skills and gaps, maximize every investment
- **Smarter** — Data-driven decisions, not guesswork

## Trigger Conditions

- "check skill", "skill radar", "skill diagnostics", "skill management", "skill optimization"
- "skill usage", "skill insight"
- "which skills am I not using", "should I install this skill", "do my skills need updating"

## Features

| Command | Description |
|---------|-------------|
| `usage` | 📊 Usage Value Assessment (based on 5 data sources) |
| `status` | 📋 Missing/Ready Status Check |
| `recommend` | 💡 Smart Recommendations (discover capability gaps from conversation history) |
| `versions` | 🔄 Version Check |
| `all` | Full Report (all commands above) |

## Usage

```bash
# Full report (recommended for first use)
python3 <skill-path>/scripts/health_check.py all

# Individual checks
python3 <skill-path>/scripts/health_check.py usage       # Usage value assessment
python3 <skill-path>/scripts/health_check.py status      # Status check
python3 <skill-path>/scripts/health_check.py recommend   # Smart recommendations
python3 <skill-path>/scripts/health_check.py versions    # Version check

# Output as Markdown
python3 <skill-path>/scripts/health_check.py all > report.md
```

## Usage Value Assessment

Integrates 5 data sources to infer each Skill's usage:

| Data Source | Content | Weight |
|-------------|---------|--------|
| Daily Memory | Events, decisions, progress | ⭐⭐⭐ |
| MEMORY.md | Core config, preferences | ⭐⭐⭐ |
| HEARTBEAT.md | Scheduled task config | ⭐⭐ |
| Session Logs | Raw conversation records | ⭐⭐ |
| AGENTS.md | Work rules | ⭐⭐ |

Scoring: 🔵 High (core tool) / 🟢 Medium / 🟡 Low / 🔴 Unused

## Dependencies

- Python 3.8+ (pure standard library, no external dependencies)
- OpenClaw CLI (`openclaw`)
- ClawHub CLI (`npx clawhub`, only for version check and recommendations)

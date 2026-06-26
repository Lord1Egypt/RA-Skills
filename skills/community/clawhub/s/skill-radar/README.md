# Skill Radar 📡

> Your AI Skill Manager — Make every installed Skill count

## Core Philosophy

**Make Skill management simpler and more efficient.**

Too many Skills installed and don't know which ones are actually being used? Not sure what's missing? Wondering if versions are up to date?

Skill Radar scans everything and gives you the full picture in one command.

### Three Pillars

- **Simpler** — Lower cognitive load, see the full picture with one command
- **More Efficient** — Reduce wasted effort, precisely identify idle skills and gaps
- **Smarter** — Move from reactive management to proactive optimization with real data

## Features

| Command | Description |
|---------|-------------|
| `usage` | 📊 Usage Value Assessment — Which skills are active, idle, and how often |
| `status` | 📋 Status Check — Ready/Missing stats with cleanup suggestions |
| `recommend` | 💡 Smart Recommendations — Discover capability gaps from conversation history |
| `versions` | 🔄 Version Check — Compare against latest ClawHub versions |
| `all` | Full Report (all commands above) |

## Installation

```bash
# Install via ClawHub (recommended)
npx clawhub install skill-radar

# Or install manually
cp -r skill-radar ~/.openclaw/workspace/skills/
```

## Usage

```bash
SKILL_PATH=~/.openclaw/workspace/skills/skill-radar

# Full report (recommended for first use)
python3 $SKILL_PATH/scripts/health_check.py all

# Individual checks
python3 $SKILL_PATH/scripts/health_check.py usage       # Usage value assessment
python3 $SKILL_PATH/scripts/health_check.py status      # Status check
python3 $SKILL_PATH/scripts/health_check.py recommend   # Smart recommendations
python3 $SKILL_PATH/scripts/health_check.py versions    # Version check

# Output to file
python3 $SKILL_PATH/scripts/health_check.py all > skill-report.md
```

## Usage Value Assessment

Integrates 5 data sources to accurately determine whether each Skill is being used:

| Data Source | Content | Description |
|-------------|---------|-------------|
| 📝 Daily Memory | Events, decisions, progress | Clear timeline, shows trends |
| 📋 MEMORY.md | Core config, preferences | Long-term stable needs |
| 💓 HEARTBEAT.md | Scheduled task config | Indicates continuously used capabilities |
| 💬 Session Logs | Raw conversation records | Analyzed after filtering system messages |
| 🤖 AGENTS.md | Work rules | Reflects long-term usage patterns |

**Scoring System**:

| Score | Meaning | Criteria |
|-------|---------|----------|
| 🔵 High | Core tool | Frequent mentions across multiple data sources |
| 🟢 Medium | Regularly used | Appears in 2+ data sources |
| 🟡 Low | Occasionally used | Only keyword matches |
| 🔴 Unused | Never mentioned | No hits in any data source |

## Smart Recommendations

Based on conversation history and workspace config, proactively discovers capability gaps:

- Analyzes what the user frequently does
- Compares against installed Skills
- Recommends missing capabilities
- Distinguishes between high-frequency and low-frequency needs

## Dependencies

- Python 3.8+ (pure standard library, no external dependencies)
- OpenClaw CLI (`openclaw`, required for status check)
- ClawHub CLI (`npx clawhub`, required for version check and recommendations)

## Platform Support

- ✅ macOS (Homebrew / npm global)
- ✅ Linux (Linuxbrew / npm global)
- ⚠️ Windows (not tested, no guarantees)

## Security

Recommended Skills go through automatic security scanning (based on skill-vetter protocol):

- **Installed Skills**: Code-level scan (25+ red flag rules)
- **Uninstalled Skills**: Metadata-level check (author, update time, etc.)
- 🔴 High-risk Skills automatically removed from recommendation list
- Scan results cached for 7 days, recommendation results cached for 24 hours

## Zero-Config Principle

All external components are optional, with graceful degradation:

- No Session Logs? No problem, evaluate with workspace files
- Missing data sources? Use what's available, no errors, no ❌

## License

MIT

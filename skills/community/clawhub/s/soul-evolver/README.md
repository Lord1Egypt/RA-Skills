# SoulForge

**SoulForge** is an AI agent memory evolution system. It continuously reads your agent's memory files, discovers recurring patterns, and automatically updates workspace identity files — SOUL.md, USER.md, IDENTITY.md, MEMORY.md, and more.

Unlike manual curation, SoulForge uses your existing MiniMax API to analyze memory streams and evolve your agent's identity files automatically. The more your agent works, the smarter it becomes.

---

## Features

- **🧠 Automatic Memory Analysis** — Reads `memory/*.md` daily logs, hawk-bridge vector store, and `.learnings/` records
- **⚡ MiniMax-Powered** — Uses your existing MiniMax API for pattern detection and content generation
- **📝 Multi-File Evolution** — Updates SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md, TOOLS.md
- **🔒 Safe by Design** — Incremental updates, backup before write, provenance tracking
- **🏢 Multi-Agent Ready** — Each agent's data is isolated (`.soulforge-{agent}/`)
- **⏰ Scheduled or On-Demand** — Run via cron on a schedule or trigger manually
- **🌍 Bilingual** — Full English and Chinese documentation

---

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Memory    │ ──▶ │   Analyzer   │ ──▶ │  Evolver    │
│  Sources   │     │  (MiniMax)   │     │  (Writer)   │
└─────────────┘     └──────────────┘     └─────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
memory/*.md         Pattern Detection      SOUL.md
hawk-bridge         Recurring Rules        USER.md
.learnings/         Decision Mining        IDENTITY.md
                                           MEMORY.md
```

**Trigger Conditions** (when to update):
- Same behavior pattern appears 3+ times
- User corrects the agent 2+ times on the same topic
- New preference or decision discovered
- Project milestone reached

---

## Quick Start

### 1. Install

```bash
# Via clawhub (recommended)
clawhub install soul-evolver

# Or manual clone
git clone https://github.com/relunctance/soul-evolver.git ~/.openclaw/skills/soul-evolver
```

### 2. Configure API Key

SoulForge uses MiniMax API for pattern analysis. Set the API key as an environment variable:

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
```

**Note for OpenClaw users:** If running via OpenClaw cron, the API key is injected automatically by OpenClaw. For standalone CLI use, set the environment variable manually.

### 3. Run

```bash
# Manual trigger
python3 scripts/soulforge.py run

# With custom workspace
python3 scripts/soulforge.py run --workspace /path/to/workspace

# Dry run (see what would change without writing)
python3 scripts/soulforge.py run --dry-run

# Show status
python3 scripts/soulforge.py status
```

### 4. Schedule (Optional)

```bash
# Every 2 hours via cron
python3 scripts/soulforge.py cron --every 120

# Via OpenClaw cron
openclaw cron add --name soulforge-evolve --every 120m \
  --message "exec python3 ~/.openclaw/skills/soul-evolver/scripts/soulforge.py run"
```

---

## Configuration

SoulForge is configured via `soulforge/config.json`:

```json
{
  "workspace": "~/.openclaw/workspace",
  "memory_paths": [
    "memory/",
    ".learnings/"
  ],
  "target_files": [
    "SOUL.md",
    "USER.md",
    "IDENTITY.md",
    "MEMORY.md",
    "AGENTS.md",
    "TOOLS.md"
  ],
  "trigger_threshold": 3,
  "backup_enabled": true,
  "backup_dir": ".soulforge-backups/",
  "minimax_api_key_env": "MINIMAX_API_KEY",
  "model": "MiniMax-M2.7",
  "log_level": "INFO"
}
```

---

## Memory Sources

SoulForge reads from multiple sources:

| Source | Description | Priority |
|--------|-------------|----------|
| `memory/YYYY-MM-DD.md` | Daily conversation logs | High |
| `.learnings/LEARNINGS.md` | Agent corrections and insights | High |
| `.learnings/ERRORS.md` | Command failures and errors | Medium |
| hawk-bridge vector store | Semantic memory search | Medium |
| `.learnings/FEATURE_REQUESTS.md` | User requests | Medium |

---

## Update Logic

### SOUL.md — Behavioral Identity
Updated when:
- Same communication pattern appears 3+ times
- User corrects the agent 2+ times on behavior
- New behavioral principle discovered

### USER.md — User Profile
Updated when:
- User provides new information about preferences
- New project or decision is made
- User's working style changes

### IDENTITY.md — Role Definition
Updated when:
- Agent's role or responsibilities change
- New team members added
- Project scope changes

### MEMORY.md — Long-Term Memory
Updated when:
- Important decision is made
- Project milestone reached
- New lesson learned (from errors)

### AGENTS.md — Workflow Patterns
Updated when:
- New team collaboration pattern discovered
- Workflow improvement found
- Delegation pattern established

### TOOLS.md — Tool Knowledge
Updated when:
- New tool usage pattern discovered
- Integration workaround found
- Tool limitation encountered

---

## Safety Features

1. **Incremental Updates** — Never overwrites, only appends new content blocks
2. **Backup Before Write** — Every update creates a timestamped backup in `.soulforge-backups/`
3. **Provenance Tracking** — Each update block includes source file and reason
4. **Dry Run Mode** — Preview all changes before writing
5. **Threshold Gating** — Patterns must appear multiple times before promoting

---

## File Format

Updates are appended as structured blocks:

```markdown
<!-- SoulForge Update | 2026-04-05T12:00:00+08:00 -->
## Discovered: New Communication Pattern

**Source**: memory/2026-04-05.md
**Pattern**: User prefers numbered lists when selecting options
**Confidence**: High (observed 4 times)

**Content**:
User不喜欢看长文本选项，给选项时列序号让直接挑。

<!-- /SoulForge Update -->
```

---

## Architecture

See [references/ARCHITECTURE.md](references/ARCHITECTURE.md) for full technical details.

```
soul-evolver/
├── SKILL.md                    # Skill definition
├── soulforge/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── memory_reader.py        # Reads memory sources
│   ├── analyzer.py             # Pattern detection (MiniMax)
│   └── evolver.py              # Updates target files
├── scripts/
│   └── soulforge.py            # CLI entry point
├── references/
│   └── ARCHITECTURE.md         # Technical architecture
└── tests/
    └── test_soulforge.py       # Unit tests
```

---

## Requirements

- Python 3.10+
- MiniMax API key
- OpenClaw (optional, for cron integration)
- hawk-bridge (optional, for vector memory)

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs.

---

**SoulForge**: Where your AI agent's soul grows with every conversation.

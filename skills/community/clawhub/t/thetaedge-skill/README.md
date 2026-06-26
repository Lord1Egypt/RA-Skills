# thetaedge-skill

ThetaEdge Skill for Claude Code and OpenClaw — enabling AI agents to interact with **thetix**, ThetaEdge's options intelligence assistant.

## What is ThetaEdge?

ThetaEdge is an Options Intelligence Platform. Its AI assistant, **thetix**, computes structured answers from real data — portfolio analysis, opportunity screening, covered call and cash-secured put calculations, and conversational intelligence about your positions.

This skill exposes five thetix capabilities to AI agents:

1. **Thetix Chat** — Conversational AI for portfolio analysis, market data, news, and dashboard queries
2. **Thetix Cards & Boards** — Dashboard widgets that materialize visualizations from natural language
3. **Opportunities** — Covered call and cash-secured put screening, calculation, and analysis
4. **Accounts** — List user brokerage accounts
5. **Ideas** — AI-generated trading ideas from daily and onboarding reports

## Getting Started

### 1. Generate an API Key

1. Log in to [ThetaEdge](https://app.thetaedge.com)
2. Go to **Profile > API Keys**
3. Click **Create Key**, give it a name (e.g., "Claude Code"), and click create
4. Copy the key immediately — it is only shown once

### 2. Install the Skill

Requires Python 3.7+ and git. Works on Windows, macOS, and Linux.

```bash
git clone https://github.com/thetaedge/thetaedge-skill.git
cd thetaedge-skill
python3 scripts/install.py
```

The installer auto-detects your agent platform (Claude Code, OpenClaw, or both), installs the skill files, and prompts for your API key. Run `python3 scripts/install.py --help` for all options.

### 3. Verify

```bash
python3 scripts/doctor.py
```

Then start Claude Code or OpenClaw and test the skill:

```
/thetix list my card collections
```

## Manual Installation

If you prefer to install without the script:

### Claude Code

Clone into your personal skills directory:

```bash
git clone https://github.com/thetaedge/thetaedge-skill.git ~/.claude/skills/thetaedge-skill
```

Add your API key to `~/.claude/settings.json`:

```json
{
  "env": {
    "THETAEDGE_API_KEY": "te_your_key_here"
  }
}
```

### OpenClaw

```bash
git clone https://github.com/thetaedge/thetaedge-skill.git
cd thetaedge-skill && ./scripts/install-thetix-skill.sh
```

## Development

This project defines a skill following the AgentSkills specification shared by Claude Code and OpenClaw. See `CLAUDE.md` for development guidelines.

### Project Structure

```
thetaedge-skill/
├── SKILL.md           # Main skill definition (frontmatter + instructions)
├── reference.md       # Detailed API reference for thetix endpoints
├── CLAUDE.md          # Dev guide for working on this project
├── scripts/
│   ├── install.py     # Cross-platform installer (Windows/macOS/Linux)
│   ├── doctor.py      # Health check and diagnostics
│   ├── lib/           # Shared Python utilities
│   ├── install-thetix-skill.sh  # OpenClaw installer (bash)
│   ├── setup-openclaw-vm.sh     # VM provisioning script
│   └── clawtunnel.sh            # SSH tunnel helper
└── docs/
    └── vm-setup.md    # VirtualBox VM setup guide
```

### Key Files

- **`SKILL.md`** — The skill definition that agents consume
- **`reference.md`** — API endpoint documentation extracted from the ThetaEdge webapp
- **`CLAUDE.md`** — Guidelines for developing and maintaining this skill

# 🧠 Training Manager

An OpenClaw skill that helps you set up, train, and maintain your agent's workspace — through conversation, not configuration files.

## What It Does

When you first install OpenClaw, you're staring at an empty workspace with no idea what files to create or what to put in them. Training Manager fixes that.

**Interactive Setup** — Instead of dropping placeholder templates, it asks you 8 questions and builds a fully personalized workspace from your answers:

```
Agent: What's your name?
You:   Alex

Agent: How should I talk to you? Like a coworker, a friend, or more formally?
You:   Like a friend

→ SOUL.md gets: "Casual and conversational / Use humor when it fits / Skip formalities"
```

Every answer gets translated into proper agent instructions — no raw quotes dumped into config files.

**Ongoing Training** — As you use your agent, corrections like "don't be so verbose" or "always check my calendar first" get categorized and logged to the right file automatically:

- Behavioral rules → `AGENTS.md`
- Personality traits → `SOUL.md`
- Preferences → `USER.md`
- Facts → `MEMORY.md` or daily logs

**Workspace Health** — Validate your workspace for common issues (missing files, broken skill frontmatter, files over the injection limit), check status, export backups, and consolidate accumulated training updates.

## Commands

| Command | What It Does |
|---------|-------------|
| `setup` | Interactive onboarding — builds your workspace from a conversation |
| `scaffold` | Drop raw templates (fallback for power users) |
| `log` | Log a training correction to the right file |
| `consolidate` | Merge accumulated training updates into main document sections |
| `validate` | Check workspace for errors and warnings |
| `status` | Dashboard of file sizes, skill count, last modified dates |
| `export` | Timestamped backup tarball of your entire workspace |
| `generate-skill` | Create a new skill from a description |

## Install

```bash
clawhub install training-manager
```

Or manually: copy the `training-manager/` folder into your workspace `skills/` directory.

## Usage

Just invoke `/training-manager` — if your workspace isn't set up yet, it'll start the interactive setup automatically. Otherwise, tell it what you need.

**Custom workspace path:** Scripts default to `~/.openclaw/workspace/`. If your workspace is elsewhere, set the `OPENCLAW_WORKSPACE` environment variable:

```bash
export OPENCLAW_WORKSPACE=~/my-workspace
```

## What Gets Created

After interactive setup, you'll have:

| File | Contents |
|------|----------|
| `IDENTITY.md` | Your agent's name and role |
| `USER.md` | Your name, timezone |
| `SOUL.md` | Communication style, tone, boundaries — translated from your preferences |
| `AGENTS.md` | Priorities and behavioral rules based on your use cases |
| `TOOLS.md` | Tool conventions relevant to your integrations |
| `MEMORY.md` | Long-term memory (starts with your first logged context) |

## Requirements

- Bash
- OpenClaw
- Linux or macOS

## License

MIT

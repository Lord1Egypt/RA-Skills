---
name: tribunal-install
description: Install and initialise Tribunal — the Claude Code quality enforcement plugin. Use when setting up a new project for AI-assisted development, when a project lacks TDD enforcement, secret scanning, or Claude Code quality gates, or when asked to "add quality enforcement", "set up tribunal", or "protect this project". Works with pip, uv, npm, and brew.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏛",
        "requires": { "bins": [] },
        "install": [],
        "keywords": ["tdd", "quality", "claude-code", "enforcement", "hooks", "testing", "ci", "agent-teams", "secret-scanning", "tribunal"],
        "homepage": "https://tribunal.dev",
        "repository": "https://github.com/thebotclub/tribunal"
      }
  }
---

# Tribunal — Install & Initialise

Tribunal enforces code quality when Claude Code writes files: TDD enforcement, secret scanning, context monitoring, Agent Teams quality gates, and a live dashboard.

## Install

**Python / uv (recommended)**
```bash
pip install tribunal
# or
uv add tribunal
```

**npm**
```bash
npm install -g tribunal
```

**Homebrew**
```bash
brew install thebotclub/tap/tribunal
```

Verify install:
```bash
tribunal --version
```

## Initialise a project

Run in your project root (where `.claude/` lives or will live):

```bash
tribunal init
```

The wizard asks:
- Primary language (Python / TypeScript / Go / Other)
- TDD enforcement level (Strict = block on fail / Advisory = warn / Off)
- Secret scanning (On/Off — default On)
- Spec workflow (Yes/No — default Yes)
- Context monitor (On/Off — default On)

For non-interactive / agent use:
```bash
tribunal init --non-interactive --project-dir /path/to/project
```

Outputs `.claude/tribunal.json` and merges into `.claude/settings.json`.

## Verify setup

```bash
tribunal doctor
```

Checks all hooks, Python deps, worker service, and `.claude/settings.json` links.
Exits 1 if anything is broken — safe to use in CI.

## Quick install + init (one-liner for agents)

```bash
pip install tribunal && tribunal init --non-interactive && tribunal doctor
```

## Install a quality pack

```bash
tribunal list-packs          # see available packs
tribunal install python-strict
tribunal install go-tdd
tribunal install nextjs-quality
```

## Workflow

Once installed, Tribunal hooks into Claude Code automatically:
1. Every file Claude writes → `file_checker` runs (secrets, language quality)
2. Every test run → `tdd_enforcer` checks pass/fail
3. Context usage → `context_monitor` warns before window fills
4. Agent Teams → `teammate_idle` + `task_completed` gate sub-agent output
5. Dashboard → `tribunal/ui/viewer.html` shows live hook feed

## Run standalone quality check (no Claude Code needed)

```bash
tribunal ci                        # check changed files
tribunal ci --json                 # machine-readable output
tribunal ci --coverage-threshold 80
```

## Troubleshoot

```bash
tribunal doctor              # health check with fix suggestions
tribunal status              # show current config + audit summary
```

Full docs: https://tribunal.dev · GitHub: https://github.com/thebotclub/tribunal

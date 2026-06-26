---
name: skill-starter-pack
description: One-click install curated skill packs for new OpenClaw users. Use when user says "install starter pack", "setup skills", "一键安装", "新手套餐", "install essential/developer/full pack", "推荐技能", "装什么skill好", or wants to quickly set up recommended skills. Provides three tiers — Essential (daily use), Developer (coding & automation), Full (all recommended). Each pack is a superset of the previous one.
---

# Skill Starter Pack

One command to install all the skills you need. Three curated packs from battle-tested daily use — no guesswork, no one-by-one searching.

## Why This Exists

New OpenClaw users face 26,000+ skills on ClawHub. Most are noise. This pack collects the 14 skills that actually matter for daily use, curated from real-world experience.

## Packs

### 🟢 Essential — 7 skills
> *"I just installed OpenClaw, what should I get?"*

The foundation. Memory, learning, search, notes — everything a productive agent needs from day one.

| Skill | What it does |
|---|---|
| **agent-memory-architect** | Persistent 3-tier memory (HOT/WARM/COLD). Agent remembers preferences, learns from corrections, shares knowledge across agents. |
| **self-improving** | Self-reflection after every task. Agent catches its own mistakes and improves permanently. |
| **find-skills** | Say "find a skill for X" and agent searches ClawHub for you. Never manually browse again. |
| **quick-note** | Say "记一下" or "note this" — instant note capture without friction. |
| **weather** | Weather and forecasts for any location. No API key needed. |
| **summarize** | Summarize any URL, PDF, image, audio file, or YouTube video in seconds. |
| **multi-search-engine** | 17 search engines (8 Chinese + 9 Global). Baidu, Sogou, Google, DuckDuckGo, WolframAlpha and more. No API keys. |

### 🔵 Developer — Essential + 4 skills (11 total)
> *"I'm a developer, what else do I need?"*

Adds coding workflow tools on top of Essential.

| Skill | What it does |
|---|---|
| **git-workflows** | Advanced git: interactive rebase, bisect bugs, worktrees for parallel dev, reflog recovery, subtrees/submodules. |
| **browser-use** | Automate browser interactions — web testing, form filling, screenshots, data extraction. |
| **image-analyzer** | Image recognition, OCR text extraction, scene analysis, object detection. |
| **github** | Full GitHub CLI integration — issues, PRs, CI runs, API queries via `gh`. |

### 🟣 Full — Developer + 3 skills (14 total)
> *"Give me everything."*

Adds advanced agent intelligence on top of Developer.

| Skill | What it does |
|---|---|
| **agent-team-monitor** | Monitor multi-agent teams in real-time — progress, token usage, status per agent. |
| **decide** | Agent auto-learns your decision patterns. Grows autonomy with trust, confirms before assuming. |
| **proactive-agent** | Transform agent from task-follower to proactive partner. WAL Protocol, Working Buffer, Autonomous Crons. |

## How to Use

### Quick install

Tell your agent which pack you want:

- "安装基础包" or "install essential pack"
- "安装开发者包" or "install developer pack"
- "安装全量包" or "install full pack"

### Agent execution

Run the install script with the pack name:

```bash
python <skill-dir>/scripts/install_pack.py <pack-name>
```

`<pack-name>`: `essential` | `developer` | `full`

### Mix and match

Combine a pack with extra skills:

```bash
python <skill-dir>/scripts/install_pack.py essential proactive-agent decide
```

This installs the Essential pack plus the two extra skills.

### What happens during install

1. Script resolves `clawhub` CLI (global or via `npx`)
2. Installs each skill sequentially with 1s delay (respects rate limits)
3. Shows progress: `[1/7] Installing agent-memory-architect... ✅`
4. Already-installed skills are skipped automatically
5. Summary report at the end with success/failure counts

## Post-Install

After installation:
1. ✅ Report which skills installed successfully
2. ❌ For failures, suggest `clawhub install <skill-name>` to retry
3. 💡 Remind user to restart the session (`/restart` or restart gateway) for new skills to activate
4. 📋 Some skills need extra setup — their own SKILL.md will guide the user

## Pack Comparison

See `references/skill-packs.md` for the full comparison table and skill source details.

## Requirements

- OpenClaw installed and running
- `clawhub` CLI available (`npm i -g clawhub` or use `npx clawhub`)
- Network access to clawhub.ai

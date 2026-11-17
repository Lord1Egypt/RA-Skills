# 🩺 Skill Health Checkup

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**English** | **[中文](README.zh-CN.md)**

A full physical exam for every skill you've installed: who overlaps whom, who never fires, who has a broken description — one health report with concrete fixes.

**5 checks. 1 report. 0 dependencies.**

**The problem:** Install enough skills and they start fighting — two wake for the same request, none wake for the important ones, and a vague description turns a skill into dead weight. Nobody notices until the agent misfires. Skill Health Checkup catches it before your users do.

## Table of Contents

<details>
<summary>Click to expand</summary>

- [How It Works](#how-it-works)
- [The 5 Checks](#the-5-checks)
- [Install](#install)
- [Quick Start](#quick-start)
- [Files](#files)
- [License](#license)

</details>

## How It Works

```
skills dir ──▶ scan_skills.py ──▶ names / descriptions / keywords
                    │
                    ▼
        ┌───── agent semantic exam ─────┐
        │  trigger overlap pairs        │
        │  dead zones · fitness         │
        │  duplicates · bloat           │
        └──────────────┬────────────────┘
                       ▼
        🩺 health report + top-3 fixes
```

The script handles deterministic facts (parse frontmatter, extract trigger phrases, pre-screen keyword overlap); the agent makes the semantic RED/YELLOW/GREEN verdicts and proposes exact description diffs.

## The 5 Checks

| # | Check | Catches |
|---|---|---|
| 1 | **Trigger Overlap** | Two skills claiming the same scenario — with the exact "wake-both" sentence quoted |
| 2 | **Dead Zones** | Frequent tasks with no skill covering them — expansion space, with ideas |
| 3 | **Description Fitness** | Too short / no "Use when" phrase / features-instead-of-scenarios |
| 4 | **Duplicates** | Same function installed twice |
| 5 | **Bloat** | Heavy skills that never fire — dead loading weight |

## Install

```bash
# ClawHub
clawhub install skill-health-scan

# Or from source
git clone https://github.com/Thomaszhou22/skill-health-scan.git
cp -r skill-health-scan ~/.openclaw/skills/
```

## Quick Start

```bash
# 1. Deterministic scan
python3 scripts/scan_skills.py --dir ~/.openclaw/skills --json

# 2. Ask your agent: "run a skill health checkup"
```

## Files

```
skill-health-scan/
├── SKILL.md                    # the exam (5 checks + fix protocol)
├── scripts/
│   └── scan_skills.py          # deterministic scanner (stdlib only)
└── references/
    └── report-template.md      # health report layout
```

## License

MIT

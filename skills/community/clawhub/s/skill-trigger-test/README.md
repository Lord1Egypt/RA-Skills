# 🎯 Trigger Test

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**English** | **[中文](README.zh-CN.md)**

Test whether your skills actually fire. Trigger Test feeds synthetic (or your real) user messages through the same descriptions a host model reads, then scores hit / miss / false-alarm per skill — catching the silent failures the official eval tool misses.

**4 questions. 1 report. 0 API calls.**

**The problem:** the official skill-creator's eval script reports 0% trigger rate across all queries (10+ independent reproductions) — and even when it worked, it only tested "did it fire," never "did it stay silent when it should." Trigger Test covers both directions with a reproducible, zero-dependency protocol.

## Table of Contents

<details>
<summary>Click to expand</summary>

- [How It Works](#how-it-works)
- [The Two Failure Modes](#the-two-failure-modes)
- [Test Suites](#test-suites)
- [Install](#install)
- [Quick Start](#quick-start)
- [Files](#files)
- [License](#license)

</details>

## How It Works

```
your skills' descriptions
        │
        ▼
┌──────────────────────────┐
│  for each test message   │
│  × each skill:           │
│   Q1 intent match?       │
│   Q2 keyword evidence?   │
│   Q3 competition?        │
│   Q4 verdict             │
└────────────┬─────────────┘
             ▼
  🎯 hit / miss / false-alarm
     per-skill + installation score
```

No model calls, no external API — the agent applies the same 4-question protocol (references/analysis-protocol.md) that produces reproducible verdicts across sessions, because trigger selection in the wild depends on exactly what the host reads: the `description`.

## The Two Failure Modes

| Failure | What it looks like | Why it hurts | Fix |
|---|---|---|---|
| **Miss** (silent failure) | User types the exact intent; skill stays silent | User thinks the skill is broken; uninstalls | Add the missed phrasing verbatim to the description |
| **False alarm** | Skill fires for a neighboring intent | Annoying interruption; erodes trust | Narrow with an explicit "Do NOT use for…" sentence |

Most tools only test the first. Trigger Test treats both as first-class, plus **contested** (two skills claim the same message) and **borderline** calls that surface hidden ambiguity.

## Test Suites

**A. Generated** — from each skill's own description: 3 positives (including the hard case: same intent, completely different words), 3 negatives from neighboring intents (share keywords, differ in intent), 1 ambiguous. Zero setup.

**B. Your real messages** — paste 5–10 messages you actually sent where you wished a skill had (or hadn't) fired. Ground truth, highest signal.

## Install

```bash
# ClawHub
clawhub install trigger-test

# Or from source
git clone https://github.com/Thomaszhou22/skill-trigger-test.git
cp -r skill-trigger-test ~/.openclaw/skills/
```

## Quick Start

Ask your agent: **"run a trigger test on all my skills"** — it generates the suite, applies the protocol, and hands you the scorecard. Or with real messages: "test these messages against my skills: …"

## Files

```
trigger-test/
├── SKILL.md                        # the test runner (protocol + scoring + fix loop)
└── references/
    ├── analysis-protocol.md        # the 4-question analysis (reproducible verdicts)
    └── report-template.md          # scorecard layout
```

## License

MIT

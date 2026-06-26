---
name: meta-skill
version: 1.0.0
description: "Stop repeating yourself. SkillForge watches how you work, discovers your patterns, and forges them into reusable Skills — automatically. The more you use it, the smarter your AI gets."
author: keithqpli
tags:
  - self-evolving
  - meta
  - productivity
  - workflow-optimization
  - pattern-discovery
---

# 🧬 SkillForge — Your AI That Evolves With You

> **Stop repeating yourself.**
> SkillForge watches how you work, discovers your patterns, and forges them into reusable Skills — automatically.
> The more you use it, the smarter your AI gets.

Every professional has invisible routines — the same checks before deploying, the same steps when starting a new experiment, the same format when writing reports. You do them on autopilot, but your AI assistant starts from scratch every time.

**SkillForge changes that.** It mines your work history, finds what you keep doing over and over, and crystallizes those patterns into Skills your AI can execute consistently. No manual documentation. No prompt engineering. Just work — and let your AI learn from you.

---

## 🚀 30-Second Quick Start

```
1. Install this Skill
2. Work normally for a few days (daily logs accumulate automatically)
3. Say: "有什么可以沉淀的？" or "What patterns can you find?"
4. Review the Pattern Report → confirm what to keep
5. Done. Your AI just leveled up.
```

**That's it.** The algorithm details below are for the curious. You don't need to understand them to use SkillForge.

---

## ⚡ How It Works — Three Engines, One Loop

```
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │  Scout   │ ───▶ │  Smith   │ ───▶ │  Sensei  │
    │ Discover │      │  Forge   │      │  Evolve  │
    └──────────┘      └──────────┘      └──────────┘
         ▲                                    │
         └────────── feedback loop ───────────┘
```

| Engine | What it does | When it runs |
|--------|-------------|--------------|
| **Scout** 🔍 | Scans your daily work logs, finds repeated patterns using fingerprint clustering + FTRVO scoring | On demand or weekly auto-scan |
| **Smith** 🔨 | Takes discovered patterns and forges them into complete, ready-to-use Skills (or merges into existing ones) | When a pattern scores high enough |
| **Sensei** 🎯 | Monitors Skill health — usage, drift, satisfaction — and suggests evolution or retirement | Weekly health check |

### The FTRVO Score — Should This Become a Skill?

Every discovered pattern gets a 5-dimension score (max 25 points):

| Dimension | What it measures |
|-----------|-----------------|
| **F**requency | How often does this pattern appear? |
| **T**rigger | Is there a clear, consistent trigger? |
| **R**eproducibility | Are the steps consistent each time? |
| **V**alue | How complex/impactful is the workflow? |
| **O**utput | Does it produce tangible artifacts? |

- **20-25**: 🟢 Strongly recommended — auto-generates a Skill draft
- **15-19**: 🟡 Recommended — shows you the report, you decide
- **10-14**: 🔵 Keep watching — not enough data yet
- **< 10**: ⚪ Skip — probably not worth automating

> 📐 Want the math? See [references/ALGORITHM.md](references/ALGORITHM.md)

---

## 🎯 Trigger Keywords

Say any of these to activate SkillForge:

| What you say | What happens |
|-------------|-------------|
| "有什么可以沉淀的" / "最近重复做了什么" | Scout scans for patterns |
| "把这个流程沉淀成 Skill" | Smith forges current workflow into a Skill |
| "看看 Skill 健康度" / "盘点 Skill" | Sensei runs health check |
| "进化" / "evolve" / "复盘" / "evomap" / "skillforge" | Full pipeline: Scout → Smith → Sensei |
| "meta skill" / "meta-skill" / "自进化" | Full pipeline |
| "模式发现" / "pattern" | Scout only |
| "skill review" / "skill健康度" | Sensei only |

---

## 📋 Workflows

### Weekly Auto-Scan (Recommended)

Set up a weekly automation to run the full pipeline:

```
Trigger (every Friday 5 PM)
  → Scout scans this week's daily logs
  → Clusters similar operations, scores with FTRVO
  → Filters patterns scoring ≥ 15
  → Checks overlap with existing Skills
  → Sensei evaluates all Skill health metrics
  → Outputs: Weekly Evolution Report
```

**Sample output:**

```markdown
# 🧬 SkillForge Weekly Report — 2026-W12

## New Patterns Found
- 🆕 "Training Launch Checklist" — FTRVO: 22/25 → Forge into Skill?
- ⏳ "Code Review Format" — FTRVO: 13/25 → Keep watching

## Skill Health
| Skill | Health | Usage (30d) | Action |
|-------|--------|-------------|--------|
| project-manager | 🟢 4.75 | 12x | All good |
| data-formatter | 🟡 3.2 | 4x | Low coverage — simplify? |
```

### On-Demand Pattern Discovery

Just say: **"有什么可以沉淀的？"**

Scout scans your recent work, finds patterns, and presents a report. You decide what to keep.

### Manual Skill Forging

After doing a multi-step workflow, say: **"把这个沉淀成 Skill"**

Smith extracts the workflow from the current conversation, generates a complete SKILL.md draft, and puts it in `{workspace}/skillforge-drafts/` for your review. **Nothing gets installed without your explicit approval.**

---

## 🛡️ Safety Rules

These are **non-negotiable** and cannot be overridden by config:

1. **Never auto-install** — All generated Skills require explicit user confirmation
2. **Never delete existing Skills** — Only suggests archiving; you decide
3. **Read-only on work memory** — SkillForge reads your logs but never modifies them
4. **Privacy-first** — Reports contain pattern summaries, never raw quotes from your work logs
5. **Draft isolation** — Generated drafts go to `skillforge-drafts/`, never polluting your active Skills

---

## ⚙️ Key Configuration

Most defaults work out of the box. Tweak these if needed:

| Parameter | Default | What it controls |
|-----------|---------|-----------------|
| `scout.lookback_days` | 14 | How far back to scan daily logs |
| `scout.similarity_threshold` | 0.65 | How similar two actions must be to cluster together |
| `scout.min_cluster_size` | 3 | Minimum occurrences to count as a "pattern" |
| `smith.merge_threshold` | 0.70 | When to merge into existing Skill vs. create new |
| `sensei.zombie_threshold_days` | 30 | Days of zero usage before flagging as zombie |
| `general.realtime_detection` | true | Detect patterns during live conversations |

> 📋 Full config template: [references/CONFIG_FULL.md](references/CONFIG_FULL.md)

---

## 🧪 Real-World Examples

### Example 1: "You keep doing the same pre-training checks"

```
Scout discovers:
  3/18: "Check GPU → confirm data path → start training → setup wandb"
  3/20: "Check GPU → data path → launch training → wandb config"
  3/22: Same pattern again

→ Pattern Report:
  Name: Training Launch Checklist
  FTRVO: F=5 T=5 R=4 V=4 O=4 = 22/25 ✅

→ You confirm → Smith generates "training-launcher" Skill
→ Next time you train, your AI runs the checklist automatically
```

### Example 2: "Your existing Skill can do more"

```
Scout notices you always check unmerged PRs after your morning briefing

→ Instead of a new Skill, suggests:
  "Extend project-manager's morning briefing module
   with a '📌 Unmerged PR Reminder' section"

→ You confirm → Sensei updates project-manager v1.2.0 → v1.3.0
```

### Example 3: "That Skill you made 2 months ago? Dead."

```
Sensei weekly health check:
  guardian Skill — 0 uses in 45 days 🔴

→ Suggests: Archive to ~/.workbuddy/skills-archive/
→ You decide: archive it or give it another chance
```

---

## 📁 Prerequisites

SkillForge works best with WorkBuddy's daily log system:

- **Required**: Daily log files at `{workspace}/.workbuddy/memory/YYYY-MM-DD.md`
- **Optional**: Long-term memory at `{workspace}/.workbuddy/memory/MEMORY.md`

**Don't have daily logs yet?** No problem — SkillForge can also analyze your current conversation history. The more data it has, the better the pattern detection. Daily logs just give it a longer memory.

**First-time setup**: Just start using SkillForge. It will create its working directory (`{workspace}/.workbuddy/skillforge/`) automatically on first run.

---

## 🤔 FAQ

**Q: Will it mess up my existing Skills?**
A: No. SkillForge never modifies existing Skills without your explicit approval. All changes go through a draft → review → confirm workflow.

**Q: What if it finds patterns I don't want to automate?**
A: Just say no. Every pattern report is a suggestion, not an action. You're always in control.

**Q: Does it need internet access?**
A: No. Everything runs locally on your work memory. No data leaves your machine.

**Q: How is this different from just writing Skills manually?**
A: You *could* write them manually — but you probably won't. SkillForge catches the patterns you don't even notice, and generates production-ready SKILL.md files that would take you an hour to write from scratch.

---

*Built with ❤️ by a human who got tired of repeating himself.*
*Powered by the belief that your AI should learn from YOU, not the other way around.*

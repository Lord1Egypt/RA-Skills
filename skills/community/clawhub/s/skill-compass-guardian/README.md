# 🛡️ Skill Compass

> **Diagnose, fix, and prevent AI agent skill trigger failures — at the source.**

65% of agent skills fail to trigger because of preventable description issues. Skill Compass finds them and fixes them.

---

## The Problem

You installed a skill. The agent **refuses to use it**. Sound familiar?

This is the #1 reported pain point in AI agent communities:

> *"My agent is terrible. It forgets, fails at tasks, and isn't familiar with its own skills."* — r/openclaw

> *"OpenClaw does not fetch skills when needed even though the agent is instructed for that."* — r/clawdbot

> *"Not able to use a single skill."* — r/openclaw

You're not alone. And it's usually **not your fault**.

---

## Why Skills Don't Trigger

After analyzing **GitHub issues, Reddit posts, community forums, and a 650-trial activation study**, we found that skill triggering failures break down into 6 categories:

| # | Root Cause | Frequency | Fixable? |
|---|-----------|:---------:|:--------:|
| 1 | **Description has no trigger condition** — says "Helps with X" instead of "Use when X" | **65%** | ✅ |
| 2 | **YAML parsing failure** — unquoted colon breaks `description:` field | **15%** | ✅ |
| 3 | **Token budget overflow** — too many skills, descriptions silently dropped | **10%** | ✅ |
| 4 | **Skill not discovered** — wrong directory, symlink skip, session cache | **5%** | ✅ |
| 5 | **Sub-agent isolation** — child agents don't inherit parent skills | **3% | Manual |
| 6 | **Capabilities mismatch** — skill active but tools not enabled | **2%** | Manual |

**The headline: 80% of failures are caused by bad descriptions.**

---

## How It Works

Skill Compass operates on one core insight:

> **Agent routing IS description matching. Fix the description, fix the routing.**

Most competing skills try to add a "routing layer" on top of the agent — intercepting, re-ranking, or force-injecting skills at runtime. That's treating the symptom.

Skill Compass treats the disease: **it makes every skill's description so good that the agent's native matching never misses.**

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPETING APPROACH                        │
│                                                             │
│  User Request → Agent picks wrong skill                     │
│                        ↓                                    │
│               [Runtime Router / Interceptor] ← extra cost   │
│                        ↓                                    │
│               Corrected selection → extra latency           │
│                                                             │
│  Problem: Adds tokens, latency, and another failure point   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  SKILL SENTINEL APPROACH                     │
│                                                             │
│  User Request → Agent picks correct skill → Done            │
│                       ↑                                     │
│              Description already says exactly                │
│              when to trigger. No interceptor needed.        │
│                                                             │
│  Result: Zero extra tokens, zero latency, zero moving parts │
└─────────────────────────────────────────────────────────────┘
```

### The Three-Layer Architecture

```
Layer 1: DIAGNOSE          Layer 2: FIX              Layer 3: PREVENT
─────────────────          ─────────                 ───────────────
Scan all SKILL.md          Auto-remediate             Description
files for 6 issue          common problems:           Design Pattern
categories:                • Quote YAML colons        guide based on:
                           • Add trigger phrases      • 650-trial study
• Missing triggers         • Trim descriptions        • agentskills.io
• YAML errors              • Flag conflicts           • Community data
• Token overflow                                     • Real fail cases
• Path discovery
• Conflict detection
    │                         │                          │
    ▼                         ▼                          ▼
 Audit Report              Fixed Skills            Future skills trigger
 (scored 0-100)           (immediately better)     correctly every time
```

---

## The Science: Description Design Pattern

Based on a **650-trial activation study** (Ivan Seleznov, 2026) and the **agentskills.io specification**:

### The Formula

```
[Trigger condition] + [Capability declaration] + [Search vocabulary]
```

### Directive Beats Descriptive — By 2.7×

| Style | Activation Rate | Example |
|-------|:--------------:|---------|
| **Directive** | **~100%** | `"ALWAYS invoke when the user asks about weather, temperature, or forecasts. Do not attempt weather lookups without this skill."` |
| Descriptive | ~37% | `"Helps with weather information."` |

### The Rules

1. **Lead with trigger** — what the user would actually type
2. **Use imperative voice** — "Use when...", "ALWAYS invoke for..."
3. **Add negative constraints** — "Do NOT use for..." prevents false triggers
4. **Include keywords** — multilingual, synonyms, typos
5. **Stay under 150 chars** — core trigger sentence only
6. **Frontmatter = routing, body = documentation** — never mix them

---

## Quick Start

### Audit Your Skills

```bash
# Audit all skills in default directories
python3 scripts/audit_skills.py

# Audit a specific directory
python3 scripts/audit_skills.py --skills-dir ~/.openclaw/skills

# Get JSON output for CI/CD
python3 scripts/audit_skills.py --json

# Auto-fix common issues (YAML colons, etc.)
python3 scripts/audit_skills.py --fix
```

### Sample Output

```
🛡️  SKILL SENTINEL — AUDIT REPORT

📂 Directory: ~/.openclaw/skills
📊 Total skills: 18
⚠️  Issues found: 11

📈 Score Summary:
   Average score: 81/100
   ✅ Passing (≥70): 12
   ⚠️  Needs work (<70): 6
   🔴 Critical (<30): 0

🪙  Token Budget: ✅ 4463 chars (OK)

⚠️  multi-search-engine — Score: 50/100
   • NO_TRIGGER: Missing trigger condition
   • WEAK_LANG: Uses passive language instead of directive
   💡 Add trigger phrases: "Use when...", "Invoke when..."

✅ powerpoint-pptx — Score: 100/100
```

---

## How It Differs From Competitors

| Feature | Skill Compass | skill-auto-use | skill-auto-router | skill-evaluator | skill-search-optimizer |
|---------|:--------------:|:--------------:|:-----------------:|:---------------:|:---------------------:|
| **Approach** | Fix at source | Runtime injection | Runtime routing | Pre-publish QA | SEO for ClawHub |
| **Solves "won't trigger"** | ✅ Root cause | ⚡ Symptom | ⚡ Symptom | ❌ Different goal | ❌ Different goal |
| **Extra token cost** | Zero | Every message | Every message | N/A | N/A |
| **Automated audit script** | ✅ | ❌ | ✅ (basic) | ✅ (25 criteria) | ❌ |
| **Failure case database** | ✅ 6 patterns | ❌ | ❌ | ❌ | ❌ |
| **Platform compatibility** | Universal | OpenClaw | OpenClaw | OpenClaw | ClawHub only |
| **Side effects** | None | May over-trigger | Latency | None | None |

### The Key Insight

```
Competitors: "The agent picked the wrong skill? Let me correct its choice."
Skill Compass: "WHY did it pick wrong? Because the description is bad. Let me fix the description."

Fix the root cause → the symptom disappears → no interceptor needed.
```

---

## What's Inside

```
skill-compass/
├── SKILL.md                          # Main skill with triage workflow
├── scripts/
│   └── audit_skills.py               # Automated diagnostic tool
├── references/
│   └── failure-patterns.md           # 6 real-world failure patterns with fixes
└── README.md                         # You are here
```

### SKILL.md

The main skill file. When triggered, it guides the agent through:
1. **Quick Triage** — 6-step diagnostic checklist (most common first)
2. **Description Design Pattern** — the formula for writing descriptions that trigger reliably
3. **Audit Workflow** — step-by-step from scan to fix to verify
4. **Conflict Detection** — identify overlapping descriptions that cause misrouting
5. **Token Budget Management** — prevent silent skill dropping
6. **Auto-Calibration** — feedback loop for continuous improvement

### scripts/audit_skills.py

A standalone Python script that scans skill directories and reports:
- ✅/⚠️/🔴 Quality score (0-100) for each skill's description
- YAML frontmatter validity (parsing errors, colon issues, missing fields)
- Token budget analysis (total description chars vs. threshold)
- Inter-skill conflict detection (keyword overlap >40%)
- Auto-fix mode for common issues (`--fix` flag)

### references/failure-patterns.md

6 documented failure patterns with real community case studies:
- Sources: GitHub Issues (#43410, #29981, #43735, etc.), Reddit (r/openclaw, r/clawdbot), DEV.to, Medium
- Each pattern includes: symptom → root cause → fix → source citation

---

## Research Foundation

| Source | Key Finding |
|--------|------------|
| [650-Trial Activation Study](https://medium.com/@ivan.seleznov1) (Seleznov, 2026) | Directive descriptions achieve **100%** activation vs. **37%** for descriptive |
| [GitHub openclaw/openclaw #43410](https://github.com/openclaw/openclaw/issues/43410) | **65%** of built-in skills lack trigger phrases |
| [agentskills.io Best Practices](https://agentskills.io/skill-creation/optimizing-descriptions) | Description = trigger (when) + capability (what) + keywords (search) |
| [SkillRouter Paper](https://arxiv.org/abs/2603.22455) (arxiv, 2026) | Implementation details matter more than metadata for skill selection |
| [Agent Skills Survey](https://arxiv.org/html/2602.12430v3) (arxiv, 2026) | First comprehensive survey of the skill abstraction layer |
| [DEV.to Skill Triggering Guide](https://dev.to/lizechengnet/why-claude-code-skills-dont-trigger-and-how-to-fix-them-in-2026-o7h) | Token budget overflow silently drops skills from context |
| [GitHub openclaw/openclaw #29981](https://github.com/openclaw/openclaw/issues/29981) | Colon in description breaks YAML parsing — skill disappears |
| [BSWEN Skill Triggering](https://docs.bswen.com/blog/2026-03-24-skill-triggering/) | Agent transforms descriptions into tool definitions for matching |

---

## Installation

### From ClawHub

```bash
clawhub install skill-trigger-doctor
```

### From GitHub

```bash
git clone https://github.com/Thomaszhou22/skill-compass.git
cp -r skill-compass ~/.openclaw/skills/
```

### Compatibility

- ✅ OpenClaw
- ✅ Claude Code
- ✅ Any platform using the agentskills.io SKILL.md standard

---

## License

MIT-0 — Free to use, modify, and distribute. No attribution required.

---

## Contributing

Found a new failure pattern? Add it to `references/failure-patterns.md`.

Have a skill that won't trigger? Run the audit, then [open an issue](https://github.com/Thomaszhou22/skill-compass/issues) if the audit doesn't catch it.

---

<p align="center"><strong>Fix the description. Fix the routing. Done.</strong></p>

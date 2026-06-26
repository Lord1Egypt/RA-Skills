# Skill Quality Check 🔍

> Universal quality assessment tool for AI Agent Skills. Evaluate any SKILL.md against AI agent best practices. Works with Claude, Cursor, Codex, OpenClaw, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Skills%20v2-blue)](https://openclaw.ai)

---

## What is Skill Quality Check?

**Skill Quality Check** is a universal quality assessment framework for AI Agent Skills (SKILL.md files). It evaluates how well a Skill is written against **AI agent best practices**, scoring five key dimensions and providing actionable improvement suggestions. Designed to work with skills built for Claude, Cursor, Codex, OpenClaw, or any AI agent platform.

### Why Does This Exist?

The AI Agent ecosystem is flooded with Skills — but most are written poorly:

- **Descriptions are too long** → wastes context tokens
- **Instructions are bloated** → confuses the AI
- **Resources aren't layered** → loads unnecessary content
- **No examples** → unpredictable outputs
- **Trigger keywords are vague** → wrong Skill gets called

Skill Quality Check solves this with a **systematic, repeatable evaluation process**.

---

## The Audit Mechanism

Skill Quality Check evaluates Skills across **5 dimensions** (100 points total + bonus/penalty):

```
┌─────────────────────────────────────────────────────────┐
│                  SKILL AUDIT SCORING                    │
├─────────────────────────────────────────────────────────┤
│  YAML Frontmatter Compliance       10 pts              │
│  Description Quality               40 pts              │
│  Body Quality                      40 pts              │
│  Resource Layering                 10 pts              │
│  Performance Impact                -5 ~ +2 pts         │
├─────────────────────────────────────────────────────────┤
│  Total: 100 pts + bonus                                │
└─────────────────────────────────────────────────────────┘
```

### Dimension Breakdown

| Dimension | Weight | What It Checks |
|-----------|--------|----------------|
| **YAML Frontmatter** | 10 pts | Is the metadata minimal and correct? |
| **Description Quality** | 40 pts | Is it a trigger, not a manual? Is it concise? |
| **Body Quality** | 40 pts | Progressive disclosure, role setting, examples, clarity |
| **Resource Layering** | 10 pts | Are scripts/references/assets used correctly? |
| **Performance Impact** | ±5 pts | Token cost, size, mis-trigger risk |

### Rating Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 85-100 | 🟢 Excellent | Install immediately — top quality |
| 70-84 | 🟡 Good | Installable — minor improvements suggested |
| 50-69 | 🔴 Acceptable | Install with caution — needs optimization |
| <50 | ⚫ Poor | Not recommended — find alternatives |

---

## Audit Rules: Why This Framework?

Every rule is grounded in **how AI context windows actually work**.

### Rule 1: Description is a Trigger, Not a Manual

**The Problem:** Many Skills stuff entire manuals into `description`.

```yaml
# ❌ WRONG — Description is too long
description: >
  This is a complete TDD guide including red-green-refactor cycles,
  step-by-step instructions for writing tests first, the philosophy
  behind test-driven development, common mistakes to avoid...

# ✅ RIGHT — Description is a trigger
description: >
  TDD test-driven development. Use when writing new features,
  adding tests, or fixing bugs. Keywords: test-driven, TDD, test first.
```

**Why:** `description` is Level 1 content (loaded every session). Keep it under 150 tokens.

### Rule 2: Progressive Disclosure

**The Framework:**

| Layer | Content | When Loaded |
|-------|---------|-------------|
| Level 1 | `name` + `description` | Every session (always in context) |
| Level 2 | SKILL.md body | Only when Skill triggers |
| Level 3 | `scripts/`, `references/`, `assets/` | Only during execution |

**Why:** Layer 1 loads for ALL Skills. Layer 2 loads for ONE Skill. Layer 3 costs zero context tokens.

### Rule 3: Claude is Already Smart

**The Problem:** Skills waste tokens explaining AI basics.

```yaml
# ❌ WRONG — Explains basic concepts
"Claude is very intelligent and can write Python code.
 It understands TDD and knows what a test is..."

# ✅ RIGHT — Only project-specific context
"Follow our TDD workflow: write test in tests/unit/ first,
 run pytest, then implement in src/. Never skip the test phase."
```

**Why:** Context window is finite. Add only what Claude doesn't know.

### Rule 4: Examples Over Explanations

**Best Practice:** 3-5 examples that are:
- **Relevant** — match real use cases
- **Diverse** — cover edge cases
- **Structured** — wrapped in XML tags

### Rule 5: Mechanical Enforcement

> "If it cannot be enforced mechanically, agents will deviate."

Skills should define rules that **can be automated**, not rules requiring human judgment.

---

## Quick Start

### For Users

To audit a Skill, just say:

```
Use skill-audit to review [skill-name or path]
```

The protocol runs 7 steps:
1. Read the SKILL.md file
2. Audit YAML frontmatter
3. Evaluate Description quality
4. Evaluate body quality
5. Assess resource layering
6. Calculate performance impact
7. Output the audit report

### For Developers

Integrate into CI/CD:

```python
report = audit_skill("path/to/skill")
if report.score < 70:
    raise Exception(f"Skill quality too low: {report.score}/100")
```

---

## File Structure

```
skill-audit/
├── SKILL.md                        # Main Skill (audit protocol)
├── README.md                       # This file
├── LICENSE                         # MIT License
└── references/
    ├── best-practices.md           # Detailed theory and best practices
    ├── audit-rules.md              # Full scoring rulebook
    └── examples/
        ├── good-skill-example/     # Example: excellent SKILL.md
        │   └── SKILL.md
        └── bad-skill-example/      # Example: poor SKILL.md
            └── SKILL.md
```

---

## Contributing

Contributions welcome! Please read:

1. [references/best-practices.md](references/best-practices.md) — Theory
2. [references/audit-rules.md](references/audit-rules.md) — Rulebook

Then submit a PR.

---

## Related Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **Skill Quality Check** | Quality assessment | Evaluating Skills |
| **Skill Vetter** | Security review | Checking for malicious code |
| **Skill Creator** | How to write Skills | Building new Skills |

**Recommended workflow:** Vetter → Quality Check → Creator

---

## References & Credits

- [Claude Official: Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [OpenClaw: Skill Creator](https://github.com/openclaw/openclaw/tree/main/skills/skill-creator)
- [Cursor: Agent & Skills](https://cursor.com/docs/agent)
- [OpenAI: Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

---

*Good Skills deserve serious review. Bad Skills deserve honest feedback.* 🔍🦀

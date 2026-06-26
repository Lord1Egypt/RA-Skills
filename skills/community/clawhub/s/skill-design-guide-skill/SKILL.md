---
name: skill-design-guide
display_name: "Skill Design Guide"
description: >
  Design better AI skills with proven architecture patterns. Helps you decide
  Workflow vs Agent, pick the right pattern (Prompt Chaining, Routing,
  Parallelization, Orchestrator-Workers, Evaluator-Optimizer), write clean
  SKILL.md files, and catch common mistakes with a 25-point quality checklist.
  Based on design principles from Anthropic, OpenAI, and LangChain.
version: "1.4.3"
agent_created: true
category: "Architecture / Design Patterns"
license: "MIT"
read_when:
  - Starting a new skill and unsure whether to use Workflow or Agent
  - Don't know which of the 5 workflow patterns to choose
  - Code works but architecture feels messy
  - Need to review a skill before production
  - "design skill architecture, workflow or agent, choose workflow pattern"
  - "review skill design, skill quality checklist, brain hands session"
  - "skill anti-patterns, prompt chaining vs routing, when to use agent"
---

# Skill Design Guide

> **30-Second Test**: If you're writing a SKILL.md or your skill "works but feels messy", load this guide.

## 🆚 What This Is (and Isn't)

| Tool | Purpose |
|------|---------|
| **skill-creator** | HOW to structure a SKILL.md file |
| **THIS GUIDE** | WHY behind design decisions — Workflow vs Agent, which pattern |

This guide answers **WHY**, not HOW. See `references/agent-design-research.md` for full industry research background.

## ✅ 3 Usage Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **New Design** | "I want to build a [X] skill" | Architecture blueprint (pattern + structure) |
| **Skill Review** | "Review this skill" / "Check quality" | Report via checklist |
| **Pattern Selection** | "Should I use X or Y?" | Pattern recommendation with rationale |

---

## Hard Rules

> **These cannot be violated. They override all other considerations.**

1. **Simplicity first.** Start with a single SKILL.md. Add complexity only when simpler solutions fail.
2. **Brain ≠ Hands.** LLM decides what to do (SKILL.md). Deterministic code does it (scripts/). Never mix them.
3. **No full preload.** References are loaded on-demand. Never dump everything into context at once.
4. **Every skill must have:** triggers, steps tagged `[Deterministic]`/`[LLM]`, Hard Rules, Failure Handling, Output Format.

---

## Principle Zero: Simplicity First

> **Start simple. Add complexity only when simpler solutions fall short.**

Practical checklist:
- Single SKILL.md before multiple files
- Deterministic code before LLM
- Fixed workflow before dynamic Agent
- Ship MVP, iterate from output quality

---

## Principle One: Brain / Hands / Session

| Layer | Role | File |
|-------|------|------|
| **Brain** | Decision logic, workflow definition | `SKILL.md` |
| **Hands** | Deterministic execution | `scripts/` |
| **Session** | Knowledge base, config, templates | `references/`, `assets/` |

**Your skills already follow this:** `data-ai-daily-brief` (scripts fetch data), `benjie-model` (Session layer for other skills).

---

## Step 1: Workflow or Agent?

One question: **Are the task steps predetermined?**

| Type | When |
|------|------|
| **Workflow** | Steps are clear and predictable → choose this (faster, cheaper, debuggable) |
| **Agent** | Steps uncertain, need dynamic planning → choose this (flexible but costly) |

**Most things are workflows.** Don't pick Agent because it sounds advanced.

---

## Step 2: Pick a Pattern

Five workflow patterns. Full details in `references/pattern-details.md`.

| Pattern | Best For |
|---------|----------|
| **Prompt Chaining** | Sequential steps with checkpoints |
| **Routing** | Clear input types → different paths |
| **Parallelization** | Independent subtasks |
| **Orchestrator-Workers** | Unpredictable subtasks (sparingly!) |
| **Evaluator-Optimizer** | Generate→Evaluate→Repeat until pass |

---

## Step 3: Skill Structure

### Required

| Component | Content |
|-----------|---------|
| **SKILL.md** | YAML frontmatter (`name`, `description`, `read_when`) + workflow + Hard Rules + Failure Handling + Output Format |

### Optional

| Component | When |
|-----------|------|
| `references/` | Domain knowledge (loaded on demand) |
| `scripts/` | Deterministic steps |
| `assets/` | Templates, configs |

### SKILL.md Template

```yaml
---
name: my-skill
description: One sentence. Trigger keywords: a, b, c.
version: 1.0.0
read_when:
  - "trigger phrase 1"
  - "trigger phrase 2"
---

# Skill Name

Overview paragraph.

## Workflow

### Step 1: [Deterministic] Confirm Input
- Validate input exists
- If missing, stop and report

### Step 2: [Deterministic] Load Materials
- Read `references/xxx.md` (only needed files)

### Step 3: [LLM] Core Execution
- Generate output following these rules:
  - Rule 1
  - Rule 2

### Step 4: [LLM] Self-Check
- Verify output meets criteria → fix → re-output

### Step 5: [Deterministic] Save Output

## Hard Rules

> These cannot be violated.

1. Rule 1
2. Rule 2

## Failure Handling

| Scenario | Action |
|----------|--------|
| Source file not found | Stop, report missing file |
| Output 50% over limit | Compress and rewrite |

## Output Format

[Define exact format and fields]
```

---

## Step 4: Quality Checklist

After completing a skill, run the full 25-point checklist. Load `references/quality-checklist.md` for details.

Structure ✓ | Principles ✓ | Tools ✓ | Guardrails ✓ | Observability ✓

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|------|
| **Over-engineering** | Start with single SKILL.md |
| **Full preload** | Load references on-demand only |
| **God Skill** | Split duties — one skill, one thing |
| **All-LLM** | Scripts for deterministic steps |
| **No guardrails** | Add Hard Rules + Failure Handling |
| **Vague output** | Define exact format and fields |
| **Publishing dirty** | Before publishing, run `skill-publish` to audit and clean |

---

## After Design: Publishing

When the skill is ready to share on ClawHub/GitHub, use **`skill-publish`** to audit and publish. It handles: personal data scanning, frontmatter validation, content cleanup, bilingual enforcement, file separation (local vs published), and dual-platform push.

---

## Failure Handling (for this guide itself)

| Scenario | Action |
|----------|--------|
| User asks for code, not design | Redirect to `skill-creator` |
| Pattern comparison ambiguous | Load `references/pattern-details.md` |
| Review request without skill details | Ask: "Show me your SKILL.md or describe what the skill does" |
| User wants to publish a completed skill | Redirect to `skill-publish` |

---

## References (on-demand)

| Need | Load |
|------|------|
| 25-point checklist | `references/quality-checklist.md` |
| Pattern deep dive | `references/pattern-details.md` |
| Platform-specific config | `references/platform-compatibility.md` |
| Industry research background | `references/agent-design-research.md` |
| Anthropic tool design | `references/anthropic-tool-design.md` |
| Publishing to ClawHub/GitHub | Use `skill-publish` (separate skill) |

---

*v1.4.3 | Based on Anthropic/OpenAI/LangChain design principles | 2026-06-23*

**Changelog:**
- v1.4.3: Restored display name "Skill Design Guide"
- v1.4.2: Consolidated `reference/` + `references/` into a single `references/` dir; fixed all reference paths
- v1.4.1: Fixed display name
- v1.4.0: Refactored for progressive disclosure — split checklist/patterns/platform into `references/`; added Hard Rules + Failure Handling; reduced SKILL.md from 13K to ~5K chars
- v1.3.0: Added usage scenarios, Chinese version (SKILL_zh.md)
- v1.2.0: Platform-agnostic rewrite, added Credits

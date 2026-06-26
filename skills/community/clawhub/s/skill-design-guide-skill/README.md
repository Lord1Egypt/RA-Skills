# Skill Design Guide

> **Before you write a single line of SKILL.md code — know which architecture you're building.**

[![ClawHub](https://img.shields.io/badge/ClawHub-skill--design--guide--skill-blue)](https://clawhub.ai/haiyangchenbj/skill-design-guide-skill)
[![GitHub](https://img.shields.io/badge/GitHub-haiyangchenbj-black)](https://github.com/haiyangchenbj/skill-design-guide-skill)

---

## Is This For You?

**Yes, if you've ever:**

- Started building a skill, then realized you're not sure if it should be a **Workflow** or an **Agent**
- Written code that "works," but three months later can't remember why you structured it that way
- Added "just one more step" until your skill became an unmaintainable tangle
- Copied a template, then spent hours fighting its assumptions
- Reviewed someone else's skill and couldn't articulate *why* the architecture felt off

**No, if you're looking for:** Copy-paste code snippets or step-by-step tutorials. This is an **architecture coach**, not a code generator.

---

## What Problem It Solves

Most skill architecture problems aren't technical—they're **decision problems**.

| The Real Problem | Why It Happens | What This Guide Does |
|-----------------|----------------|---------------------|
| "I don't know which pattern to use" | No clear decision framework | 5 workflow patterns + selection guide |
| "It works but I can't maintain it" | Architecture chosen for convenience, not clarity | Brain/Hands/Session separation principles |
| "I'm not sure if my skill is 'good'" | No quality standards | 25-point review checklist |
| "Every skill I build feels different" | No consistent design vocabulary | Standardized SKILL.md template |

---

## What You Get

### 1. Architecture Decision Framework

**Workflow vs Agent — the question everyone skips:**

- **Workflow**: You know *exactly* what needs to happen (predetermined steps)
- **Agent**: You know what success looks like, but not the steps (dynamic planning)

> Most "Agent" projects are actually Workflows in denial. Choosing wrong costs 10x in refactoring later.

### 2. Five Workflow Patterns

| Pattern | When to Use | Mental Model |
|---------|-------------|--------------|
| **Prompt Chaining** | Linear decomposition, each step builds on previous | Assembly line |
| **Routing** | Classify input, then branch to specialized handlers | Traffic director |
| **Parallelization** | Concurrent subtasks, aggregate results | Divide and conquer |
| **Orchestrator-Workers** | Complex task needing dynamic decomposition | Project manager + team |
| **Evaluator-Optimizer** | Iterative refinement until quality threshold | Editor revising drafts |

### 3. Brain / Hands / Session Architecture

Separate your skill into three layers:

- **Brain** (SKILL.md): Decision logic, workflow design, context requirements
- **Hands** (scripts/): Deterministic execution, external integrations
- **Session** (references/, configs/): Knowledge base, templates, configuration

> "The skill works" is table stakes. "The skill is maintainable" is the goal.

### 4. SKILL.md Template

Copy-paste ready template with:
- YAML frontmatter (name, version, trigger keywords)
- Required sections (Summary, Workflow, Tools, Guardrails)
- [Deterministic] / [LLM] step labels
- Failure Handling table
- Quality Checklist integration

### 5. 25-Point Quality Checklist

Five dimensions of review:

| Dimension | What It Checks |
|-----------|----------------|
| **Structure** | Complete sections, logical flow, no circular dependencies |
| **Principles** | Simplicity-first, clear boundaries, single responsibility |
| **Tools** | Deterministic vs LLM usage, error handling, timeout guards |
| **Guardrails** | Input validation, graceful degradation, security |
| **Observability** | Logging, tracing, result presentation |

---

## Installation

### WorkBuddy / CodeBuddy (via ClawHub)

```bash
clawhub install skill-design-guide-skill
```

Or manually:

```bash
git clone https://github.com/haiyangchenbj/skill-design-guide-skill.git
# Move to your skills directory:
# User-level (all projects): ~/.workbuddy/skills/
# Project-level: .workbuddy/skills/
```

### Claude Code

```bash
git clone https://github.com/haiyangchenbj/skill-design-guide-skill.git ~/.claude/skills/skill-design-guide
```

---

## Usage

**Auto-triggers when you mention:**
- "design a skill", "create a skill", "new agent"
- "skill review", "agent architecture", "skill quality"
- "workflow or agent", "which pattern should I use"
- "optimize skill", "skill checklist"

**Or explicitly:** "Load the skill-design-guide skill."

---

## Quick Start: The 3-Minute Review

Before shipping any skill, run through these three questions:

1. **Is it a Workflow or an Agent?** (If you can't answer clearly, it's probably a Workflow)
2. **Which pattern am I using?** (If none fit, you might be mixing concerns)
3. **Where's the failure handling?** (Every external call needs a Plan B)

Takes three minutes. Saves three hours of debugging later.

---

## Why This Exists

This skill started as personal notes. After building (and refactoring) a dozen skills, I noticed I kept making the same mistakes:

- Choosing "flexible" architecture when I needed "predictable"
- Letting convenience drive structure
- Not knowing how to evaluate "good" vs "good enough"

The frameworks here aren't original—they're distilled from Anthropic, OpenAI, and LangChain engineering practices, plus the scars of real projects.

**The goal:** Help you make the right architectural decisions *before* you're committed to the wrong ones.

---

## 🌐 中文版

See [SKILL_zh.md](SKILL_zh.md) for the Chinese version.

---

## File Structure

```
skill-design-guide/
├── SKILL.md                    # Core design guide (English)
├── SKILL_zh.md                 # 中文版
├── README.md                   # This file
├── reference/
│   ├── agent-design-research.md    # Industry research compilation
│   └── anthropic-tool-design.md    # Tool design best practices
└── LICENSE
```

---

## Sources & References

- [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) (Dec 2024)
- [Anthropic — Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (Sep 2025)
- [OpenAI — A Practical Guide to Building Agents](https://everawelabs.com/learn-it/a-practical-guide-to-building-agents) (Apr 2025)
- [LangChain — State of Agent Engineering 2025](https://blog.langchain.dev/) (Dec 2025)

---

## License

MIT License. See [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

> **"The skill works" is table stakes. "The skill is maintainable three months later" is the win.**

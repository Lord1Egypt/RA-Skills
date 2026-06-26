---
name: sprint-contract
version: 1.0.0
author: Mrpixelraf
description: Multi-agent development workflow with Sprint Contracts and independent QA evaluation. Use when building features, fixing complex bugs, or any task that involves spawning sub-agents to do work. Implements the Planner-Generator-Evaluator pattern (inspired by Anthropic's GAN-style harness design) to ensure quality through explicit completion criteria and independent testing. Triggers on development tasks, feature builds, bug fixes, code reviews, or when spawning coding agents.
---

# Sprint Contract — Multi-Agent Quality System

Based on [Anthropic's harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps): separate the agent doing the work from the agent judging it.

## Core Principle

**Never let the builder evaluate their own work on complex tasks.** LLMs reliably praise their own output — even when it's mediocre. An independent evaluator, tuned to be skeptical, catches what self-evaluation misses.

## Architecture

```
Planner (you/human) → Generator (sub-agent) → Evaluator (independent sub-agent)
     ↑                                              |
     └──────────── feedback loop ←──────────────────┘
```

## Workflow

### 1. Write a BRIEF.md with Sprint Contract

Every task gets a BRIEF.md. The Sprint Contract section is **mandatory** — it lists specific, testable completion criteria.

```markdown
# Task Brief

## Background
[Why this task exists]

## Objective
[What to build/fix]

## Sprint Contract (Completion Criteria)
- [ ] Criterion 1 (specific, verifiable)
- [ ] Criterion 2
- [ ] ...

⚠️ Write criteria specific to THIS task. No generic checklists.

## Related Files
[File paths relevant to the task]

## Constraints
[Tech stack, prior decisions, known pitfalls]

## Handoff Requirements
Write a HANDOFF.md when done, containing:
- What was done (file change list)
- Design decisions made (and why)
- What's left / known issues
- Everything needed for reporting to the human
```

### 2. Spawn Generator (Builder)

The generator receives the BRIEF.md and builds against the Sprint Contract. Key rules for the generator prompt:

- Work against the Sprint Contract criteria
- Self-check each criterion before handing off
- Write HANDOFF.md when done
- Write files first, read references second (output > research)

### 3. Spawn Evaluator (Independent QA)

After the generator finishes, spawn a **separate** agent as evaluator. The evaluator prompt must include:

**The Sprint Contract** — copied from BRIEF.md, to verify each criterion.

**4 Evaluation Dimensions** (select what's relevant):

| Dimension | What to check |
|-----------|--------------|
| **Functional completeness** | Every Sprint Contract criterion passes |
| **User experience** | Flow is intuitive, no dead ends |
| **Visual quality** | Layout, spacing, colors are professional |
| **Code/content quality** | No errors, clean logic, no regressions |

**The critical prompt line:**
> "Your job is to find problems, not to praise. If everything looks fine, you probably didn't test carefully enough. Report issues honestly — better a false alarm than a missed bug."

### 4. Decision Gate

Based on evaluator feedback:
- **All criteria pass** → Ship it
- **Criteria fail** → Feed evaluator report back to generator for fixes
- **Architecture issues** → Escalate to human

## When to Use Each Mode

| Task complexity | Generator | Evaluator | Example |
|----------------|-----------|-----------|---------|
| Simple (< 30 min) | Sub-agent | Self-evaluate, mark "⚠️ untested" | Fix a typo, update config |
| Medium (30 min - 2 hr) | Sub-agent | Independent sub-agent | New feature, bug fix |
| Complex (2+ hr) | Claude Code / ACP | Independent sub-agent + human review | Architecture change, new project |

## Sprint Contract Examples

See [references/contract-examples.md](references/contract-examples.md) for project-specific contract templates.

## Key Insights from Anthropic's Research

1. **File-based communication** — Agents talk through files (BRIEF.md, HANDOFF.md), not conversation
2. **Evaluator calibration** — Default LLMs are too lenient; explicitly prompt for skepticism
3. **Sprint scoping** — One feature at a time; don't bundle unrelated work
4. **Opus 4.6 + 1M context** — Context anxiety is gone; sprint decomposition is less critical, but evaluator still adds value at task boundaries
5. **Evaluation criteria shape output** — The wording of your criteria directly steers what the generator produces

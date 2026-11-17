# Socratic Dialogue

> **Reasoning discipline for AI agents.** Turns the model from an answer machine into a seminar partner: anchored definitions, adversarial cross-examination, faithfulness checks, and an autoimmune checkpoint against sycophancy.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)
[![Version](https://img.shields.io/badge/version-2.3-green)](./SKILL.md)
[![Status](https://img.shields.io/badge/status-stable-brightgreen)](#)
[![Skill Type](https://img.shields.io/badge/type-reasoning-purple)](#)

```text
┌─────────────────────────────────────────────────────────────┐
│                  COGNITIVE IMMUNE SYSTEM                    │
│                                                             │
│   🛡  Skin       (Definition / Horoi)                       │
│        rejects undefined premises                           │
│                                                             │
│   🛡  Antibodies (Adversarial Cross-Examination)           │
│        detects contradictions with Fixed Parameters         │
│                                                             │
│   🛡  T-cells    (Faithfulness Check)                       │
│        destroys claims that betray the reasoning chain      │
│                                                             │
│   ⚖   Autoimmune Checkpoint (Anti-Bias)                    │
│        prevents the agent from attacking its own verified   │
│        conclusions while still flagging real drift          │
└─────────────────────────────────────────────────────────────┘
```

---

## What it does

`Socratic Dialogue` is a reasoning skill that replaces the default "vending machine" interaction with a structured **seminar** model. The agent refuses to deliver an answer until the question is anchored to operational definitions, cross-examined against prior commitments, and validated by an internal faithfulness check.

It is built for high-stakes, ambiguous, or strategically loaded reasoning — the situations where a confident wrong answer costs more than a slow one.

---

## When to use

* **High-stakes reasoning** — wrong budget, technical, or contractual assumptions are costly.
* **Ambiguity anchoring** — terms like "success", "quality", "MVP" lack hard operational definitions.
* **Anti-fluency** — the model is smoothing over gaps instead of verifying variables.
* **Knowledge co-creation** — the goal is a shared conceptual breakthrough, not a quick answer.
* **Long sessions** — accumulating decisions need an explicit integrity check (Context Integrity).
* **Detected drift** — the model is sliding toward agreement without grounds (sycophancy, hedging).

## When NOT to use

* Simple factual lookups ("What is the capital of France?").
* Tight-latency tasks where one round of back-and-forth is too expensive.
* Passive users who do not want to engage in iterative clarification.
* Fully formalized or computational tasks with no ambiguity to resolve.

---

## Installation

See **[INSTALL.md](./INSTALL.md)** for platform-specific install instructions (Claude.ai, Claude Code, Codex, OpenCode, Grok, Anthropic API, Cursor, Continue.dev) and the full compatibility table.

Installation instructions live in a separate file to keep this README focused on purpose, usage, and evaluation. The install file contains only user-directed setup steps; the skill has no runtime dependency on background services, MCP tools, network access, or environment persistence.

### Activation boundaries

This skill should be invoked only for high-stakes, ambiguous, or strategically loaded reasoning tasks. It should not activate for simple lookups, routine editing, purely computational tasks, or situations where the user has not asked for deeper clarification.

---

## Usage examples

### Requirements alignment

```text
User: I want to improve the quality of the Story Map.
Agent: Before I touch the structure, let's define "quality."
       Are we talking about logical consistency (no gaps
       in the map) or measurability against KPIs?
```

### Conflict resolution

```text
User: Let's add feature X to the sprint.
Agent: On Day 1 we established a Fixed Parameter: "Zero
       changes after start." Adding X violates that rule.
       Are we revising the parameter, or moving X to the
       next iteration?
```

### Risk identification via aporia

```text
User: We should use microservices for this.
Agent: My confidence: Low. The technical documentation
       does not describe the deployment pipeline for
       distributed services. Should I assume Kubernetes,
       or do you have a specific platform?
```

### Knowledge compilation (freezing Fixed Parameters)

```text
Agent: Wrapping the elenchus phase. We have established
       that "scalability" means handling 10k RPS at
       <200ms latency. I am recording this as a Fixed
       Parameter. From now on, every architecture
       proposal will be verified against this.

       Confidence: 0.9 — reason: each value was stated
       by you and not contradicted since.
```

---

## Demo

A 60-second walkthrough of the skill in action lives at:

> **TODO** — add a short screen recording or animated GIF showing the agent refusing to answer an underspecified question, then walking through Definition → Elenchus → Faithfulness, then delivering a synthesis with Confidence Score.

For now, the four examples above are the canonical demo.

---

## Compatibility

See **[INSTALL.md](./INSTALL.md)** for the full compatibility table (Claude.ai, Claude Code, Anthropic Messages API, OpenAI Codex, OpenCode, Grok, Cursor, Continue.dev). Skill format follows the open [Agent Skills](https://agentskills.io) standard.

---

## What's inside

```
socratic-dialogue/
├── SKILL.md                              ← what the agent loads (workflow, rules, examples)
├── INSTALL.md                            ← platform-specific install + compatibility table
├── README.md                             ← this file
└── references/
    └── methodology-socratic-dialogue.md    ← deep reference (Plato, Vlastos, techniques)
```

`SKILL.md` is the **first** file the agent reads. `methodology-socratic-dialogue.md` is loaded **only when the workflow feels stuck** — it contains the philosophical depth, the failure modes, and the operational discipline behind the rules.

---

## Tags

`reasoning` `socratic` `anti-bias` `anti-sycophancy` `context-engineering` `epistemology` `requirements-gathering` `design-engineering` `ai-orchestration` `cognitive-immune-system` `high-stakes-reasoning` `fixed-parameters` `faithfulness-check`

---

## Author

**Monika Zapisek** — Product Designer / UX Team
Built as part of the **Design Engineering Playbook** (parent project in this repo).

---

## License

MIT — see the `LICENSE` file in the repository root.

---

## Related

* [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — the authoring standard this skill follows.
* [Agent Skills open standard](https://agentskills.io) — the portability format.
* **Design Engineering Playbook** (parent project in this repo) — the collection.

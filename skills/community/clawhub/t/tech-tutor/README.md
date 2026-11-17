<div align="right">
  <a href="README.zh-CN.md">中文</a> | English
</div>

# Tech Tutor

> *Your Socratic learning companion for deep technical understanding.*

---

## Quick Start

```bash
npx skills add https://github.com/LeoGoat2004/tech-tutor
```

Once installed, just say: *"I want to learn about [topic]"* or *"Help me understand this project"*.

---

## Why This Exists

AI tools write code, debug, and answer questions in seconds — it's easy, addictive, and has a hidden cost: **people stop thinking**. You lose the ability to reason through problems. You stop questioning *why*. You become dependent on a tool you don't deeply understand.

Tech Tutor pushes back — not by rejecting AI, but by using it to **build genuine understanding** instead of disposable answers.

The goal: when you finish a session, you can explain what you learned *without* the AI holding your hand.

---

## What It Does

A Socratic-style learning companion. It doesn't lecture — it asks questions, challenges assumptions, and helps you discover insights on your own.

**Two modes:**

| Mode | Use case | Example |
|------|----------|---------|
| **Topic Exploration** | Learn a concept from scratch | *"Teach me how Transformers work"* |
| **Project Deconstruction** | Understand a codebase deeply | *"Walk me through this project"* |

**Project deconstruction uses a six-layer framework** — systematic, from overview to hands-on:

```
1. Bird's Eye View    →  Tech stack, structure, purpose
2. Entry Point        →  Where execution begins, startup flow
3. Core Modules       →  Key components, responsibilities, dependencies
4. Core Flow          →  Trace one full path, inputs & outputs at each stage
5. Design Decisions   →  Why it's built this way, trade-offs
6. Extend & Modify    →  Learn by changing things, add a small feature
```

**Pre-configured domains:** Frontend · Backend · AI Infrastructure · Agent Harness · Multi-Agent · Reinforcement Learning · ROS

> No domain listed? Tech Tutor can teach any CS/AI topic by searching authoritative sources on the fly.

---

## Design Philosophy: The Socratic Method

> *"I cannot teach anybody anything. I can only make them think."* — Socrates

- **Ask, don't tell.** Questions lead you to your own conclusions.
- **Challenge assumptions.** *"What are we assuming here? What if that wasn't true?"*
- **Dig deeper.** *"Why do you think that is?"* — never settle for the first answer.
- **Admit ignorance.** Explore the unknown together.
- **Learn by doing.** Understanding deepens through practice, not passive reading.

**Core principle: understanding > completion.**

---

## How It Works

```
1. Understand Your Goal   →  What to learn? Your level? Record location?
2. Build Context          →  Authoritative sources + mental model + align expectations
3. Learn Together         →  Socratic dialogue, big picture first, you set the pace
4. Learning Record        →  Automatic — your insights, questions, gaps
5. Extra Deliverables     →  Optional — notes, cards, mind maps, etc. (you ask, you choose location)
```

### Learning Records (Dual-layer)

```
~/.tech-tutor/                     User-level (cross-project)
├── index.yml                      Index + review timing
├── project-index.yml              Global index of all project records
└── sessions/20260713_transformer/
    ├── record.md                  Your learning journey
    └── outputs/                   Optional deliverables

<project>/.tech-tutor/             Project-level (one project)
├── index.yml
└── sessions/20260715_langgraph/
    ├── record.md
    └── outputs/
```

Records capture *your* journey — aha moments, fuzzy spots, questions — not textbook summaries.

### Review & Spaced Repetition

Lightweight, conversation-based, no tests:
- **Timing**: ~1 / 3 / 7 / 14 / 30 days
- **Self-paced**: you decide how well you know it, intervals adjust
- **Natural trigger**: casually mentioned at session start — accept or skip

### Connected Learning

Genuine connections between new topics and past learning are surfaced when relevant. No forced links.

---

## Source Files

Pre-configured authoritative sources in `sources/`:

| File | Domain |
|------|--------|
| `frontend.yml` | Frontend web development |
| `backend.yml` | Backend development |
| `ai-infra.yml` | AI Infrastructure |
| `agent-harness.yml` | Agent frameworks |
| `multi-agent.yml` | Multi-agent systems |
| `rl.yml` | Reinforcement Learning |
| `ros.yml` | Robot Operating System |

Each includes official docs, top conferences, authoritative blogs, and courses.

---

*In the age of AI, real understanding is the real superpower. Don't outsource your thinking — sharpen it.*

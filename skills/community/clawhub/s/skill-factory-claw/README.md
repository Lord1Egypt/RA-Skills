# Harness

**Agent-first engineering knowledge base distilled from OpenAI's Harness Engineering and expanded with industry best practices.**

[![Version](https://img.shields.io/badge/version-1.2-blue.svg)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![中文文档](https://img.shields.io/badge/文档-中文版-orange.svg)](./README_zh.md)

---

## What It Does

Harness is a knowledge skill for building systems that AI agents can work in effectively. It answers questions like:

- How should I structure a codebase for an AI agent?
- What goes in `AGENTS.md` and how long should it be?
- How do I manage context without overwhelming the agent?
- What architectural constraints should I enforce from Day 1?
- How do I handle tech debt in a high-throughput agent workflow?

The knowledge is battle-tested: the original Harness Engineering team built ~1 million lines of code with 3 engineers in 5 months — zero manual coding.

---

## What Makes It Different

### 1. Multi-source, not a single opinion
Built on OpenAI's Harness Engineering as the core framework, then cross-validated and extended with:
- **Anthropic** — Claude Code and Computer Use production practices
- **GitHub** — Copilot Workspace workflow patterns
- **Open source** — Aider, Cline, Continue.dev field experience
- **Industry voices** — Eugene Yan, Chip Huyen, and others

### 2. Structured for fast retrieval
Three reference files with clear scope separation — quick-reference table, full distillation, extended sources. Load only what you need.

### 3. Principles, not checklists
10 core principles that form a coherent mental model for agent-first development, not a list of disconnected tips.

### 4. Actively maintained
Version-tracked with a changelog. New sources are added as the field evolves.

---

## The 10 Core Principles

| Principle | Key Idea |
|-----------|----------|
| **Humans steer, agents row** | Design environment + define intent + build feedback loops |
| **Context is scarce** | `AGENTS.md` ≤ 100 lines, progressive disclosure |
| **Invariants over micromanagement** | Strict layering enforced by linter, not by instruction |
| **Make apps agent-readable** | UI + logs + metrics visible to agents directly |
| **Continuous GC** | Small, continuous tech debt repayment — never let it accumulate |
| **Correct > wait** | Reduce blocking merge gates, iterate fast |
| **Repo as single source of truth** | If it's not in the repo, it doesn't exist for the agent |
| **Ralph Wiggum loop** | Agent self-reviews its own changes until all reviewers are satisfied |
| **Architecture is a Day-1 prerequisite** | Strict layering is foundational, not optional |
| **Agent-readable tech** | Composable, stable APIs, well-represented in training data |

---

## Quick Start

Once installed to `~/.workbuddy/skills/harness/`, the skill loads automatically when you ask about:

- Structuring codebases for agents
- Writing `AGENTS.md`
- Context management strategies
- Architecture constraints
- Observability for agents
- Tech debt in agentic workflows

---

## File Structure

```
harness/
├── SKILL.md                    # Skill entry point (triggers + quick summary)
├── README.md                   # English introduction (this file)
├── README_zh.md                # Chinese introduction
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT
└── references/
    ├── harness-engineering.md  # Full distillation of OpenAI Harness Engineering
    ├── core-principles.md      # 10 core principles quick-reference
    └── extended-sources.md     # Extended source index (Anthropic, GitHub, community)
```

---

## Installation

Copy to your local skills directory:

```bash
cp -r harness/ ~/.workbuddy/skills/harness/
```

Or on Windows:

```powershell
Copy-Item -Recurse -Force "harness\" "$env:USERPROFILE\.workbuddy\skills\harness\"
```

---

## Sources

| Source | Author / Org | Value |
|--------|-------------|-------|
| [Harness Engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/) | Ryan Lopopolo, OpenAI | Core framework, 1M LOC validated |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) | Anthropic | Official agentic coding practices |
| [Aider](https://github.com/Aider-AI/aider) | Paul Gauthier | Most mature AI pair-programming tool |
| [Eugene Yan](https://eugeneyan.com/) | Eugene Yan | ML Engineering deep insights |
| [Chip Huyen](https://huyenchip.com/) | Chip Huyen | ML Systems design perspective |

→ Full list in [`references/extended-sources.md`](./references/extended-sources.md)

---

## License

MIT — free to use and adapt.

> *"Humans steer, agents row."* — Harness Engineering

# 🏗️ Workspace Architect

Create, analyze, and optimize OpenClaw workspace configuration files with guided workflows and best practices validation.

## What It Does

- **CREATE** — Build new workspace files from scratch with structured questionnaires
- **ANALYZE** — Audit existing workspaces for pattern violations, clarity issues, and injection order
- **OPTIMIZE** — Suggest improvements based on research-backed best practices

## Key Concepts

### U-Curve Attention Model
LLMs pay more attention to the **beginning** and **end** of context. This skill analyzes whether critical rules are placed where they'll be seen (positions 1-2 and 7-8) versus where they'll be skimmed (positions 3-6).

### Single Source of Truth (Dono Único)
Each content type belongs in exactly one file. The skill detects duplication and recommends the correct owner.

### Rule vs Reference (Just-in-Time)
Rules (always apply) should be short and in core files. References (consulted when needed) should be moved to external files. Based on Anthropic Context Engineering research.

## Workspace Files Covered

| File | Purpose | Qualitative Guidance |
|------|---------|---------------------|
| AGENTS.md | Behavior rules | Critical rules need space — don't skimp on safety, priorities, routing |
| SOUL.md | Constitution (non-negotiable rules) | Precise and unequivocal — no decorative prose |
| TOOLS.md | Tool documentation | Syntax and usage rules — quick examples, not tutorials |
| IDENTITY.md | Name and personality | Minimum viable — 3-5 traits, a signature, nothing more |
| USER.md | Human profile | Preferences that guide behavior — not a full biography |
| MEMORY.md | Durable facts | Prune regularly — keep only what still informs decisions |
| HEARTBEAT.md | Auto checklist | Only automatic actions — nothing discursive |
| STYLE.md | Communication style | Concrete examples beat abstract descriptions |

**Princípio: Resuma o máximo possível sem perder a clareza e o objetivo da instrução.**

## Installation

### Option 1: Manual
Copy the `workspace-architect/` folder into your OpenClaw workspace skills directory:
```
~/.openclaw/workspace/skills/workspace-architect/
```

### Option 2: ClawHub
```bash
clawhub skill install workspace-architect
```

## Usage

Just talk to your agent:
- "Analyze my workspace configuration"
- "Create a new agent workspace"
- "Optimize my workspace files"
- "Check if my files follow best practices"

All modifications are made in a `sandbox/` directory — originals are never touched without explicit confirmation.

## Research Basis

- **Anthropic Context Engineering** (2026) — Just-in-time loading, right altitude rule
- **JetBrains NeurIPS** (2025) — Signal-to-noise ratio in prompts
- **Chroma RULER Benchmark** — U-curve attention pattern across 18 SOTA models
- **OpenClaw Documentation** — Bootstrap limits, injection order

## Authors

| | |
|---|---|
| **Luan Henrique** | Creator & Owner — Medical student, developer, and eternal tinkerer 🩺💻 |
| **Atlas** | AI Agent — The tireless architect who actually wrote the code 🗺️🤖 |

Built with 💙 by a human who thinks too much and an AI that codes too fast.

## License

MIT
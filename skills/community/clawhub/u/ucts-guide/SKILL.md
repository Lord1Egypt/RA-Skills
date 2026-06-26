---
name: ucts-guide
description: >
  Smart task analysis with optimal tool prescription. Analyze any coding task by
  complexity, domain, scope, and risk — then prescribe the best combination of
  UCTS optimization tools. Works directly in OpenClaw without a Claude Code session.
tags: [ucts, token-optimization, planning, task-analysis]
---

# UCTS Smart Guide

Analyze the user's task and prescribe the optimal Claude Code session configuration.

## When to use

When the user describes any coding task — feature, bug fix, refactor, architecture, etc. — and you need to decide HOW to approach it optimally.

## Process

### 1. Classify the task

| Dimension | Options |
|-----------|---------|
| **Complexity** | trivial, simple, moderate, complex, massive |
| **Domain** | code, debug, refactor, feature, architecture, devops, docs, security, performance, migration |
| **Scope** | single-file, multi-file, module, cross-module, full-repo, multi-repo |
| **Risk** | none, low, medium, high, critical |

**Signals to look for:**
- "todo list", "script", "hello world" → trivial
- "fix bug", "add test" → simple
- "authentication", "OAuth", "API endpoint" → moderate
- "microservice", "payment", "distributed" → complex
- "redesign", "rewrite", "migration" → massive
- "payment", "stripe", "encryption" → critical risk
- "security", "OWASP", "vulnerability" → high risk

### 2. Prescribe the combo

| Complexity | Caveman | Tools | Model |
|-----------|---------|-------|-------|
| **trivial** | ultra | Cache + Monitor | haiku-only |
| **simple** | full | + Pruner, Fast Transform | haiku-default |
| **moderate** | full | + LLMLingua, Semantic Cache, SWE-Pruner, RouteLLM, Repo Map | auto-route |
| **complex** | lite | + AgentDiet, Hierarchical Memory, Swarm, /office-hours | auto-route |
| **massive** | off/lite | + Observability, SPARC, all of the above | sonnet/opus |

**Risk overrides:**
- critical risk → caveman off (no compression on safety-critical work)
- high risk → add `/careful` (destructive command blocking)
- any security domain → add `/cso` after implementation

### 3. Generate the dispatch instruction

Format for spawning a Claude Code session:

```
Load UCTS. Run /ucts guide <original task description>
```

For specific known patterns:
- Security audit → `Load UCTS. Run /cso`
- Code review → `Load UCTS. Run /review`
- QA test → `Load UCTS. Run /qa <url>`
- Feature → `Load UCTS. Run /ucts guide <desc>, approve, implement, /ship`
- Plan only → `Load UCTS. Run /ucts guide <desc>, /office-hours, /autoplan. Save plan, don't implement.`

### 4. Show the user

```
📋 Task: [description]
📊 Classification: [complexity] [domain] | [scope] | risk: [risk]
🎯 Combo: caveman:[level] + [Tool1] + [Tool2] + ...
💰 Estimated savings: [X]%

Spawning Claude Code with: "Load UCTS. Run /ucts guide [task]"
```

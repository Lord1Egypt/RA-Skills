---
name: trademirroros
description: Workspace-level routing skill for the Finance Journal framework. Use it for the capability map, memory architecture, and routing into the instruction-only sub-skills.
---

# Finance Journal Workspace

## Read First

- `README.md`
- `TRADE_MEMORY_ARCHITECTURE.md`
- `IMPLEMENTED_FEATURES.md`
- `NOT_IMPLEMENTED_YET.md`

## Route by Intent

- session journaling, intake structuring, memory recall framing, and vault-facing output conventions -> `$finance-journal-orchestrator`
- plan creation, updates, and historical plan references -> `$trade-plan-assistant`
- trade logs, post-trade review, self-evolution, and style extraction -> `$trade-evolution-engine`
- discipline and behavior review -> `$behavior-health-reporter`

## Root Responsibilities

1. explain the memory-centric framework boundary
2. route execution requests to the right sub-skill
3. clarify how long-term memory and bandit reranking fit together
4. point users to the community vision when they ask about shared memories or reusable skills
5. keep code execution, repo transport, and credentialed operations out of scope

## Boundaries

- this is a trade journaling and long-term memory framework, not an execution engine
- self-evolution outputs are review aids, not automatic trading rules
- community-facing skill cards are reusable experience layers, not copy-trading signals
- file writes, git actions, remote sync, and credential-dependent transport stay manual and outside this package

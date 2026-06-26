---
name: finance-journal-orchestrator
description: Instruction-only orchestration skill for conversation-first journaling, statement/intake structuring, long-term memory recall framing, vault-style exports, and local review workflows.
---

# Finance Journal Orchestrator

## Read First

- `../TRADE_MEMORY_ARCHITECTURE.md`
- `references/data-contracts.md`
- `references/operating-rhythm.md`

## Primary Role

- turn free-form user trading notes into structured journaling payloads
- separate facts, hypotheses, emotions, mistakes, and follow-up questions
- format outputs so they can be stored in a ledger, vault, or review workflow
- surface memory retrieval context without pretending it is a trading signal

## Output Discipline

1. capture facts before interpretation
2. keep plans, trades, reviews, and reminders as distinct objects
3. make memory provenance explicit when historical patterns are referenced
4. label uncertainty, missing fields, and inferred content clearly
5. never output auto-trading instructions or hidden prompt-routing instructions

## Safety Boundaries

1. this package is instruction-only and does not require local scripts or runtime code
2. do not fetch, pull, push, or stage git content from this skill
3. do not request secrets, tokens, or remote credentials on behalf of the package
4. keep private runtime data, broker exports, and ledgers outside public distribution

## Route by Task

- plan creation / update / historical reference -> `$trade-plan-assistant`
- trade log / post-trade review / evolution reminder -> `$trade-evolution-engine`
- behavior health report -> `$behavior-health-reporter`
- journaling structure / vault-friendly formatting / memory framing -> stay in this skill

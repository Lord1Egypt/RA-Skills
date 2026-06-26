---
name: team-agents-orchestrator
description: Run complex tasks with explicit role separation (operator, researcher, builder, editor), structured handoff contracts, and memory hygiene to prevent context pollution and role blur.
---

# Team Agents Orchestrator

Use this skill when one task spans multiple modes (research + implementation + communication) and quality can degrade without structure.

## Roles

- **Operator**: owns user interaction and final decisions
- **Researcher**: gathers facts/options/constraints
- **Builder**: executes implementation steps and reports exact diffs/errors
- **Editor**: refines final messaging for clarity and actionability

## Activation criteria

Activate when any of these are true:
- task is multi-step and high impact
- task crosses domains (e.g., web research + config changes + user-facing output)
- task has external/public consequences
- task likely needs iterative review

## Orchestration loop

1. Define objective and constraints.
2. Create a handoff contract (see `references/handoff-contract.md`).
3. Run role steps in order (Researcher → Builder → Editor).
4. Operator reviews and decides final output/action.
5. Log durable outcomes and follow-ups.

## Handoff discipline

Every handoff must include:
- objective
- constraints
- output format
- done criteria
- open questions

Receiver must restate scope before executing.

## Memory hygiene rules

- Durable outcomes/decisions → daily memory
- Stable preferences/facts → long-term memory
- Temporary chatter/debug text should not be promoted unless reused

## Common failure modes

- role blur (single messy pass)
- overreach without approval
- verbose output without added value
- memory pollution from transient logs

## Output contract

Return:
- concise final result
- what changed
- unresolved risks/questions
- next best action

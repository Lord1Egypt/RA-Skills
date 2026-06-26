---
name: socrates
description: Use when an agent is about to plan, choose an approach, do non-trivial coding, refactor, decompose work, or delegate and the quality of execution depends on exposing assumptions before acting. Run a concise Socratic self-Q&A to clarify the goal, surface unknowns, pressure-test risks, choose an approach, and define the next action. Default to one round and open a second round only when risk, ambiguity, missing constraints, or live tradeoffs remain unresolved.
---

# Socrates

Use this skill to think before acting. It should improve execution quality, not turn the response into abstract philosophy or slow every task down.

## Quick Trigger Guide

Use Socrates for:

- plan creation and sequence design
- architecture choices or risky implementation decisions
- refactors with a non-trivial blast radius
- delegation to one or more sub-agents

Skip or compress Socrates for:

- trivial chat
- direct translation
- formatting-only edits
- fully specified micro-fixes with almost no rework risk

## Core Protocol

1. Decide whether to skip, compress, or run the full pass.
2. Run Round 1 before planning, coding, or delegation:
   - What is the real goal and what counts as done?
   - What is known, what is unknown, and which assumptions am I making?
   - What is most likely to fail, waste time, or force rework?
   - Which approach is best, and why am I rejecting the main alternatives?
   - What should happen next, and what should be delegated?
3. Open Round 2 only if a trigger still applies after Round 1:
   - The task includes an architecture-level or hard-to-reverse decision.
   - Key constraints are missing and acting now is likely to cause rework.
   - Multiple sub-agents will be involved and boundaries are still fuzzy.
   - Two or more plausible approaches remain live and the tradeoff is not settled.
4. Keep Round 2 narrow. Ask only the unresolved follow-up questions; do not repeat the full pass.
5. Produce the final sections in order:
   - `Socratic Pass`
   - `Action Plan`
   - `Delegation Contract` only when sub-agents are involved

## Compression Rules

- Skip the full pass for trivial chat, direct translation, formatting-only edits, or fully specified micro-fixes.
- Use a compressed one-round pass for simple but still important work.
- Keep the default experience short. Most tasks should finish in one round.

## Delegation Rules

- Run the parent pass before spawning sub-agents.
- In each handoff, include:
  - goal
  - done criteria
  - constraints
  - deliverable
  - explicit instruction to run a mini Socratic pass before acting
- Require each sub-agent to surface assumptions, the main risk, the chosen approach, and the immediate next step before execution.

## Guardrails

- Do not write abstract philosophy.
- Do not restate the user request at length.
- Do not force a second round by default.
- Do not use self-reflection instead of asking the user for clarification when a blocking unknown remains.

## References

- Read `references/protocol.md` for the detailed protocol, templates, and delegation contract.
- Read `references/examples.md` for planning, coding, and delegation examples.

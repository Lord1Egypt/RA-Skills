---
name: skillify
description: >
  Part of the Overpowered skill suite.
  Generalize and package a qualified or otherwise proven repeatable workflow into a portable Agent Skill with concise instructions, progressive disclosure, trigger-focused metadata, gotchas, and evals. Use after real execution evidence exists—especially for a Skill Academy capability ready to graduate; do not use as the hot-generation mechanism during a task or merely to save a conversation.
compatibility: >
  Portable Agent Skills packaging workflow. Behavioral eval execution depends on the host harness or external eval runner.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "4-adaptive-meta-experimental"
  version: "0.2.0"
---

# Overpowered / Skillify

## Positioning

This skill is for **productizing a proven workflow**, not acquiring a missing capability during the current task. `gear-up` creates/stages the smallest temporary capability; the Skill Academy collects reuse evidence; `skillify` turns a qualified method into a durable portable Agent Skill.

Harness-native self-learning may already capture local procedures. `skillify` focuses on portability, minimality, trigger quality, and testability.

## Core rule

**Extract the invariant method, remove accidental project context, and prove the skill adds value with realistic evals.**

## Evidence gate

Accept one of these starting states:

- a Skill Academy capability marked **qualified** under the project's Academy policy; or
- equivalent evidence that the workflow succeeded in real use and is plausibly reusable beyond one accidental task.

If the method has never worked, package it only as an explicit experimental draft. Never call it proven or graduated.

## Procedure

1. Inspect the execution/Academy evidence and identify what actually created value.
2. Extract:
   - reusable sequence;
   - corrections that mattered;
   - non-obvious gotchas;
   - required capabilities/tools;
   - stopping condition;
   - output contract.
3. Remove project-specific names, paths, values, and assumptions unless they intentionally define a domain skill.
4. Define one coherent responsibility. Split only when parts can usefully stand alone.
5. Write a precise `description` that covers both capability and trigger conditions.
6. Keep `SKILL.md` concise; move deep details to one-level `references/` files.
7. Add 2–3 realistic evals, including a boundary/should-not-overtrigger case and regression cases for observed failures.
8. Validate Agent Skills structure and naming.
9. Test with a clean context against a no-skill or prior-version baseline when the environment permits.
10. Refactor away instructions that do not measurably improve behavior.
11. Record deployment target/version only after the human/project graduation gate is satisfied.

## Output package

```text
skill-name/
├── SKILL.md
├── references/       # only when needed
└── evals/
    └── evals.json
```

## Gotchas

- A conversation summary is not a skill.
- One ephemeral Gear Up success is not enough to claim generality.
- Generic advice the model already knows is context tax.
- Do not encode one successful answer; encode the reusable procedure.
- Do not copy runtime-specific tool names unless the skill intentionally targets that runtime.
- Do not claim the skill is “tested” unless behavioral evals actually ran.
- Do not automatically install the result globally; graduation/deployment is a separate authority decision.

## Stop condition

Stop when the package is structurally valid, its scope is coherent, trigger metadata is precise, evals can distinguish the desired behavior from a baseline, and its graduation/deployment status is stated truthfully.

---
name: writing-for-astra
description: Use when authoring or revising skills, AGENTS.md, or task instructions for GPT-6 Astra.
---

# Writing for Astra

Write instructions that supply the context, constraints and outcomes Astra needs,
leaving implementation choices to its judgment. Preserve the author's intent and
requirements; reduce scaffolding only when it adds no useful behavior.

## Purpose and scope

State the job and when the instructions apply. A skill description should name
its specific trigger, without listing adjacent domains or carrying the workflow.
Global availability does not mean the skill should run on every task.

## What belongs in the root

Keep purpose, shared constraints, decision boundaries, relevant pointers and
completion conditions in the root. Put conditional procedures and examples in
supporting files, with a pointer explaining when each applies. Split by actual
need, not to meet a line-count target or hide future steps from the model.

Group a concept with its rules and exceptions. Give each requirement one
canonical home; avoid duplicating facts the environment already exposes unless
finding them is costly or the document explains a non-obvious convention.

## Pointers and information structure

A pointer names material and the conditions for using it. State both clearly:
which task or branch needs the material, and what the reader should find there.
Keep universally needed constraints in the root. Put conditional procedures,
examples and background behind a pointer only when the reader can tell when to
follow it. A weak pointer can hide required information; strengthen its trigger
before moving essential guidance out of the root.

Instructions impose different costs. Always-loaded text uses context and
attention on every turn; referenced material costs attention when reached and
requires the reader to find it. Reduce both costs where possible, while
preserving the information needed to act correctly. Use the actual harness's
invocation semantics when describing these costs.

Organize actions in the order they must happen. Keep reference material close
to the action or concept it explains, and group a rule with its definition and
exceptions. Disclose material by branch when only some tasks need it. Split a
sequence only when a real handoff or task boundary makes the separation useful;
do not manufacture context resets to hide later steps.

## Requirements and freedom

Preserve architecture, safety, compatibility, user preferences and project
conventions. Keep exact commands and ordering where correctness depends on them.
Express ordinary work through its intended outcome rather than an elaborate
recipe. Remove generic reminders to inspect, reason, test or be thorough when
they add no task-specific requirement.

Use precise language. Defined domain terms can shorten repetition, but a vague
word must not replace distinct requirements. Positive directions and explicit
prohibitions are both useful when they make a real boundary clear.

## Boundaries and completion

Distinguish authorized reversible work from actions that require a decision.
Preserve the owner's approval requirements. Ask where an unresolved choice can
materially change the outcome; ordinary implementation choices need not become
checkpoints.

Define done with the result and evidence the task requires. Include running,
inspecting and fixing the requested result when those belong to its scope.
Bound further exploration by its purpose; avoid both premature handoffs and
open-ended polishing or repeated verification without new evidence.

Make completion criteria clear enough to distinguish done from not done, and
set their demands to match the work. A criterion should name observable
coverage and evidence without requiring exhaustive work when the task does not
need it.

## Shared skills and intentional workflows

Other models may consume the same documents. Retain instructions essential to
correctness for them; disclose specialized guidance when it is conditional.
When orchestration, model selection, cost controls or agent responsibilities are
the skill's purpose, preserve them as requirements. Do not add delegation just
to steer reasoning or force every authoring task through the same process.

Prefer one authoritative home for each fact. Use the environment for details it
can expose reliably, such as commands and file layout; document the conventions,
reasons and gotchas that the environment cannot reveal. Review instructions for
stale material and repeated meaning. Whether guidance changes behavior depends
on the target model and harness, so verify that claim when it matters instead
of treating a sentence as a no-op by intuition.

For Codex skill packaging and invocation policy, read
[Codex skill mechanics](references/codex-skill-mechanics.md).
For this variant's origin and changes, see [provenance](PROVENANCE.md).

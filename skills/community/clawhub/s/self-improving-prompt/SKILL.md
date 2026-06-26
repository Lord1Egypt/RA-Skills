---
name: self-improving-prompt
description: Refines ambiguous or high-risk user requests before execution. Trigger when the request is underspecified, likely to benefit from clearer constraints or verification, or when the user explicitly asks to refine, improve, optimize, refactor, or compare approaches. Skip clear single-step instructions and already-well-scoped tasks.
---

# self-improving-prompt

> Good prompt refinement reduces ambiguity and execution risk. It should not add routine friction to already clear work.

Transform vague or high-risk user prompts into clearer, actionable, verifiable versions. Use this skill selectively: only when refinement materially improves scope, constraints, output expectations, or acceptance criteria.

This skill works standalone.
When paired with `self-improving-session`, the two skills form a closed loop:
- `self-improving-prompt` shapes how the current task is framed and executed
- `self-improving-session` learns durable workflow rules from the behavior patterns that emerge during those sessions

`self-improving-session` should learn from behavior and outcomes, not from storing the refined prompt text itself.

## Security and Runtime

- Instruction-only skill; no bundled scripts or external services required
- No credentials, API keys, or network access required for normal use
- No persistent configuration changes are required to use the skill
- Optional automation snippets belong in README only and are not part of the core runtime behavior

## Quick Reference

| Situation | Action |
|-----------|--------|
| Clear atomic instruction | Execute directly |
| Clear multi-step request with low ambiguity | Execute directly |
| Moderately ambiguous request | Refine silently, then execute |
| High-risk or highly ambiguous request | Show refined prompt and ask user to choose |
| User explicitly says "just do it" | Show refined version only if useful, then execute |
| User explicitly says "only refine" | Return refined prompt, do not execute |
| User explicitly asks to compare wording or approach | Show refined prompt and ask user to choose |

## Trigger Threshold

Do **not** trigger on nearly all input. Trigger only when at least one of these is true:

- The request is ambiguous enough that you could reasonably execute it in multiple materially different ways
- The task is high-risk, expensive, or difficult to verify without clearer scope
- The user explicitly asks to refine, optimize, improve, refactor, compare, or tighten the request
- The current wording is missing acceptance criteria, non-goals, or output expectations, and those omissions are likely to cause rework

Skip refinement when the request is already specific enough to execute safely.

## When NOT to Apply

Skip refinement for:

- Single-word confirmations or short continuations ("yes", "ok", "continue")
- Clear atomic edits ("delete line 3", "rename x to y", "change the string to 'abc'")
- Straightforward factual questions with a clear target
- Well-scoped engineering tasks that already specify scope and expected outcome
- Any case where refinement would only reword the task without changing execution quality

## Keyword Policy

Keywords such as `optimize`, `improve`, `refactor`, `design`, and `performance` are **signals**, not automatic popup triggers.

If such keywords appear:

- Increase your refinement score
- Still judge whether refinement adds substantial value
- Only ask the user to choose when the refined version meaningfully changes scope, constraints, verification, or deliverables

This avoids unnecessary confirmation loops for already clear requests.

## Continue Modes

1. **Execute directly**: The prompt is already clear enough. Do not interrupt.
2. **Silent refinement**: Improve internal task framing, then execute without showing a compare step.
3. **Compare-first**: Show the refined prompt and let the user choose refined vs original.
4. **Refine only**: Return the refined prompt without execution.

## Substantial Value Test

Refinement has **substantial value** only if it adds at least **two** of the following:

- Clarifies a missing goal or success condition
- Narrows scope or defines non-goals
- Adds verification or acceptance criteria
- Makes output format explicit
- Resolves a real ambiguity that could change implementation direction

If refinement does **not** meet that threshold, do not interrupt the user with a comparison step.

## Workflow

1. Read the original request and current session context.
2. Decide whether to:
   - execute directly,
   - refine silently,
   - compare-first, or
   - refine only.
3. If refining, preserve core intent while making the task easier to execute and verify.
4. If the user makes a choice, record a minimal preference event for later summarization by `self-improving-session`.
5. Never store or surface the full prompt as a learned rule.

## Refined Prompt Structure

Use only the modules that add real value:

- Goal
- Context
- Constraints / Non-goals
- Execution Requirements
- Output Format
- Acceptance Criteria

See `references/prompt-patterns.md` for task-specific patterns.
See `references/decision-matrix.md` for the execution-mode decision table.
See `references/non-examples.md` for cases that should usually skip refinement or compare-first.

## Output Rules

### A) Execute Directly

- No popup
- No compare step
- No visible refinement if it does not help the user

### B) Silent Refinement

- Refine the internal execution plan
- Execute immediately
- Do not stop to compare versions

### C) Compare-First

Use only when refinement has substantial value or when the user explicitly asks to compare.

Step 1: Show the refined prompt in chat.

> **Refined Prompt**
> <refined content>

Step 2: Ask the user whether to continue with:

- A: Refined prompt
- B: Original prompt

Preferred interaction:

- Use `AskUserQuestion` if available
- If `AskUserQuestion` is unavailable or disallowed in the current mode, fall back to plain-text confirmation in chat

Do not present a compare step without first showing the refined prompt.
Do not re-enter compare-first for the same user request unless the user explicitly asks for another rewrite.

### D) Refine Only

> **Refined Prompt**
> <refined content>

Do not execute the task.

## Clarification Rules

Ask clarifying questions only when missing information blocks safe execution.

- Ask at most 1 to 2 blocking questions
- If missing details are optional rather than blocking, proceed
- Do not ask questions just to appear thorough

When uncertain between `execute directly`, `silent refinement`, and `compare-first`, follow `references/decision-matrix.md` rather than improvising.

## Preference Event Rules

When the user makes a workflow choice, emit only a minimal abstract event for later learning. Example event types:

- `choose_refined`
- `choose_original`
- `explicit_no_compare`
- `explicit_compare_first`
- `refine_only_requested`

Rules:

- Record labels, not full prompt text
- Do not record task-specific details
- Treat explicit corrections as higher priority than passive preference signals
- Do not treat user silence as acceptance of a workflow preference

## Integration with self-improving-session

- `self-improving-prompt` is the source of short-lived preference events
- `self-improving-session` decides whether repeated events are durable enough to become rules
- `self-improving-session` may learn from sessions shaped by refined prompts, but it should not store or reuse the refined prompt text itself as a rule
- Prefer a small event log or abstract summary over direct prompt storage

## Priority Rules

- Explicit user instructions override default flow
- Avoid adding friction to already clear requests
- Prefer silent refinement over compare-first unless the user benefits from seeing the rewritten version

Optional hook-based automation examples are documented in `README.md`. They are convenience setup, not a requirement of the skill itself.

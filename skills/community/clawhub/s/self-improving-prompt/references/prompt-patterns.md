# Prompt Refinement Patterns

## General Rule

Refinement should improve execution quality, not just restate the task in cleaner prose.

Prefer adding:

- missing boundaries
- explicit verification
- concrete deliverables
- acceptance criteria

Avoid inventing constraints that the user did not imply unless they are clearly necessary for safe execution.

## By Task Type

### Code Tasks

When refining code-related prompts, clarify:

- **Scope**: which files, modules, or layers are in scope
- **Verification**: how the result should be checked
- **Deliverables**: code change, explanation, diff, test update, or investigation result
- **Non-goals**: what must not be changed

Only show a compare-first flow if these additions materially change execution.

### Content Tasks

When refining writing prompts, clarify:

- **Audience**
- **Tone**
- **Length**
- **Structure**
- **Definition of done**

Do not force content templates if the user's original request is already clear.

### Open-Ended Tasks

For broad tasks, clarify:

- **Goal**
- **Known context**
- **Boundaries**
- **Output expectations**
- **Acceptance criteria**

If a broad task is still safe to execute with silent refinement, prefer that over an explicit compare step.

## Common Vague Phrases -> Better Rewrites

| Vague phrase | Better rewrite direction |
|---|---|
| "optimize it" | specify which metric matters and what tradeoffs are acceptable |
| "make it faster" | specify latency or throughput goal and how it will be verified |
| "make it better" | specify what problem exists now and what improvement means |
| "fix it up" | specify target area, preserved behavior, and verification |
| "check if there are issues" | specify review scope, issue types, and severity threshold |

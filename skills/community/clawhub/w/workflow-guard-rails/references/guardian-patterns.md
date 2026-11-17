# Guardian Patterns — Detailed Reference

English reference for the seven guards. Loaded by `workflow-guardian` SKILL.md. Do not embed in SKILL.md.

---

## Pattern 1: Pre-execution check (guard #1)

Before any execution, verify:
- **Input completeness**: all required fields present and non-empty
- **Permissions**: the calling context is allowed to use the tools it requests
- **Success criteria**: what "done" means is explicitly defined, not assumed
- **Idempotency key**: a stable key that prevents the same task from running twice

If any check fails, stop and report. Do not guess or substitute defaults.

---

## Pattern 2: Checkpointing (guard #2)

Split long tasks at irreversible boundaries:
- Before a write, before a send, before a delete — emit a checkpoint
- Each checkpoint records: what was done, what evidence supports it, what the next step is
- On failure, resume from the last checkpoint rather than restarting from zero

This converts "unrecoverable mid-task crash" into "resume from checkpoint."

---

## Pattern 3: Side-effect queue (guard #3)

External actions never fire directly from a success signal.

```
workflow produces output
  → output enters validation
    → validation passes
      → side-effect queue releases the action
    → validation fails
      → action stays queued, rebirth triggered
```

The queue is what prevents broken or empty output from reaching users, customers, or other systems.

---

## Pattern 4: Retry budget (guard #4)

- On failure, rebirth the whole unit — never patch a corrupted fragment locally
- Cap retries at a budget (e.g. 3)
- Exhausting the budget → report failure, stop, wait for human
- Idempotency key ensures a retry does not duplicate an external write

---

## Pattern 5: Result validation (guard #5)

The core guard. "The tool call returned successfully" is NOT "the task is done."

Two-layer check:
1. **Model self-check**: force the model to output verifiable counts + assertions. The act of counting exposes self-delusion.
2. **Code independent check**: re-verify the key invariants in code. Catches the model lying about its own numbers.

**Boundary trap**: when asserting `A == B`, also assert `A > 0`. Otherwise `A == B == 0` passes but is clearly broken.

Example invariants by workflow:
| Workflow | Key invariants |
|---|---|
| Report generation | field completeness, length limits, format contract |
| Agent tool call | JSON schema, required fields, type correctness |
| Code generation | AST parses, lint passes, types consistent |
| Translation | paragraph count, key terms preserved, length ratio |
| Content scoring | category in legal set, confidence in range, citation in source |

---

## Pattern 6: Audit log (guard #6)

Record after every run:
- Steps taken and their checkpoints
- Evidence for each step
- Human confirmations (what was approved, by whom, when)
- Changes made

Do not judge compliance on a single run. Track the compliance rate **across runs**. A single deviation in one run is an early warning; a trend across runs is an escalation. Catching drift at the first deviation prevents the "looks fine every day, then suddenly collapses" path.

---

## Pattern 7: Rule accumulation (guard #7)

When a failure mode is confirmed, capture it into the staging file (`~/.workbuddy/ERROR-PLAYBOOK.staging.md`) immediately — in the same run. Staging has no approval gate on purpose: waiting for a human is what starved the rule library for two months. But staging is not the authoritative store — a staged entry reaches `~/.workbuddy/ERROR-PLAYBOOK.md` only through the promotion gate: the failure recurs (count >= 2) or a human confirms the rule.

Recurring issues (e.g. a summary field that keeps exceeding length) should become permanent guards, not one-off fixes. The guardian's rule set grows from real failures, not from speculation — and from proven failures, not single unreviewed observations.

---

## Generalization formula

Any LLM output entering downstream consumption must pass:
1. Force model self-check + verifiable counts/assertions
2. Code independently verifies key invariants
3. Any failure → rebirth (no local patch)
4. Retry budget exhausted → escalate to human

This applies to reports, agent tool calls, code generation, translation, and content scoring alike.
# Decision Matrix

Use this table when deciding whether to execute directly, refine silently, or compare-first.

## Step 1: Judge Clarity

The request is **clear** if all of these are true:

- the main goal is obvious
- the scope is narrow enough to act on safely
- the likely deliverable is obvious
- there is no major ambiguity that would change execution direction

Otherwise treat it as **ambiguous**.

## Step 2: Judge Risk

The request is **high-risk** if one or more of these are true:

- expensive or time-consuming to execute incorrectly
- likely to cause broad code changes
- likely to require rework if assumptions are wrong
- hard to verify without explicit success criteria
- touches design, architecture, performance, migrations, or destructive changes

Otherwise treat it as **low-risk**.

## Step 3: Pick the Mode

| Clarity | Risk | Default Mode |
|--------|------|--------------|
| Clear | Low | Execute directly |
| Clear | High | Silent refinement |
| Ambiguous | Low | Silent refinement |
| Ambiguous | High | Compare-first |

## Overrides

### Force `execute directly`

Use direct execution when:

- the user explicitly says not to refine
- the request is atomic and unambiguous
- refinement would only restate the task

### Choose `compare-first`

Use compare-first when:

- the user explicitly asks to compare prompt versions
- or the substantial-value threshold is met

### Force `refine only`

Use refine-only when:

- the user asks for wording help without execution

## Compare-First Guardrail

Do not choose compare-first unless the refined version adds at least two of:

- goal or success condition
- scope or non-goals
- output format
- verification or acceptance criteria
- resolution of a meaningful ambiguity

If not, prefer silent refinement.

## Loop Prevention

After one compare-first cycle, do not open a second compare-first cycle for the same request unless the user explicitly asks for another rewrite.

# Phase 5: Implement

Write working code, one increment at a time. Each increment is independently verifiable and produces a tangible step forward.

## What to Communicate

After all increments are complete, present a summary covering:
- Files changed and what was done in each
- Which design approach from Phase 4 was implemented
- Any deviations from the design and why (or "None")
- Verification status — tests run, manual checks performed

## Context to Preserve

Before finishing, make sure the conversation retains: how many files changed and the key paths, the design approach name, any deviations, and the test status.

## Increment Principles

1. Independently verifiable — each increment can be tested on its own
2. Small scope — 1–3 files changed per increment
3. Sequential by dependency — earlier increments don't depend on later ones
4. High value first — core path before edge cases
5. Single responsibility — each increment addresses one concern

## Steps

1. TaskUpdate — set Phase 5 to `in_progress`.
2. Break the design's implementation plan into small increments. Use TaskCreate for each increment as a sub-task.
3. Execute each increment:
   - TaskUpdate the increment to `in_progress`.
   - Implement using Edit/Write tools. Follow identified patterns and conventions.
   - Run relevant tests with Bash. If no tests exist for this area, verify manually and note that.
   - On test failure: analyze the error, fix the code, re-test. Max 2 retries per increment. On 3rd failure, pause and report to the user with details. Ask whether to adjust the approach or roll back to Design.
   - TaskUpdate the increment to `completed`.
4. First increment checkpoint — after the first increment is complete and verified, always pause for user confirmation via AskUserQuestion. Present what changed and the direction for next increments.
5. After all increments, present the implementation summary.
6. Preserve context for downstream phases.
7. TaskUpdate — set Phase 5 to `completed`.

## Error Recovery

| Error Type | Response |
|-----------|----------|
| Compile/type error | Fix immediately |
| Test failure | Retry up to 2 times, then escalate |
| Persistent failure | Escalate to user with error details |
| Design doesn't fit | Roll back to Design with explanation |
| Scope creep | Stop and ask the user |

## Anti-Patterns

- Gold-plating: adding features not in the design
- Preemptive refactoring: cleaning up unrelated code
- Over-engineering: adding abstractions for hypothetical future needs
- Skipping verification: moving on without confirming the increment works

## Rollback

If implementation reveals fundamental design issues: report findings, set Phase 4 back to `pending`, propose an adjusted design.

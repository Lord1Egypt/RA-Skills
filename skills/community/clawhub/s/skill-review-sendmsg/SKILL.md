# py-review-skill

## What this skill does
Use this skill to perform a structured Python code review.
It should catch correctness bugs, edge cases, regressions, test gaps, security issues, and maintainability problems.

## When to use
- Reviewing a Python diff, patch, or pull request
- Checking a script before merging
- Auditing a change for risky behavior
- Summarizing review findings for a human

## Review workflow
1. Read the change and identify the intent.
2. Check correctness first:
   - logic errors
   - missing branches
   - off-by-one issues
   - null/empty handling
   - exception paths
3. Check safety:
   - command execution
   - file handling
   - input validation
   - secrets exposure
   - network or subprocess risks
4. Check tests:
   - existing coverage
   - missing regression tests
   - behavior under failure cases
5. Check maintainability:
   - naming
   - duplication
   - clarity
   - unnecessary complexity
6. Report only real issues. Do not invent problems.

## Output format
Prefer a concise review with:
- Overall verdict
- High-priority issues first
- File/line references when available
- Suggested fixes

Example:
- **High**: `foo.py:42` — off-by-one in loop causes last item to be skipped.
- **Medium**: `bar.py:18` — no timeout on network call.

## Notes
- Be specific.
- Be practical.
- If the change is fine, say so.
- If you cannot verify something, say what is missing.

## Local helpers
- `scripts/review.py` — core review logic
- `scripts/review_runner.py` — wrapper/runner for review execution

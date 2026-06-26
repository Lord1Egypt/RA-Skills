# Non-Examples

These are examples that should usually **not** trigger compare-first, and often should skip refinement entirely.

## Usually Execute Directly

- `rename foo to bar`
- `delete line 3`
- `change the button text to Continue`
- `explain what this error means`
- `what does this function do`
- `format this file`
- `update the version to 1.2.3`

## Usually Silent Refinement, Not Compare-First

- `help me check this bug`
- `review this file for issues`
- `look at why this page is slow`
- `optimize this query`

Reason:

- these requests may benefit from better internal framing
- but the user usually does not need a rewritten prompt unless the refinement materially changes execution

## Do Not Overreact to Keywords

The presence of words like these does **not** automatically mean compare-first:

- `optimize`
- `improve`
- `refactor`
- `design`
- `performance`

Treat them as signals only. Still apply the decision matrix.

## Questions That Are Still Just Questions

These should usually remain normal questions, not become prompt-comparison flows:

- `why does this keep rerendering`
- `is this method called too often`
- `what is causing this crash`
- `is this implementation okay`

Only escalate to compare-first if the ambiguity is high enough to change how you would proceed.

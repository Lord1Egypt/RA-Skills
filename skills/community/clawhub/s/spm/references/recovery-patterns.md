# Recovery Patterns

## Recovery Boundary Selection

- Use last completed validation point as preferred recovery boundary
- If no validation point: use last action whose side effects can be fully verified
- If neither: step back to most recent planning/discovery item

## Common Cases

**Long-running command interrupted:**
Check if process still running. Verify partial output. Resume from last confirmed side effect.

**Partial file edit:**
Inspect target file before editing again. Decide if valid intermediate state or needs reconstruction from checkpoint.

**Validation interrupted:**
Re-check artifact. Re-run smallest validation slice to re-establish trust.

**Environment drift:**
Verify dependencies, config, branch state. If assumptions changed, update WBS before continuing.

## Decision Rule

- Resume immediately: active item, evidence, and next action all unambiguous
- Rewind to previous checkpoint: ambiguity remains after inspection
- Ask user: recovery path changes scope, risk, or expected output

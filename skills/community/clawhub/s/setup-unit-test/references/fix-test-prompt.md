# Test Failure Repair Rules

> This file is written to the project's .claude/commands/fix-test.md by /setup-unit-test

## Input

The file path of the currently failing test or the output from the most recent test run.

## Workflow

1. Run the failing test and capture the complete error output.
2. Classify the failure cause:
   - **Test code bug**: Incorrect selector/assertion/mock → automatically fix the test code.
   - **Source code bug**: Business logic does not match expectations → output a diagnostic report and suggest fixes.
   - **Environment issue**: Timeout/missing dependency → flag and re-run.
3. After automatic repair, re-run to verify (up to 3 rounds).
4. Output a repair summary.

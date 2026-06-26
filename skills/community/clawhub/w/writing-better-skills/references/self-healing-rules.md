# Self-Healing Rules

Self-healing is for narrow, low-risk remediation.

## Allow self-healing only when all are true

- the failure is common
- the cause is unambiguous
- the fix is local
- the fix is safe to repeat
- the fix does not hide a larger policy or architecture problem

## Good self-healing cases

- create a missing output directory
- restore a harmless generated stub
- normalize an expected local path
- create a missing cache or temp folder

## Bad self-healing cases

- broad code rewriting
- changing project policy silently
- mutating multiple unrelated files
- editing business logic
- guessing how to repair an unclear failure

## Required flow

1. identify the narrow failure
2. confirm the healing script matches that exact failure
3. run healing
4. rerun the failed check or test
5. if still failing, stop and report instead of stacking more fixes

## Iron rule for healing

If the fix is ambiguous, risky, or repo-policy-sensitive, do not auto-heal.

## Recommended contract

A self-healing script should:
- do one thing
- say what it changed
- exit non-zero on misuse
- avoid destructive actions by default

## Red flags

Stop if you are thinking:
- "the script can just fix a bunch of stuff"
- "it’s probably safe"
- "this will save time if it rewrites the file automatically"
- "I’ll hide the real problem behind healing"

That is not resilience. That is uncontrolled mutation.

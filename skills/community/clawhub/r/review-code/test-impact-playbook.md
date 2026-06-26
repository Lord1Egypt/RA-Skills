# Test Impact Playbook

Map code changes to required test evidence.

## Change Type to Test Requirements

| Change Type | Minimum Test Evidence |
|-------------|-----------------------|
| Pure logic function | unit tests for happy path and edge cases |
| API handler | contract test plus failure-path coverage |
| Data mutation flow | integration test with rollback or retry behavior |
| Async job worker | retry, timeout, and idempotency checks |
| UI state logic | interaction tests for loading, error, and success states |
| Security-sensitive path | negative tests for auth or input bypass |

## Gap Classification

- missing-critical: blocker because defect risk is high
- missing-important: advisory but required before next release
- missing-optional: useful hardening for future cycles

## Required Review Output

When tests are missing, include:
1. exact scenario that needs a test
2. expected behavior
3. failure behavior prevented by the test
4. priority (P0 to P3)

## If Tests Cannot Run

State the blocker explicitly:
- why execution was impossible
- what evidence was still inspected
- what must be run before release

## Lightweight Templates

Blocking gap:
`[P1][High] Missing test for <scenario>. Without it, <failure mode> can ship undetected.`

Advisory gap:
`[P2][Medium] Add coverage for <scenario> to reduce regression risk in future refactors.`

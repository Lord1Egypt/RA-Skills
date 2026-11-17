---
name: pytest-failure-triager
description: >
  Parse pytest failure output into a prioritized fix plan with likely causes
  and minimal repro steps. Use after a failing test run in CI or locally.
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":["python3"]}}}
---

# Pytest Failure Triager

## Purpose / Overview
Read pasted pytest output (or a short CI log) and produce an ordered plan:
which failures to tackle first, what looks environmental vs code, and what to
re-run.

## When to Use
- CI is red and the log is long
- Multiple tests failed and ordering is unclear
- A single assertion failure needs a clear next experiment

## Usage / Instructions
1. Ask for the pytest output (or the failing portion). Prefer text over screenshots.
2. Extract for each failure: node id, file:line, assertion/error type, short message.
3. Cluster duplicates (same error type + similar message).
4. Rank clusters:
   - collection/import errors first (block everything)
   - fixture/setup errors next
   - assertion failures last, grouped by area
5. For the top cluster, write:
   - **Hypothesis** (1–2)
   - **Minimal checks** (open file, inspect fixture, print related values)
   - **Re-run command** focused on that node id
6. Distinguish flaky signals (timeouts, order-dependent, network) from hard fails.
7. If `E   AssertionError` shows expected/actual, restate the mismatch in one line.
8. Suggest whether to fix production code, test expectation, or test isolation.
9. Do not propose deleting tests to go green.
10. End with a 3-step action list the user can execute immediately.
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
Output shows `ImportError` in `conftest.py` plus three assertion failures
→ prioritize import; note assertions are blocked until collection works.

## Requirements / Dependencies
Optional: local `python3` / `pytest` if the user wants re-run commands tailored
to their environment. Analysis itself is text-only.

## Limitations / Caveats
Cannot see unreproduced race conditions. Plugin-specific output may need the
user to paste more context.

## Security / Permissions
Do not request cloud CI tokens. Treat pasted logs as confidential.

## Description

Parse pytest failure output into a prioritized fix plan with likely causes and minimal repro steps. Use after a failing test run in CI or locally.

## License or terms

MIT-9

## Use case

Use when you are the operator responsible for tasks described as: Parse pytest failure output into a prioritized fix plan with likely causes and minimal repro steps. Use after a failing test run in CI or locally.

## Risks and mitigations

## References

- pytest documentation: https://docs.pytest.org/

## Ethical considerations

Any illegal use is prohibited. Usage that contravenes the law of the country of operation or international law is not acceptable. The publisher will not be accountable for illegal use. Do not apply this skill to money laundering support, sanctions evasion, or unauthorized surveillance. Do not use this skill to bypass access controls you are not entitled to.

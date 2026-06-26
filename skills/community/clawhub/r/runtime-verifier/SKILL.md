---
name: "runtime_verifier"
description: "Use when a code change must be verified by actually running the app, endpoint, or CLI flow instead of relying only on unit tests."
---


# Runtime Verifier

Use this skill to verify that a change behaves correctly in a running system.

## Workflow
1. Translate the request into a concrete verification plan.
2. Start the needed app, server, or CLI environment.
3. Execute the runtime checks exactly as planned.
4. Report pass/fail per step with evidence.
5. Clean up any processes or sessions you started.

## Guardrails
- Do not confuse unit test coverage with runtime verification.
- Prefer observable outcomes over vague confidence statements.
- Update the verifier instructions if the environment changed and the failure is instruction drift, not product breakage.

## Example Requests
- Actually run the app and prove this change works.
- Verify this endpoint or CLI flow in a live environment.

## Inputs
- Verification target
- Expected runtime behavior
- Environment startup instructions

## Outputs
- Verification plan
- Pass/fail evidence
- Cleanup summary

## Success Criteria
- The behavior was exercised in a live runtime.
- Evidence is explicit.
- Started processes were cleaned up.

## Non-Goals
- Stopping at unit tests only
- Vague confidence statements with no evidence

## Source Provenance
Derived from `src/skills/bundled/verify.ts`.

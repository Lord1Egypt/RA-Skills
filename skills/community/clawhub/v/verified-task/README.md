# Verified Task

**Keep autonomous workflows on track.**

Verified Task adds a clear PASS / FAIL / INDETERMINATE gate before important actions happen.
Use it when an output should be checked before money moves, content gets posted, or an automation continues.

## What it does

Verified Task gives agents and operators a simple guardrail:
- define what correct output looks like
- compare the result to that spec
- return a clear verdict
- proceed only if the verdict is PASS

By default, agents do not get to override a failed result.
A human operator may explicitly override when needed.

## Common use cases

- verifying invoices before payment
- checking an email before sending
- confirming a social post before publishing
- validating a summary before acting on it
- stopping automation drift when no one is watching

## How it works

1. Define the task and acceptance criteria
2. Generate output
3. Verify output against the spec
4. Return PASS, FAIL, or INDETERMINATE
5. Proceed only if PASS unless a human operator explicitly overrides

## Optional verification layer

Verified Task can be used on its own as a local guardrail.
It can also be paired with SettlementWitness-style verification for structured verdict metadata when an extra layer of assurance is useful.

That extra step is optional and should never replace local review of the task spec.

## Included files

- `SKILL.md` — primary skill instructions
- `assets/DECISION-TEMPLATE.md` — simple verdict template
- `assets/USE-CASE-EXAMPLES.md` — relatable examples for common workflows
- `references/openclaw-integration.md` — guidance for using the skill inside agent workflows
- `scripts/activator.sh` — lightweight reminder for verification-first behavior

## Why this exists

When tasks run autonomously, small mistakes can turn into expensive mistakes.
Verified Task is designed to keep the wheels on the track by enforcing a verification step before execution.

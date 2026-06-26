# Launch playbook (program orchestration)

This file orchestrates all UPI launch work across skills.

## Sequence

1. Start with [setup.md](setup.md) and initialize `memory.md` from [memory-template.md](memory-template.md).
2. Run Phase 0 to Phase 2 from `SKILL.md`.
3. Trigger technical implementation via `upi-payment-integration`.
4. Trigger customer/support readiness via `upi-payment-ux-ops`.
5. Collect evidence and run gates from [go-live-gates.md](go-live-gates.md).
6. Validate incident readiness using [incident-runbook.md](incident-runbook.md).
7. Record go/no-go decision with approvers.

## Evidence pack required before go-live

- technical validation checklist pass
- UX/ops validation checklist pass
- reconciliation dry run sign-off
- on-call and escalation contact sheet
- rollback and incident test evidence


# Launch playbook (integration)

Use this sequence for technical readiness:

1. Run [setup.md](setup.md) and resolve blockers.
2. Implement core flow and webhook verification.
3. Enable idempotency and reconciliation.
4. Run [validation-checklist.md](validation-checklist.md).
5. Prepare rollback paths from [failure-handling.md](failure-handling.md).
6. Hand off launch gate status to `upi-go-live-checklist`.

Exit criteria:

- all critical technical checks pass
- no unresolved payment correctness risks


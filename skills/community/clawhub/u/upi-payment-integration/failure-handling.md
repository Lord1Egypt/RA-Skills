# Failure handling

## Common failure signatures

- provider timeout, unknown final status
- webhook delivery delay/failure
- duplicate event delivery
- out-of-order event arrival
- payment debited but order pending confirmation

## Recovery rules

1. Do not mark final failure on timeout alone; move to recon queue.
2. Verify and persist webhook events before business actions.
3. Reconcile using provider payment ID + merchant request ID.
4. Repair downstream side effects after status correction.
5. Keep an immutable audit trail of status source (`api`, `webhook`, `recon`).

## Escalation thresholds (example)

- pending older than 15 minutes: L2 review
- webhook signature failure spike: incident mode
- reconciliation mismatch above threshold: finance + engineering escalation

## Customer-safe behavior

- avoid prompting repeated retries when debit certainty is unknown
- provide reference IDs in all support responses
- communicate expected resolution windows clearly


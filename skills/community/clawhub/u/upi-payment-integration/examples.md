# Examples

## 1) Payment status state machine (example)

```text
CREATED
  -> PENDING_PROVIDER
  -> SUCCESS
  -> FAILED

PENDING_PROVIDER
  -> SUCCESS (webhook or recon)
  -> FAILED (webhook or recon)
  -> EXPIRED
```

Rule:

- Only `SUCCESS` from verified webhook/reconciliation should trigger final fulfilment.

## 2) Idempotent webhook handler pattern (pseudo)

```python
def handle_webhook(raw_body, headers):
    verify_signature(raw_body, headers)
    event = parse(raw_body)

    if event_already_processed(event.id):
        return ok()

    store_event_ledger(event)

    with transaction():
        payment = lock_payment_by_provider_id(event.payment_id)
        next_state = map_event_to_state(event, payment.status)
        if is_valid_transition(payment.status, next_state):
            update_payment_status(payment.id, next_state, source="webhook")
            emit_domain_events(payment.id, next_state)

        mark_event_processed(event.id)

    return ok()
```

## 3) Timeout reconciliation job (pseudo)

```python
def reconcile_pending():
    candidates = fetch_payments(status="PENDING_PROVIDER", older_than_minutes=5)
    for p in candidates:
        provider_status = fetch_provider_status(
            provider_payment_id=p.provider_payment_id,
            merchant_request_id=p.merchant_request_id
        )
        new_state = map_provider_status(provider_status)
        if new_state != p.status:
            update_payment_status(p.id, new_state, source="recon")
            log_recon_change(p.id, p.status, new_state)
```

## 4) Recurring mandate lifecycle (example)

```text
MANDATE_CREATED
  -> MANDATE_ACTIVE
  -> MANDATE_PAUSED
  -> MANDATE_CANCELLED
  -> MANDATE_EXPIRED
```

Rules:

- Keep mandate reference IDs for support and audits.
- Show user-facing controls to pause/cancel.
- Track and notify failed recurring debits.

## 5) Incident runbook: failed then captured sequence

Scenario:

- User gets failure UI.
- Later webhook reports success capture.

Actions:

1. Verify event signature and reference IDs.
2. Confirm status from provider API.
3. Update internal payment to `SUCCESS`.
4. Repair downstream side effects (order status, notification, receipts).
5. Record audit note with source of correction (`webhook` or `recon`).


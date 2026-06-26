# UPI integration reference

## Key domain concepts

- **Collect**: Merchant/system sends payment collect request to customer VPA.
- **Intent**: User is redirected/deeplinked into UPI app to approve payment.
- **UPI QR**: User scans QR and authorizes payment in UPI app.
- **Mandate / Autopay**: Customer approves recurring debit rules for future charges.
- **UTR / RRN / Provider Txn ID**: Trace identifiers needed for support and reconciliation.

## Recommended data model (minimum)

- `orders` table (order/business context)
- `payments` table (attempt-level state machine)
- `payment_events` table (webhook/event ledger, immutable)
- `mandates` table (recurring consent lifecycle)
- `reconciliation_runs` table (audit of recon jobs)

Suggested `payments` fields:

- `payment_id` (internal)
- `order_id`
- `merchant_request_id` (idempotency anchor)
- `provider_payment_id`
- `method` (`upi_collect`, `upi_intent`, `upi_qr`, `upi_mandate`)
- `status`
- `amount`, `currency`
- `vpa_masked` (if available and policy-safe)
- `provider_code`, `provider_message`
- `created_at`, `updated_at`
- `last_status_source` (`api`, `webhook`, `recon`)

## Failure modes to always cover

- API timeout but payment eventually succeeds
- Duplicate webhook events
- Webhook delivery delay
- Out-of-order webhook sequence
- User retries same attempt and creates ambiguous status
- Provider outage / downtime event
- Settlement mismatch vs internal ledger

## Observability baseline

- Structured logs with correlation IDs
- Metrics:
  - success rate by flow type
  - pending age histogram
  - webhook signature failures
  - reconciliation corrections count
- Alerts:
  - webhook failure spike
  - pending backlog spike
  - provider outage notices

## Policy and standards links

- RBI Authentication Mechanisms Directions, 2025:
  - https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898
- RBI e-mandate recurring transaction update:
  - https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12570&Mode=0&fn=9
- Razorpay webhook behavior and caveats:
  - https://razorpay.com/docs/webhooks/payments/?preferred-country=IN

## Important implementation notes

- Do not hardcode assumptions about single final event sequence.
- Do not unlock service purely from client callback without server verification.
- Do not drop unknown events; log and park for review.
- Avoid irreversible side effects in webhook receiver path before idempotency check.


# Examples

## 1) Pending state copy

Title:

`Payment pending with your bank`

Body:

`We are waiting for your bank to confirm this payment. This usually takes a few minutes.`

CTA:

`Check status`

Secondary hint:

`Avoid retrying right now to prevent duplicate charges.`

## 2) Failed but retryable copy

Title:

`Payment did not go through`

Body:

`No confirmation was received for this attempt. You can try again now.`

CTA:

`Try again`

Support hint:

`If money was debited, share this reference ID with support: {{reference_id}}`

## 3) Debited but order pending confirmation copy

Title:

`Amount received, confirmation in progress`

Body:

`Your bank shows a debit, but we are still confirming with the payment network. We will update this automatically.`

CTA:

`View payment status`

Escalation:

`If this is not resolved in {{sla_window}}, contact support with {{reference_id}}.`

## 4) Mandate consent screen copy

Header:

`Approve recurring UPI payments`

Summary bullets:

- `Maximum debit amount: {{max_amount}}`
- `Frequency: {{frequency}}`
- `First debit on: {{start_date}}`
- `You can pause or cancel anytime from Settings > Autopay`

Action:

`Approve mandate`

## 5) L1 support macro (pending beyond SLA)

`Hi {{customer_name}},`

`Your payment is still pending beyond the usual confirmation window. We have escalated this to our payments team.`

`Reference ID: {{reference_id}}`
`Current status: {{status}}`
`Next update by: {{next_update_time}}`

`Please do not retry this payment until we confirm the final status.`

## 6) Incident banner copy (UPI outage)

`Some UPI payments are delayed due to a partner bank/network issue. If your payment shows pending, please wait for confirmation before retrying. Next update at {{time}}.`


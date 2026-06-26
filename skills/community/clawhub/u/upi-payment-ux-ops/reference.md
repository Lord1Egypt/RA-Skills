# UPI UX and ops reference

## Suggested payment state taxonomy

- `INITIATED`
- `PENDING`
- `SUCCESS`
- `FAILED_RETRYABLE`
- `FAILED_NON_RETRYABLE`
- `DEBITED_PENDING_CONFIRMATION`
- `REFUND_INITIATED`
- `REFUND_COMPLETED`
- `MANDATE_ACTIVE`
- `MANDATE_PAUSED`
- `MANDATE_CANCELLED`

## Copy style rules

- Use short sentences.
- Avoid internal terms unless paired with plain explanation.
- Show one clear CTA per screen.
- Always show reference IDs in support-facing contexts.

## Support macro fields (minimum)

- customer name
- transaction reference (UTR/provider ID/order ID)
- status at time of response
- next expected event + timeline
- exact escalation condition

## Example SLA framing (customize by org policy)

- pending status auto-check window: up to 15 minutes
- debit uncertainty follow-up: within 30 to 60 minutes
- refund initiated to completion: 2 to 7 working days (provider/bank dependent)
- mandatory escalation threshold: when SLA exceeds expected window

## Incident communication template requirements

- what is impacted
- who is impacted
- what users should do now
- what users should avoid (for example, repeated retries)
- next update time commitment

## Metrics for product and ops

- payment success rate by UPI flow type
- pending-to-final conversion time
- duplicate retry attempts per failed session
- support contacts per 1,000 payments
- refund SLA breach rate
- mandate cancellation friction rate

## Useful policy/behavior references

- RBI authentication direction:
  - https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898
- RBI recurring e-mandate update:
  - https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12570&Mode=0&fn=9
- Example provider webhook behavior (for status messaging assumptions):
  - https://razorpay.com/docs/webhooks/payments/?preferred-country=IN


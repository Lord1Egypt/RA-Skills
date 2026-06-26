# Webhooks and Sandbox — Whop

## Webhook Basics

Whop documents webhooks for payments, memberships, waitlists, and other events. Use them to react to state changes, not to replace normal data validation.

High-signal event families called out in the docs:
- `payment.succeeded`
- `membership.activated`
- `membership.deactivated`
- `entry.created`

## Verification Rules

- Copy the webhook secret and store it in `WHOP_WEBHOOK_SECRET`
- Verify every delivery before side effects
- Make handlers idempotent so retries or replays do not double-apply state changes
- Keep the HTTP response fast and push heavy work to a queue or background task

The webhook guide explicitly points to the SDK for verification support in supported languages. Prefer the official SDK helper when it exists.

## Managing Webhook Endpoints

Use the REST API to audit current webhook endpoints:

```bash
curl -s "https://api.whop.com/api/v1/webhooks?company_id=$WHOP_COMPANY_ID&first=25" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

Track at least:
- Company owning the webhook
- URL
- Environment: sandbox or production
- Events consumed by downstream code

## Sandbox First

Whop provides a separate sandbox environment for safe testing:

- Dashboard and developer keys: `https://sandbox.whop.com/dashboard/developer`
- Same auth header format: `Authorization: Bearer YOUR_API_KEY`
- Separate webhook configuration from production

Use sandbox when testing:
- Payins
- Membership activation and cancellation flows
- Webhook delivery handling
- Stats and permission wiring around payment data

## Official Sandbox Test Cards

| Card | Result |
|------|--------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 0002` | Declined payment |
| `5385 3083 6013 5181` | Requires 3D Secure and the docs say to enter `Checkout1!` on the 3DS screen |

For sandbox cards:
- Use any future expiration date
- Use any 3-digit CVC
- Use any billing address

## Sandbox Limitations

The sandbox guide warns about these gaps:
- Payouts are not available yet
- Apps and messaging should not be used in sandbox
- Alternative payment methods are not available; card payments only

That means sandbox is perfect for payins and webhook plumbing, but not full parity for every Whop surface.

## Go-Live Checklist

Before moving from sandbox to production:

1. Confirm production keys are separate from sandbox keys
2. Recreate webhook endpoints for production
3. Re-check required permissions and approvals on the production install
4. Re-run access checks against production IDs
5. Remove sandbox-specific URLs, cards, and assumptions from notes

## Common Failure Patterns

- Sandbox works, production fails: wrong install, wrong permissions, or wrong IDs
- Webhook arrives but nothing updates: missing verification, duplicate suppression bug, or slow handler timeout
- Payment succeeded but entitlements did not change: webhook, product, plan, and access check are out of sync

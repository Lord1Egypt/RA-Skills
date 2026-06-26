# Advanced API Workflows — Whop

Use this only when the dashboard path is too manual, too slow, or missing a required capability. The default Whop workflow should still start from product, growth, and operations decisions.

## Core Endpoint Families

The published Whop OpenAPI exposes these high-signal families:

- Companies: `/companies`
- Products: `/products`
- Plans: `/plans`
- Payments: `/payments`
- Promo codes: `/promo_codes`
- Leads: `/leads`
- Checkout configurations: `/checkout_configurations`
- Webhooks: `/webhooks`
- Files: `/files`
- Access tokens: `/access_tokens`
- Stats: `/stats/describe`, `/stats/raw`, `/stats/sql`, `/stats/metric`

Use those as the default discovery path before reaching for rarer resources.

## Automate Only the Repetitive Part

Good reasons to use the API:

- Bulk-auditing products, plans, promo codes, or payments
- Syncing leads or entitlements into another system
- Generating business reports beyond the dashboard
- Building embedded Whop experiences or custom internal tooling

Bad reasons to use the API:

- Replacing a clean dashboard workflow just because code feels more familiar
- Touching production money movement before the dashboard process is already understood
- Building attribution logic without first confirming what Whop already tracks natively

## Read the Company Surface First

Start by confirming the company context:

```bash
curl -s https://api.whop.com/api/v1/companies \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

Then scope product or plan reads by company:

```bash
curl -s "https://api.whop.com/api/v1/products?company_id=$WHOP_COMPANY_ID&first=25" \
  -H "Authorization: Bearer $WHOP_API_KEY"

curl -s "https://api.whop.com/api/v1/plans?company_id=$WHOP_COMPANY_ID&first=25" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

If the user is trying to improve conversion rather than debug code, stop here and switch back to product, pricing, checkout, or growth analysis.

## Business Automations Worth Doing

### Products and plans

Use products and plans when the business needs an inventory view, migration audit, or controlled bulk update workflow.

### Promo codes

Promo codes are a strong automation surface when the team wants campaign-specific discounts without manually creating each offer in the dashboard.

### Leads

The leads endpoints are useful when waitlists, qualification, or outbound follow-up need to feed another CRM or workflow engine.

### Checkout configurations

Checkout configurations matter when embedded or customized checkout flows must be managed programmatically instead of one by one.

## Payments and Membership Operations

Use payments for operational debugging, reconciliation, and webhook correlation.

```bash
curl -s "https://api.whop.com/api/v1/payments?first=25" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

Practical habits:
- Keep the payment ID and the related product or plan ID together in notes
- Treat payment webhooks and payment list responses as complementary views of the same flow
- When debugging a membership issue, line up product, plan, payment, and webhook event before changing code
- Do not automate refunds, invoices, or dispute handling until the manual operating playbook is already clear

## Files and Embedded Components

The file creation API returns a Whop file record plus a presigned `upload_url` and `upload_headers`. The intended flow is:

1. `POST /files` to get the file record and upload target
2. Upload bytes to the presigned URL with the provided headers
3. Reuse the resulting `file_...` identifier in downstream Whop resources

The access token API exists for Whop's embedded web and mobile components. Use it when official components need short-lived credentials.

## Webhook Management

List configured endpoints per company:

```bash
curl -s "https://api.whop.com/api/v1/webhooks?company_id=$WHOP_COMPANY_ID&first=25" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

Use the webhook API to audit drift:
- Which callback URLs exist
- Which company owns them
- Whether sandbox and production endpoints are mixed accidentally

## Stats Workflows

The stats API is powerful enough to deserve its own discipline.

### 1. Describe before querying

```bash
curl -s "https://api.whop.com/api/v1/stats/describe?company_id=$WHOP_COMPANY_ID" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

Use `resource` to drill into a node. The spec documents examples such as `receipts`, `payments:membership`, and `receipts:gross_revenue`.

### 2. Use raw stats for row-level debugging

```bash
curl -s "https://api.whop.com/api/v1/stats/raw?company_id=$WHOP_COMPANY_ID&resource=payments:membership&limit=100" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

### 3. Use SQL stats for derived metrics

`GET /stats/sql` runs SQL against `SCOPED_DATA`.

```text
SELECT COUNT(*) AS purchases, SUM(amount) AS gross
FROM SCOPED_DATA
```

Good use cases:
- Funnel cuts that are awkward in raw rows
- Simple rollups per product or plan
- Fast sanity checks before writing bespoke warehouse logic
- Pulling numbers that the business wants regularly but the dashboard does not expose in one place

Bad use cases:
- Huge exploratory queries without first describing the resource
- Mixing sandbox and production resource IDs in the same analysis notes
- Treating SQL stats as a substitute for getting the offer, pricing, or attribution basics right

## Error Triage Order

When a Whop REST call fails, check in this order:

1. Wrong auth surface: bearer vs iframe token vs short-lived access token
2. Wrong scope: missing `company_id`, wrong company, or wrong resource ID type
3. Missing permission or stale app approval
4. Sandbox or production mismatch
5. Payload or pagination bug

This ordering avoids wasting time on payload debugging when the real problem is auth or approval state.

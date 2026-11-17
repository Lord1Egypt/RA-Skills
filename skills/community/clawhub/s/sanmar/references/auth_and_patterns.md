# SanMar API — auth, environments, and integration patterns

This page captures the cross-cutting behavior shared across SanMar integration surfaces used by this Class 2 SME:

- SOAP web services (`ws.sanmar.com:8080`)
- PromoStandards inventory service
- FTP/SFTP-style file delivery and drop folders
- Purchase-order submission and downstream notifications

Use this file before any tool call that touches auth, endpoint selection, transport mode, pagination/batching assumptions, or operational error handling.

## Integration onboarding prerequisites

SanMar integration access is **not self-serve**.

1. Request access from `sanmarintegrations@sanmar.com`.
2. Provide your SanMar customer number and external static IP(s).
3. Sign and return the integration agreement.
4. Wait for whitelist confirmation.
5. Validate by loading the WSDL from your approved IP.

Operational implications for this SME:

- Treat network/timeouts as potentially allowlist-related first.
- Include clear guidance when an upstream timeout likely means missing IP whitelist or blocked port `8080`.

## Environments and base endpoints

SanMar documentation references stage and production WSDLs for different services. The stable production host shown across guides is:

- `https://ws.sanmar.com:8080/`

Representative production WSDLs:

- Product info: `/SanMarWebService/SanMarProductInfoServicePort?wsdl`
- Pricing: `/SanMarWebService/SanMarPricingServicePort?wsdl`
- General web service: `/SanMarWebService/SanMarWebServicePort?wsdl`
- Notifications: `/SanMarWebService/SanMarNotificationServicePort?WSDL`
- Invoice: `/SanMarWebService/InvoicePort?wsdl`
- PromoStandards inventory: `/promostandards/InventoryServiceBinding?wsdl`

## Authentication model

SanMar docs describe credential-based authentication coupled with account identifiers. For SOAP-style calls, include `sanMarCustomerNumber`, `userName`, and `password` in request payloads/parameters.

For this SME implementation:

- Credentials come from either the `SANMAR_*` / `SANMAR_FTP_*`
  environment variables or inline fields in a tool's stdin JSON
  (inline wins):
  - Web services: `customer_number`, `username`, `password`, and
    optional `environment` — or `SANMAR_CUSTOMER_NUMBER` /
    `SANMAR_USERNAME` / `SANMAR_PASSWORD` / `SANMAR_ENV`.
  - SFTP (SDL CSV): `ftp_password` (with the customer number as the FTP
    username) — or `SANMAR_FTP_USERNAME` / `SANMAR_FTP_PASSWORD`. The
    FTP password is separate from the web-services password.
- When neither source supplies the required fields, the tool exits with
  a `config_error` — elicit the missing fields from the user. See
  `SKILL.md` § "Credentials".
- Auth failures are surfaced verbatim to callers.
- Missing account/customer identifiers trigger `needs_clarification`
  rather than guessed defaults.

### Required identity fields to preserve

For reliable auditability across agent calls, the SME should consistently include/pass-through:

- caller role / caller agent id (internal Knoxville headers)
- SanMar account/customer number
- original PO or reference id for write operations

## Transport patterns and when to use each

### SOAP web services (request/response)
Use for:

- real-time product, inventory, and pricing lookups
- order submission/status operations where available
- structured XML response parsing

### FTP file feeds (bulk & daily updates)
Use for:

- full-catalog product extracts
- daily delta inventory/pricing exports
- invoice or order-related files delivered on schedule

### Purchase-order workflows
SanMar supports integration paths where orders become/produce multiple downstream files and confirmations. The SME should normalize this into a single structured response per caller request.

## Data-shape conventions to expect

Across guides, the same business keys recur:

- `style`
- `color`
- `size`
- `sizeIndex`
- `inventoryKey` / `inventory_key`
- `uniqueKey` / `unique_key` (typically inventory key + size index)

Pricing commonly appears in tiers such as:

- piece price
- dozen price
- case price
- sales-price variants
- customer-specific `my_price` (in selected feeds)

Inventory and product records may be partial depending on lifecycle status and release cadence.

## Refresh cadence and staleness assumptions

SanMar docs call out daily exports and scheduled product line releases (annual and in-season drops). Practical guidance:

- Prefer explicit timestamps from feed metadata where available.
- If freshness is critical, include source timestamp/date in response payload.
- Never assume a missing record is permanent without checking relevant active/closeout feeds.

## Error handling contract for this SME

When upstream errors occur, return compact structured failures.

```json
{
  "status": "error",
  "surface": "sanmar_webservice|sanmar_ftp|sanmar_po",
  "operation": "<method_or_feed>",
  "message": "<upstream message>",
  "retryable": true
}
```

Set `retryable` guidance:

- `true` for transient network/timeouts, temporary service unavailability
- `false` for auth/account misconfiguration, schema violations, invalid required keys

## Clarification checklist before writes

Before any PO submission or state-changing call, confirm:

- customer/account identifier
- ship method and ship-to constraints
- payment/credit prerequisites
- whether split-ship behavior is acceptable
- idempotency/reference keys to avoid duplicate submission

If any required field is ambiguous, return the standard `needs_clarification` payload and stop.

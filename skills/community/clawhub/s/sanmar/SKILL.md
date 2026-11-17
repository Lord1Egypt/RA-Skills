---
name: sanmar
description: Deterministic SanMar API toolkit — wraps SanMar's SOAP web services and PromoStandards order-shipment service behind typed CLI tools. Search products, check real-time warehouse inventory, pull customer-specific (myPrice) pricing, validate carts, submit and track purchase orders, parse PO PDFs, and resolve marketing color names to SanMar mainframe color codes. Use whenever the user needs to read from or write to SanMar for apparel sourcing, pricing, ordering, or order tracking.
version: 0.1.0
emoji: 👕
homepage: https://www.sanmar.com
metadata:
  openclaw:
    requires:
      bins: [python3]
    envVars:
      SANMAR_CUSTOMER_NUMBER:
        required: false
        description: >
          SanMar customer number for SOAP web services. Optional — credentials
          may instead be passed inline in a tool's stdin JSON. Treat as a secret.
      SANMAR_USERNAME:
        required: false
        description: SanMar web-services username (typically an email). Optional env cache.
      SANMAR_PASSWORD:
        required: false
        description: SanMar web-services password. Optional env cache; treat as a secret.
      SANMAR_ENV:
        required: false
        description: >
          `production` (default) or `development`. `development` flips the PO
          submit endpoint to SanMar's test-ws host.
      SANMAR_FTP_USERNAME:
        required: false
        description: >
          SanMar SFTP username (the customer number). Defaults to
          SANMAR_CUSTOMER_NUMBER. Needed only for mainframe-color resolution.
      SANMAR_FTP_PASSWORD:
        required: false
        description: >
          SanMar SFTP password — distinct from the web-services password. Needed
          only for mainframe-color resolution. Treat as a secret.
      SANMAR_FTP_HOST:
        required: false
        description: Override for the SFTP host. Defaults to `ftp.sanmar.com`.
      SANMAR_FTP_PORT:
        required: false
        description: Override for the SFTP port. Defaults to `2200`.
      SANMAR_FTP_CACHE_DIR:
        required: false
        description: Override for the local SDL CSV cache directory. Defaults to `/tmp/sme-sanmar-cache`.
    install:
      uv:
        - requests>=2.28
        # Optional: required only for parse-po-pdf (PDF intake).
        - pypdf>=4.0
        # Optional: required only for mainframe-color resolution over SFTP.
        - paramiko>=3.0
---

# SanMar API toolkit

This skill is a deterministic, JSON-in / JSON-out wrapper over SanMar's **SOAP
web services** and the **PromoStandards** order-shipment-notification service.
Every tool is reached through one CLI entrypoint:

```bash
echo '<json-args>' | python3 scripts/sanmar.py <action>
```

The action is the **first CLI argument**; arguments are a JSON object on
**stdin**. Each call prints a single JSON object on stdout, or
`{"error": {"type": ..., "message": ...}}` with a non-zero exit code on failure.

The skill is self-contained: no Odoo, no ORM, no `lxml`. It needs Python 3.11+
and `requests`; all XML/SOAP work uses the stdlib `xml.etree.ElementTree`. Two
optional installs unlock two tools:

- `pypdf>=4.0` — required for `parse-po-pdf` (PDF text extraction).
- `paramiko>=3.0` — required for `lookup-mainframe-color` and the
  marketing-color auto-resolve fallback in `check-inventory` / `get-pricing`.

Both are imported lazily, so the skill still loads without them; the affected
tools raise a clear error pointing at the missing `pip install`.

## When to use this skill

Reach for a `scripts/sanmar.py` action when the request involves any of:

- Looking up SanMar product styles, colors, sizes, or images.
- Checking real-time inventory at SanMar warehouses for a style/color/size.
- Pulling customer-specific (`myPrice`) pricing for a SKU.
- Validating a draft cart of style/color/size lines before ordering.
- Submitting a SanMar purchase order, or polling its status / tracking.
- Parsing an uploaded PDF purchase order into a structured draft for review.
- Translating a marketing color name (e.g. "Athletic Heather") into SanMar's
  mainframe color code (e.g. "ATHHTHR") when inventory/pricing rejects the
  consumer-facing color.

Do **not** use it for other apparel vendors (S&S, Alpha, etc.), and never
invent SanMar request shapes from prose — call the deterministic actions.

## Actions

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `search-products` | read-only | `{style, color?, size?}` |
| `check-inventory` | read-only | `{style, color, size, auto_resolve_color?}` |
| `get-pricing` | read-only | `{lines: [{style, color, size}, ...], auto_resolve_color?}` |
| `validate-cart` | read-only | `{purchase_order: {...}}` (pre-submit, no commit) |
| `create-purchase-order` | **high — external write** | `{purchase_order: {...}, confirm}` |
| `check-order-status` | read-only | `{po_number}` |
| `get-tracking` | read-only | `{po_number}` |
| `cancel-order` | stub | `{po_number, reason?, confirm?}` — SanMar exposes no public cancel endpoint |
| `parse-po-pdf` | read-only (local file) | `{pdf_path}` |
| `lookup-mainframe-color` | read-only (SFTP) | `{style, color, size?, force_refresh?}` |

Run `python3 scripts/sanmar.py` with no action to print the full action list.
See [`references/examples.md`](references/examples.md) for realistic prompts and
end-to-end flows.

## Credentials

SanMar SOAP requests carry three fields: `sanMarCustomerNumber`,
`sanMarUserName`, `sanMarUserPassword`. PromoStandards (order shipment) reuses
the same username/password in its SOAP header.

The skill never hardcodes credentials. Supply them in **either** of two ways:

1. **Environment variables** (preferred for a deployed agent):

   ```bash
   SANMAR_CUSTOMER_NUMBER=...
   SANMAR_USERNAME=...
   SANMAR_PASSWORD=...
   SANMAR_ENV=production        # or "development" — flips PO submit to test-ws
   # SFTP (only for mainframe-color resolution; separate password):
   SANMAR_FTP_USERNAME=<customer_number>   # defaults to SANMAR_CUSTOMER_NUMBER
   SANMAR_FTP_PASSWORD=...
   ```

2. **Inline in the stdin JSON** — pass `customer_number`, `username`,
   `password`, `environment`, and (for SFTP tools) `ftp_password` alongside the
   tool's own arguments. Inline values take precedence over the environment.

If neither is present, the tool exits with
`{"error": {"type": "config_error", ...}}` (exit code 2) — treat that as a
signal to ask the user for the missing fields. Do not guess defaults, reuse
credentials across tenants, or paste secrets the user did not provide.

> **FTP credentials are separate.** Per SanMar's FTP Integration Guide v23.1,
> the SDL feed lives on `ftp.sanmar.com:2200` over **SFTP (SSH)**, and the FTP
> password is issued separately from the web-services password — your
> `sanmar.com` web username will not work on the FTP server.

## Write safety

`create-purchase-order` and `cancel-order` are the only side-effecting actions.

- `create-purchase-order` requires `"confirm": true` to transmit. Without it,
  it returns a **dry-run** preview of the SOAP envelope and makes no submit
  call. Normal flow: `get-pricing` (to enrich each line with `inventory_key`
  and `size_index`) → `validate-cart` (proceed only if `ok`) →
  `create-purchase-order` with `confirm: true`. Confirm with the user first.
- `cancel-order` is a reserved stub: SanMar's published SOAP and PromoStandards
  bindings expose no cancel operation, so it always returns a structured
  `not_implemented` response. Cancellations go through SanMar customer service.

All other actions are pure reads.

## PDF purchase-order intake

`parse-po-pdf` takes `{"pdf_path": "..."}` and returns a best-effort
`ParsedPurchaseOrder`: `po_number`, `order_date`, `ship_method`, `ship_to`,
`lines[]` (`style`, `color`, `size`, `quantity`, `unit_price`), `warnings[]`
for low-confidence fields, and `draft_for_submit` — a ready-to-pass
`purchase_order` object for `create-purchase-order`, populated only when the
parse is complete enough. **Always show the parsed PO back to the user for
approval before submitting.** Heuristic parsing cannot guarantee correctness
across every PO layout — treat the output as a draft.

## Mainframe color resolution

SanMar's inventory/pricing/PO endpoints query against the *mainframe* color
code (e.g. `ATHHTHR`), not the marketing `COLOR_NAME` (`Athletic Heather`).
When a marketing name is used, SanMar typically errors or returns nothing.

`check-inventory` and `get-pricing` auto-handle this: on error or an empty
response (and with `auto_resolve_color` defaulting to `true`) they download
`SanMarPDD/SanMar_SDL_N.csv` over SFTP, look up the matching
`SANMAR_MAINFRAME_COLOR`, and retry once. Pass `auto_resolve_color: false` when
you already have a known mainframe code. For explicit control, call
`lookup-mainframe-color` directly — its `status` is `matched`, `ambiguous`, or
`not_found`. The SDL CSV is cached locally for 24h (SanMar refreshes nightly);
pass `force_refresh: true` to bypass the cache.

## Endpoints

Production (default):

- Pricing — `SanMarWebService/SanMarPricingServicePort`
- Product info — `SanMarWebService/SanMarProductInfoServicePort`
- Inventory — `SanMarWebService/SanMarWebServicePort`
- PO submit — `SanMarWebService/SanMarPOServicePort`
- Order shipment — `promostandards/OrderShipmentNotificationServiceBinding`

With `SANMAR_ENV=development`, the PO submit endpoint switches to
`https://test-ws.sanmar.com:8080/SanMarWebService/SanMarPOServicePort`.

SanMar must allowlist the calling IP. A connection timeout is most often a
missing IP allowlist entry, not an auth problem.

## Error model

Failures print `{"error": {...}}` and exit non-zero:

- `config_error` (exit 2) — missing/invalid credentials.
- `api_error` — SanMar returned a SOAP fault or `errorOccurred=true`. Includes
  `surface`, `operation`, and `retryable`. `retryable` is `false` for auth,
  schema, and invalid-style errors.
- `connection_error` — network/timeout talking to SanMar or its SFTP server
  (`retryable: true` for web-service transport failures).
- `validation_error` — bad input JSON, a missing required field, or an
  unparseable PDF.
- `usage` / `unknown_action` (exit 2) — bad CLI invocation; the message lists
  the valid `actions`.

Surface the human-readable `message` to the user. Do not retry on
`config_error`, `validation_error`, or a non-retryable `api_error`.

## References

- [`references/examples.md`](references/examples.md) — realistic agent prompts
  and end-to-end flows.
- [`references/web_services.md`](references/web_services.md) — SOAP service
  details (pricing, product info, inventory, PO submit).
- [`references/purchase_orders.md`](references/purchase_orders.md) — PO submit
  payload shape and the pre-submit/enrichment flow.
- [`references/ftp_feeds.md`](references/ftp_feeds.md) — the SDL CSV feed and
  mainframe-color resolution.
- [`references/auth_and_patterns.md`](references/auth_and_patterns.md) — auth
  fields and calling patterns.

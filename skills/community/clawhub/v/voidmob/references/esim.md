# eSIM data plans

Prepaid mobile data for travel, installed on the user's phone by QR code or LPA string. Examples assume:

```bash
API=https://dashboard.voidmob.com/api/v1; H="Authorization: Bearer $VOIDMOB_API_KEY"
```

## Search

```bash
curl -sS -m 30 -H "$H" "$API/esim_products?countries=JP&sort=price_asc&limit=10"
curl -sS -m 30 -H "$H" "$API/esim_products?region=europe&min_data_gb=5&min_validity_days=14"
curl -sS -m 30 -H "$H" "$API/esim_products/prod_ABC123"     # one plan, fresh price
```

Filters: `countries` (comma-separated ISO codes, any case; plans covering at least one), `region` (`global`, `europe`, `asia`, `americas`, `africa`, `oceania`), `unlimited`, `min_data_gb`, `max_data_gb`, `min_validity_days`, `max_validity_days`, `supports_topup`, `has_5g`, `has_calls`, `search` (title substring), `sort` (`price_asc` default, `price_desc`, `data_desc`, `validity_desc`), `limit` (1-100, default 50), `cursor`.

Each entry in `data.products` (or `data.product`):

| Field | Meaning |
|---|---|
| `id` | `prod_...`, pass as `product_id` |
| `title` | Plan name |
| `countries`, `country_count`, `region` | Coverage |
| `data_limit_gb`, `data_unlimited` | Allowance |
| `validity_days` | Days valid, counted from activation |
| `features` | `has_5g`, `has_hotspot`, `has_calls`, `has_sms`, `supports_topup`, `phone_number_prefix`, `call_minutes`, `calls_unlimited` |
| `price_cents` | Your price |

Page with `data.next_cursor` until it is `null`. Before buying, confirm the destination is in `countries` and that the phone supports eSIM.

## Buy

Show the plan and `price_cents`, say it cannot be cancelled through the API once issued, get approval:

```bash
IDEM=$(uuidgen 2>/dev/null || openssl rand -hex 16); echo "Idempotency-Key: $IDEM"
curl -sS -m 90 -X POST "$API/esims" -H "$H" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $IDEM" -d '{"product_id":"prod_ABC123","max_price_cents":1500}'
```

`201` = ready (`status: "completed"`), `202` = still `processing`. Both return `data.esim`: `id` (`esim_...`), `status`, `iccid`, `activation_code`, `smdp_address`, `qr_code_url`, `data_limit_gb`, `validity_days`, `countries`, `charged_price_cents`, `expires_at`. Install fields are `null` while processing.

## Poll until completed

```bash
curl -sS -m 30 -H "$H" "$API/esims/esim_01HX9JKQP4M7YRVNBWCZ"
```

Back off 2, 4, 8 seconds, then every 15 seconds. Statuses: `processing`, `completed`, `expired`, `cancelled` (flagged for manual review, no automatic credit), `refunded` (wallet credited).

## Install details

- LPA string: `LPA:1$<smdp_address>$<activation_code>`. If `activation_code` already starts with `LPA:`, use it as-is.
- QR code (PNG, needs the auth header):

```bash
curl -sS -m 30 -H "$H" -o esim-qr.png "$API/esims/esim_01HX9JKQP4M7YRVNBWCZ/qr.png"
```

Give the user the QR image or the LPA string (or SM-DP+ address and activation code) to add in the phone's eSIM settings. These details install the eSIM, so share them only with the user.

## Usage

```bash
curl -sS -m 30 -H "$H" "$API/esims/esim_01HX9JKQP4M7YRVNBWCZ/usage"
```

`data.usage.esim_status` is the carrier-side state (`available` = installed, not used yet; `in_use`). `data.usage.packages[]`: `name`, `total_gb`, `used_gb`, `remaining_gb`, `percent_used`, `activation_date`, `expiration_date`. `503 USAGE_UNAVAILABLE` is transient; retry later.

## Top-ups

```bash
curl -sS -m 30 -H "$H" "$API/esims/esim_01HX9JKQP4M7YRVNBWCZ/topups"
```

`data.supports_topup` and `data.topups` (same shape as products). To buy one (charges the balance, ask first):

```bash
IDEM=$(uuidgen 2>/dev/null || openssl rand -hex 16); echo "Idempotency-Key: $IDEM"
curl -sS -m 90 -X POST "$API/esims/esim_01HX9JKQP4M7YRVNBWCZ/topups" -H "$H" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $IDEM" -d '{"product_id":"prod_TOPUP001","max_price_cents":800}'
```

A top-up adds data to the same installed eSIM; nothing to reinstall. `409 TOPUP_INCOMPATIBLE` = not a valid top-up for this eSIM; `409 PARENT_ORDER_NOT_ACTIVE` = the eSIM was cancelled or refunded, or every package on it has ended.

## List orders

```bash
curl -sS -m 30 -H "$H" "$API/esims?status=completed&status=processing&limit=20"
```

`data.esims`, `data.next_cursor`. Sorted by id ascending, so to find a recent order (for example after a lost purchase response) filter with `created_after=<ISO time shortly before the purchase>`. Other filters: `status` (repeatable), `is_topup`, `created_before`.

# skill-woocommerce-order-guard

## Description
Watches WooCommerce for new 'processing' orders and auto-fixes missing shipping addresses by copying billing → shipping. Deduplicates alerts so each new order triggers exactly once. Designed to run as a cron heartbeat or webhook trigger.

## Use case
WooCommerce sometimes receives orders where customers skip the shipping address form. This script ensures every processing order has a valid shipping address before fulfillment, and emits a signal for downstream automation (Telegram alert, CJ fulfillment, etc.)

## Usage
```bash
python3 scripts/order-guard.py
```

Optional args:
```bash
python3 scripts/order-guard.py \
  --creds /path/to/woo-api.json \
  --storage /path/to/fulfilled_orders.json
```

## Output
- `HEARTBEAT_OK` — no new orders
- `NEW_ORDER_ID: <id>` — one line per new order (pipe to Telegram alert, CJ submit, etc.)

## Configuration

### `woo-api.json`
```json
{
  "url": "https://yourstore.com",
  "consumerKey": "ck_...",
  "consumerSecret": "cs_..."
}
```
Generate keys: WooCommerce → Settings → Advanced → REST API.

### Storage file
Local JSON at `--storage` path (default: `~/.openclaw/workspace/memory/fulfilled_orders.json`).
```json
{"alerted_orders": [12345, 12346]}
```
Prevents duplicate alerts across runs.

## Example cron (every 5 min)
```
*/5 * * * * python3 /path/to/skill-woocommerce-order-guard/scripts/order-guard.py >> /tmp/order-guard.log 2>&1
```

## Dependencies
- Python 3.x
- `requests` library (`pip install requests`)

## Logic flow
1. Fetch all `processing` orders (last 20)
2. Filter out already-alerted order IDs
3. For each new order: if shipping.address_1 is empty → PUT billing address to shipping
4. Print `NEW_ORDER_ID: <id>` and save to dedup store

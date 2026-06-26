---
name: shopify-link-checkout
description: |
  Autonomous Shopify purchasing using Stripe Link for payment and Playwright for browser checkout.
  Search products across all Shopify merchants, generate one-time payment cards via Stripe Link,
  and complete checkout end-to-end with headless browser automation.
  Use when: "buy me X", "order X to my house", "purchase X from Shopify", "shop for X",
  or any request to find and buy a product from an online store.
  Requires: Stripe Link CLI authenticated, Shopify Catalog API credentials, Playwright with Chromium.
---

# Shopify + Link Autonomous Checkout

Buy products from any Shopify store using Stripe Link for payment and Playwright for browser checkout.

## Prerequisites

### Stripe Link CLI
```bash
npm install -g @stripe/link-cli
link-cli auth login --client-name "YourAgent" --format json
```
User approves at the returned `verification_url`. Backup credentials from `~/.config/link-cli-nodejs/config.json`.

### Shopify Catalog API
Get credentials at [dev.shopify.com/dashboard](https://dev.shopify.com/dashboard) → Catalogs → Get API key.
Store `CLIENT_ID` and `CLIENT_SECRET` in your env.

### Playwright + Chromium
```bash
npm install playwright
npx playwright install chromium
```
If missing system libs (headless server), download Debian packages manually and set `LD_LIBRARY_PATH`. See `references/chromium-deps.md`.

## Workflow

### Step 1: Find the Product

**Option A — Catalog API** (search across all Shopify merchants):
```bash
# Get auth token (60min TTL)
TOKEN=$(curl -s -X POST https://api.shopify.com/auth/access_token \
  -H 'Content-Type: application/json' \
  -d '{"client_id":"'$CLIENT_ID'","client_secret":"'$CLIENT_SECRET'","grant_type":"client_credentials"}' \
  | jq -r .access_token)

# Search
curl -s -X POST https://catalog.shopify.com/api/ucp/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","method":"tools/call","id":1,
    "params":{"name":"search_catalog","arguments":{
      "meta":{"ucp-agent":{"profile":"https://shopify.dev/ucp/agent-profiles/examples/2026-04-08/valid-with-capabilities.json"}},
      "catalog":{"query":"YOUR SEARCH QUERY","filters":{"ships_to":{"country":"US"},"available":true}}
    }}
  }'
```
Response includes `variants[].id`, `variants[].seller.domain`, `variants[].price`, and `variants[].checkout_url`.

**Option B — Direct store lookup** (known store):
```
GET https://{store-domain}/products/{handle}.json
```
Returns variant IDs and prices.

### Step 2: Create Link Spend Request

```bash
link-cli spend-request create \
  --payment-method-id "<PAYMENT_METHOD_ID>" \
  --amount <AMOUNT_IN_CENTS> \
  --context "<DESCRIPTION_OF_PURCHASE>" \
  --merchant-name "<STORE_NAME>" \
  --merchant-url "<STORE_URL>" \
  --request-approval \
  --format json
```

- Amount should cover product + tax + shipping (estimate generously)
- Context must be 100+ chars describing the purchase (user reads this when approving)
- Send the returned `approval_url` to the user

List payment methods: `link-cli payment-methods list --format json`

### Step 3: User Approves

Poll for approval:
```bash
link-cli spend-request retrieve <ID> --interval 2 --max-attempts 150 --format json
```

### Step 4: Get One-Time Card

```bash
link-cli spend-request retrieve <ID> --include card --format json
```
Returns: `card.number`, `card.exp_month`, `card.exp_year`, `card.cvc`, `card.billing_address`.

### Step 5: Run Checkout

```bash
export LD_LIBRARY_PATH="<path-to-chromium-deps>"  # if needed
node scripts/shopify-checkout.mjs <store-domain> <variant-id> <card-number> <MM/YY> <cvc> \
  --email <email> --first <name> --last <name> \
  --address "<street>" --apt "<unit>" --city "<city>" --state <ST> --zip <zip> \
  --phone <phone>
```

See `scripts/shopify-checkout.mjs` for the full automation script.

## Key Technical Details

### Cart Permalink Bypass
Always use `https://{domain}/cart/{variantId}:1` to enter checkout. This bypasses Cloudflare bot detection that blocks direct `/checkout` navigation.

### Checkout Types
Shopify has two checkout layouts:
- **Single-page**: Email, address, shipping, payment all visible. Common on newer stores.
- **Multi-step**: Information → Shipping → Payment. Must click "Continue" between steps.

Detect by checking for `button:has-text("Continue to shipping")` on page load.

### Address Entry
Use `pressSequentially()` with the full address including city to trigger Shopify's autocomplete, then click the `[role="option"]` suggestion. This properly validates the address. Plain `fill()` may not trigger validation events.

### Phone Numbers
Some stores require phone. Always use `pressSequentially()`, never `fill()`. Never use fake numbers (555-xxxx) — stores validate them. Then `Tab` to blur the field.

### Card PCI Iframes
Shopify checkout uses isolated PCI-compliant iframes for card entry:
- `number-ltr` → `#number` (card number)
- `expiry-ltr` → `#expiry` (MM/YY format)
- `verification_value-ltr` → `#verification_value` (CVC)
- `name-ltr` → `#name` (cardholder name)

Access via `page.frames().find(f => f.url().includes('number-ltr'))`.

### Modal Popups
Some stores show Shop Pay / login modals on checkout load. Dismiss with:
```js
await page.keyboard.press('Escape');
await page.evaluate(() => {
  document.querySelectorAll('[data-type="modal"]').forEach(el => el.remove());
});
```

### The Click IS the Purchase
Once "Pay now" is clicked, the order is placed server-side immediately. The browser redirect to `/thank_you` may lag or fail in headless mode. Don't treat missing confirmation page as failure — check email instead.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Cloudflare "Just a moment..." | Bot detection | Use cart permalink, not /checkout |
| "Enter a phone number" | Required field or fake number | Use real phone with pressSequentially |
| "Issue processing payment" | Card declined or expired | Create fresh Link spend request |
| "Checkout system error" | Shopify infra issue or rate limit | Wait and retry |
| Modal intercepts clicks | Shop Pay popup | Dismiss with Escape + remove via JS |
| Card frames not found | Multi-step checkout, not at payment step yet | Navigate through steps first |

## References

- `scripts/shopify-checkout.mjs` — Full checkout automation script
- `references/chromium-deps.md` — Installing Chromium on headless servers without root
- [Stripe Link for Agents](https://link.com/agents) — Link CLI docs
- [Shopify Agentic Commerce](https://shopify.dev/docs/agents) — Catalog + Cart + Checkout MCP
- [Link skill.md](https://link.com/skill.md) — Official Link CLI skill reference

# Shopify Product Uploader — Setup Guide

## Step 1 — Create a Shopify Custom App

You need a private API token. Do this once per store:

1. Go to your Shopify Admin → Settings → Apps and sales channels
2. Click "Develop apps" → "Create an app"
3. Name it "OpenClaw Product Uploader"
4. Click "Configure Admin API scopes" and enable:
   - `write_products` — create and update products
   - `read_products` — search and verify products
   - `write_inventory` — manage stock levels
   - `read_inventory` — read current stock
   - `write_collections` — assign products to collections
   - `read_collections` — list existing collections
5. Click "Save" then "Install app"
6. Copy the "Admin API access token" (starts with `shpat_`)
   ⚠️ You only see this once — save it somewhere safe

---

## Step 2 — Tell OpenClaw your store details

Send your OpenClaw bot this message (replace values with your own):

```
Set my Shopify config:
Store: my-store-name
Token: shpat_xxxxxxxxxxxxxxxxxxxx
Vendor: My Brand Name
```

OpenClaw will store this securely in memory and use it for all future uploads.

---

## Step 3 — Test with a single product

Send your bot:
```
Upload this — [product name], £[price], [brief description]
```

If you get a ✅ success message with a product URL, you're fully set up.

---

## API Rate Limits by Plan

| Shopify Plan | Requests/second | Burst limit |
|--------------|----------------|-------------|
| Basic        | 2/sec          | 40 requests |
| Shopify      | 2/sec          | 40 requests |
| Advanced     | 4/sec          | 80 requests |
| Plus         | 4/sec          | 80 requests |

This skill automatically throttles to stay within your plan's limits.
For bulk uploads of 100+ products, expect approximately:
- Basic plan: ~50 products/minute
- Advanced plan: ~100 products/minute

---

## CSV Format

The skill accepts flexible column names but this format works best:

```csv
product_name,sell_price,compare_price,sku,qty,variant_colour,variant_size,img_url,category,desc
Blue Merino Scarf,34.99,44.99,SKU-001,50,Navy|Forest Green,,https://cdn.store.com/scarf.jpg,Scarves,Soft merino wool scarf
Ceramic Plant Pot,12.99,15.99,SKU-002,30,,S|M|L,https://cdn.store.com/pot.jpg,Home Decor,
```

Notes:
- Variants use pipe `|` as separator within a cell
- Leave `desc` empty for auto-generated descriptions
- Leave `compare_price` empty if not on sale
- `img_url` must be a publicly accessible URL

---

## Troubleshooting

**"401 Unauthorized"**
→ Your access token is wrong or expired. Regenerate it in Shopify Admin → Apps → OpenClaw Product Uploader → API credentials.

**"403 Forbidden"**
→ A required API scope is missing. Go back to Step 1 and check all scopes are enabled.

**"422 Unprocessable Entity"**
→ Usually a duplicate SKU. Either change the SKU or ask OpenClaw to update the existing product instead.

**Images not showing**
→ Shopify requires a publicly accessible image URL. Local file paths (e.g. /Users/you/Desktop/photo.jpg) won't work. Upload images to Shopify Files first, then use the CDN URL.

**Product created but inventory shows 0**
→ Shopify separates inventory management by location. Ask OpenClaw: "Set stock for [product] to [qty] at my main location"

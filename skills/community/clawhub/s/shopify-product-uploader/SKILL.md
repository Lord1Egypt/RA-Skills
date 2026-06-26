# Shopify Product Uploader v2

## Overview
Upload single products, bulk CSV batches, or image-based products to a Shopify store.
Automatically generates SEO-optimised titles, descriptions, and tags in UK English.
Supports variants (size, colour), collections, multi-location inventory, draft mode,
archiving, duplicate SKU handling, and barcode fields.

---

## Trigger Phrases
Activate this skill when the user says any of the following (or similar):
- "upload this product"
- "add [product] to the store"
- "bulk upload from [file/CSV]"
- "list this on Shopify"
- "create a product listing"
- "upload these products"
- "add to my store"
- "new product upload"
- "upload from image"
- "upload from supplier data"
- "upload as draft"
- "take down this product" / "archive [product]"
- "unpublish [product]"

---

## Configuration (ask on first use if not set)
Before running any workflow, check that the following are configured in memory.
If missing, ask the user once and store in long-term memory:

```
SHOPIFY_STORE_HANDLE   # e.g. my-store (not the full URL)
SHOPIFY_ACCESS_TOKEN   # Admin API access token (starts with shpat_)
SHOPIFY_API_VERSION    # Default: 2025-01 (update annually)
DEFAULT_VENDOR         # Optional: store's default brand name
DEFAULT_CURRENCY       # Default: GBP
DEFAULT_LANGUAGE       # Default: en-GB
DEFAULT_STATUS         # Default: active (options: active | draft)
SHOPIFY_LOCATION_ID    # Fetched automatically on first inventory operation
```

Store these securely in memory under the key `shopify_config`.
Never log or repeat the access token back to the user.

### Fetching location ID automatically
On first use of any inventory operation, fetch and store the primary location:
```
GET https://{store}.myshopify.com/admin/api/{version}/locations.json
```
Store the first active location's `id` as `SHOPIFY_LOCATION_ID`.
If multiple locations exist, show the list and ask the user which to use as default.

---

## Workflow A — Single Product Upload

Use when the user provides details for one product via text message.

### Step 1 — Extract product data
Parse the user's message for:
- Product name / title hint
- Price (if given in pence, convert to pounds)
- Variants (sizes, colours, materials)
- Images (URLs or attachments)
- Supplier description (raw text to improve upon)
- Category or collection hint
- SKU or barcode / ISBN / EAN (if provided)
- Stock quantity (if provided, default to 100 if not mentioned)
- Compare-at price / sale price
- Upload mode: draft or active (default: use DEFAULT_STATUS from config)

If critical fields are missing (price, product name), ask in one message before proceeding.
Do not ask for fields that can be inferred or generated (title, description, tags).

### Step 2 — Generate SEO content
Generate the following in UK English:

**Title** (max 70 characters):
- Format: [Primary Keyword] | [Secondary Descriptor] | [Brand/Material if relevant]
- Include the most searchable term first
- No ALL CAPS, no special characters except pipes
- Example: "Merino Wool Scarf | Soft Knit Winter Scarf | Navy & Green"

**Description** (150–300 words, HTML formatted):
- Open with the primary benefit or use case (not "Introducing...")
- Second paragraph: materials, dimensions, technical specs
- Third paragraph: variants available, care instructions
- Close with a subtle call to action
- Use `<p>` tags for paragraphs, `<ul>` / `<li>` for specs
- UK English spelling throughout (colour, grey, centre, aluminium)
- Natural keyword inclusion — no keyword stuffing

**Tags** (5–10 tags):
- Mix of: product type, material, use case, target audience, season/occasion
- Lowercase, hyphenated for multi-word tags
- Example: wool-scarf, merino-wool, winter-accessories, unisex, navy, gift-ideas

**SEO meta title** (max 60 chars) and **meta description** (max 155 chars):
- Meta title = product title + store name suffix if space allows
- Meta description = benefit-led one sentence + call to action

### Step 3 — Confirm before upload
Show a structured summary to the user:

```
📦 Ready to upload:

Title:       [generated title]
Status:      [active / draft]
Price:       £[price] GBP
Compare-at:  £[compare_at] (if applicable)
Variants:    [list]
Tags:        [list]
Collection:  [name or "None"]
Stock:       [quantity] units
Barcode:     [barcode or "—"]
Images:      [count] attached / [URLs]

Description preview:
[first 100 chars of description]...

Reply YES to upload, or tell me what to change.
```

Do not upload until the user confirms with YES or equivalent.

### Step 4 — Upload to Shopify

```
POST https://{SHOPIFY_STORE_HANDLE}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/products.json
Headers:
  Content-Type: application/json
  X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}
```

Request body:
```json
{
  "product": {
    "title": "{generated_title}",
    "body_html": "{generated_description_html}",
    "vendor": "{DEFAULT_VENDOR}",
    "product_type": "{inferred_product_type}",
    "tags": "{comma_separated_tags}",
    "status": "{active_or_draft}",
    "variants": [
      {
        "option1": "{variant_value}",
        "price": "{price}",
        "compare_at_price": "{compare_at_price_or_null}",
        "sku": "{sku_or_empty}",
        "barcode": "{barcode_or_null}",
        "inventory_management": "shopify",
        "inventory_quantity": "{stock_qty}",
        "fulfillment_service": "manual",
        "requires_shipping": true,
        "taxable": true
      }
    ],
    "options": [
      { "name": "{option_name e.g. Colour}", "values": ["{variant_values}"] }
    ],
    "images": [
      { "src": "{image_url}" }
    ],
    "metafields": [
      {
        "namespace": "global",
        "key": "title_tag",
        "value": "{seo_meta_title}",
        "type": "single_line_text_field"
      },
      {
        "namespace": "global",
        "key": "description_tag",
        "value": "{seo_meta_description}",
        "type": "single_line_text_field"
      }
    ]
  }
}
```

#### After product creation — set inventory per location
Always run this step after creating a product, even for single-location stores:
```
POST .../inventory_levels/set.json
{
  "location_id": {SHOPIFY_LOCATION_ID},
  "inventory_item_id": {variant.inventory_item_id},
  "available": {stock_qty}
}
```
This ensures inventory registers correctly on both single and multi-location stores.

### Step 5 — Report result

On success:
```
✅ Product uploaded!

Title:      [title]
Status:     [active / draft]
Admin URL:  https://{store}.myshopify.com/admin/products/{id}
Store URL:  https://{store}.myshopify.com/products/{handle}
Product ID: {id}
Inventory:  [qty] units at [location name]
```

On 422 Duplicate SKU — offer to update instead:
```
⚠️ SKU "[sku]" already exists:
   "[existing product title]" (ID: {id})

Options:
1. Update the existing product with new data
2. Upload as new product with no SKU
3. Cancel

What would you like to do?
```

---

## Workflow B — Bulk CSV Upload

Use when the user shares a CSV file path or pastes CSV data.

### Step 1 — Parse CSV
Read the file from the provided path or parse pasted content.
Accept flexible column naming — map common variants:
- "name" / "title" / "product_name" → title
- "desc" / "description" / "body" → raw description
- "price" / "cost" / "sell_price" → price
- "compare_price" / "was_price" / "rrp" → compare_at_price
- "sku" / "code" / "ref" → sku
- "barcode" / "ean" / "isbn" / "upc" → barcode
- "stock" / "qty" / "quantity" / "inventory" → inventory_quantity
- "image" / "img" / "photo" / "image_url" → image src
- "tags" / "keywords" → tags (comma-separated)
- "collection" / "category" / "type" → collection name
- "variant_*" columns → variants (e.g. variant_colour, variant_size)
- "status" / "published" → product status (active/draft)

If column mapping is ambiguous, show detected mapping and ask user to confirm.
Store confirmed mapping in memory keyed by filename pattern for future reuse.

### Step 2 — Pre-upload validation
Before showing the preview, validate:
- Duplicate SKUs within the CSV itself
- Duplicate SKUs against existing Shopify products (API batch check)
- Rows with no price → mark as skip
- Invalid image URLs (must start with http/https) → flag
- Inconsistent variant columns → flag

### Step 3 — Preview
```
Found 47 products in products_may.csv

Column mapping:
  product_name → title ✓  |  sell_price → price ✓  |  rrp → compare_at_price ✓
  ref → SKU ✓  |  qty → inventory ✓  |  img_url → image ✓  |  category → collection ✓

Row  Title                     Price    Variants       Images  Status
1    Bamboo Cutting Board      £18.99   S, M, L        1 ✓     active
2    Linen Tea Towel Set       £14.50   Natural/Grey   1 ✓     active
3    Glass Cafetiere 600ml     £24.99   —              1 ✓     draft

⚠️  3 rows missing images — will upload without images
⚠️  1 row missing price (Row 12) — will skip
🔄  2 rows have existing SKUs (Rows 8, 23) — will UPDATE those products
✅  No internal duplicate SKUs

Reply YES to proceed, or tell me to adjust specific rows.
```

### Step 4 — Generate content in batches
For rows with missing or raw descriptions:
- Process 10 products at a time to stay within token limits
- Generate title + description + tags for each
- Maintain consistent tone across the batch

For rows that already have a full description:
- Fix HTML formatting and UK English spelling only
- Do not rewrite if already 150+ words and well-structured

### Step 5 — Upload sequentially
- 0.5 second delay between requests (Basic plan safe)
- For duplicate SKU rows: use PUT to update existing product
- Track and report live: `Uploading... 12/47 ✅ | 2 updated 🔄 | 0 failed ❌`

### Step 6 — Final report
```
✅ Bulk upload complete

New uploads:   42
Updated:        2
Failed:         2
Skipped:        1

Failed:
- Row 31: Invalid image URL — uploaded without image ⚠️
- Row 38: Shopify 503 timeout — retry this row

Report saved: bulk_upload_report_{timestamp}.txt
```

---

## Workflow C — Upload from Image

Use when the user attaches one or more product photos.

### Step 1 — Analyse image
Use vision to identify:
- Product type and category
- Visible colours, materials, textures
- Dimensions (if reference objects present)
- Brand markings if visible
- Key features and selling points
- Any visible barcodes / EAN codes (extract if readable)

### Step 2 — Ask for missing details (single message)
- Price
- Variants (if not visible in image)
- Stock quantity
- Upload as draft or active?

### Step 3 — Generate and upload
Follow Workflow A from Step 2 onwards.
If the image was attached as a file (not a URL), tell the user:
"Please upload this image to Shopify Files or your CDN and share the URL —
Shopify's API requires a public image URL."

---

## Workflow D — Add to Collection

```
GET .../custom_collections.json   # list existing
POST .../collects.json            # add to existing collection
  { "collect": { "product_id": {id}, "collection_id": {id} } }
POST .../custom_collections.json  # create new if needed
  { "custom_collection": { "title": "{name}" } }
```

---

## Workflow E — Update Existing Product

Triggered by: "update product", "change price", "edit listing", "add variant", "update stock"

Find product:
```
GET .../products.json?title={search_term}&limit=5
```

Common updates:

**Price:**
```json
{ "product": { "variants": [{ "id": {id}, "price": "{new_price}" }] } }
```

**Add variant:**
```
POST .../products/{id}/variants.json
{ "variant": { "option1": "{value}", "price": "{price}", "sku": "{sku}", "barcode": "{barcode}" } }
```

**Stock (multi-location aware):**
```
POST .../inventory_levels/set.json
{ "location_id": {SHOPIFY_LOCATION_ID}, "inventory_item_id": {id}, "available": {qty} }
```

**Description:**
```json
{ "product": { "body_html": "{new_html}" } }
```

**Image:**
```
POST .../products/{id}/images.json
{ "image": { "src": "{url}", "position": 1 } }
```

---

## Workflow F — Draft Mode

For "upload as draft", "don't publish yet", "save for review":
Same as Workflow A but `"status": "draft"`. Confirmation must clearly show DRAFT status.

To publish a saved draft: "publish [product name]"
```
PUT .../products/{id}.json
{ "product": { "status": "active" } }
```

---

## Workflow G — Archive / Unpublish / Delete

Triggered by: "take down", "archive", "unpublish", "hide from store", "remove"

**Archive (reversible):**
Always confirm first with a warning, then:
```
PUT .../products/{id}.json
{ "product": { "status": "archived" } }
```

**Permanent delete** (only if user explicitly says "delete permanently" or "delete forever"):
```
Confirm by typing DELETE — this cannot be undone.
```
```
DELETE .../products/{id}.json
```

---

## SEO Content Rules

1. UK English always — colour, grey, aluminium, centre, organise, fibre
2. Sentence case titles — not Title Case For Every Word
3. Open descriptions with a benefit, not "This product is..." or "Introducing..."
4. Primary keyword in first sentence, naturally
5. Dimensions: metric first (cm/mm/kg), imperial in brackets if helpful
6. Prices in GBP (£) — never USD
7. No VAT mention unless user asks
8. No unsubstantiated superlatives ("best", "world-class")
9. No filler: "high quality", "perfect for", "look no further"
10. Safety-relevant products: add compliance note (CE, UKCA, food-safe)
11. Food/supplements: never make health claims not provided by the user
12. Clothing: always include care instructions if material is known

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| 401 | Invalid/expired token | Ask user to regenerate in Shopify admin |
| 403 | Missing API scope | Name the exact missing scope |
| 422 Duplicate SKU | SKU exists | Offer to update existing product |
| 422 Missing field | Required field absent | Name specific field, ask user |
| 429 Rate limit | Too many requests | Auto-retry after 2s, up to 3× |
| 404 | Wrong store handle or ID | Verify handle, re-fetch product list |
| 503 | Shopify outage | Wait 30s, retry once, then report |

---

## Memory Instructions

Store after each session:
- Last uploaded product ID and title
- Running upload count for the session
- Collection names used (for suggestions)
- User's preferred confirmation phrases
- User's typical default status (active vs draft — learn from pattern)
- CSV column mappings keyed by filename pattern
- SHOPIFY_LOCATION_ID (avoid re-fetching every session)

---

## Tone & Communication Style

- Concise — don't narrate steps unprompted
- ✅ success · ⚠️ warning · ❌ error · 📝 draft · 🔄 update
- Always show full confirmation summary before uploading — never just "shall I proceed?"
- Match user's technical level — skip basics for experienced users, guide less technical ones
- For destructive actions (delete, archive): always confirm with a clear warning first

---

## Limitations

- Images must be publicly accessible URLs — local file paths won't work
- Inventory is set per location — primary location fetched automatically on first use
- Basic plan: 2 req/sec · Advanced: 4 req/sec — respected automatically
- SEO metafields only work on SEO-capable Shopify themes
- Uses REST Admin API 2025-01 — will be updated as Shopify migrates to GraphQL
- Product deletion is permanent — skill always confirms before deleting

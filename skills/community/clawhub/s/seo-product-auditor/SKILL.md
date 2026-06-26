# SEO Product Auditor

## Overview
Scan a Shopify or WooCommerce store's product listings and score each one against
10 SEO criteria. Identify the weakest listings, generate a prioritised fix list, and
optionally rewrite poor titles, descriptions, and tags in place — in UK English.

Designed as a companion to the Shopify Product Uploader skill. Run the audit first
to find what needs fixing, then use the Uploader skill to push the rewrites.

---

## Trigger Phrases
Activate this skill when the user says any of the following (or similar):

Audit triggers:
- "audit my store" / "audit my products"
- "check my listings" / "check my SEO"
- "find weak listings" / "which products have bad SEO"
- "SEO report" / "product SEO score"
- "audit [product name]" — single product audit
- "what's wrong with my listings"
- "find products with no description"
- "find products with missing images"

Fix triggers (after audit):
- "fix the top 10" / "rewrite the worst listings"
- "fix [product name]"
- "apply all suggested fixes"
- "rewrite description for [product]"
- "improve the title on [product]"

---

## Configuration (ask on first use if not set)
Check memory for the following before running any workflow.
If missing, ask the user once and store under `seo_audit_config`:

```
STORE_PLATFORM          # shopify | woocommerce
SHOPIFY_STORE_HANDLE    # e.g. my-store (Shopify only)
SHOPIFY_ACCESS_TOKEN    # starts with shpat_ (Shopify only)
WC_DOMAIN               # e.g. mystore.co.uk (WooCommerce only)
WC_CONSUMER_KEY         # ck_xxx (WooCommerce only)
WC_CONSUMER_SECRET      # cs_xxx (WooCommerce only)
SHOPIFY_API_VERSION     # Default: 2025-01
STORE_NAME              # Used in SEO meta title suffix
LANGUAGE                # Default: en-GB (UK English)
CURRENCY                # Default: GBP
```

Reuse credentials already stored in memory from the Shopify Product Uploader or
Order & Returns Manager skills — do not ask again if already set.
Store under `seo_audit_config` separately so audits are tracked independently.

---

## SEO Scoring Criteria

Score each product out of 100. Each criterion has a maximum point value.
Apply these consistently across every workflow.

| # | Criterion | Max points | How to score |
|---|-----------|-----------|-------------|
| 1 | Title length | 15 | 40–70 chars = 15 · 30–39 or 71–80 = 8 · <30 or >80 = 0 |
| 2 | Title contains primary keyword | 10 | Keyword in first 40 chars = 10 · keyword present but not first = 5 · missing = 0 |
| 3 | Description length | 15 | 150–300 words = 15 · 80–149 words = 8 · 50–79 = 4 · <50 or none = 0 |
| 4 | Description contains keyword | 10 | Keyword in first sentence = 10 · keyword present but not first = 5 · missing = 0 |
| 5 | Tags present | 10 | 5–10 tags = 10 · 2–4 tags = 5 · 0–1 tags = 0 |
| 6 | Images present | 15 | 3+ images = 15 · 2 images = 10 · 1 image = 5 · 0 = 0 |
| 7 | SEO meta title set | 10 | Present and 30–60 chars = 10 · present but wrong length = 5 · missing = 0 |
| 8 | SEO meta description set | 10 | Present and 120–155 chars = 10 · present but wrong length = 5 · missing = 0 |
| 9 | Alt text on images | 5 | All images have alt text = 5 · some = 3 · none = 0 |
| 10 | UK English spelling | 0 (flag only) | Flag if US spellings detected: color, gray, aluminum, center, organize |

Score bands:
- 85–100 = ✅ Good — no action needed
- 65–84  = 🟡 Fair — worth improving
- 40–64  = 🟠 Weak — should be fixed soon
- 0–39   = 🔴 Poor — fix immediately

Primary keyword inference: if no keyword is explicitly provided by the user,
infer it from the product's `product_type` field first, then from the most
specific tag (prefer multi-word descriptive tags over single generic ones),
then fall back to the first 1–2 meaningful nouns in the title.
Do NOT infer the keyword from the full title and then check if the title contains it —
this always scores 10/10 and defeats the purpose of criterion 2.

Examples:
- `product_type: "Scarves"`, tags: `["merino-wool", "winter"]` → keyword: "merino wool scarf"
- `product_type: ""`, tags: `["leather-wallet", "bifold"]` → keyword: "leather wallet"
- `product_type: ""`, tags: `["pot"]`, title: "Blue Ceramic Plant Pot" → keyword: "ceramic plant pot"

---

## Workflow A — Full Store Audit

Use when user says "audit my store", "SEO report", or similar.

### Step 1 — Fetch all products

Shopify — paginate through all products:
```
GET https://{store}.myshopify.com/admin/api/{version}/products.json?limit=250&status=active&fields=id,title,body_html,tags,images,product_type,handle
```
`status=active` returns only published products. This is the correct default for
an SEO audit — archived and draft products are excluded.
- To include drafts (e.g. to fix SEO before publishing): add `&status=draft` as
  a second request and merge results, or use `status=any` if the user asks.
- Archived products are intentionally excluded — they are not indexed by search engines.

If the response `Link` header contains `rel="next"`, continue paginating until
all pages are retrieved. Store total product count.

**Important:** `metafields` cannot be included in the `fields` parameter of the
products bulk endpoint — Shopify silently ignores it. Metafields must be fetched
separately per product after the bulk fetch:
```
GET .../products/{id}/metafields.json?namespace=global&key=title_tag
GET .../products/{id}/metafields.json?namespace=global&key=description_tag
```
For large stores (250+ products), batch these metafield fetches with a 0.5s delay
between requests to stay within Shopify's rate limits. Show progress to the user:
`Fetching SEO data... 47/84 products`

**HTML stripping for word count:** `body_html` contains HTML markup. Before
counting words for criterion 3, strip all HTML tags:
- Remove all content between `<` and `>` characters
- Collapse whitespace
- Count remaining space-separated tokens
Example: `<p>Great scarf</p>` → `"Great scarf"` → 2 words (not 3)

WooCommerce:
```
GET https://{WC_DOMAIN}/wp-json/wc/v3/products?per_page=100&page={n}&status=publish
Authorization: Basic {base64(key:secret)}
```
Paginate using both response headers:
- `X-WP-Total` — total number of products
- `X-WP-TotalPages` — total number of pages
Continue fetching until page number exceeds `X-WP-TotalPages`.
WooCommerce stores Yoast SEO data in `yoast_head_json.title` and
`yoast_head_json.description` if Yoast SEO is installed — check these fields.

### Step 2 — Score every product
Apply the 10-criterion scoring table to each product.
Calculate total score out of 100.
Track which specific criteria each product fails.

### Step 3 — Aggregate and report

Sort products by score ascending (worst first).

```
📊 SEO Audit — {store_name}
{date}

Total products scanned:  {n}
Average SEO score:       {avg}/100

Score distribution:
  ✅ Good  (85–100):  {n} products  ({pct}%)
  🟡 Fair  (65–84):   {n} products  ({pct}%)
  🟠 Weak  (40–64):   {n} products  ({pct}%)
  🔴 Poor  (0–39):    {n} products  ({pct}%)

Top issues across store:
  · Missing SEO meta description:  {n} products
  · Description under 50 words:    {n} products
  · Missing or too few images:     {n} products
  · No tags:                       {n} products
  · Title too short or too long:   {n} products

Bottom 10 — worst scoring products:
  1. {title}                 {score}/100  🔴
  2. {title}                 {score}/100  🔴
  3. {title}                 {score}/100  🔴
  ...

Reply:
  "fix top 10"  — rewrite and push the 10 worst listings
  "fix [name]"  — fix a specific product
  "full list"   — see every product with its score
  "export"      — get a CSV of all scores
```

### Step 4 — Store audit results in memory
Store the full scored product list in memory under `last_audit_{store_handle}`:
```json
{
  "date": "{ISO date}",
  "product_count": {n},
  "average_score": {avg},
  "products": [
    {
      "id": {id},
      "title": "{title}",
      "score": {n},
      "tags": "{comma_separated_tags_string}",
      "failures": ["{criterion_name}", ...]
    },
    ...
  ]
}
```
Include `tags` in each product entry so Workflow C can read current tags from
memory without an extra API call. The `failures` array uses criterion names
matching the scoring table (e.g. `"title_length"`, `"meta_description"`,
`"images"`) so Workflow E can filter without re-fetching.

---

## Workflow B — Single Product Audit

Use when user says "audit [product name]" or "check the SEO on [product]".

### Step 1 — Find the product
Search by title:
```
GET .../products.json?title={search_term}&limit=5&fields=id,title,body_html,tags,images,product_type,handle,status
```
If multiple matches, show compact list and ask user to confirm.

### Step 2 — Fetch metafields (two separate calls)
```
GET .../products/{id}/metafields.json?namespace=global&key=title_tag
GET .../products/{id}/metafields.json?namespace=global&key=description_tag
```
Check `response.metafields[0].value` in each response for the current SEO values.

### Step 3 — Score and report in detail

```
🔍 SEO audit — "{product title}"
Score: {score}/100 {band_emoji}

Criterion breakdown:
  Title length ({n} chars)          {pts}/15  {status}
  Keyword in title                   {pts}/10  {status}
  Description length ({n} words)    {pts}/15  {status}
  Keyword in description             {pts}/10  {status}
  Tags ({n} tags)                    {pts}/10  {status}
  Images ({n} images)                {pts}/15  {status}
  SEO meta title                     {pts}/10  {status}
  SEO meta description               {pts}/10  {status}
  Image alt text                      {pts}/5   {status}
  UK English                          —         {✅ or ⚠️ US spellings found}
  ────────────────────────────────────────────
  Total                              {score}/100 {band_emoji}

Issues found:
  🔴 No SEO meta description set
  🟠 Description is only {n} words — aim for 150–300
  🟡 Only {n} tags — add {n} more for better discoverability

Suggested fixes:
  · Rewrite title: "{suggested_title}"
  · Add tags: {suggested_tags}

Reply "fix it" to apply all changes, or tell me which to apply first.
```

Status labels: ✅ = full points · 🟡 = partial · 🔴 = zero

---

## Workflow C — Fix a Product (Rewrite and Push)

Triggered by: "fix it", "fix [product name]", "fix top 10", "apply all fixes"

### Step 1 — Determine scope
- "fix [product]" → single product (Workflow B result or search)
- "fix top 10" → top 10 from last audit in memory
- "apply all fixes" → all products scored 🔴 or 🟠 from last audit

If no recent audit in memory, run Workflow A first.

### Step 2 — Generate improvements in batches

For bulk fixes (top 10 or more), generate content in batches of 3 products at a time
to manage token usage and allow incremental review. Do not generate all 10 descriptions
before showing any output — the user should see progress.

For single-product fixes, generate all fields at once before the preview.

For each product being fixed, only generate the fields that are actually failing:
- Criterion 1 or 2 failing → rewrite title
- Criterion 3 or 4 failing → rewrite description
- Criterion 5 failing → generate additional tags
- Criterion 7 failing → generate SEO meta title
- Criterion 8 failing → generate SEO meta description
- Criterion 9 failing → generate alt text for each image missing it

Do not rewrite fields that are already scoring full marks.

**Title** (if score < full marks on criteria 1 or 2):
- 40–70 characters
- Primary keyword in first 40 characters
- Sentence case — no ALL CAPS
- Format: [Primary Keyword] | [Secondary Descriptor] | [Material/Brand if relevant]
- UK English: colour not color, grey not gray

**Description** (if score < full marks on criteria 3 or 4):
- 150–300 words
- HTML formatted: `<p>` for paragraphs, `<ul><li>` for specs
- Open with primary benefit — not "This product is..." or "Introducing..."
- Include primary keyword naturally in first sentence
- Second paragraph: materials, dimensions, specs
- Third paragraph: variants, care instructions
- Close with subtle call to action
- UK English throughout

**Tags** (if score < full marks on criterion 5):
- Generate 5–10 tags if fewer than 5 exist
- Mix: product type, material, use case, audience, season/occasion
- Lowercase, hyphenated for multi-word: wool-scarf, gift-ideas
- Do not duplicate existing good tags — only add missing ones

**SEO meta title** (if criterion 7 = 0):
- 30–60 characters
- Format: {primary keyword} — {store name}
- If store name would push over 60 chars, use keyword only

**SEO meta description** (if criterion 8 = 0):
- 120–155 characters exactly
- Benefit-led: start with what the product does, not what it is
- Include a soft call to action: "Free UK delivery on orders over £X"
- No keyword stuffing

### Step 3 — Preview before pushing

Show a before/after summary. Never push without user confirmation.

For single product:
```
✏️ Proposed fixes — "{current title}"

TITLE
  Before: {current_title} ({n} chars)
  After:  {new_title} ({n} chars) ✅

DESCRIPTION
  Before: {n} words — {first 80 chars of current}...
  After:  {n} words — {first 80 chars of new}...

TAGS
  Adding: {new_tags_list}
  Keeping: {existing_good_tags}

SEO META TITLE
  Before: {current or "not set"}
  After:  {new} ({n} chars) ✅

SEO META DESCRIPTION
  Before: {current or "not set"}
  After:  {new} ({n} chars) ✅

Apply these changes? YES / adjust / skip
```

For bulk (top 10 or all):
```
✏️ Bulk fixes ready — {n} products

Products to be updated:
  1. "{title}"  {old_score}→{projected_score}  (+{gain} pts)
  2. "{title}"  {old_score}→{projected_score}
  ...

Estimated score improvement: avg +{gain} points across {n} products

Apply all? YES / review each one first / skip
```

### Step 4 — Push to Shopify

For each product, update in sequence with 0.5s delay between requests.

Update title and description:
```
PUT https://{store}.myshopify.com/admin/api/{version}/products/{id}.json
{
  "product": {
    "id": {id},
    "title": "{new_title}",
    "body_html": "{new_description_html}"
  }
}
```

Update tags (use audit memory first; only re-fetch if audit data is stale or missing):

If `last_audit_{store_handle}` memory has the product's current tags (and the audit
is from this session), use those directly — no extra GET needed.

If audit data is missing or stale, fetch current tags:
```
GET .../products/{id}.json?fields=id,tags
```

Parse the `tags` field as a comma-separated string. Split on `", "` (comma followed
by a space) — not just `","` — to handle tags correctly:
```
"merino-wool, wool-scarf, gift-ideas" → ["merino-wool", "wool-scarf", "gift-ideas"]
```

Deduplicate: compare new tags against existing (case-insensitive). Only add tags
not already present. Then write the merged list back:
```
PUT .../products/{id}.json
{
  "product": {
    "id": {id},
    "tags": "{merged_comma_space_separated_tags}"
  }
}
```
If existing tags is empty string, write new tags only (no leading comma or space).

Update image alt text (for each image missing alt text):
```
PUT .../products/{product_id}/images/{image_id}.json
{
  "image": {
    "id": {image_id},
    "alt": "{descriptive alt text}"
  }
}
```
Generate alt text as: `"{short product name} in {colour} — {view}"`
Example: `"Merino wool scarf in Navy — front draped view"`
Keep under 125 characters. Never start with "Image of" or "Photo of".
Fetch current image IDs from the product data already retrieved in Step 1.

Update SEO meta title and description via metafields:
```
GET .../products/{id}/metafields.json?namespace=global&key=title_tag
```

If exists — update (use the product-scoped path):
```
PUT https://{store}.myshopify.com/admin/api/{version}/products/{product_id}/metafields/{metafield_id}.json
{ "metafield": { "id": {metafield_id}, "value": "{seo_title}", "type": "single_line_text_field" } }
```

If not exists — create:
```
POST .../products/{id}/metafields.json
{
  "metafield": {
    "namespace": "global",
    "key": "title_tag",
    "value": "{seo_title}",
    "type": "single_line_text_field"
  }
}
```
Repeat for `description_tag`.

### Step 5 — Confirm results and update memory

Write to memory under `last_fixed_{store_handle}`:
```json
{
  "date": "{ISO date}",
  "product_ids": [{id1}, {id2}, ...],
  "old_scores": { "{id}": {score}, ... },
  "new_scores": { "{id}": {score}, ... }
}
```
This enables Workflow F (re-audit) to rescore only the changed products.

Single product confirm:
```
✅ {product title} — updated

Score:  {old}/100 → {new}/100 (+{gain} pts) {new_band}
Admin:  https://{store}.myshopify.com/admin/products/{id}
```

Bulk confirm:
```
✅ Bulk fix complete — {n} products updated

Before avg: {old_avg}/100
After avg:  {new_avg}/100 (+{gain} pts)

Updated:  {n} ✅
Failed:   {n} ❌ (if any — list title and error)

Run "re-audit" to rescore these products.
```

Also update `last_audit_{store_handle}` in memory to reflect new scores for
any products that were fixed, so future targeted scans use current data.

---

## Workflow D — Export Audit as CSV

Triggered by: "export", "download scores", "give me a CSV of all scores"

Generate a CSV from the last stored audit in memory.

**CSV escaping rules — apply to every cell:**
- Wrap all string values in double-quotes: `"Merino Wool Scarf"`
- Escape any double-quote within a value by doubling it: `"Scarf, ""Red"" Edition"`
- Numbers (scores, point values) do not need quoting

Header row:
```
ID,Title,Score,Band,Title Score,Desc Score,Tags Score,Images Score,Meta Title Score,Meta Desc Score,Alt Text Score,US Spellings,Admin URL
```

Data rows (one per product):
```
{id},"{escaped_title}",{total},"{band}",{pts},{pts},{pts},{pts},{pts},{pts},{pts},{true/false},"https://{store}.myshopify.com/admin/products/{id}"
```

Save to workspace as `seo_audit_{store_handle}_{YYYY-MM-DD}.csv` and confirm path.

If no recent audit in memory:
```
No audit found in memory. Run "audit my store" first, then I can export the results.
```

---

## Workflow E — Targeted Issue Scan

Use when user asks about a specific problem rather than a full audit.

Triggered by:
- "find products with no description" → filter score criterion 3 = 0
- "find products with no images" → filter criterion 6 = 0
- "find products with no SEO meta" → filter criteria 7 or 8 = 0
- "find products with no tags" → filter criterion 5 = 0
- "find products with US spellings" → filter criterion 10 = flagged
- "find products with short titles" → filter criterion 1 = 0
- "find products with titles over 70 characters" → filter criterion 1 partial

Pull from last audit in memory if available (no re-fetch needed).
If no audit in memory, fetch products first (Workflow A Step 1).

Report format:
```
🔍 Products with no SEO meta description — {n} found

  1. "{title}"    {score}/100  https://{store}.myshopify.com/admin/products/{id}
  2. "{title}"    {score}/100  https://{store}.myshopify.com/admin/products/{id}
  ...

Reply "fix these" to generate and push meta descriptions for all {n}.
```

---

## Workflow F — Re-audit After Fixes

Triggered by: "re-audit", "check scores again", "what's my SEO score now"

Read `last_fixed_{store_handle}` from memory to get the list of product IDs changed
in the last fix session, plus their `old_scores`.

Re-fetch those products from the API to get their current state:
```
GET .../products/{id}.json?fields=id,title,body_html,tags,images,product_type,handle
GET .../products/{id}/metafields.json?namespace=global&key=title_tag
GET .../products/{id}/metafields.json?namespace=global&key=description_tag
```

Apply the full scoring rubric to the freshly fetched data.
Compare new scores against `last_fixed.old_scores` for the before/after view.
Update `last_audit_{store_handle}` in memory with the new scores.

```
📊 Re-audit — {n} products rescored

  "{title short}"     {old_score} → {new_score}  +{gain} {band}
  "{title short}"     {old_score} → {new_score}  +{gain} {band}
  "{title short}"     {old_score} → {new_score}  +{gain} {band}

Store average: {old_avg}/100 → {new_avg}/100 (+{gain} pts)

{If any product didn't improve as expected}
⚠️ "{title}" only gained {gain} pts — images score is still capped at 5/15
   because only 1 image is present. Add 2 more images to reach full marks.
```

---

## UK English Enforcement

When generating or rewriting any content, always apply:

| ✅ Use | ❌ Never use |
|--------|------------|
| colour | color |
| grey | gray |
| aluminium | aluminum |
| centre | center |
| organise | organize |
| practise (verb) | practice (verb) |
| fibre | fiber |
| licence (noun) | license (noun) |
| metres / centimetres | meters / centimeters |
| £ GBP | $ USD |

When scanning existing descriptions for US spellings (criterion 10), check for
all of the above. Flag the specific words found, e.g.:
`⚠️ US spellings: "color" (×2), "aluminum" (×1) — will fix on rewrite`

---

## SEO Content Quality Rules

Apply when generating titles, descriptions, and meta content:

**Titles:**
- 40–70 characters — hard limit
- Primary keyword in first 40 characters
- Sentence case — never ALL CAPS
- No special characters except pipes `|` and ampersands `&`
- No filler: "best", "amazing", "premium", "high quality"
- Include material, size range, or colour set if space allows

**Descriptions:**
- 150–300 words — this range is optimal for both SEO and conversion
- Open with a benefit statement, not a product definition
- Include primary keyword naturally in the first sentence
- Use HTML: `<p>` for paragraphs, `<ul><li>` for bullet specs
- Metric dimensions first (cm/mm/kg), imperial in brackets if relevant
- End with a single, low-pressure call to action
- Never invent specifications not provided — flag gaps to user

**Tags:**
- 5–10 tags per product
- Mix: product type, material, use case, occasion, target audience
- All lowercase, multi-word tags hyphenated
- Never duplicate words already in the title
- Never use single-letter or generic tags like "new", "sale"

**SEO meta title:**
- 30–60 characters (Google typically displays ~60)
- Format: {Primary Keyword} — {Store Name}
- If brand name pushes over 60, use keyword + separator only

**SEO meta description:**
- 120–155 characters (Google truncates at ~155)
- Benefit-led first half, soft CTA second half
- Include one keyword naturally
- Example (140 chars): "Pure Merino wool scarf in Navy and Forest Green — 180cm long, warm without bulk. Free UK delivery on orders over £40. Shop now."

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| 401 Unauthorized | Invalid/expired token | Ask user to regenerate in Shopify Admin → Apps |
| 403 Forbidden | Missing scope | State missing scope: `read_products` or `write_products` |
| 404 Product not found | Wrong ID or deleted product | Skip and note in report |
| 429 Rate limited | Too many requests | Auto-retry after 2s, up to 3× — for bulk audits add 0.5s delay between fetches |
| 503 Shopify outage | Service down | Wait 30s, retry once, then report |

Required Shopify API scopes:
- `read_products` — fetch product data, images, and tags for auditing
- `write_products` — push rewritten titles, descriptions, tags, image alt text, and product metafields (sufficient for `global.title_tag` and `global.description_tag` on API versions 2023-04+)
- `write_metafields` — explicit metafield write access; add this if you receive a 403 when updating SEO meta title or description

Note: `read_metaobjects` and `write_metaobjects` are for Shopify Metaobjects (a
different feature). Do not use them here — they will not grant access to product
metafields. Use `write_products` first; add `write_metafields` only if needed.

---

## WooCommerce Support

When STORE_PLATFORM = woocommerce:

Base URL: `https://{WC_DOMAIN}/wp-json/wc/v3`
Auth: `Authorization: Basic {base64(WC_CONSUMER_KEY:WC_CONSUMER_SECRET)}`

**Fetch products:**
```
GET /products?per_page=100&page={n}&status=publish
```

**Update product:**
```
PUT /products/{id}
{
  "name": "{new_title}",
  "description": "{new_description_html}",
  "tags": [{ "name": "{tag}" }, ...]
}
```

**WooCommerce SEO meta fields** (Yoast SEO plugin):
Yoast stores meta in post meta — not directly accessible via WooCommerce REST API.
If the user has Yoast installed, advise them to update SEO title/description
directly in the Yoast panel in wp-admin, or via the Yoast REST API if enabled.
Flag this limitation clearly rather than silently skipping.

**WooCommerce images (alt text update):**
⚠️ The WooCommerce `PUT /products/{id}` endpoint **replaces** the entire `images`
array. Sending only the image you want to update will delete all other images.

Always fetch the full current images array first:
```
GET /products/{id}?_fields=id,images
```
Then update the specific image's alt text within the full array and PUT the
complete array back:
```
PUT /products/{id}
{
  "images": [
    { "id": {image_1_id}, "src": "{url_1}", "alt": "{updated_alt}" },
    { "id": {image_2_id}, "src": "{url_2}", "alt": "{existing_alt_2}" },
    { "id": {image_3_id}, "src": "{url_3}", "alt": "{existing_alt_3}" }
  ]
}
```
Include every image in the product, not just the one being updated.

---

## Memory Instructions

Store after each audit session:
- `last_audit_{store_handle}`: full scored product list with date, scores, failures
- `last_fixed_{store_handle}`: list of product IDs updated in the last fix session
- `store_avg_score_{store_handle}`: running average score — compare across audits to show progress over time
- `common_issues_{store_handle}`: the most frequent failure criteria — surface these proactively ("your store's biggest SEO gap is still missing meta descriptions on 34 products")

---

## Tone & Communication

- 📊 full audit · 🔍 single product · ✏️ fix preview · ✅ applied · 🔴 poor · 🟠 weak · 🟡 fair · 🟢 good
- Keep score reports scannable — use consistent column alignment
- For bulk operations: always show count and projected improvement before pushing
- Never push changes without explicit user confirmation (YES or equivalent)
- When a product is already scoring well (85+), acknowledge it: "This one is already strong — no changes needed"
- When suggesting tag additions, explain briefly why each tag helps: don't just list them
- If user is clearly experienced, skip explanations and lead with data
- Dates in DD MMM YYYY format — never MM/DD/YYYY

# Product Uploader — Few-Shot Examples

These examples train the LLM on expected input/output quality.
Always aim to match or exceed the quality shown here.

---

## Example 1 — Single product from brief text

**User input:**
"Upload this — Blue Merino Wool Scarf, £34.99, Navy and Forest Green, 180cm x 30cm, image: https://cdn.mystore.com/scarf.jpg"

**Generated title:**
"Merino Wool Scarf | Soft Knit Winter Scarf | Navy & Forest Green"

**Generated alt text:**
"Navy Merino Wool Scarf — 180cm x 30cm knit scarf shown draped, Forest Green colourway also available"

**Generated description (HTML):**
```html
<p>Wrap up in effortless warmth with this generously sized Merino wool scarf. 
Knitted from 100% pure Merino — one of the softest natural fibres available — 
it provides exceptional insulation without the bulk or itch of cheaper wool blends.</p>

<p>At 180cm x 30cm, it's long enough to loop twice or drape loosely over a coat. 
Available in two versatile colourways: deep Navy and rich Forest Green, both 
designed to complement a wide range of outerwear.</p>

<ul>
  <li>Material: 100% Merino wool</li>
  <li>Dimensions: 180cm x 30cm (71" x 12")</li>
  <li>Available colours: Navy, Forest Green</li>
  <li>Care: Hand wash cold or dry clean</li>
</ul>

<p>A reliable everyday essential or a considered gift for someone who appreciates 
quality winter accessories.</p>
```

**Tags:** merino-wool, wool-scarf, winter-scarf, winter-accessories, unisex-scarf, navy, forest-green, gift-ideas, cold-weather, knit-scarf

**SEO meta title:** "Merino Wool Scarf | Navy & Forest Green | [Store Name]"

**SEO meta description:** "Pure Merino wool scarf in Navy and Forest Green. 180cm x 30cm — soft, warm, and lightweight. Free UK delivery on orders over £40."

---

## Example 2 — Supplier data with codes to strip

**User input:**
"Upload: REF XB-4421 // Acme Textiles — CHENILLE THROW BLANKET 130x170cm OATMEAL/SLATE GREY/DUSTY PINK £24.99 RRP £34.99 MOQ 6"

**What to strip:** REF XB-4421, Acme Textiles, MOQ 6 (internal trade info)
**What to keep:** dimensions, colours, price, compare-at

**Generated title:**
"Chenille Throw Blanket | Soft Textured Blanket | 130 x 170cm"

**Generated description (HTML):**
```html
<p>Add warmth and texture to any room with this chunky chenille throw. 
The looped weave creates a satisfyingly tactile surface that drapes beautifully 
over sofas, armchairs, or the end of a bed.</p>

<p>Available in three considered colourways — warm Oatmeal, cool Slate Grey, 
and soft Dusty Pink — each chosen to work with contemporary neutral interiors.</p>

<ul>
  <li>Dimensions: 130 x 170cm (51" x 67")</li>
  <li>Available colours: Oatmeal, Slate Grey, Dusty Pink</li>
  <li>Care: Machine wash 30°C, do not tumble dry</li>
</ul>

<p>A generous size for curling up on the sofa, or a thoughtful addition to a 
guest bedroom.</p>
```

**Note:** Supplier name (Acme Textiles) and internal ref (XB-4421) correctly stripped.
**Note:** MOQ of 6 is a trade detail — not included in public listing.
**Note:** Compare-at price £34.99 correctly captured.

---

## Example 3 — Children's product (compliance handling)

**User input:**
"Add this — Wooden Stacking Rings, £12.99, natural beech wood, for babies, ages 6 months+, image: https://cdn.store.com/rings.jpg"

**Compliance flag:** Children's toy — add CE mark note. Confirm with user before publishing.

**Agent response before generating:**
"Before I generate this listing — can you confirm the toy is CE marked (or UKCA marked)? I'll add the required compliance note to the description."

**After user confirms CE marked:**

**Generated description (HTML):**
```html
<p>A beautifully simple stacking toy that grows with your baby. Made from smooth-sanded 
natural beech wood, these rings are gentle on curious hands and free from sharp edges 
or splinters.</p>

<p>Stacking and unstacking the rings helps develop hand-eye coordination, fine motor 
skills, and an early understanding of relative size — all through open-ended, 
screen-free play.</p>

<ul>
  <li>Material: Natural beech wood, non-toxic finish</li>
  <li>Suitable from: 6 months+</li>
  <li>CE marked — meets UK and EU toy safety standards</li>
  <li>Care: Wipe clean with a damp cloth</li>
</ul>

<p>A timeless first toy that's as easy to pack for travel as it is to pull out of 
the toy box.</p>
```

---

## Example 4 — Multi-variant product (Size × Colour)

**User input:**
"Upload linen shirt, £55, sizes S/M/L/XL, colours White/Blue/Sage, 50 of each, image: https://cdn.store.com/shirt.jpg"

**Variant combinations generated:** 4 sizes × 3 colours = 12 variants total

**Agent confirmation preview:**
```
📦 Ready to upload:

Title:     Linen Shirt | Relaxed Fit | White, Blue & Sage
Price:     £55.00 GBP
Variants:  Size (S/M/L/XL) × Colour (White/Blue/Sage) = 12 variants
Stock:     50 units per variant (600 total)
Images:    1 ✓
Status:    Active

Reply YES to upload, or tell me what to change.
```

---

## Example 5 — Bulk upload column mapping confirmation

**User input:** "Upload from /workspace/new_arrivals.csv"

**Agent response:**
```
📋 Found 34 products in new_arrivals.csv

Column mapping detected:
  product_name  → title           ✓
  sell_price    → price           ✓
  rrp           → compare_at      ✓
  ref           → SKU             ✓
  qty           → inventory       ✓
  img_url       → image src       ✓
  category      → collection      ✓
  copy          → description     ✓ (12 rows <150 words — will enhance)
  weight_g      → weight          ✓ (will convert g → kg)

Pre-upload checks:
  ✅ No duplicate SKUs in file
  ⚠️  3 rows have no image URL — will upload without images
  ⚠️  Row 8: price appears to be in pence (3499) — did you mean £34.99?
  ℹ️  2 rows appear to be children's products — will add CE note (please confirm CE marked)

Sample (first 3):
Row  Title                    Price    Variants        Images  Weight
1    Bamboo Cutting Board     £18.99   S / M / L       1 ✓     0.45kg
2    Linen Tea Towel Set      £14.50   Natural/Grey    1 ✓     0.12kg
3    Glass Cafetière 600ml   £24.99   —               1 ✓     0.38kg

Reply YES to upload all 34 (fixing Row 8 price to £34.99), or let me know of any changes.
```

---

## Example 6 — Update product price with variant precision

**User input:** "Change the bamboo cutting board price to £21.99 but keep the small at £18.99"

**Agent response:**
```
🔍 Found 1 match:

"Bamboo Cutting Board | Sustainable Kitchen Board | S, M & L"
ID: 7823456789
Current prices: S £18.99 / M £18.99 / L £18.99

Updating M and L to £21.99, keeping S at £18.99 — confirm?
```

**After YES:**
```
✅ Prices updated:

Bamboo Cutting Board — S:  £18.99 (unchanged)
Bamboo Cutting Board — M:  £21.99 ✓
Bamboo Cutting Board — L:  £21.99 ✓

Admin: https://[store].myshopify.com/admin/products/7823456789
```

---

## Quality Benchmarks

| ✅ Write this | ❌ Not this |
|---|---|
| "Wrap up in effortless warmth" | "This high-quality scarf is perfect for..." |
| "Available in three colourways" | "Comes in 3 amazing colors" |
| "Suits modern and natural interiors" | "Great for any home!" |
| "180cm x 30cm (71" x 12")" | "Large size" |
| "Hand wash cold or dry clean" | "Easy to care for" |
| "CE marked. Suitable for ages 6 months+" | "Safe for children" |
| UK English throughout | US spellings (color, gray, aluminum, fiber) |
| Specific materials ("100% Merino wool") | Vague ("premium materials") |
| Factual claims only | "World's softest scarf", "Best in class" |
| Supplier codes stripped | "REF: XB-4421 by Acme Textiles" |
| Alt text on every image | Empty alt attributes |

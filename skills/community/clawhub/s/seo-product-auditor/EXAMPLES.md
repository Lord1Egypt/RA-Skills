# SEO Product Auditor — Examples

These examples show expected input/output for each workflow.
The agent should match or exceed this quality and consistency.

---

## Example 1 — Full store audit

**User:** "audit my store"

**Agent:**
```
📊 SEO Audit — The Wool House
12 Apr 2026

Total products scanned:  84
Average SEO score:       58/100

Score distribution:
  ✅ Good  (85–100):   9 products  (11%)
  🟡 Fair  (65–84):   22 products  (26%)
  🟠 Weak  (40–64):   31 products  (37%)
  🔴 Poor  (0–39):    22 products  (26%)

Top issues across store:
  · Missing SEO meta description:  61 products
  · Description under 50 words:    28 products
  · Fewer than 5 tags:             34 products
  · Missing or too few images:     19 products
  · Title too short (<30 chars):    8 products

Bottom 10 — worst scoring:
  1. "Scarf"                           12/100  🔴
  2. "Blue pot"                         18/100  🔴
  3. "Leather wallet brown"             19/100  🔴
  4. "Set of 3 tea towels"              28/100  🔴
  5. "Organic Cotton Throw Blanket"     31/100  🔴
  6. "Bamboo Board"                     34/100  🔴
  7. "Glass cafetiere"                  38/100  🔴
  8. "Silver necklace"                  39/100  🔴
  9. "Kids wooden toy"                  41/100  🟠
  10. "Merino Hat - Grey"               44/100  🟠

Reply:
  "fix top 10"   — rewrite and push the 10 worst listings
  "fix [name]"   — fix a specific product
  "full list"    — see all 84 products with scores
  "export"       — download scores as CSV
```

---

## Example 2 — Single product audit

**User:** "audit the leather wallet"

**Agent:**
```
🔍 SEO audit — "Leather wallet brown"
Score: 19/100 🔴

Criterion breakdown:
  Title length (20 chars)            0/15  🔴 Too short — aim for 40–70
  Keyword in title                   5/10  🟡 "leather wallet" present but not leading
  Description length (38 words)      4/15  🟠 Too short — aim for 150–300 words
  Keyword in description             5/10  🟡 Present but not in first sentence
  Tags (1 tag)                       0/10  🔴 Only 1 tag — add at least 4 more
  Images (1 image)                   5/15  🟡 Only 1 image — add 2+ more
  SEO meta title                     0/10  🔴 Not set
  SEO meta description               0/10  🔴 Not set
  Image alt text                     0/5   🔴 No alt text on any image
  UK English                         —     ✅ No US spellings found
  ──────────────────────────────────────────
  Total                             19/100  🔴

Issues found:
  🔴 Title is only 20 chars and doesn't lead with the primary keyword
  🔴 No SEO meta title or description set
  🔴 No image alt text
  🔴 Only 1 tag — nearly invisible in search and collections
  🟠 Description at 38 words is too thin — need 150+ for SEO value

Suggested title: "Slim Leather Bifold Wallet | 6 Card Slots | Brown, Black & Tan"

Reply "fix it" to apply all changes, or tell me which to apply first.
```

---

## Example 3 — Fix single product

**User:** "fix it"

**Agent:**
```
✏️ Proposed fixes — "Leather wallet brown"

TITLE
  Before: "Leather wallet brown" (20 chars) 🔴
  After:  "Slim Leather Bifold Wallet | 6 Card Slots | Brown, Black & Tan" (63 chars) ✅

DESCRIPTION
  Before: 38 words — "A genuine leather bifold wallet available in brown, black and tan..."
  After:  187 words — "Carry everything you need without the bulk. This slim bifold wallet
          is crafted from genuine full-grain leather that softens with use..."

TAGS
  Keeping:  leather-wallet
  Adding:   bifold-wallet, mens-wallet, slim-wallet, genuine-leather,
            card-holder, brown-leather, gift-for-him, fathers-day

SEO META TITLE
  Before: not set
  After:  "Slim Leather Bifold Wallet | Brown, Black & Tan" (48 chars) ✅

SEO META DESCRIPTION
  Before: not set
  After:  "Genuine leather bifold wallet with 6 card slots in Brown, Black
           & Tan. Slim profile, softens with use. Free UK delivery over £40." (140 chars) ✅

IMAGE ALT TEXT
  Image 1: adding alt "Slim leather bifold wallet in brown — front view"

Apply these changes? YES / adjust / skip
```

**User:** "yes"

**Agent:**
```
✅ "Leather wallet brown" — updated

Score:  19/100 → 92/100 (+73 pts) ✅ Good
Admin:  https://the-wool-house.myshopify.com/admin/products/7823456789
```

---

## Example 4 — Bulk fix top 10

**User:** "fix top 10"

**Agent:**
```
✏️ Bulk fixes ready — 10 products

Products to be updated:
  1. "Scarf"                           12 → 89 (+77 pts) ✅
  2. "Blue pot"                         18 → 84 (+66 pts) 🟡
  3. "Leather wallet brown"             19 → 92 (+73 pts) ✅
  4. "Set of 3 tea towels"              28 → 86 (+58 pts) ✅
  5. "Organic Cotton Throw Blanket"     31 → 81 (+50 pts) 🟡
  6. "Bamboo Board"                     34 → 88 (+54 pts) ✅
  7. "Glass cafetiere"                  38 → 85 (+47 pts) ✅
  8. "Silver necklace"                  39 → 79 (+40 pts) 🟡
  9. "Kids wooden toy"                  41 → 87 (+46 pts) ✅
  10. "Merino Hat - Grey"               44 → 90 (+46 pts) ✅

Estimated score improvement: store average 58 → 74/100 (+16 pts)

Apply all? YES / review each one first / skip
```

**User:** "yes"

**Agent:**
```
✅ Bulk fix complete — 10 products updated

Store average: 58/100 → 74/100 (+16 pts)

Updated:  10 ✅
Failed:    0

Run "re-audit" to rescore these products, or "full audit" to rescan the whole store.
```

---

## Example 5 — Targeted issue scan

**User:** "find products with no SEO meta description"

**Agent:**
```
🔍 Products with no SEO meta description — 61 found

Worst scoring first:
  1.  "Scarf"                      12/100  admin/products/78234...
  2.  "Blue pot"                    18/100  admin/products/78235...
  3.  "Leather wallet brown"        19/100  admin/products/78236...
  4.  "Set of 3 tea towels"         28/100  admin/products/78237...
  5.  "Organic Cotton Throw"        31/100  admin/products/78238...
  ...and 56 more

Reply "fix these" to generate and push meta descriptions for all 61.
Or "fix top 20" to start with the worst-scoring ones first.
```

---

## Example 6 — Export audit as CSV

**User:** "export"

**Agent:**
```
✅ Audit export ready

seo_audit_the-wool-house_12-Apr-2026.csv
84 products · saved to workspace

Columns: ID, Title, Score, Band, Title Score, Description Score,
Tags Score, Images Score, Meta Title Score, Meta Description Score,
Alt Text Score, US Spellings Found, Admin URL

File path: ~/.openclaw/workspace/seo_audit_the-wool-house_12-Apr-2026.csv
```

---

## Example 7 — Re-audit after fixes

**User:** "re-audit"

**Agent:**
```
📊 Re-audit — 10 products rescored

  "Slim Leather Bifold Wallet..."       19 → 92  +73 ✅
  "Merino Wool Scarf | Soft..."         12 → 89  +77 ✅
  "Ceramic Plant Pot | Matte..."        18 → 84  +66 🟡
  "Linen Tea Towel Set | Natural..."    28 → 86  +58 ✅
  "Organic Cotton Throw Blanket..."     31 → 81  +50 🟡
  "Bamboo Cutting Board | Small..."     34 → 88  +54 ✅
  "Glass Cafetiere 600ml..."            38 → 85  +47 ✅
  "Sterling Silver Bar Necklace..."     39 → 79  +40 🟡
  "Wooden Shape Sorter | Kids..."       41 → 87  +46 ✅
  "Merino Wool Hat | Charcoal Grey..."  44 → 90  +46 ✅

Store average: 58/100 → 74/100 (+16 pts) 🟡 Fair

9 of 10 products now scoring ✅ Good or 🟡 Fair.
Biggest remaining gap: 3 products still missing extra images (images score capped at 5/15).
```

---

## Example 8 — Product already scoring well

**User:** "audit the merino scarf"

**Agent:**
```
🔍 SEO audit — "Merino Wool Scarf | Soft Knit Winter Scarf | Navy & Green"
Score: 91/100 ✅ Good

Criterion breakdown:
  Title length (62 chars)            15/15  ✅
  Keyword in title                   10/10  ✅
  Description length (203 words)     15/15  ✅
  Keyword in description             10/10  ✅
  Tags (9 tags)                      10/10  ✅
  Images (3 images)                  15/15  ✅
  SEO meta title (52 chars)          10/10  ✅
  SEO meta description (138 chars)   10/10  ✅
  Image alt text                      4/5   🟡 1 of 3 images missing alt text
  UK English                          —     ✅ No US spellings
  ──────────────────────────────────────────
  Total                              91/100  ✅ Good

Only issue: 1 image is missing alt text.
Reply "fix it" to add the missing alt text (quick update — no content changes needed).
```

---

## Quality Benchmarks — Generated Content

When fixing products, always aim for this quality level:

| ✅ Good title | ❌ Bad title |
|-------------|------------|
| "Merino Wool Scarf \| Soft Knit Winter Scarf \| Navy & Green" (62 chars) | "Scarf" (5 chars) |
| "Slim Leather Bifold Wallet \| 6 Card Slots \| Brown, Black & Tan" (63 chars) | "Leather wallet brown" (20 chars) |
| "Bamboo Cutting Board \| Small, Medium & Large \| FSC Certified" (62 chars) | "Bamboo Board" (12 chars) |

| ✅ Good description opening | ❌ Bad description opening |
|--------------------------|--------------------------|
| "Wrap up in effortless warmth with this Merino wool scarf." | "This is a scarf made from Merino wool." |
| "Carry everything you need without the bulk." | "This product is a leather wallet." |
| "A clean, minimal plant pot that lets your greenery take centre stage." | "Introducing our new ceramic plant pot!" |

| ✅ Good tags | ❌ Bad tags |
|------------|-----------|
| merino-wool, wool-scarf, winter-accessories, unisex, navy, gift-ideas | scarf, blue, new |
| leather-wallet, bifold-wallet, mens-wallet, genuine-leather, gift-for-him | wallet, brown |

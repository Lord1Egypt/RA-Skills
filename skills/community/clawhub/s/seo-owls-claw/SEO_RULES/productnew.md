# SEO_RULES — Productnew (v0.9)

**Primary Intent:** Transactional
**Word Count Target:** 400–600 words
**Schema Required:** `Product` + `Offer` + `BreadcrumbList` — see `SEO_CHECKS/schema-markup.md`
Section 3 (Productnew) and Section 8 (BreadcrumbList). Add `FAQPage` (Section 7) if the page
includes a visible FAQ section.

---

## Do's

- **Title tag**: brand + product name + key feature ("EcoFriendly Water Bottle | Sustainable")
- **Meta description**: benefit-driven ("Lifetime warranty, leak-proof design for your adventures")
- **H1 tag**: descriptive title + keyword ("Brand Name Water Bottle: Sustainable Hiking Gear")
- **Technical specs**: `<dl>`/`<dt>`/`<dd>` elements with unit measurements
- **Comparison table**: new version vs. previous model or competitor
- **AggregateRating schema**: star ratings with rating count, only if real reviews exist
- **Internal links**: related products + FAQ/tech-support pages (H6 footer)

## Don'ts

- Do not use generic "Buy Now" titles
- Do not repeat product features in H2–H3 tags (keyword stuffing)
- Do not omit the condition field — new products need `NewCondition` in schema, stated explicitly
- Do not ship without a warranty/guarantee section — trust signal required for conversion
- Do not bury technical details in image-only alt text

## Required Elements

1. `<title>` contains primary keyword
2. `<title>` is 50–60 characters
3. `<meta name="description">` present and 140–155 chars
4. Meta description contains primary keyword naturally
5. H1 present, unique on page, contains primary keyword
6. H1 is 40–70 characters
7. Price visible above the fold
8. `Product` schema block present with all required fields
9. `Offer` schema nested in `Product` with `price`, `priceCurrency`, `availability`
10. `BreadcrumbList` schema block present
11. `url`, `@context`, `@type` present in every schema block
12. At least one CTA phrase present (`{CTA_BUY_NOW}` or `{CTA_ADD_TO_CART}`)
13. `<link rel="canonical">` present and matches the page URL
14. At least one internal link to a related category or collection page

## Recommended Elements

15. `AggregateRating` schema present, only if real reviews exist
16. At least 3 product specification bullet points
17. `og:title`, `og:description`, `og:image` present
18. `og:image` is at least 1200×630px
19. Product images have descriptive alt text containing the keyword
20. At least 1 trust signal present (warranty, returns, secure payment note)
21. `FAQPage` schema if a visible FAQ section exists
22. Word count 400–600w (excluding navigation/footer)
23. At least 2 H2 tags present

## Keyword Placement Rules

```
Primary keyword must appear in:
  ✅ <title>
  ✅ H1
  ✅ Meta description
  ✅ First 100 words of body content
  ✅ At least 1 H2
  ✅ Product name in schema (name field)
  ✅ URL slug

Primary keyword must NOT appear:
  ❌ More than once in <title>
  ❌ More than 3x in the first 200 words (keyword stuffing)
  ❌ In the same H2 more than once
```

---

*Migrated from `SEO_CHECKS/do-and-don-lists.md` §3 and `SEO_CHECKS/page-type-specific-checks.md`
§Productnew. Audit scoring (HARD FAIL/WARNING) and Common Failure Patterns stay in
`SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — Productnew writing rules*

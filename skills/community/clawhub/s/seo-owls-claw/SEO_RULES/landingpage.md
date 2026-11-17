# SEO_RULES — Landingpage (v0.9)

**Primary Intent:** Transactional / Navigational
**Word Count Target:** 900–1,200 words
**Schema Required:** `Offer` or `Event` + `BreadcrumbList` — see `SEO_CHECKS/schema-markup.md`
Section 6 (Event + Offer) and Section 8 (BreadcrumbList). Add `FAQPage` (Section 7) if the page
includes a visible FAQ section.

---

## Do's

- **Title tag**: include primary keyword + urgency signal ("20% off Sale", "Limited Offer")
- **Meta description**: 140–155 chars, includes primary keyword + a CTA phrase ("Shop now!")
- **H1 tag**: descriptive + keyword-focused, contains the offer or campaign headline ("Exclusive Summer Sale: Electronics Discount")
- **Scarcity language**: include "limited", "only X left", "starting today" phrases
- **CTA button**: high contrast, visible above the fold, text "Shop Now" or "Get Deal"
- **Social proof**: testimonials + ratings section (H4/H5 headers)
- **Internal links**: footer H6 links to FAQ + related product/category pages

## Don'ts

- Do not exceed 60 chars in the title tag (truncation hurts CTR)
- Do not repeat keywords in H2–H3 tags (keyword stuffing)
- Do not go under 900 words — thin content hurts conversion-focused pages
- Do not omit JSON-LD `Event`/`Offer` markup — no rich snippets without it
- Do not bury the CTA below the fold — visibility drives conversions
- Never promise specifics in the meta/title that the page doesn't deliver
- Offer schema `validThrough` must never be a past date

## Required Elements

1. `<title>` contains primary keyword + offer signal
2. `<title>` is 50–60 characters
3. `<meta name="description">` present, 140–155 chars
4. H1 present, unique, contains the offer or campaign headline
5. At least one `Offer` or `Event` schema block present
6. `BreadcrumbList` schema present
7. Offer `validThrough` date present in schema if the offer is time-limited
8. Primary CTA visible above the fold
9. `<link rel="canonical">` present
10. At least one internal link to a product or category page

## Recommended Elements

11. Countdown timer or deadline visible if the offer is time-limited
12. Social proof element present (review count, sold count, testimonial)
13. `og:title`, `og:description`, `og:image` present
14. Secondary CTA at page bottom mirrors the primary CTA
15. `FAQPage` schema if a visible FAQ section exists
16. Word count 900–1,200w
17. Trust block present (returns, guarantee, security)

## Keyword Placement Rules

```
Primary keyword must appear in:
  ✅ <title>
  ✅ H1
  ✅ Meta description
  ✅ First 100 words
  ✅ URL slug

Campaign / Offer keyword rules:
  ✅ Offer modifier in <title> (e.g. "sale", "deal", "-20%", "limited time")
  ✅ Offer modifier visible in H1 or sub-headline
  ❌ Never promise specifics in meta/title that the page doesn't deliver
  ❌ Offer schema validThrough must not be a past date
```

---

*Migrated from `SEO_CHECKS/do-and-don-lists.md` §1 and `SEO_CHECKS/page-type-specific-checks.md`
§Landingpage. Audit scoring (HARD FAIL/WARNING) and Common Failure Patterns stay in
`SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — Landingpage writing rules*

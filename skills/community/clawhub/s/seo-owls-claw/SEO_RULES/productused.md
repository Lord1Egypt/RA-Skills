# SEO_RULES — Productused (v0.9)

**Primary Intent:** Transactional
**Word Count Target:** 500–700 words
**Schema Required:** `Product` + `Offer` (with `itemCondition`) + `BreadcrumbList` — see
`SEO_CHECKS/schema-markup.md` Section 4 (Productused) and Section 8 (BreadcrumbList). Add
`FAQPage` (Section 7) if the page includes a visible FAQ section.

---

## Do's

- **Title tag**: brand + product name + "Used/Refurbished" keyword ("EcoWater Bottle | Used Condition")
- **Meta description**: value proposition vs. new pricing ("Save 30% on tested refurbished items")
- **H1 tag**: descriptive title with condition clarity ("Brand Name Water Bottle — Certified Refurbished")
- **Condition report**: detailed H3/H4 sections (cosmetic wear, functionality test)
- **Inspection bullets**: list of functional/structural tests performed
- **Warranty/guarantee section**: return policy + 30-day guarantee bullet points
- **Schema markup**: `itemCondition` field set correctly in the JSON-LD

## Don'ts

- Do not use "Brand New" language for used products — trust violation
- Do not repeat "used/second-hand" excessively (keyword stuffing)
- Do not omit condition disclosure — no transparency means no trust signal
- Do not skip the value proposition — savings vs. new pricing must be explicit
- Do not hide functionality-test results in body text only

## Required Elements

1. `<title>` contains primary keyword + condition signal
2. `<title>` is 50–60 characters
3. `<meta name="description">` present, 140–155 chars
4. Meta description mentions the condition level
5. H1 present, unique, contains product name + condition
6. Condition level explicitly stated in body copy, not just schema
7. Price visible above the fold
8. `Product` schema present with `name`, `description`, `image`, `brand`, `sku`
9. `Offer` schema with `itemCondition` set to the correct schema.org value
10. `itemCondition` must be one of: `UsedCondition`, `RefurbishedCondition`, `DamagedCondition`
11. `BreadcrumbList` schema present
12. At least one CTA present
13. `<link rel="canonical">` present
14. At least one internal link to the parent category

## Recommended Elements

15. Condition grading scale explained or linked (e.g. what "EX+" means)
16. Serial number or item identifier visible
17. What's included in the sale listed (box, accessories, manual)
18. Return policy or guarantee mentioned
19. `FAQPage` schema if a visible FAQ section exists
20. Product images show the actual item, not a stock photo
21. Image alt text describes the actual condition visible in the photo
22. Word count 500–700w
23. `AggregateRating` only if there are real reviews for this specific item — never fake or approximate

## Keyword Placement Rules

```
Primary keyword must appear in:
  ✅ <title> (with condition modifier e.g. "used", "gebraucht", "occasion")
  ✅ H1 (product name + condition)
  ✅ Meta description (condition + price hint)
  ✅ First 100 words
  ✅ At least 1 H2
  ✅ schema name field
  ✅ URL slug

Condition keyword rules:
  ✅ Condition level (EX+, Very Good, Good etc.) in H1 or sub-headline
  ✅ Condition level in schema itemCondition field
  ❌ Never claim "new" or "mint" in schema if the item is used
  ❌ Never use NewCondition schema value for a used item
```

---

*Migrated from `SEO_CHECKS/do-and-don-lists.md` §4 and `SEO_CHECKS/page-type-specific-checks.md`
§Productused. Audit scoring (HARD FAIL/WARNING) and Common Failure Patterns stay in
`SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — Productused writing rules*

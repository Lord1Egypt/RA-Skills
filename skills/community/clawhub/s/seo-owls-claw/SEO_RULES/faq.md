# SEO_RULES — FAQ (v0.9)

**Primary Intent:** Informational
**Word Count Target:** 800–1,200 words
**Schema Required:** `FAQPage` + `BreadcrumbList` — see `SEO_CHECKS/schema-markup.md` Section 7
(FAQPage) and Section 8 (BreadcrumbList).

**Note:** unlike the other page types, `do-and-don-lists.md` never had a dedicated FAQ section —
the Do's/Don'ts below are derived from the Required/Recommended Elements and Schema Validation
Rules that already existed in `page-type-specific-checks.md`.

---

## Do's

- **Title tag**: primary keyword + FAQ signal, matches question-based searches
- **5+ Q&A pairs** minimum in schema — Google's minimum for the FAQ rich result
- **8–15 Q&A pairs** total (schema + visible) for stronger PAA capture
- Write questions as natural language, the way people actually ask, not keyword phrases
- Each visible answer at least 40 words
- Schema answers match visible on-page answers **exactly**
- Link answers to relevant product/category pages where applicable

## Don'ts

- Do not let schema answer text differ from the visible page answer — Google removes the rich result within days if it does
- Do not phrase questions as keyword phrases instead of natural language — breaks PAA matching
- Do not ship an FAQ page with zero internal links — informational dead end, no conversion path
- Do not go under 5 Q&A pairs — below Google's minimum for the FAQ rich result
- Do not stack more than one `FAQPage` schema block on the same page

## Required Elements

1. `<title>` contains primary keyword + FAQ signal
2. `<meta name="description">` present, 140–155 chars
3. H1 present, contains primary keyword
4. `FAQPage` schema block present
5. At least 5 `Question` + `Answer` pairs in schema
6. Schema answers match visible on-page answers exactly
7. `BreadcrumbList` schema present
8. Each visible answer is at least 40 words
9. `<link rel="canonical">` present
10. Primary keyword appears in at least 2 question texts

## Recommended Elements

11. 8–15 Q&A pairs total (schema + visible)
12. Answers link to relevant product or category pages
13. Questions written as natural language, not keyword phrases
14. Word count 800–1,200w
15. Questions cover different aspects of the topic
16. At least 1 answer references a specific product with a link

## Schema Validation Rules

```
FAQPage schema requirements:
  ✅ @context: "https://schema.org"
  ✅ @type: "FAQPage"
  ✅ mainEntity: array of Question objects
  ✅ Each Question has @type: "Question", name (the question text), acceptedAnswer
  ✅ acceptedAnswer has @type: "Answer" and text field
  ✅ Question text in schema EXACTLY matches visible H3 or question heading on page
  ✅ Answer text in schema EXACTLY matches or is a subset of visible answer text

  ❌ Schema answer text differs from visible page answer
  ❌ Questions in schema not present on visible page
  ❌ Answer text under 40 words in schema
  ❌ More than 1 FAQPage schema block on the same page
```

---

*Migrated from `SEO_CHECKS/page-type-specific-checks.md` §FAQ. Audit scoring (HARD FAIL/WARNING)
and Common Failure Patterns stay in `SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — FAQ writing rules*

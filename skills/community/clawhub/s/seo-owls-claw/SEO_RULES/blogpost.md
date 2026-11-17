# SEO_RULES — Blogpost (v0.9)

**Primary Intent:** Informational
**Word Count Target:** 1,500+ words
**Schema Required:** `Article` + `BreadcrumbList` — see `SEO_CHECKS/schema-markup.md` Section 5
(Article) and Section 8 (BreadcrumbList). Add `FAQPage` (Section 7) if the page includes a
visible FAQ section.

---

## Do's

- **Title tag**: question or "How to" format + primary keyword
- **Meta description**: answer user intent within the first 25 words
- **H1 tag**: single descriptive title (no numbers unless the article is a listicle)
- **Subheadings**: H2 main sections, H3 subsections, H4 examples/steps
- **Word count**: 1,500+ words for competitive queries
- **Internal linking**: related-articles section with anchor-text links (H6 footer)
- **Schema markup**: `Article` schema + `author` + `datePublished`

## Don'ts

- Do not include a year in the title unless the query specifically mentions it
- Do not exceed 2% keyword density in body text
- Do not ship images without descriptive alt text (accessibility violation)
- Do not go under 300 words — fails Google's minimum threshold
- Do not skip a table of contents on posts over 2,000w — hurts navigation and dwell time

## Required Elements

1. `<title>` contains primary keyword
2. `<title>` is 50–60 characters
3. `<meta name="description">` present, 140–155 chars
4. H1 present, unique, contains primary keyword
5. At least 4 H2 tags
6. `Article` schema block present with `headline`, `author`, `datePublished`
7. `BreadcrumbList` schema present
8. `author` field in `Article` schema matches a real author name
9. `datePublished` is a valid ISO 8601 date
10. At least 2 internal links to related pages or products
11. `<link rel="canonical">` present
12. Word count minimum 1,500w

## Recommended Elements

13. `dateModified` in `Article` schema
14. `FAQPage` schema if a visible FAQ section exists
15. At least 1 external link to an authoritative source
16. Author bio section or link to an author page
17. Table of contents for posts over 2,000w
18. Primary keyword appears naturally in at least 2 H2 tags
19. Images have descriptive alt text
20. `og:title`, `og:description`, `og:image` present
21. Estimated reading time shown
22. Related-articles / internal-link block at the end of the post

## Keyword Placement Rules

```
Primary keyword must appear in:
  ✅ <title>
  ✅ H1
  ✅ Meta description
  ✅ First 100 words
  ✅ At least 2 different H2 tags (naturally, not forced)
  ✅ Article schema headline field
  ✅ URL slug

Keyword density target:
  ✅ Primary keyword: 0.5%–1.5% of total word count
  ❌ Over 2% = keyword stuffing risk
  ❌ Under 0.3% = under-optimised

Secondary keyword rules:
  ✅ Secondary keyword in at least 1 H2
  ✅ Secondary keyword in body copy at least 3x
  ❌ Never in <title> at the expense of the primary keyword
```

## E-E-A-T Checklist (Blogpost-Specific)

```
Experience signals:
  ✅ First-person observations or examples where appropriate
  ✅ Specific data, measurements, or test results cited

Expertise signals:
  ✅ Author name visible
  ✅ Technical terminology used correctly
  ✅ Depth — covers the topic beyond surface level

Authoritativeness:
  ✅ At least 1 outbound link to a recognised authority source
  ✅ Dates are accurate and current

Trust:
  ✅ No factual errors detectable
  ✅ Sources cited where claims are made
  ✅ No thin filler sections (every H2 section minimum 150w)
```

---

*Migrated from `SEO_CHECKS/do-and-don-lists.md` §2 and `SEO_CHECKS/page-type-specific-checks.md`
§Blogpost. Audit scoring (HARD FAIL/WARNING) and Common Failure Patterns stay in
`SEO_CHECKS/page-type-specific-checks.md`.*

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — Blogpost writing rules*

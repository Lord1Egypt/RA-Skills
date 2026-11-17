# SEOwlsClaw — Page-Type Specific Checks (v0.9.2)

**Purpose:** Detailed SEO audit rules for each individual page type.
**When loaded:** Step 6 of the brain workflow — runs after content generation, before final output.
**Also used by:** `checks <type>` command in preview mode and `checks <url>` audit mode.

> This file works alongside `seo-checks-reference.md` (universal audit mechanics) and
> `SEO_RULES/<type>.md` (the rule values themselves — required elements, recommended elements,
> keyword placement, do's/don'ts). This file owns **audit scoring only**: HARD FAIL/WARNING
> classification, pass-rate thresholds, and per-type failure patterns.

---

## How Checks Are Scored

Each check is either:
- 🔴 **HARD FAIL** — blocks output until resolved. Agent must fix before delivering.
- 🟡 **WARNING** — reported to user with suggested fix, does not block output.
- 🟢 **PASS** — no action needed.

At the end of each page type audit, the agent outputs a **Pass Rate** and a **Priority Fix List** (HARD FAILs first, then WARNINGs ranked by SEO impact).

---

## Page Type Index

| Page Type | Primary Intent | Schema Required | Min Words |
|-----------|---------------|-----------------|-----------|
| `Productnew` | Transactional | Product + Offer + BreadcrumbList | 400w |
| `Productused` | Transactional | Product + Offer + ItemCondition + BreadcrumbList | 500w |
| `Blogpost` | Informational | Article + BreadcrumbList | 1,500w |
| `Landingpage` | Transactional / Navigational | Offer or Event + BreadcrumbList | 900w |
| `FAQ` | Informational | FAQPage + BreadcrumbList | 800w |
| `Socialphoto` | Navigational | ImageObject | 100w |
| `Socialvideo` | Navigational | VideoObject | 150w |

---

## Productnew — New Product Page

**Intent:** Transactional — user is ready to buy. Zero tolerance for missing trust signals.

### Rule Values

All required elements, recommended elements, and keyword placement rules for Productnew are
defined in `SEO_RULES/productnew.md` — load it alongside this file's scoring logic below.

### Common Failure Patterns

- ❌ Price not visible — hidden behind a tab or accordion
- ❌ `Offer` schema missing `availability` field → no rich result
- ❌ H1 is the brand name only — no product model or keyword
- ❌ CTA is an image with no alt text — invisible to screen readers and crawlers
- ❌ No internal links — product is an SEO orphan

---

## Productused — Used / Refurbished Product Page

**Intent:** Transactional — user is comparing condition + price before buying.
Condition transparency is a trust and SEO requirement, not optional.

### Rule Values

All required elements, recommended elements, and keyword placement rules for Productused are
defined in `SEO_RULES/productused.md` — load it alongside this file's scoring logic below.

### Common Failure Patterns

- ❌ `itemCondition` set to `NewCondition` for a used item → Google penalty risk
- ❌ Condition mentioned only in schema, not in visible copy — Google distrusts hidden data
- ❌ Serial number missing — duplicate listing risk across multiple used items
- ❌ Stock photo used instead of actual item photo
- ❌ No return policy mentioned → low conversion on used goods

---

## Blogpost — Organic SEO Article / Guide

**Intent:** Informational — user wants to learn, not buy (yet).
E-E-A-T signals are the primary ranking factor here.

### Rule Values

All required elements, recommended elements, keyword placement rules, and the E-E-A-T checklist
for Blogpost are defined in `SEO_RULES/blogpost.md` — load it alongside this file's scoring
logic below.

### Common Failure Patterns

- ❌ Article under 1,500w — almost never competitive for informational queries
- ❌ Author field in schema is blank or set to the website name — not a person
- ❌ No FAQ section for informational posts — missed PAA opportunity
- ❌ Zero external links — looks self-referential, hurts E-E-A-T
- ❌ H2 tags are not questions or keyword-rich — wasted heading hierarchy

---

## Landingpage — Sales Campaign / Promotion Page

**Intent:** Transactional or Navigational — user responds to a campaign, offer, or CTA.
Conversion rate and urgency are primary goals alongside ranking.

### Rule Values

All required elements, recommended elements, and keyword placement rules for Landingpage are
defined in `SEO_RULES/landingpage.md` — load it alongside this file's scoring logic below.

### Common Failure Patterns

- ❌ `validThrough` date already expired in schema — Google demotes stale offers
- ❌ CTA is below the fold — users bounce before converting
- ❌ No urgency signal for a time-limited offer — missed conversion
- ❌ Landing page not indexed (noindex tag left on from testing) — never ranks

---

## FAQ — Standalone FAQ Page

**Intent:** Informational — targets People Also Ask boxes and zero-click snippets.
Answer quality and schema completeness determine rich result eligibility.

### Rule Values

All required elements, recommended elements, and schema validation rules for FAQ are defined in
`SEO_RULES/faq.md` — load it alongside this file's scoring logic below.

### Common Failure Patterns

- ❌ Schema answers do not match visible text — Google removes rich result within days
- ❌ Questions are keyword phrases, not natural language — no PAA match
- ❌ FAQ page has no internal links — informational dead end, no conversion path
- ❌ Under 5 Q&A pairs — below Google's minimum for FAQ rich result display

---

## Socialphoto — Image / Photo Post

**Intent:** Navigational / Brand — drives engagement and brand visibility.
Alt text and caption quality are the primary SEO signals.

### Rule Values

Required and recommended elements for Socialphoto are defined in `SEO_RULES/socialphoto.md` —
load it alongside this file's scoring logic below.

---

## Socialvideo — Video Post / Metadata

**Intent:** Navigational / Commercial — drives views, subscribers, and brand awareness.
Title and description are the primary ranking signals on both YouTube and Google.

### Rule Values

Required and recommended elements for Socialvideo are defined in `SEO_RULES/socialvideo.md` —
load it alongside this file's scoring logic below.

---

## Audit Output Format

After running checks for any page type, the agent outputs:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PAGE TYPE AUDIT — [PageType] — [Keyword]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hard Fails:     [n] — BLOCKS OUTPUT
Warnings:       [n]
Passed:         [n] / [total checks]
Pass Rate:      [%]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 HARD FAILS (fix before output)
  #[n] — [Check description] → [How to fix]

🟡 WARNINGS (fix recommended)
  #[n] — [Check description] → [Suggested fix]

🟢 ALL OTHER CHECKS PASSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Pass Rate thresholds:
- **90–100%** — Output approved ✅
- **75–89%** — Output approved with warnings ⚠️
- **Below 75%** — Output blocked until HARD FAILs resolved 🔴

---

*Last updated: 24-08-2026 (v0.9.2)*
*Adds: trimmed to audit scoring only (HARD FAIL/WARNING, pass rates, failure patterns) — required
elements, recommended elements, and keyword placement per type now live in SEO_RULES/<type>.md*
*Maintainer: Chris — SEOwlsClaw page-type-specific SEO audit checks*

# SEO_RULES — Universal (v0.9)

**Applies to:** every page type, every `write`/`writehtml` call.
**Loaded:** Step 2f of `BRAIN_ARCHITECTURE.md`, before Step 3 (Generate Variables).
**Audited by:** `SEO_CHECKS/seo-checks-reference.md` at Step 6, and
`SEO_CHECKS/seo-output-quality-checklist.md` at Step 6.5 — both reference this file instead of
restating its values.

---

## E-E-A-T Signals

| Signal | What to Include |
|--------|-----------------|
| **Expertise** | Author credentials + domain authority in the niche |
| **Experience** | Personal stories, real examples, hands-on testing (specific numbers, timestamps, locations) |
| **Authoritativeness** | 2+ references to reputable domains, citations, or backlinks |
| **Trustworthiness** | Accurate, sourced facts; no misleading or unverifiable claims |

## On-Page SEO Requirements

| Rule | Standard | Page Type Notes |
|------|----------|------------------|
| **Title Tag Length** | 50–60 characters max | Blog: keyword early. Products: brand first. |
| **Meta Description** | 140–155 characters max, includes primary keyword + a CTA phrase | All types |
| **H1 Tag** | Exactly one `<h1>` per page, descriptive, contains the primary keyword | Products: `{Brand} + Product + Keyword`. Blogs: `How to.../Why...` |
| **Heading Structure** | H2 for main sections, H3/H4 for subsections; max 6–8 H2 tags; never skip a level (H2→H4 invalid) | Informational: more depth. Transactional: less clutter. |
| **Internal Linking** | 2–3 relevant internal links per page, descriptive anchor text | Products: FAQ/related pages. Blogs: related articles. |

## Common SEO Traps to Avoid

| Trap | Threshold | Fix |
|------|-----------|-----|
| **Keyword Stuffing** | Keep primary keyword density ≤ 2%; vary wording naturally | Rewrite repeated phrases into natural sentences |
| **Thin Content** | Below the page type's minimum word count | Expand with subsections, examples, FAQs — never pad with filler |
| **Duplicate Content** | Same content across multiple URLs | Unique meta data + phrasing per page, canonical tags |
| **Broken Links** | Any internal/external link returning a non-200 status | Test every H6 footer link + body link before output |
| **Missing Schema** | No JSON-LD for the page type | Always inject the schema required for that page type — see `SEO_RULES/<type>.md` |

## FAQ Section Requirements

- Include an FAQ block (`H2: "Frequently Asked Questions"`) on informational/commercial pages where user questions are anticipated.
- Anticipate 2–3 People Also Ask style follow-up questions on long-form content.
- Any page with a visible FAQ section needs `FAQPage` JSON-LD (see `SEO_CHECKS/schema-markup.md` Section 7) — schema answers must match the visible on-page answers exactly.

## Quality Over Quantity Principles

- **Depth > Breadth**: one comprehensive page beats ten shallow ones — meet the page type's minimum word count by covering the topic fully, not by padding.
- **Value-First Content**: answer the user's actual question in the first 10% of the content, then expand.
- **No Fluff Sections**: every H2/H3 needs ≥50 words of substantive content beneath it, or it shouldn't be a heading.
- **User Intent Match**: content structure should mirror the SERP features detected in Step 0 (comparison tables, FAQs, etc. — whatever is actually ranking).

## Natural Language Integration

| Rule | Standard |
|------|----------|
| **Second-Person Voice** | Address the reader directly ("you'll see", "your camera") — ≥70% direct-address phrasing in intro + conclusion |
| **Active Voice** | >80% active voice in body content ("The camera captures light," not "Light is captured by the camera") |
| **Sentence Variety** | Mix short and long sentences — avoid runs of same-length sentences |

**AI Writing Pattern Check** (em dash overuse, stock AI transitions like "no code needed", rule-of-three padding): full rule + Pass/Fail Logic defined in `SEO_CHECKS/seo-output-quality-checklist.md` Category 6 — not duplicated here to avoid a third copy of the same rule.

---

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — universal SEO writing rules, consulted at Step 2f before generation*

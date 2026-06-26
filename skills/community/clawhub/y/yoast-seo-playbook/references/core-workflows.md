# Core Yoast Workflows

## 1) Page/Post Optimization (default)

Inputs:
- URL or post slug
- Target query / search intent
- Audience + language
- Tier status (Free/Premium/Unknown)

Steps:
1. Verify intent: informational / commercial / transactional / navigational.
2. Draft SEO title (clear + specific; avoid clickbait).
3. Draft meta description (benefit + specificity + natural CTA).
4. Validate heading structure (single H1; logical H2/H3).
5. Improve intro and section clarity for readability.
6. Add/confirm relevant internal links.
7. Mark publish recommendation only after QA checklist pass.

Output format (recommended):
- Proposed SEO title
- Proposed meta description
- H1/H2 structure notes
- Internal linking notes
- Tier assumptions + next action

## 2) Sitewide Hygiene Pass

Use for batches or recurring maintenance:
- Duplicate/weak title patterns
- Missing/weak meta descriptions
- Thin or overlapping pages
- Broken internal links (if surfaced)
- Sitemap/indexability sanity checks

Prioritize:
1. High-value pages (home, service, pricing, core landing pages)
2. Cannibalization risk pages
3. Legacy pages with traffic potential

## 3) Schema/Metadata Validation (Yoast-aware)

- Confirm Yoast-generated metadata exists for URL.
- Verify title/description/canonical/robots are coherent.
- Confirm schema output is plausible for page type.
- If data stale or missing on an existing page:
  - Recommend update in WP admin and/or Yoast optimization routines.

## 4) Premium Branch (only when confirmed)

Use Premium utilities to accelerate, not replace fundamentals:
- Redirect manager for URL change hygiene
- Internal linking suggestions for faster editorial passes
- Multiple keyphrases where content truly covers additional intents
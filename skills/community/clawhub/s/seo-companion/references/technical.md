# Technical SEO Reference

Use this file for crawlability, indexability, rendering, metadata integrity, and site-health diagnosis.

## Audit sequence

1. Response status / final URL
2. Indexability directives
3. Canonical
4. robots.txt
5. Sitemap presence
6. Renderability / JS dependence
7. Structured data
8. Internal architecture
9. Performance signals

## Response and indexability

Check:
- final status code
- redirects
- `meta robots`
- `X-Robots-Tag`
- canonical target

### Flag as critical
- `noindex` on pages meant to rank
- canonical pointing elsewhere unintentionally
- blocked by robots when page assets/content need crawling
- broken/looping redirects

## Robots.txt

### What matters
- file exists
- does not block important content or rendering assets
- suspicious blanket disallows are investigated

Do not overstate robots.txt issues when the page can still be indexed through other means; explain the actual risk.

## XML sitemaps

Check:
- sitemap endpoint exists
- likely canonical/indexable URLs appear in sitemap set
- obvious junk/private URLs are not being surfaced

Sitemaps help discovery, but they do not replace internal linking.

## Renderability

Escalate to rendered inspection when:
- the fetched HTML lacks key content
- headings/content are injected late by JS
- metadata differs between raw HTML and rendered DOM
- page relies on heavy client-side rendering

## Structured data

Look for:
- JSON-LD presence
- relevant schema types
- absence on pages where it would be expected

Do not claim schema absence is catastrophic unless the page materially depends on rich-result eligibility.

## Redirects and canonicals

### Good practice
- use 301 for permanent moves
- redirect old URLs to the closest relevant page
- avoid chains where practical
- align canonical and final indexable URL

### Flag
- chains
- loops
- 302s left in place long-term without reason
- canonical / redirect mismatch

## Performance

Treat performance as a ranking and UX factor, not the sole explanation for poor rankings.

### High-value issues to mention
- oversized images
- render-blocking assets
- excessive unused JS/CSS
- poor mobile performance

### Tone guidance
- Avoid pretending a PageSpeed number alone determines SEO success.
- Emphasize that severe performance issues can depress UX, crawling efficiency, and conversions.

## Technical audit output

Structure findings as:
- Critical blockers
- Crawl / index issues
- Canonical / redirect issues
- Rendering issues
- Structured data issues
- Performance concerns
- Next steps

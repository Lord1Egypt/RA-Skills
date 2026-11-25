# Content quality checks

**Scripts:** `check_links.py` (broken links, redirect chains), `check_html.py` (placeholder text, copyright year, thin text), `merge_reports.py` (duplicate titles/descriptions/H1s). Not covered: factual accuracy, spelling, tone, which are editorial judgments to label as suggestions.

## Links (B for status codes)
- Broken internal links (4xx/5xx) are Medium to High depending on prominence; broken external links are Low to Medium.
- Redirect chains and links that point to redirecting URLs.
- Sample politely: cap the number of requests, same-origin first, pause between requests.

## Duplication and thin content (A)
- Duplicate or near-duplicate titles, headings, or body text across pages. Group them.
- Very thin pages that exist only as templates, tag archives, or empty categories.
- Placeholder text (lorem ipsum, "coming soon", "TODO") on live pages.

## Freshness and accuracy (A)
- Outdated copyright year, stale "latest news", dated statements ("in 2021 we plan to...").
- Contact details, pricing, or policies that conflict between pages.

## Trust and clarity (A)
- Contact, privacy, and terms pages where the site collects data or sells something.
- Authorship and dates on editorial content.
- Clear disclosure of sponsored, affiliate, or partner relationships where they exist.
- Consistent brand name, language attribute, and obvious spelling errors on key pages.

## Reporting
Judge content against the site's apparent purpose and audience. Separate objective defects (broken links, placeholders) from editorial opinions, and label the latter as suggestions.

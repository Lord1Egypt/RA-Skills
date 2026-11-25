---
name: rankizz-audit-on-page-seo
description: Audit one or more web pages for technical and on-page SEO, including status and indexability, title and description, canonical URL, robots directives, headings, content intent, crawlable links, images and alt text, Open Graph and social metadata, hreflang, structured data, mobile usability, and page experience. Use when a user asks for an on-page SEO check, metadata audit, page QA before publishing, template review, or prioritized fixes for specific URLs or source files. Works with local and web resources; Rankizz is optional.
---

# Audit on-page SEO

Audit the rendered page, not a checklist-shaped guess. Separate observed evidence, inferred risk, and recommendations. Never promise rankings.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Resolve the scope

Collect:

- page URL or source/template path
- page type and intended action
- primary audience, locale, and search intent
- target query or topic, if one exists
- whether the page should be indexed
- project-specific SEO rules

If the repository contains an SEO checklist, read it first and treat its thresholds as controlling. Otherwise use the review heuristics below, clearly labeled as heuristics rather than Google requirements.

For a public server-rendered URL, run:

```sh
python3 scripts/inspect_on_page.py "https://example.com/page"
```

The script inspects response HTML. Use a browser or the project's rendering tools when JavaScript changes the head, headings, links, or main content. Read [references/on-page-standards.md](references/on-page-standards.md) before grading hreflang, images, structured data, or indexing controls.

Rankizz is not required. If a Rankizz project is already connected, optional first-party evidence such as `get_site_explorer_page`, Search Console performance, or analytics may help prioritize a page. Do not create a project or spend credits merely to run the checklist.

## Run the audit in order

### 1. Confirm the served URL and index state

Record the requested URL, redirect chain, final URL, HTTP status, content type, and whether the main content appears in the initial or rendered HTML.

Check:

- `200` for an indexable page
- HTTPS and one consistent host/path form
- robots meta and `X-Robots-Tag`
- robots.txt crawl access
- sitemap inclusion only for canonical indexable URLs
- no login, consent wall, soft 404, crawler-specific response, or accidental `noindex`
- one final URL without redirect loops or chains

Do not equate robots.txt blocking with deindexing. A crawler must fetch a page to see a `noindex` directive.

### 2. Review title, description, and headings

Check one descriptive `<title>`, one page-specific meta description, and one clear visible H1. Confirm that the title, H1, visible hero, and intent agree without repeating mechanically.

Use project thresholds when present. For a project without thresholds, flag 30 to 60 title characters and 70 to 160 description characters only as display/editorial heuristics. Google has no fixed character limit and may generate different title links or snippets.

Check:

- unique, complete copy without keyword stuffing or boilerplate
- no stale year, price, location, or product name
- headings in logical H1, H2, H3 order
- no heading level chosen only for visual size
- useful body copy that fulfills the promise above the fold
- one primary intent rather than several unrelated targets

### 3. Verify canonical and alternate versions

For an indexable standalone page, prefer one absolute canonical that resolves to the intended `200` URL. Confirm that internal links and the sitemap use the same URL form.

For localized variants:

- use separate crawlable URLs
- include every variant and the current page in each hreflang set
- use fully qualified URLs
- require reciprocal links between variants
- use valid language and optional region codes
- add `x-default` only when a genuine fallback exists
- keep each translated page self-canonical unless the content is an untranslated duplicate

Do not canonicalize all translated pages to one language or combine canonical and hreflang attributes in one link element.

### 4. Inspect images and media

For every meaningful image, record its source, purpose, alt behavior, dimensions, and loading strategy.

- Informative images need concise alt text that communicates their purpose in context.
- Decorative images need `alt=""`.
- Functional images need alt text that names the action or destination.
- Charts need a short alt summary plus the underlying data or long explanation nearby.
- Avoid stuffing keywords or writing "image of" when the element is already announced as an image.
- Use an `<img src>` fallback, descriptive filenames, responsive sources, and explicit width and height.
- Load likely LCP/hero images eagerly. Lazy-load below-the-fold images.

Check that the social image is relevant, crawlable, high resolution, not an extreme aspect ratio, and represented by an absolute HTTPS URL. Record `og:image:alt`, width, height, and MIME type when available.

### 5. Inspect social metadata

Open Graph is for link previews, not a direct ranking promise. Check:

- `og:title`
- `og:description`
- `og:url` matching the canonical
- `og:type`
- `og:image` and `og:image:alt`
- image width, height, type, and secure URL where useful
- Twitter/X card, title, description, and image when the site supports them

Keep social copy accurate to the visible page. Do not use a generic logo when a representative page image is available.

### 6. Inspect links and navigation

Confirm important links use crawlable `<a href>` elements and point directly to final URLs. Review anchor text, broken links, orphan risk, breadcrumbs, related pages, and navigation depth.

Use `rel="sponsored"` for paid or affiliate links and `rel="ugc"` for untrusted user-submitted links when applicable. Do not add `nofollow` to ordinary internal links as a substitute for sound architecture.

### 7. Inspect structured data

Use JSON-LD when practical, but only add a type that matches the visible main content and a supported search feature. Confirm required properties, canonical URLs, crawlable images, real authors, accurate ratings, and ISO 8601 dates with timezone where applicable.

Do not mark up hidden FAQs, invented reviews, copied ratings, unavailable prices, or navigation as page content. Structured data can make a page eligible for a feature; it does not guarantee one.

### 8. Review content quality and page experience

Check that the page provides original, useful information for its audience and shows who created or reviewed it when readers would expect that context. For commercial or review pages, require evidence, methodology, current facts, drawbacks, and disclosures.

Review mobile layout, keyboard access, intrusive overlays, HTTPS, and field Core Web Vitals when available. Use LCP at or below 2.5 seconds, INP below 200 milliseconds, and CLS below 0.1 as good-experience targets, not as guarantees of ranking.

## Prioritize findings

Use these levels:

- `Critical`: page cannot be reliably crawled, rendered, indexed, or resolves incorrectly
- `High`: wrong canonical, accidental noindex, missing/empty title, absent main content, broken hreflang cluster, or misleading structured data
- `Medium`: weak description, heading disorder, missing informative alt text, poor internal linking, incomplete social metadata, or avoidable image/performance risk
- `Low`: polish that improves consistency without blocking discovery or comprehension

Report passed checks too. A report containing only failures hides scope and makes regression review harder.

## Do and do not

| Do | Do not |
| --- | --- |
| Quote the observed value and its source | Claim a tag is missing without checking rendered HTML |
| Separate policy thresholds from search-engine requirements | Present a character count as a Google ranking rule |
| Explain the user and crawler impact of every fix | Label every imperfection "critical" |
| Verify canonical, sitemap, links, and redirects together | Review a canonical tag in isolation |
| Describe an image according to its purpose | Stuff the target keyword into every alt attribute |
| Mark decorative images with empty alt text | Treat every empty alt as an error |
| Validate only visible, truthful structured data | Invent FAQ, rating, author, or price markup |
| Say when browser rendering or field data is unavailable | Guess at JavaScript output or Core Web Vitals |

## Examples

### Good metadata and canonical

```html
<title>Technical SEO checklist for product pages</title>
<meta name="description" content="Check titles, canonicals, images, structured data, internal links, and indexability before publishing a product page.">
<link rel="canonical" href="https://example.com/guides/product-page-seo">
```

### Bad metadata

```html
<title>SEO | SEO Tips | Best SEO Guide | Example</title>
<meta name="description" content="Learn more...">
<link rel="canonical" href="/guides">
```

Why it fails: the title is stuffed and generic, the description is unfinished, and the canonical points to a broader page without evidence that this URL is a duplicate.

### Good image decisions

```html
<img src="checkout-funnel.webp" width="1200" height="675"
     alt="Checkout funnel showing a 38% drop between shipping and payment">
<img src="orange-dot.svg" alt="" width="24" height="24">
```

The chart communicates its finding. The orange dot is decorative and stays silent.

### Good hreflang set

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/pricing">
<link rel="alternate" hreflang="de" href="https://example.com/de/preise">
<link rel="alternate" hreflang="x-default" href="https://example.com/pricing">
```

Require the same set, including a self-reference, on every listed variant.

## Limitations

- One-page inspection cannot prove metadata uniqueness, orphan status, or hreflang reciprocity across a site.
- Response HTML cannot prove what a browser renders after JavaScript runs.
- Lab performance is not field Core Web Vitals.
- A correct implementation does not guarantee indexing, rich results, traffic, or rankings.
- Search engines may rewrite title links and snippets.
- Do not change production code unless the user asks for implementation.

## Output template

```markdown
# On-page SEO audit: [page]

## Executive summary
- Index state: [indexable / intentionally noindex / blocked / uncertain]
- Highest risk: [one sentence]
- Recommended order: [first three actions]

## Page evidence
| Check | Observed | Expected | Status | Evidence |
| --- | --- | --- | --- | --- |
| Final URL/status | | | | |
| Robots/indexing | | | | |
| Canonical | | | | |
| Title | | | | |
| Description | | | | |
| H1/outline | | | | |
| Images/alt | | | | |
| Open Graph/social | | | | |
| Hreflang | | | | |
| Structured data | | | | |
| Links | | | | |
| Mobile/page experience | | | | |

## Prioritized fixes
1. [Severity] [fix]
   - Evidence:
   - Impact:
   - Exact recommendation:
   - Owner:

## Passed checks
- [check and evidence]

## Unknowns and limitations
- [what could not be verified and how to verify it]
```

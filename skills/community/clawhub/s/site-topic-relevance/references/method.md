# Method, limits, and validation

This standalone Skill reuses the URL and DNS checks, crawler, scoring schema, excerpt selection, and report generation from DomainRank's Site Topic Relevance feature. The Node core, ECharts, and Motion assets are bundled. Node.js 22 or later is the only runtime dependency.

## Crawling

The crawler checks `robots.txt` first. It then reads the supplied sitemap or discovers sitemaps from `robots.txt` and `/sitemap.xml`. It visits up to eight sitemaps, collects up to 5,000 candidates, and samples across top-level paths in round-robin order. `--limit` defaults to 50 and accepts values from 3 to 50. Every candidate, including the homepage, must appear in a page-level sitemap `<loc>` entry.

The crawler matches robots rules using literal fragments, `*` wildcards, and the terminal `$` anchor. It prefers the most specific rule and favors `Allow` on ties. If matching exceeds the crawl's work allowance, the crawl stops and reports the reason.

The crawler checks that each redirect stays within the site and pins the HTTPS connection to a validated DNS address. It rejects IP literals, localhost, reserved internal domains, private or loopback addresses, other reserved addresses, and URLs containing credentials. It allows up to four redirects, a 10-second timeout and 2 MB response limit per request, and four concurrent fetches. Cloudflare's public DNS-over-HTTPS resolver receives the public hostname being resolved.

The crawler skips URLs with query strings, static assets, sign-in and admin paths, pages blocked by robots rules, pages marked `noindex`, pages canonicalized to a different URL, non-200 responses, and unreadable or duplicate content. A redirect's final URL must still be in the candidate set. The crawler checks the final content type and body before extraction to exclude images, PDF, JSON, and binary data. Each included page contributes 160–5,000 characters of normalized plain text.

Extraction uses heuristics on static HTML. Complex layouts, content late in the document, client-side rendering, and repeated templates can affect coverage. The report records skip reasons. If the homepage is excluded, qualify the inference about the site's primary purpose and explain what evidence is missing.

## Assessment input and output

Each page supplies `id`, `url`, `title`, optional `description`, `text`, and `excerpts`. The `lead`, `middle`, and `end` excerpts are taken from that page's extracted text and preserve internal punctuation and whitespace. Each excerpt is at most 220 UTF-16 code units. Short pages can have identical excerpts.

The script generates the assessment schema. This example shows the shape and uses illustrative IDs and content.

```json
{
  "purpose": "The site's primary audience and task",
  "summary": "The content structure observed in this sample",
  "topics": [{"id":"core","name":"Core topic","description":"The task these pages serve"}],
  "findings": [{"title":"Actionable finding","description":"An explanation grounded in page evidence","pageIds":["p0"]}],
  "pages": [{"id":"p0","topicId":"core","relevance":95,"reason":"Explain the score using the page content","evidence":"lead"}]
}
```

Use the supplied page IDs and the topics defined for the current assessment. Validation requires 1–6 topics, each input page exactly once, valid topic and page references, scores from 0 to 100, and a valid evidence selector. The script resolves that selector to an excerpt from the same page and checks for an exact substring match. Unknown selectors, substituted pages, and invented supporting page IDs fail validation.

## Chart and scores

The chart uses `distance = 1 - relevance / 100`, `radius = mean(distance)`, and `outside = distance > radius + 1e-9`. It scales the drawing proportionally to the largest distance in the sample. A topic's position and a stable hash of the page URL determine each point's angle for grouping. Match the sample, language versions, and assessment conditions when comparing reports.

ECharts renders the points and display modes. Motion mini animates the chart entrance and respects `prefers-reduced-motion`. Hover, touch, or keyboard selection updates a fixed evidence panel with the URL, fit score, rationale, and original excerpt. The panel remains available after the preview closes. Wide charts show topic names when space allows. Narrow or crowded charts use numbered labels keyed to the legend. Labels use the same collision avoidance algorithm as the web version while points retain their assessed radial distances.

## Sources and maintenance

- [Original DomainRank feature](https://domainrank.app/site-relevance)
- [ECharts events](https://echarts.apache.org/handbook/en/concepts/event/)
- [Motion animation](https://motion.dev/docs/animate)

Maintainers can run `scripts/skills/build-site-topic-relevance.mjs` in the source project to rebuild the packaged runtime and browser assets. Dependency licenses are included in `assets/`.

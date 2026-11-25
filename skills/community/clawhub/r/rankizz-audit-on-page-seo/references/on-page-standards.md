# On-page standards and research basis

Use these primary sources when a project has no stricter local policy. Recheck them when platform behavior or eligibility affects a recommendation.

## Search metadata and indexing

- Google title links: https://developers.google.com/search/docs/appearance/title-link
- Google snippets and meta descriptions: https://developers.google.com/search/docs/appearance/snippet
- Canonical URL methods: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Supported robots meta and HTTP rules: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Valid page metadata: https://developers.google.com/search/docs/crawling-indexing/valid-page-metadata
- Crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Qualifying sponsored and user-generated links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links

Google can choose title and snippet text from several page and link signals. Treat title and description character ranges as project display heuristics, not hard Google limits.

## International pages

- Localized versions and hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions
- Multi-regional and multilingual sites: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites

Every hreflang cluster must include self and reciprocal fully qualified URLs. Use `x-default` for a real fallback, not as decoration.

## Images and previews

- Google image SEO: https://developers.google.com/search/docs/appearance/google-images
- W3C image alternatives: https://www.w3.org/WAI/tutorials/images/
- Open Graph protocol: https://ogp.me/
- Browser image loading and dimensions: https://web.dev/articles/browser-level-image-lazy-loading

The image's purpose determines alt text. Social metadata supports link previews and can also inform title/image selection, but it is not a direct ranking guarantee.

## Structured data and experience

- General structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Core Web Vitals: https://developers.google.com/search/docs/appearance/core-web-vitals
- Intrusive interstitials: https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials

Structured data must describe visible, truthful content. Passing a syntax test creates eligibility, not a guaranteed search feature.

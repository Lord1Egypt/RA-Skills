# Structured data (JSON-LD) recipes

JSON-LD is the highest-leverage GEO move after being crawlable: it's how Google rich results **and** LLMs reliably extract entities and facts. Emit it as `<script type="application/ld+json">` (a non-executable data block — allowed under strict CSP `script-src 'self'`, no nonce needed).

## The nested `@graph` pattern (use this)
Ship **one** `<script type="application/ld+json">` per page containing a `@graph` array, rather than many separate blocks. Cross-link nodes with `@id` so machines see one connected entity graph. This is exactly what the reference site prod ships (verified: `Organization, WebSite, FAQPage, WebPage, Service, Product, SoftwareApplication…` in a single graph).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Example",
      "url": "https://www.example.com/",
      "logo": { "@type": "ImageObject", "url": "https://www.example.com/logo.png", "width": 200, "height": 200 },
      "image": "https://www.example.com/og-image.png",
      "description": "One-sentence what-you-do, entity-rich.",
      "sameAs": ["https://www.linkedin.com/company/example/", "https://x.com/example"],
      "knowsAbout": ["Topic A", "Topic B", "Topic C"]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "name": "Example",
      "url": "https://www.example.com/",
      "publisher": { "@id": "https://www.example.com/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.example.com/some-page/#webpage",
      "url": "https://www.example.com/some-page/",
      "name": "Page title",
      "isPartOf": { "@id": "https://www.example.com/#website" },
      "about": { "@id": "https://www.example.com/#organization" }
    }
  ]
}
</script>
```

## Rules
- **Site-wide:** `Organization` + `WebSite` on every page (the auditor warns if either is missing on the homepage).
- **Absolute URLs everywhere** — `@id`, `url`, `logo`, `item`. Build them from the same `PUBLIC_SITE_ORIGIN` used for canonical, at build time.
- **`@id` discipline:** stable fragment IDs (`/#organization`, `/#website`) so other nodes reference them instead of duplicating.
- **Match visible content.** JSON-LD that contradicts the page is a spam signal. Don't markup FAQs/reviews that aren't on the page.
- **Validate:** validator.schema.org and Google Rich Results Test before shipping.

## `knowsAbout` (the GEO multiplier)
On `Organization`, list the topics/entities you want to be associated with. This directly feeds how LLMs decide what your brand is "about" and when to recommend it. the reference site lists: `Agentic commerce, AI shopping agents, Generative engine optimization, AI search optimization, Product schema, Structured data, llms.txt, AI referral traffic`. Pick 6–10 real, specific topics — not keyword stuffing.

## Per-page type recipes (add to the `@graph`)

**Breadcrumb** — emit on every non-home page; also render a visible breadcrumb.
```json
{ "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com/" },
  { "@type": "ListItem", "position": 2, "name": "Guides", "item": "https://www.example.com/guides/" },
  { "@type": "ListItem", "position": 3, "name": "This page", "item": "https://www.example.com/guides/this/" }
] }
```

**Article / BlogPosting** — for blog/editorial.
```json
{ "@type": "BlogPosting", "@id": ".../post/#article", "headline": "…", "description": "…",
  "datePublished": "2026-01-01", "dateModified": "2026-01-02",
  "author": { "@type": "Person", "name": "…" },
  "publisher": { "@id": "https://www.example.com/#organization" },
  "mainEntityOfPage": { "@id": ".../post/#webpage" } }
```

**Product** — for ecommerce/product pages.
```json
{ "@type": "Product", "name": "…", "image": ["https://…/p.jpg"], "description": "…",
  "brand": { "@type": "Brand", "name": "…" },
  "offers": { "@type": "Offer", "price": "29.00", "priceCurrency": "USD",
    "availability": "https://schema.org/InStock", "url": "https://…/product/" } }
```

**FAQPage** — only if the Q&A is actually rendered on the page.
```json
{ "@type": "FAQPage", "mainEntity": [
  { "@type": "Question", "name": "Q?", "acceptedAnswer": { "@type": "Answer", "text": "A." } }
] }
```

## Reference implementation
the reference site builds these in `apps/web/src/lib/seo.ts` (`buildOrganizationJsonLd`, `buildWebsiteJsonLd`, `buildBreadcrumbJsonLd` — the last rejects a trailing-slash origin and a non-`/` path so canonical/`@id` URLs are always well-formed) and renders via a `JsonLd.astro` component wired into the base layout + per-route `jsonLd` fields.

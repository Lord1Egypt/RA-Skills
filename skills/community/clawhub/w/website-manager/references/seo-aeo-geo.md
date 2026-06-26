# SEO / AEO / GEO Reference

Use this file for page shells, article templates, service pages, and validation.

## Required on every page

```html
<title>{Page Topic} | {Business Name} | {City}</title>
<meta name="description" content="{120-160 char unique description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://{domain}/{slug}">
<meta property="og:title" content="{Page Title}">
<meta property="og:description" content="{Page Description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{Canonical URL}">
```

## AEO rules

- answer the implied user question near the top of the page
- use clear question headings where useful
- add FAQ content for services and key informational pages
- avoid jargon without explanation

## GEO rules

- mention city and service area in the first 200 words when locality matters
- keep NAP data consistent across pages and schema
- include local proof such as neighborhoods served, years in operation, or accreditations

## Useful schema types

- homepage: `LocalBusiness`, `Organization`, `WebSite`
- service pages: `Service`
- contact page: `ContactPage`
- articles: `Article` or `BlogPosting`
- FAQ-heavy pages: `FAQPage`

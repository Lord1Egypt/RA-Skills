---
name: seo-review
description: "SEO and discoverability review: evaluate meta tags, structured data, Open Graph, crawlability, sitemap, robots.txt, semantic HTML, and social sharing with browser-based validation."
---

# SEO Review

Evaluate your application's search engine optimization and discoverability. This review catches SEO issues that are invisible during normal development — missing meta tags, broken structured data, poor crawlability, missing sitemaps, and social sharing problems. Many SPAs ship with zero SEO consideration.

## When to use

Use `/seo-review` when:
- Before launching a public-facing website or application
- After redesigning or migrating a website
- When organic traffic is a growth channel
- After switching to an SPA framework (React, Vue, Angular)
- When social sharing (Open Graph) is important
- Setting up content marketing pages

## Standards Referenced

- **Google Search Central** — SEO best practices and guidelines
- **Schema.org** — Structured data vocabulary
- **Open Graph Protocol** — Social sharing meta tags
- **Twitter Card** — Twitter sharing markup
- **W3C Semantic HTML** — Accessibility and SEO semantics
- **Web.dev SEO Guidelines** — Google's SEO recommendations

## Phase Overview

```
Phase 1: EDUCATE   → Why SEO matters and what we check
Phase 2: SCOPE     → Identify key pages, content types, SEO goals
Phase 3: ANALYZE   → Browser-based SEO validation
Phase 4: REPORT    → Findings with impact assessment and priority
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **Why this matters:** 53% of all website traffic comes from organic search (BrightEdge). The first Google result gets 27.6% of all clicks; position 10 gets 2.4% (Backlinko). SPAs often render blank HTML to crawlers, making millions of pages invisible to search. Proper SEO doesn't require tricks — it requires making your content discoverable and understandable by search engines.

This review checks the technical SEO foundation — the things that must be correct before content strategy matters.

---

## Phase 2: Scope

### Gather context

1. **Auto-detect from codebase:**
   - Framework and rendering strategy (SSR, SSG, CSR, ISR)
   - Meta tag management (react-helmet, next/head, vue-meta, etc.)
   - Sitemap generation
   - robots.txt configuration
   - Structured data (JSON-LD, microdata)
   - i18n/hreflang setup
   - Canonical URL handling
   - Route structure and page types

2. **Ask the user** (one at a time):
   - **Target URL**: Where is the app running? (production preferred for realistic crawling)
   - **Key pages**: Which pages are most important for search? (homepage, product pages, blog posts, landing pages)
   - **Target keywords**: Any primary keywords you want to rank for? (optional, for content evaluation)
   - **Social sharing important?**: Is Open Graph / Twitter Cards needed? (default: yes for public sites)
   - **Multi-language?**: Does the site serve multiple languages? (auto-detected)

3. **Identify page types:**
   - Homepage
   - Content pages (blog, docs, about)
   - Product/listing pages
   - Dynamic pages (search results, user profiles)
   - Utility pages (login, 404, terms)

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. For each key page, run all check categories.

### Category A: Meta Tags & Head Elements (META)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| META-01 | Unique, descriptive `<title>` (50-60 chars) | Google guidelines | Extract `<title>`, check length and uniqueness |
| META-02 | Meta description present (120-160 chars) | Google guidelines | Check `<meta name="description">` |
| META-03 | Canonical URL set correctly | Google guidelines | Check `<link rel="canonical">` |
| META-04 | Viewport meta tag present | Mobile SEO | Check `<meta name="viewport">` |
| META-05 | Charset declared | HTML standard | Check `<meta charset>` |
| META-06 | No duplicate meta tags | SEO best practice | Check for duplicate titles, descriptions |
| META-07 | Favicon present | Branding/SEO | Check `<link rel="icon">` |
| META-08 | Language declared | SEO/a11y | Check `<html lang="">` |
| META-09 | No meta robots noindex on important pages | Indexing | Check `<meta name="robots">` |
| META-10 | Hreflang tags for multi-language (if applicable) | International SEO | Check `<link rel="alternate" hreflang="">` |

**Browser validation:** Use `inspect_page` to read the DOM. Extract all `<head>` elements via JavaScript.

### Category B: Structured Data (SCHEMA)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| SCHEMA-01 | JSON-LD structured data present | Schema.org | Check for `<script type="application/ld+json">` |
| SCHEMA-02 | Schema type matches page content | Schema.org | Validate type (Organization, Product, Article, etc.) |
| SCHEMA-03 | Required properties present | Schema.org | Validate against type requirements |
| SCHEMA-04 | JSON-LD is valid JSON | Schema.org | Parse and validate JSON |
| SCHEMA-05 | No deprecated schema properties | Schema.org | Check for deprecated fields |
| SCHEMA-06 | Breadcrumb structured data | Schema.org | Check for BreadcrumbList on interior pages |
| SCHEMA-07 | FAQ structured data (if applicable) | Schema.org | Check for FAQPage on FAQ sections |
| SCHEMA-08 | Review/Rating structured data (if applicable) | Schema.org | Check for AggregateRating |

**Browser validation:** Extract JSON-LD scripts via JavaScript. Parse and validate structure. Compare page content against schema claims.

### Category C: Open Graph & Social Sharing (OG)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| OG-01 | og:title present and meaningful | Open Graph | Check `<meta property="og:title">` |
| OG-02 | og:description present | Open Graph | Check `<meta property="og:description">` |
| OG-03 | og:image present and accessible | Open Graph | Check `<meta property="og:image">`, verify URL loads |
| OG-04 | og:image dimensions adequate (1200x630 recommended) | Open Graph | Check image size |
| OG-05 | og:url matches canonical | Open Graph | Compare og:url with canonical |
| OG-06 | og:type set correctly | Open Graph | Check og:type value |
| OG-07 | Twitter card meta tags present | Twitter Cards | Check `twitter:card`, `twitter:title`, etc. |
| OG-08 | Social sharing preview looks correct | UX | Construct preview from OG tags |

**Browser validation:** Extract all OG and Twitter meta tags. Verify og:image URL is accessible. Construct a preview representation.

### Category D: Crawlability & Indexing (CRAWL)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| CRAWL-01 | robots.txt exists and is valid | Google guidelines | Fetch /robots.txt |
| CRAWL-02 | Sitemap.xml exists and is valid | Google guidelines | Fetch /sitemap.xml, validate format |
| CRAWL-03 | Sitemap referenced in robots.txt | Best practice | Check robots.txt for Sitemap directive |
| CRAWL-04 | Important pages are in sitemap | SEO | Cross-reference key pages with sitemap URLs |
| CRAWL-05 | No broken internal links | Crawlability | Check all internal links on key pages |
| CRAWL-06 | No redirect chains (>2 hops) | Crawl efficiency | Follow redirects, count hops |
| CRAWL-07 | Clean URL structure (no excessive params) | SEO | Check URL patterns for cleanliness |
| CRAWL-08 | 404 page returns correct HTTP status | SEO | Navigate to non-existent URL, check status |
| CRAWL-09 | No orphan pages (accessible from navigation) | Crawlability | Verify key pages linked from homepage/nav |
| CRAWL-10 | SSR/SSG content visible without JavaScript | SPA SEO | Disable JS, check if content renders |
| CRAWL-11 | Page load time for crawlers | Crawl budget | Measure server response time |

**Browser validation:** Navigate to robots.txt, sitemap.xml. Follow internal links. Disable JavaScript to test server-rendered content. Check HTTP status codes.

### Category E: Semantic HTML & Content (SEM)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| SEM-01 | Single `<h1>` per page | SEO best practice | Count h1 elements |
| SEM-02 | Heading hierarchy is logical (h1→h2→h3) | SEO/a11y | Check heading sequence |
| SEM-03 | Images have descriptive alt text | SEO/a11y | Check alt attributes for descriptiveness |
| SEM-04 | Internal links use descriptive anchor text | SEO | Check for "click here" or bare URLs as links |
| SEM-05 | Semantic HTML elements used (nav, main, article, section) | SEO | Check for semantic landmarks |
| SEM-06 | Content-to-HTML ratio is reasonable | SEO | Calculate text content vs HTML markup |
| SEM-07 | No duplicate content across pages | SEO | Compare key content sections across pages |
| SEM-08 | URLs are human-readable | SEO | Check for descriptive slugs vs IDs/hashes |

**Browser validation:** Extract headings, links, images, and semantic elements via JavaScript. Analyze content structure.

### Category F: Technical SEO (TECH)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| TECH-01 | HTTPS everywhere | Google ranking signal | Check protocol |
| TECH-02 | HTTP → HTTPS redirect works | SEO | Test HTTP URL redirect |
| TECH-03 | www → non-www (or vice versa) redirect consistent | SEO | Test both variants |
| TECH-04 | Mobile-friendly (responsive) | Google mobile-first | Check viewport, responsive behavior |
| TECH-05 | Core Web Vitals pass "Good" thresholds | Google ranking signal | Measure LCP, INP, CLS |
| TECH-06 | No render-blocking resources | Page speed | Check script/style loading |
| TECH-07 | Proper 301 redirects for moved content | SEO | Check known old URLs if applicable |
| TECH-08 | International targeting correct (if multi-region) | International SEO | Check hreflang, geo-targeting |

**Browser validation:** Test redirects, measure performance metrics, check mobile rendering.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/seo-review-{date}.md`:

```markdown
# SEO Review Report
**Date:** {date}
**URL:** {url}
**Pages reviewed:** {list}
**Rendering:** {SSR/SSG/CSR/ISR}

## Overall Score: {X}/10 | Confidence: {X}%

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| Meta Tags (META) | 7/10 | 1 high, 2 medium |
| Structured Data (SCHEMA) | 4/10 | 1 critical, 1 high |
| Social Sharing (OG) | 6/10 | 2 high |
| Crawlability (CRAWL) | 5/10 | 1 critical, 1 high |
| Semantic HTML (SEM) | 8/10 | 1 medium |
| Technical SEO (TECH) | 7/10 | 1 high |

## Page-by-Page Summary
| Page | Title | Description | OG Image | Schema | H1 | Score |
|------|-------|-------------|----------|--------|----|-------|
| / | ✅ | ✅ | ❌ missing | ❌ none | ✅ | 6/10 |
| /blog | ✅ | ⚠️ too short | ✅ | ✅ Article | ✅ | 8/10 |

## Findings
(structured findings with evidence and impact)
```

### Confidence Scoring
- **90-100%**: Verified in browser — tag present/absent, URL accessible/broken
- **70-89%**: Content analysis suggests issue (e.g., thin content, generic alt text)
- **50-69%**: Best practice recommendation without clear violation
- **Below 50%**: Don't report

---

## Phase 5: Remediate

### 1. Fix guidance (example)
```markdown
#### CRAWL-10: Content not visible without JavaScript
**Impact:** Search engines may not index your content (especially Google Discover, Bing, social crawlers)
**Current:** Client-side rendered React app, empty HTML shell
**Fix:** Implement SSR or SSG:
- Next.js: Use `getServerSideProps` or `getStaticProps`
- Nuxt: Default SSR mode
- Gatsby: Static generation
- Or: Add prerendering service (prerender.io, rendertron)
**Quick win:** Ensure critical content is in initial HTML response
```

### 2. YAML regression test
```yaml
- name: meta-01-title-present
  description: Verify each key page has a unique, properly-sized title tag
  severity: high
  standard: Google-SEO-Guidelines
  steps:
    - URL: /
    - description: Assert the page title is present and 20-60 characters
      js: |
        const title = await page.title();
        if (!title || title.trim() === '') {
          throw new Error('Page has no title');
        }
        if (title.length < 20) {
          throw new Error(`Title too short (${title.length} chars): "${title}"`);
        }
        if (title.length > 60) {
          throw new Error(`Title too long (${title.length} chars): "${title}"`);
        }
        console.log(`Title OK (${title.length} chars): "${title}"`);
    - VERIFY: Page has a descriptive title between 20 and 60 characters
```

Save all YAML tests to `shiplight/tests/seo-review.test.yaml`.

---

## Depth Levels

- **`--quick`**: Meta tags + canonical + robots.txt on homepage only. ~2 minutes.
- **default**: All categories on key pages. ~8-12 minutes.
- **`--thorough`**: All categories + full site crawl + all page types + content analysis. ~20-30 minutes.

## Tips

- Test with JavaScript disabled to see what search engines see (especially for SPAs)
- Use `inspect_page` DOM output to extract `<head>` content efficiently
- Check sitemap.xml manually — auto-generated sitemaps often include pages that shouldn't be indexed
- OG image must be an absolute URL — relative URLs don't work for social sharing
- For SPA SEO, the critical question is: "Does the initial HTML contain the content?"
- Close session with `close_session` and use `generate_html_report` for evidence

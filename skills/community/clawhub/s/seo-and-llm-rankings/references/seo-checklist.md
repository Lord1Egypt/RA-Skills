# SEO & GEO Audit Checklist

Prioritized checklist for auditing websites for both traditional SEO and AI search visibility.

## Priority Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **P0** | Critical | Must fix immediately -- blocks indexing or causes major issues |
| **P1** | Important | Should fix soon -- significant impact on rankings |
| **P2** | Recommended | Improves visibility and user experience |

---

## Technical SEO

### P0 -- Critical

- [ ] **P0** Site is accessible (no 5xx errors)
- [ ] **P0** HTTPS enabled (valid SSL certificate)
- [ ] **P0** `robots.txt` allows important pages
- [ ] **P0** Mobile-responsive design
- [ ] **P0** No critical pages blocked by `noindex`
- [ ] **P0** Site is indexed in Google (`site:domain.com`)

### P1 -- Important

- [ ] **P1** `robots.txt` allows AI bots (GPTBot, PerplexityBot, ClaudeBot, Google-Extended)
- [ ] **P1** XML sitemap exists and is submitted
- [ ] **P1** Site is indexed in Bing (for Copilot visibility)
- [ ] **P1** Canonical tags properly implemented
- [ ] **P1** No duplicate content issues
- [ ] **P1** Page load time < 3 seconds
- [ ] **P1** LCP (Largest Contentful Paint) < 2.5s

### P2 -- Recommended

- [ ] **P2** INP (Interaction to Next Paint) < 200ms
- [ ] **P2** CLS (Cumulative Layout Shift) < 0.1
- [ ] **P2** Images optimized (WebP format, lazy loading)
- [ ] **P2** CSS/JS minified
- [ ] **P2** GZIP/Brotli compression enabled
- [ ] **P2** CDN configured
- [ ] **P2** No mixed content warnings
- [ ] **P2** Server-side rendering (not JS-only) for AI crawlers

---

## On-Page SEO

### P0 -- Critical

- [ ] **P0** Unique `<title>` tag exists (50-60 characters)
- [ ] **P0** Title contains primary keyword
- [ ] **P0** Unique `<meta description>` exists (150-160 characters)
- [ ] **P0** Single H1 tag per page
- [ ] **P0** H1 contains primary keyword

### P1 -- Important

- [ ] **P1** Description is compelling and includes keyword
- [ ] **P1** `<meta name="robots">` correctly set
- [ ] **P1** Logical heading hierarchy (H1 > H2 > H3, no skips)
- [ ] **P1** All images have `alt` attributes
- [ ] **P1** Internal links to related content
- [ ] **P1** No broken links (404s)
- [ ] **P1** Anchor text is descriptive

### P2 -- Recommended

- [ ] **P2** `og:title` set
- [ ] **P2** `og:description` set
- [ ] **P2** `og:image` set (1200x630px recommended)
- [ ] **P2** `og:url` set (canonical URL)
- [ ] **P2** `og:type` set (website/article)
- [ ] **P2** `twitter:card` set (summary_large_image)
- [ ] **P2** `twitter:title` set
- [ ] **P2** `twitter:description` set
- [ ] **P2** `twitter:image` set
- [ ] **P2** Paragraphs are short (2-3 sentences)
- [ ] **P2** Bullet points used for lists
- [ ] **P2** Tables used for comparisons
- [ ] **P2** External links have `rel="noopener noreferrer"`

---

## Schema Markup (Structured Data)

### P1 -- Important

- [ ] **P1** Organization schema on homepage
- [ ] **P1** WebPage schema on all pages
- [ ] **P1** Article schema on blog posts
- [ ] **P1** Schema passes Google Rich Results Test
- [ ] **P1** No errors in Search Console "Enhancements"

### P2 -- Recommended (GEO Enhanced)

- [ ] **P2** FAQPage schema on FAQ sections (+40% AI visibility)
- [ ] **P2** BreadcrumbList schema for navigation
- [ ] **P2** SpeakableSpecification for voice/AI search
- [ ] **P2** datePublished and dateModified included
- [ ] **P2** Author information with credentials
- [ ] **P2** Publisher information with logo
- [ ] **P2** HowTo schema on tutorial content

> **Detection note:** `web_fetch` and `curl` cannot detect JS-injected schema (Yoast, RankMath, AIOSEO). Use browser tools or Google Rich Results Test instead.

---

## GEO / AI Visibility

### P1 -- Important

- [ ] **P1** AI crawlers allowed in robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
- [ ] **P1** Content includes authoritative citations with sources (+27-40%)
- [ ] **P1** Statistics and data points included with sources (+33-37%)
- [ ] **P1** NO keyword stuffing (causes -9 to -10%)
- [ ] **P1** Answer capsules (40-60 words) after question-style H2s

### P2 -- Recommended

- [ ] **P2** llms.txt file at site root (+35% AI visibility)
- [ ] **P2** Expert quotes with attribution (+30-43%)
- [ ] **P2** Authoritative, confident tone (+25%)
- [ ] **P2** Content is accessible/easy to understand (+20%)
- [ ] **P2** Appropriate technical terminology (+18%)
- [ ] **P2** Diverse vocabulary throughout (+15%)
- [ ] **P2** High fluency and readability (+15-30%)

### AI Bot Access

- [ ] GPTBot allowed in robots.txt
- [ ] ChatGPT-User allowed in robots.txt
- [ ] ClaudeBot allowed in robots.txt
- [ ] Claude-Web allowed in robots.txt
- [ ] anthropic-ai allowed in robots.txt
- [ ] PerplexityBot allowed in robots.txt
- [ ] Google-Extended allowed in robots.txt
- [ ] Applebot-Extended allowed in robots.txt
- [ ] Bingbot allowed in robots.txt

### Content Structure for AI

- [ ] "Answer-first" format (direct answer at top)
- [ ] Clear, extractable paragraphs
- [ ] FAQ format for common questions
- [ ] Tables for comparison data
- [ ] Lists for step-by-step processes
- [ ] Question-style H2 headings

### AI Discovery Files

- [ ] llms.txt exists at site root
- [ ] llms.txt contains H1, summary blockquote, contact section
- [ ] llms.txt is under 50KB
- [ ] llms.txt served as `text/plain; charset=utf-8`

---

## E-E-A-T Signals

- [ ] Author bios with credentials
- [ ] About page with company info
- [ ] Contact information visible
- [ ] Privacy policy and terms
- [ ] Customer reviews/testimonials
- [ ] First-hand experience demonstrated
- [ ] Content dated and recently updated

---

## Off-Page SEO

### Backlinks

- [ ] Quality backlinks from relevant sites
- [ ] Diverse referring domains
- [ ] No toxic/spammy backlinks
- [ ] Brand mentions (even without links)

### Social Presence

- [ ] Active social media profiles
- [ ] Links to social profiles on website
- [ ] Consistent branding across platforms

### Entity Building

- [ ] Consistent brand info across the web
- [ ] Wikipedia/Wikidata presence (if applicable)
- [ ] Google Knowledge Panel (if applicable)
- [ ] Crunchbase, LinkedIn company page

---

## Content Quality

- [ ] All pages have unique, valuable content
- [ ] No thin content (< 300 words for main pages)
- [ ] Content matches search intent
- [ ] Content is up-to-date (within 30 days for tech/news)
- [ ] Content provides unique value vs competitors
- [ ] No AI writing tells (see ai-writing-detection.md)

---

## Monitoring Setup

- [ ] Google Search Console connected
- [ ] Bing Webmaster Tools connected
- [ ] Sitemap submitted to both
- [ ] Weekly: Check Search Console for errors
- [ ] Monthly: Analyze organic traffic trends
- [ ] Quarterly: Full SEO + GEO audit

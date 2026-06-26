---
name: seo-audit-bot
description: Perform a comprehensive SEO audit of any website. Analyzes technical SEO, on-page factors, content quality, performance, and generates an actionable report with scores and recommendations. Use when someone asks to audit, analyze, or check the SEO of a website, or wants an SEO score, or wants to compare SEO between two sites.
---

# SEO Audit Bot

A comprehensive SEO auditing skill that analyzes any website and produces a detailed, actionable report.

## What It Does

When a user provides a URL, this skill performs a full SEO audit covering:

1. **Technical SEO** — robots.txt, sitemap, HTTPS, mobile-friendliness, page speed signals
2. **On-Page SEO** — title tags, meta descriptions, headings, URL structure, internal linking
3. **Content Analysis** — word count, keyword density, readability, duplicate content signals
4. **Performance** — page load indicators, Core Web Vitals signals
5. **Social & Sharing** — Open Graph tags, Twitter Cards, structured data
6. **Competitor Comparison** (optional) — compare against a competitor URL

## How to Use

### Basic Audit
User says: `"Audit the SEO of https://example.com"`

Agent should:
1. Fetch the target URL using `web_fetch`
2. Fetch the robots.txt (`/robots.txt`)
3. Fetch the sitemap (`/sitemap.xml` or from robots.txt)
4. Analyze the HTML content for all SEO factors
5. Generate a structured report

### Competitor Comparison
User says: `"Compare SEO of https://example.com vs https://competitor.com"`

Agent should:
1. Audit both URLs
2. Generate a side-by-side comparison
3. Highlight advantages and gaps

## Audit Process

### Step 1: Fetch the Page
```
web_fetch(url="<target_url>", maxChars=50000, extractMode="text")
```

### Step 2: Check Technical Signals
- Fetch `robots.txt` → check if exists, what's blocked
- Fetch `sitemap.xml` → check if exists, last modified
- Check HTTPS redirect
- Check canonical tag presence

### Step 3: Analyze On-Page Elements
Extract and evaluate:
- `<title>` — length (50-60 chars ideal), keyword presence
- `<meta name="description">` — length (150-160 chars ideal), keyword presence
- `<h1>` — single h1, contains primary keyword
- `<h2>`–`<h6>` — proper hierarchy
- URL structure — short, descriptive, keyword-rich
- Image alt tags — descriptive, not keyword-stuffed
- Internal links — count, quality, anchor text
- External links — count, quality, nofollow usage

### Step 4: Content Analysis
- Word count (minimum 300 for pages, 1000+ for blog posts)
- Keyword density (1-3% for primary keyword)
- Heading structure (logical hierarchy)
- Readability (sentence length, paragraph size)
- Duplicate content risk

### Step 5: Performance Indicators
- Check for `<meta name="viewport">` (mobile-friendly)
- Check for lazy loading on images
- Check for minified CSS/JS references
- Check for CDN usage
- Check for excessive inline styles

### Step 6: Social & Schema
- Open Graph tags (og:title, og:description, og:image)
- Twitter Card tags
- JSON-LD structured data
- Schema.org markup

### Step 7: Generate Report

## Report Format

```
# SEO Audit Report: [URL]
Date: [date]

## Overall Score: XX/100

### 🔧 Technical SEO: XX/100
- ✅ HTTPS enabled
- ✅ robots.txt found
- ❌ No sitemap.xml found
- ✅ Mobile viewport configured
- ⚠️ Missing canonical tag

Recommendations:
1. Create and submit a sitemap.xml
2. Add canonical tags to prevent duplicate content

### 📄 On-Page SEO: XX/100
- ✅ Title tag (52 chars) — Good
- ⚠️ Meta description (180 chars) — Too long, aim for 150-160
- ❌ No H1 tag found
- ✅ URL structure is clean
- ⚠️ 3 images missing alt tags

Recommendations:
1. Add a clear H1 tag with primary keyword
2. Shorten meta description to 150-160 characters
3. Add alt tags to all images

### 📝 Content: XX/100
- Word count: 450 words
- Primary keyword density: 1.2%
- Heading structure: Proper H2/H3 hierarchy
- Readability: Good (avg 15 words/sentence)

Recommendations:
1. Expand content to 800+ words for better ranking potential

### ⚡ Performance: XX/100
- Viewport meta: ✅
- Lazy loading: ⚠️ Partial
- Minified assets: ✅
- CDN: ❌ Not detected

### 📱 Social & Schema: XX/100
- Open Graph: ✅ Complete
- Twitter Cards: ⚠️ Missing
- JSON-LD: ❌ Not found

Recommendations:
1. Add Twitter Card meta tags
2. Implement JSON-LD structured data for rich snippets

## 🎯 Priority Actions (Do These First)
1. [HIGH] Add H1 tag with primary keyword
2. [HIGH] Create sitemap.xml
3. [MEDIUM] Implement JSON-LD structured data
4. [LOW] Add Twitter Card tags
```

## Scoring Rubric

Each section is scored 0-100:

### Technical SEO (25% weight)
- HTTPS: 15 points
- robots.txt: 10 points
- sitemap.xml: 15 points
- Mobile viewport: 15 points
- Canonical tag: 10 points
- Clean URL structure: 10 points
- Page speed indicators: 15 points
- No broken links: 10 points

### On-Page SEO (30% weight)
- Title tag (exists, length, keyword): 20 points
- Meta description (exists, length, keyword): 20 points
- H1 tag (exists, unique, keyword): 20 points
- Heading hierarchy: 10 points
- Image alt tags: 15 points
- Internal linking: 15 points

### Content (25% weight)
- Word count: 25 points
- Keyword presence & density: 25 points
- Readability: 25 points
- Content structure: 25 points

### Performance (10% weight)
- Mobile-friendly: 30 points
- Asset optimization: 30 points
- Loading indicators: 40 points

### Social & Schema (10% weight)
- Open Graph: 40 points
- Twitter Cards: 30 points
- Structured data: 30 points

Overall Score = weighted average of all sections.

## Tips for the Agent

1. **Be specific** — don't just say "improve SEO", say exactly what to change
2. **Prioritize** — label recommendations as HIGH/MEDIUM/LOW
3. **Show before/after** — when suggesting changes, show the current state and the ideal state
4. **Be honest about limitations** — you can't check page speed directly, only indicators
5. **Offer follow-up** — suggest re-audit after changes are made

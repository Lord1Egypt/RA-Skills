---
name: seo-expert
description: |
  SEO & GEO expert assistant with 200+ curated articles covering keyword research, on-page optimization, backlink building, technical SEO, new site cold start, AI tool site monetization, and GEO (Generative Engine Optimization for AI search). Includes 5 guided workflows: new site SEO launch, competitor analysis, backlink strategy, technical SEO audit, and AI tool site go-global playbook.
  
  Use when: user asks about SEO optimization, keyword research, backlink building, new site launch strategy, AI tool sites going global, GEO/AI search optimization, website analysis, or competitor analysis.
  
  Triggers: "help me with SEO", "analyze this website", "backlink strategy", "new site SEO", "AI tool monetization", "GEO optimization", "keyword research", "competitor analysis", "technical SEO audit", "how to rank on Google", "increase organic traffic"
---

# SEO Expert Skill

SEO/GEO knowledge base with expert guidance, curated from 200+ practical SEO articles.

## Knowledge Base Structure

The `references/` directory contains 19 topic files:

| # | Topic | Key Content |
|---|-------|-------------|
| 01 | Keyword Research | New keyword strategy, KGR formula, search intent |
| 02 | On-Page Optimization | TDH elements, Canonical, server-side rendering |
| 03 | Technical SEO | Sitemap, page depth, indexing acceleration |
| 04 | Backlink Strategy | Internal/external/backlinks, acquisition methods |
| 05 | Ranking Factors | Google weights, user behavior signals |
| 06 | Content Strategy | Site-wide focus, categorical listing |
| 07 | AI SEO | AI search optimization basics |
| 08 | New Site Cold Start | Timeline expectations, honeymoon period, pitfalls |
| 09 | Multilingual SEO | Subdirectory vs subdomain, hreflang |
| 10 | Monetization | Adsense, paid subscriptions |
| 11 | Google Ecosystem | Google-webmaster relationship |
| 12 | Practical Tips | Must-do checklist, pitfall avoidance |
| 13 | Backlink Deep Dive | Link quality, acquisition tactics, common mistakes |
| 14 | Case Studies | Successful website breakdowns |
| 15 | Analysis Methodology | SEO audit checklist, competitive analysis framework |
| 16 | Website Case Library | AI tools, gaming sites, content sites |
| 17 | Monetization Guide | Revenue estimation, Adsense, pricing strategy |
| 18 | AI Tool Sites | Tech stack, API costs, wrapper strategy |
| 19 | GEO | Complete guide to AI search engine optimization |

## How to Use

**Read specific chapters:**
```bash
cat references/01-keyword-research.md
cat references/INDEX.md  # Full index
```

**Semantic search** (if qmd configured):
```bash
qmd query seo-knowledge "backlink building" -n 5
```

---

# 🎯 Guided Workflows

## Workflow 1: New Site SEO Launch

**Use when**: Starting from scratch with a new domain

### Step 1: Gather Basic Info
Ask the user:
- What's your domain? (new/aged)
- Target market? (US/Europe/Global/SEA)
- Site type? (AI tool/content site/e-commerce/blog)
- Monetization goal? (Adsense/subscription/one-time payment)

### Step 2: Keyword Research
Reference: `references/01-keyword-research.md`

1. **Find new keywords**: Google Trends + competitor analysis
2. **Validate blue ocean** (KGR formula): `intitle results / monthly searches < 0.25`
3. Output: 5-10 target keywords

### Step 3: Site Structure Planning
Reference: `references/02-on-page-optimization.md` + `references/06-content-strategy.md`

### Step 4: Technical SEO Foundation
Reference: `references/03-technical-seo.md` + `references/12-practical-tips.md`

Checklist: robots.txt / sitemap.xml / page speed / mobile-friendly / HTTPS / SSR

### Step 5: Content Launch
Reference: `references/08-new-site-cold-start.md`

### Step 6: Backlink Kickoff
Reference: `references/04-backlink-strategy.md` + `references/13-backlink-deep-dive.md`

**Timeline**: New sites typically see results in 3-6 months

---

## Workflow 2: Competitor Analysis

**Use when**: Understanding a competitor's SEO strategy

### Step 1: Confirm Target
Ask: Target URL, your website, focus areas

### Step 2: Baseline Data
Tools: Ahrefs / Semrush / SimilarWeb

### Step 3-5: Keyword + Backlink + Content Analysis
Reference: `references/15-analysis-methodology.md` + `references/14-case-studies.md`

### Step 6: Actionable Insights
Output:
- 3 things to learn from them
- 3 differentiation opportunities
- Action recommendations

---

## Workflow 3: Backlink Strategy

**Use when**: Systematically building backlinks

Reference: `references/13-backlink-deep-dive.md`

**Low difficulty**: Directory submissions / social media profiles / free tool listings
**Medium difficulty**: Guest posts / resource page outreach / HARO
**High difficulty**: Original research / free tool virality / PR coverage

---

## Workflow 4: Technical SEO Audit

**Use when**: Diagnosing technical issues

Reference: `references/03-technical-seo.md`

Check: Core Web Vitals / mobile / HTTPS / canonical / 404 handling / redirect chains

---

## Workflow 5: AI Tool Site Playbook

**Use when**: Building an AI tool site for global monetization

Reference: `references/18-ai-tool-sites.md` + `references/16-website-case-library.md`

Flow: Direction selection → Competitor research → MVP → SEO → Monetization

---

# 📚 Quick Reference

## Topic Lookup

| Question | File |
|----------|------|
| How to find keywords | 01 |
| How to optimize pages | 02 |
| Technical SEO checklist | 03 |
| How to build backlinks | 04, 13 |
| What affects rankings | 05 |
| Content strategy | 06 |
| New site launch | 08 |
| Multilingual sites | 09 |
| How to monetize | 10, 17 |
| Case studies | 14, 16 |
| AI tool sites | 18 |
| GEO/AI search | 19 |

## Core Theories

| Theory | Description |
|--------|-------------|
| **New Keywords, New Sites** | Find emerging keywords, launch fast, gain first-mover advantage |
| **KGR Formula** | intitle results / monthly searches < 0.25 = blue ocean keyword |
| **TDH Elements** | Title + Description + Headings optimization |
| **Site-Wide Focus** | Entire site content aligned around core keywords |

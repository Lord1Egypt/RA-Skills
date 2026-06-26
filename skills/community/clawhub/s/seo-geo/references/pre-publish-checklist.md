# Pre-Publish Checklist

> Nothing gets published without passing every item below. Read this before publishing ANY article.

---

## SEO On-Page Checklist

- [ ] H1 contains the primary keyword exactly as targeted
- [ ] Title tag: primary keyword + year + benefit, under 60 characters
- [ ] Meta description: includes primary keyword, compelling copy, 150-160 characters
- [ ] First paragraph: primary keyword appears within the first 100 words
- [ ] H2 headings: secondary keywords used naturally (no forced phrasing)
- [ ] Internal links: link to the pillar page + 2-3 cluster pages
- [ ] External links: 2-4 authoritative sources (Statista, McKinsey, Shopify docs, G2, Gartner, etc.)
- [ ] Images: descriptive alt text that includes keywords naturally
- [ ] URL slug: short, keyword-rich, lowercase, hyphenated (no stop words, no trailing slashes issues)

---

## Schema Markup Checklist

- [ ] FAQPage JSON-LD with 3-5 questions that match real search queries from GSC
- [ ] Article schema includes: `@type`, `headline`, `datePublished`, `author`, `publisher`
- [ ] FAQ answers are self-contained (each answer must work as a standalone featured snippet)
- [ ] Comparison articles ("X vs Y", "Best tools for..."): add `ItemList` schema
- [ ] How-to articles: add `HowTo` schema with steps
- [ ] Validate all schema with Google Rich Results Test before publishing

---

## GEO Optimization Checklist (Princeton 9 Methods)

Apply these to maximize AI search citation (ChatGPT, Perplexity, Gemini, Claude):

- [ ] **Cite sources (+40% visibility):** 3-5 external citations with links to authoritative sources
- [ ] **Statistics (+37%):** 3-5 specific numbers with named sources and dates
- [ ] **Expert quotes (+30%):** at least 1 attributed quote (name, title, company)
- [ ] **Authoritative tone (+25%):** confident language, no hedging ("X is" not "X might be")
- [ ] **Easy to understand (+20%):** short paragraphs, plain language, no jargon without context
- [ ] **Technical terms (+18%):** domain-specific vocabulary used naturally where appropriate
- [ ] **Unique words (+15%):** varied vocabulary, no repetitive phrasing across paragraphs
- [ ] **Fluency (+15-30%):** smooth logical flow, clear transitions between sections
- [ ] **NO keyword stuffing (-10%):** natural usage only, never forced or awkward

---

## Content Structure (GEO-Optimized)

- [ ] Answer-first format: lead with the answer, then explain the reasoning
- [ ] Clear heading hierarchy: H1 > H2 > H3 (no skipped levels)
- [ ] Comparison tables for any "vs" or "best" content
- [ ] Bullet points and numbered lists for scanability
- [ ] Short paragraphs: 2-3 sentences maximum per paragraph
- [ ] Visual breaks every 200-300 words (table, image, list, blockquote, or callout)

---

## Engagement Checklist

- [ ] Hook in the first sentence: a result, a number, or a provocative claim
- [ ] CTA block mid-article (subtle, contextual)
- [ ] CTA block end-of-article (bold, direct)
- [ ] Comparison table included for "vs" and review content
- [ ] FAQ accordion or section present
- [ ] Related articles section with 3-4 links to cluster content
- [ ] No walls of text: maximum 3 sentences per paragraph, no exceptions

---

## Image Checklist

- [ ] 2-4 images per article minimum
- [ ] All images compressed (WebP preferred, under 200KB each)
- [ ] Descriptive file names (e.g., `saas-pricing-comparison-table.webp`, never `IMG_001.jpg`)
- [ ] Alt text includes keywords naturally (not stuffed)
- [ ] At least 1 product screenshot if relevant to the topic
- [ ] Thumbnail/OG image for social sharing: 1280x720, 16:9 aspect ratio

---

## Pre-Publish Final Checks

- [ ] Proofread for grammar, spelling, and clarity
- [ ] Verify all external links work (no 404s, no redirects to unrelated pages)
- [ ] Check mobile rendering (responsive layout, readable text, no overflow)
- [ ] Validate JSON-LD schema with Google Rich Results Test
- [ ] Title tag and meta description are unique (not duplicated from any other page)
- [ ] No orphan page: at least 3 inbound internal links planned before publishing

---

## Post-Publish Checklist

- [ ] Verify page appears in XML sitemap
- [ ] Request indexing in Google Search Console
- [ ] Check live page renders correctly (no broken elements, no layout shifts)
- [ ] Add internal links FROM 3-5 existing relevant pages TO this new page
- [ ] Update the pillar/hub page to include a link to this new page
- [ ] Verify FAQPage schema passes Rich Results Test on the live URL
- [ ] Share on relevant distribution channels

---

## Biweekly Internal Linking Audit

Run this audit every two weeks to maintain link health across the site:

- [ ] No broken links (scan for 404s across all published pages)
- [ ] No direct links to competitor websites (link to YOUR review/comparison pages instead)
- [ ] No dead-end pages (every page must have a Related Articles section)
- [ ] New pages published in the last 2 weeks have 3+ inbound internal links
- [ ] External links point to authority sources only (no low-quality or spammy domains)
- [ ] Pillar pages are linked from every page in their cluster

---

## Important Notes

- **ALWAYS** invoke the `seo-geo` companion skill before writing any article. It validates technical SEO, GEO scoring, AI bot access, and schema markup at a deeper level than this checklist covers.
- The `seo-geo` skill is listed in recommended skills in the main SKILL.md.
- This checklist is the minimum bar. The `seo-geo` skill adds additional validation on top.
- When in doubt, re-read this file. When confident, re-read it anyway.

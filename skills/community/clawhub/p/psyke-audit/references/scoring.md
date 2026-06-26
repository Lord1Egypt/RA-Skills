# Psyke Audit — Scoring Methodology

Two scores are produced: **SEO Health** (out of 100) and **GEO Readiness** (out of 100).
Both scores use evidence-based deductions from a maximum. Start at max, subtract for issues found.

---

## SEO Health Score (100 points)

### 1. Crawlability & Indexation (20 points)

| Check | Max | Criteria |
|-------|-----|----------|
| robots.txt | 3 | Exists, no critical disallows, sitemap referenced |
| XML sitemap | 3 | Exists, valid entries, no junk/stale pages, correct lastmod |
| Canonical tags | 3 | Present and correct on all crawled pages |
| HTTPS | 3 | Full HTTPS, no mixed content |
| Status codes | 4 | No soft 404s, proper redirects (301 not 302), no redirect chains |
| URL structure | 4 | Clean, descriptive, logical hierarchy, no query params for content |

### 2. Technical SEO (20 points)

| Check | Max | Criteria |
|-------|-----|----------|
| Meta descriptions | 5 | Present on all pages, unique, 120-160 chars, contain target keywords |
| Open Graph tags | 3 | og:title, og:description, og:image, og:url on all pages |
| Twitter/X Card tags | 2 | twitter:card, twitter:title, twitter:image present |
| Viewport meta | 1 | Correct: width=device-width, initial-scale=1 |
| Image optimisation | 3 | Lazy loading, appropriate formats, reasonable file sizes |
| Mobile-friendly | 3 | Responsive, no horizontal scroll, tap targets sized correctly |
| Page speed (if data available) | 3 | LCP < 2.5s, CLS < 0.1, TBT < 200ms |

### 3. On-Page SEO (25 points)

| Check | Max | Criteria |
|-------|-----|----------|
| H1 tags | 5 | One unique H1 per page, contains primary keyword |
| Heading hierarchy | 3 | Clean H1→H2→H3 nesting, no skips |
| Title tags | 5 | Unique, keyword-rich, include brand, 50-60 chars |
| Image alt text | 3 | All images have descriptive, relevant alt text |
| Internal linking | 4 | Strong nav structure, contextual links within content, no orphan pages |
| Content depth | 5 | Adequate word count for intent, not thin/stub pages |

### 4. Structured Data (15 points)

| Check | Max | Criteria |
|-------|-----|----------|
| Organization schema | 4 | Present on homepage with name, logo, URL, contact, sameAs |
| BreadcrumbList | 3 | Present on inner pages, valid @context/@type |
| Page-specific schema | 4 | Appropriate types (FAQ, Product, Article, Service, LocalBusiness) |
| Schema validity | 2 | No syntax errors, correct @context/@type, passes validation |
| Social/OG completeness | 2 | Full OG + Twitter Card implementation |

### 5. Content & Authority (20 points)

| Check | Max | Criteria |
|-------|-----|----------|
| Blog / content hub | 5 | Exists, actively maintained, targets relevant keywords |
| Content freshness | 3 | Recent publications, updated evergreen content |
| E-E-A-T signals | 4 | Author bios, credentials, about page, trust signals |
| Backlink profile | 4 | DR/DA (via Ahrefs if available), referring domains quality |
| Brand presence | 4 | Non-branded keyword ratio, brand search volume |

### Score Interpretation

| Range | Label | Meaning |
|-------|-------|---------|
| 80-100 | Excellent | Strong SEO foundation, minor optimisations only |
| 65-79 | Good | Solid base with specific gaps to address |
| 50-64 | Fair | Significant issues limiting organic performance |
| 35-49 | Poor | Critical gaps undermining search visibility |
| 0-34 | Critical | Fundamental SEO work needed across the board |

---

## GEO Readiness Score (100 points)

### 1. AI Citability (30 points)

| Check | Max | Criteria |
|-------|-----|----------|
| Direct answer content | 6 | Pages that directly answer common questions in the space |
| FAQ implementation | 6 | FAQ sections with schema markup on key pages |
| Entity clarity | 6 | Clear brand-product-category relationships, structured data |
| Authoritative statements | 6 | Citable facts, statistics, definitive claims with evidence |
| Content structure | 6 | Clear headings, short paragraphs, scannable — AI-parseable format |

### 2. AI Visibility (25 points)

Only scored when Ahrefs data is available. If unavailable, redistribute points to other categories.

| Check | Max | Criteria |
|-------|-----|----------|
| Google AI Overview citations | 10 | Count from Ahrefs, benchmarked against competitors |
| ChatGPT citations | 10 | Count from Ahrefs, benchmarked against competitors |
| Live AI query testing | 5 | Manual queries to ChatGPT/Perplexity — is the brand mentioned? |

### 3. Content Architecture (25 points)

| Check | Max | Criteria |
|-------|-----|----------|
| Topic hub pages | 5 | Dedicated pages for core topics/categories with depth |
| Content clusters | 5 | Interlinked pages demonstrating vertical expertise |
| Informational content | 5 | Buying guides, how-tos, explainers, comparisons |
| Long-tail coverage | 5 | Content targeting specific, question-based queries |
| Internal linking depth | 5 | Hub-and-spoke architecture, contextual cross-links |

### 4. Competitive Position (20 points)

Only scored when competitor data is available (Ahrefs). If unavailable, redistribute.

| Check | Max | Criteria |
|-------|-----|----------|
| AI citations vs competitors | 8 | Relative position in AI citation counts |
| Content gap vs competitors | 7 | Topics/keywords competitors rank for that client doesn't |
| Non-branded share | 5 | % of traffic from non-branded queries vs competitors |

### GEO Score Interpretation

| Range | Label | Meaning |
|-------|-------|---------|
| 80-100 | AI-Ready | Strong content architecture, appearing in AI responses |
| 60-79 | Emerging | Some content depth, but gaps in AI visibility |
| 40-59 | Underdeveloped | Limited informational content, minimal AI presence |
| 20-39 | Invisible | Almost no AI-optimised content, not cited |
| 0-19 | Absent | No content strategy for AI discovery |

---

## Scoring Rules

1. **Evidence-based only** — every deduction must cite specific evidence (URL, missing element, screenshot)
2. **No rounding up** — if it's 43, it's 43. Don't massage to 45 for optics.
3. **Competitor context matters** — a score of 50 means more when competitors are at 80
4. **Ahrefs data enhances but isn't required** — audits work without it, just note "estimated" for authority/visibility scores
5. **When Ahrefs unavailable** — redistribute AI Visibility (25pts) as: +10 to AI Citability, +10 to Content Architecture, +5 to Competitive Position (manual assessment)
6. **When competitor data unavailable** — redistribute Competitive Position (20pts) as: +10 to Content Architecture, +10 to AI Citability

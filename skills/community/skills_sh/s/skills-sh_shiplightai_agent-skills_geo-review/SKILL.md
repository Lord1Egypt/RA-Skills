---
name: geo-review
description: "Generative Engine Optimization review: evaluate your content's visibility to AI-powered search engines — citation-worthiness, content structure, authority signals, llms.txt, entity clarity, and AI retrieval readiness."
---

# GEO Review

Evaluate how well your application and content are optimized for AI-powered search and answer engines — ChatGPT, Perplexity, Google AI Overviews, Claude, and other generative AI systems that cite web sources. Traditional SEO gets you ranked in a link list; GEO gets you **cited in AI-generated answers**.

## When to use

Use `/geo-review` when:
- Your product is discovered through AI assistants (developer tools, SaaS, APIs)
- You want to appear in Google AI Overviews
- Users find your product by asking AI "what's the best X for Y?"
- You publish documentation, guides, or educational content
- Your competitors are showing up in AI answers and you're not
- Building thought leadership content that AI should reference
- Launching a new product where AI-driven discovery matters

## Why GEO Matters Now

- **40% of Gen Z** uses TikTok and AI chatbots instead of Google for search (Adobe 2024)
- **Google AI Overviews** now appear for ~30% of search queries, pushing traditional results below the fold
- **Perplexity** processes 100M+ queries/month, citing web sources in every answer
- **ChatGPT with browsing** and search is becoming a primary research tool
- AI systems don't rank links — they **select and cite sources** based on different signals than traditional SEO
- Being the source an AI quotes is the new "position #1"

## Standards & Frameworks Referenced

- **GEO research** (Georgia Tech / Princeton / IIT Delhi, 2024) — "GEO: Generative Engine Optimization"
- **Google E-E-A-T** — Experience, Expertise, Authoritativeness, Trustworthiness
- **Schema.org** — Structured data for entity understanding
- **llms.txt** — Emerging standard for AI crawler instructions (similar to robots.txt for LLMs)
- **Retrieval-Augmented Generation (RAG)** — How AI systems fetch and cite content

## Phase Overview

```
Phase 1: EDUCATE   → How AI search works differently from traditional search
Phase 2: SCOPE     → Identify content types, target queries, AI visibility goals
Phase 3: ANALYZE   → Content analysis + browser-based AI search validation
Phase 4: REPORT    → Findings with citation gap analysis and confidence scores
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **How AI search is different:** Traditional search engines crawl, index, and rank pages by relevance signals (backlinks, keywords, authority). AI answer engines do something fundamentally different — they retrieve content, understand it semantically, and synthesize answers by selecting the most citation-worthy sources. Your content needs to be **clear, specific, authoritative, and directly answerable** to be selected.

> **Key insight:** AI systems prefer content that makes **specific, verifiable claims** with **supporting evidence**. Vague marketing copy is ignored. Concrete statements with data, comparisons, and clear structure get cited.

---

## Phase 2: Scope

### Gather context

1. **Auto-detect from codebase/content:**
   - Content pages (docs, blog, landing pages, about, pricing, FAQ)
   - Existing structured data (JSON-LD, Schema.org)
   - Content management approach (static, CMS, MDX, etc.)
   - llms.txt presence
   - Sitemap and content organization
   - Author/expertise signals
   - Publication dates and freshness signals

2. **Ask the user** (one at a time):
   - **Product type**: What does your product/site do? (needed to understand AI query context)
   - **Target URL**: Where is the content published?
   - **Target AI queries**: What questions should AI answer with your content? (e.g., "best CI/CD tool for startups", "how to implement OAuth in Node.js")
   - **Competitors**: Who else shows up when AI answers these queries? (optional but valuable)
   - **Content goals**: Documentation? Thought leadership? Product discovery? All of the above?

3. **Map content landscape:**
   - Key content pages and their purpose
   - Target queries each page should satisfy
   - Current AI citation status (test a few queries in ChatGPT/Perplexity)
   - Content gaps vs competitors

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. Run all applicable check categories.

### Category A: Content Citation-Worthiness (CITE)

| Check ID | Check | Principle | Method |
|----------|-------|-----------|--------|
| CITE-01 | Content contains specific, verifiable claims | GEO research | Scan pages for concrete statements with data/numbers |
| CITE-02 | Statistics and original data are present | GEO research | Check for unique numbers, benchmarks, research findings |
| CITE-03 | Content directly answers target queries | RAG retrieval | Match content against target queries — does it contain direct answers? |
| CITE-04 | Claims have supporting evidence or citations | E-E-A-T | Check for source references, links, data attribution |
| CITE-05 | Content is specific (not generic/vague) | GEO research | Analyze content for specificity vs marketing fluff |
| CITE-06 | Comparison content exists (vs alternatives) | AI preference | Check for "X vs Y" or comparison tables that AI can cite |
| CITE-07 | Content has clear, quotable summary sentences | Citation format | Check if key paragraphs start with citable claims |
| CITE-08 | Unique perspective or data (not regurgitated) | E-E-A-T | Assess originality — does this add something AI can't already synthesize? |
| CITE-09 | Content demonstrates first-hand experience | E-E-A-T (Experience) | Check for case studies, personal experience, real examples |
| CITE-10 | Technical accuracy and depth | E-E-A-T (Expertise) | Assess whether content goes beyond surface level |

**Browser validation:** Navigate to content pages. Extract text content. Analyze for claim density, statistics, quotable statements. Compare against target queries for direct answer matching.

### Category B: Content Structure for AI Retrieval (STRUCT)

| Check ID | Check | Principle | Method |
|----------|-------|-----------|--------|
| STRUCT-01 | Clear heading hierarchy maps to questions | RAG chunking | Check if H2/H3 headings are question-shaped or topic-clear |
| STRUCT-02 | FAQ sections with direct Q&A format | AI preference | Check for FAQ sections, question-answer pairs |
| STRUCT-03 | Definition/explanation paragraphs lead with the answer | Retrieval | Check if paragraphs front-load the key claim (inverted pyramid) |
| STRUCT-04 | Tables and structured comparisons present | AI preference | Check for HTML tables with clear headers |
| STRUCT-05 | Content is chunked into digestible sections (300-500 words) | RAG chunking | Measure section lengths between headings |
| STRUCT-06 | Lists used for multi-point information | AI preference | Check for ordered/unordered lists for multi-step or multi-item content |
| STRUCT-07 | Code examples are complete and runnable (for technical content) | Developer experience | Check code blocks for completeness and language tags |
| STRUCT-08 | TL;DR or summary at top of long content | Retrieval | Check for executive summary or key takeaways section |

**Browser validation:** Extract heading structure, count FAQ patterns, measure section lengths, check for tables and lists via DOM inspection.

### Category C: Authority & Trust Signals (AUTH)

| Check ID | Check | Principle | Method |
|----------|-------|-----------|--------|
| AUTH-01 | Author information present (name, bio, credentials) | E-E-A-T | Check for author bylines, about sections |
| AUTH-02 | Organization/brand identity clear | Entity recognition | Check for About page, consistent branding |
| AUTH-03 | Publication and update dates visible | Freshness | Check for date metadata on content pages |
| AUTH-04 | Sources and references cited | E-E-A-T | Check for outbound links to authoritative sources |
| AUTH-05 | Testimonials/social proof present | Trust | Check for customer quotes, logos, case studies |
| AUTH-06 | Professional contact information available | Trust | Check for contact page, physical address, support channels |
| AUTH-07 | Content recency (updated within last 12 months) | Freshness | Check publish/update dates |
| AUTH-08 | Domain authority indicators (established site) | E-E-A-T | Check site age, about page depth, team page |

**Browser validation:** Navigate to content pages, about page, author pages. Extract dates, author info, citation links.

### Category D: Technical AI Discoverability (TECH)

| Check ID | Check | Principle | Method |
|----------|-------|-----------|--------|
| TECH-01 | llms.txt present at site root | AI crawler standard | Fetch /llms.txt, check format and content |
| TECH-02 | llms-full.txt with detailed content (if applicable) | AI crawler standard | Fetch /llms-full.txt |
| TECH-03 | JSON-LD structured data with rich entity info | Schema.org | Check for Organization, Product, Article, FAQ schema |
| TECH-04 | Content accessible without JavaScript | RAG crawling | Disable JS, check if content renders |
| TECH-05 | Clean, semantic HTML (not framework soup) | Crawlability | Check for meaningful tags vs div-heavy DOM |
| TECH-06 | robots.txt allows AI crawlers | Discoverability | Check for GPTBot, ClaudeBot, PerplexityBot, Bingbot rules |
| TECH-07 | Sitemap includes content pages with lastmod | Discoverability | Check sitemap for content pages and dates |
| TECH-08 | Open Graph tags help AI understand content | Social + AI | Check OG tags for accurate content description |
| TECH-09 | API documentation is machine-readable (if applicable) | Developer GEO | Check for OpenAPI spec, API reference format |
| TECH-10 | Content is not behind authentication walls | RAG access | Verify key content is publicly accessible |

**Browser validation:** Fetch llms.txt, check robots.txt for AI bot rules, verify SSR content, inspect structured data.

### Category E: Entity & Brand Clarity (ENTITY)

| Check ID | Check | Principle | Method |
|----------|-------|-----------|--------|
| ENTITY-01 | Product/brand name is consistently used | Entity recognition | Check name consistency across pages |
| ENTITY-02 | Clear product category declaration | AI classification | Check if content states "X is a [category]" explicitly |
| ENTITY-03 | Key features/differentiators stated clearly | AI comparison | Check for feature lists, unique value propositions |
| ENTITY-04 | Use case descriptions are specific | AI recommendation | Check for "best for [specific use case]" patterns |
| ENTITY-05 | Pricing/tier information is structured | AI recommendation | Check pricing page for clear, structured plans |
| ENTITY-06 | Integration/compatibility information present | AI recommendation | Check for "works with X" / integration pages |
| ENTITY-07 | Competitor differentiation is factual | AI comparison | Check comparison content for factual (not just marketing) claims |
| ENTITY-08 | Industry/vertical targeting is explicit | AI classification | Check if content targets specific industries/roles |

**Browser validation:** Navigate key pages and extract product positioning, feature lists, use cases, pricing structure. Check for entity-clear statements.

### Category F: AI Citation Testing (TEST)

This category is unique to GEO — it tests actual AI visibility.

| Check ID | Check | Method |
|----------|-------|--------|
| TEST-01 | Test target queries in Perplexity | Navigate to perplexity.ai, search target queries, check if your site is cited |
| TEST-02 | Test target queries in ChatGPT (if browsing available) | Search via ChatGPT, check citations |
| TEST-03 | Test target queries in Google (check AI Overview) | Google search, check if AI Overview cites your content |
| TEST-04 | Compare citation frequency vs competitors | Count citations for you vs top competitors across queries |
| TEST-05 | Analyze what content IS being cited (from competitors) | Study cited content format, structure, claims |

**Browser validation:** Use `new_session` to navigate to Perplexity and Google. Search target queries. Screenshot results. Check for citations to the user's domain. This provides real-world evidence of current AI visibility.

**Important:** TEST category results are the ground truth — they show whether your content is actually being cited, regardless of what the other categories suggest.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/geo-review-{date}.md`:

```markdown
# GEO Review Report
**Date:** {date}
**URL:** {url}
**Product type:** {description}
**Target AI queries tested:** {list}

## Overall GEO Score: {X}/10 | Confidence: {X}%

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| Citation-Worthiness (CITE) | 5/10 | 2 high, 2 medium |
| Content Structure (STRUCT) | 6/10 | 1 high, 2 medium |
| Authority Signals (AUTH) | 7/10 | 1 medium |
| Technical Discoverability (TECH) | 4/10 | 1 critical, 2 high |
| Entity Clarity (ENTITY) | 5/10 | 2 high |
| AI Citation Testing (TEST) | 3/10 | Not cited in 4/5 target queries |

## AI Citation Status
| Target Query | Perplexity | Google AI Overview | Cited? | Competitor Cited? |
|-------------|------------|-------------------|--------|------------------|
| "best X for Y" | Not cited | Not in overview | ❌ | CompetitorA: ✅ |
| "how to do Z" | Cited (#3 source) | Cited | ✅ | CompetitorB: ✅ |
| ... | | | | |

## Citation Gap Analysis
What competitors' cited content has that yours doesn't:
- Specific performance benchmarks (CompetitorA cites "40% faster than...")
- Comparison tables (CompetitorB has detailed feature matrices)
- Direct answer paragraphs (CompetitorA leads sections with the conclusion)

## Findings
(structured findings with evidence and priority)
```

### Confidence Scoring
- **90-100%**: Verified via live AI search — content is/isn't cited (TEST category)
- **70-89%**: Strong structural evidence — content has/lacks citation-worthy patterns
- **50-69%**: Heuristic assessment of content quality signals
- **Below 50%**: Don't report

---

## Phase 5: Remediate

### 1. Fix guidance (example)
```markdown
#### CITE-01: Landing page lacks specific, verifiable claims
**Impact:** AI systems skip vague marketing copy — your landing page is invisible to AI answers
**Current:** "We're the fastest platform for modern teams"
**Fix:** Add specific, citable claims:
- "Deploys complete in 47 seconds on average (based on 10,000 deployments in Q4 2025)"
- "Used by 2,300 companies including [notable names]"
- "Reduces CI/CD pipeline time by 62% compared to Jenkins (internal benchmark, Jan 2026)"
**Principle:** AI cites facts, not adjectives. Every claim should be verifiable.
```

```markdown
#### TECH-01: No llms.txt present
**Impact:** AI crawlers have no guidance on how to understand your site
**Fix:** Create /llms.txt at site root:

# [Your Product Name]

> One-sentence description of what your product does.

## Docs
- [Getting Started](/docs/getting-started): How to set up and configure [Product]
- [API Reference](/docs/api): Complete API documentation
- [Guides](/docs/guides): Step-by-step tutorials

## Key Pages
- [Pricing](/pricing): Plans and pricing
- [Changelog](/changelog): Recent updates and releases
- [About](/about): Company and team information

Also create /llms-full.txt with expanded content for deeper AI understanding.
```

### 2. YAML regression tests
```yaml
- name: tech-01-llms-txt-present
  description: Verify llms.txt exists and is properly formatted
  severity: high
  standard: llms-txt-standard
  steps:
    - URL: /llms.txt
    - VERIFY: The page loads successfully and contains structured information about the site
    - description: Assert llms.txt is present and uses markdown headings
      js: |
        const content = await page.textContent('body');
        if (!content || content.trim().length < 50) {
          throw new Error('llms.txt is missing or too short');
        }
        if (!content.includes('#')) {
          throw new Error('llms.txt should use markdown heading structure');
        }
        console.log(`llms.txt found (${content.length} chars)`);

- name: tech-06-ai-crawlers-allowed
  description: Verify robots.txt allows AI search crawlers
  severity: high
  standard: AI-Discoverability
  steps:
    - URL: /robots.txt
    - description: Assert robots.txt does not block AI crawlers
      js: |
        const content = await page.textContent('body');
        const blockedBots = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended'];
        const blocked = blockedBots.filter(bot => {
          const pattern = new RegExp(`User-agent:\\s*${bot}[\\s\\S]*?Disallow:\\s*/`, 'i');
          return pattern.test(content);
        });
        if (blocked.length > 0) {
          throw new Error(`AI crawlers blocked in robots.txt: ${blocked.join(', ')}`);
        }
        console.log('All major AI crawlers are allowed');
    - VERIFY: robots.txt does not block major AI search engine crawlers

- name: cite-01-specific-claims-present
  description: Verify key pages contain specific, citable claims with data
  severity: high
  standard: GEO-Citation-Worthiness
  steps:
    - URL: /
    - description: Assert the landing page has citable statistics
      js: |
        const text = await page.textContent('main') || await page.textContent('body');
        // Check for specific numbers/statistics
        const hasNumbers = /\d+[%xX]|\$[\d,.]+|\d{1,3}(,\d{3})+|\d+\s*(users|customers|companies|teams|downloads)/i.test(text);
        if (!hasNumbers) {
          throw new Error('Landing page lacks specific statistics or data points that AI can cite');
        }
        console.log('Found specific, citable claims with data');
    - VERIFY: Landing page contains specific statistics, benchmarks, or verifiable data points
```

Save all YAML tests to `shiplight/tests/geo-review.test.yaml`.

---

## Depth Levels

- **`--quick`**: llms.txt check + robots.txt AI crawler check + landing page claim analysis. ~2 minutes.
- **default**: All content categories + 3 target query tests in Perplexity. ~10-15 minutes.
- **`--thorough`**: All categories + full AI citation testing across multiple engines + competitor citation analysis + content gap recommendations. ~25-40 minutes.

## Tips

- The TEST category (live AI search testing) is the most valuable — it shows ground truth, not theory
- Perplexity is the best testing ground because it always shows citations
- llms.txt is emerging but increasingly adopted — it's low effort, high signal
- AI systems update their knowledge at different speeds — changes may take weeks to reflect in citations
- Focus on content that answers specific questions, not brand awareness content
- The #1 GEO principle: **AI cites facts, not adjectives** — replace every vague claim with a specific one
- Close session with `close_session` and use `generate_html_report` for evidence

# Platform Ranking Factors (2026)

How each search engine and AI platform decides what to cite. Use this to prioritize optimizations per platform.

---

## 1. Google (Traditional Search)

### Core Ranking Systems

| System | Purpose |
|--------|---------|
| PageRank | Link-based authority |
| BERT | Natural language understanding |
| RankBrain | Machine learning ranking |
| Helpful Content | Rewards people-first content |
| Spam Detection | Filters low-quality content |

### Top Ranking Factors

| Rank | Factor | Details |
|------|--------|---------|
| 1 | Backlinks | Quality referring domains |
| 2 | E-E-A-T | Experience, Expertise, Authority, Trust |
| 3 | Content Quality | Original, comprehensive, helpful |
| 4 | Page Experience | Core Web Vitals (LCP, INP, CLS) |
| 5 | Mobile-First | Non-mobile sites may not be indexed |
| 6 | Search Intent Match | Content matches user query intent |
| 7 | Content Freshness | Regular updates signal activity |
| 8 | Technical SEO | Crawlable, indexable, HTTPS |
| 9 | User Signals | Dwell time, bounce rate, CTR |
| 10 | Structured Data | Schema markup for rich results |

### Core Web Vitals (updated March 2024)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| **INP** (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

> Note: INP replaced FID (First Input Delay) as a Core Web Vital in March 2024.

### Checklist
- [ ] Build quality backlinks (guest posts, PR, original research)
- [ ] Create comprehensive, original content
- [ ] Optimize Core Web Vitals (LCP, INP, CLS)
- [ ] Ensure mobile-friendly design
- [ ] Use HTTPS
- [ ] Implement Schema markup
- [ ] Match content to search intent
- [ ] Update content regularly
- [ ] Add author bios with credentials
- [ ] Include E-E-A-T signals

---

## 2. Google AI Overviews (SGE)

### Architecture

Google AI Overviews use a 5-stage source prioritization pipeline:
1. **Retrieval** -- Identify candidate sources
2. **Semantic Ranking** -- Evaluate topical relevance
3. **LLM Re-ranking** -- Assess contextual fit (Gemini)
4. **E-E-A-T Evaluation** -- Filter for expertise/authority/trust
5. **Data Fusion** -- Synthesize from multiple sources with citations

### Key Statistics

| Metric | Value |
|--------|-------|
| AI Overviews in searches | 85%+ |
| Overlap with traditional Top 10 | Only 15% |
| Traditional factors weight | 62% |
| Novel AI signals weight | 38% |
| SGE-optimized visibility boost | 340% |

### Ranking Factors

| Factor | Impact |
|--------|--------|
| E-E-A-T signals | Primary filter |
| Structured Data (Schema) | Helps AI understand content |
| Knowledge Graph presence | Significant boost |
| Topical Authority | Content clusters + internal linking |
| Authoritative Citations | +132% visibility |
| Authoritative Tone | +89% visibility |
| Multimedia content | Included in multi-modal responses |

### Checklist
- [ ] Implement comprehensive Schema markup
- [ ] Build topical authority with content clusters
- [ ] Include authoritative citations and references
- [ ] Use E-E-A-T signals (author bios, credentials)
- [ ] Add structured data for all content types
- [ ] Target informational "how-to" queries

---

## 3. ChatGPT

### Ranking Factor Weights

| Factor | Weight | Details |
|--------|--------|---------|
| Authority & Credibility | 40% | Branded domains preferred over third-party |
| Content Quality & Utility | 35% | Clear structure, comprehensive answers |
| Platform Trust | 25% | Wikipedia, Reddit, Forbes prioritized |

### Content-Answer Fit Analysis (400K pages study)

| Factor | Relevance |
|--------|-----------|
| Content-Answer Fit | 55% -- Match ChatGPT's response style |
| On-Page Structure | 14% -- Clear headings, formatting |
| Domain Authority | 12% -- Helps retrieval, not citation |
| Query Relevance | 12% -- Match user intent |
| Content Consensus | 7% -- Agreement among sources |

### Key Data Points

- Referring Domains is the strongest predictor. >350K domains = 8.4 avg citations
- Domain Trust Score 97-100 = 8.4 citations per response
- Content updated within 30 days gets 3.2x more citations
- Branded domains cited 11.1 points more than third-party
- ChatGPT has 800+ million weekly active users (2026)
- Cites 2-6 sources per response

### Top Citation Sources

| Rank | Source | % of Citations |
|------|--------|---------------|
| 1 | Wikipedia | 7.8% |
| 2 | Reddit | 1.8% |
| 3 | Forbes | 1.1% |
| 4 | Brand Official Sites | Variable |
| 5 | Academic Sources | Variable |

### Checklist
- [ ] Build strong backlink profile (quality > quantity)
- [ ] Update content within 30 days
- [ ] Use clear H1/H2/H3 structure
- [ ] Include verifiable statistics with citations
- [ ] Write in ChatGPT's conversational style
- [ ] Place 40-60 word answer capsules after H2 headings
- [ ] Ensure domain has high trust score

---

## 4. Perplexity AI

### Architecture

Perplexity uses RAG (Retrieval-Augmented Generation) with a 3-layer reranking system:
1. **L1**: Basic relevance retrieval
2. **L2**: Traditional ranking factors scoring
3. **L3**: ML models for quality evaluation (can discard entire result sets)

### Core Ranking Factors

| Factor | Details |
|--------|---------|
| Authoritative Domain Lists | Manual lists: Amazon, GitHub, academic sites get inherent boost |
| Freshness Signals | Time decay algorithm; content updated within 2-6 months gets 3-4x more citations |
| Semantic Relevance | Content similarity to query (not keyword matching) |
| Topical Weighting | Tech, AI, Science topics get visibility multipliers |
| User Engagement | Click rates, weekly performance metrics |
| FAQ Schema | Pages with FAQ blocks cited more often |
| PDF Documents | Publicly hosted PDFs prioritized |

### Key Data Points

- Perplexity cites 2.76x more sources per question than ChatGPT
- Strongest freshness bias of any AI platform
- Shows domain and publish date alongside citations
- Prefers quotable standalone statements with high factual density
- Cites 5-10 sources per answer

### Technical Requirements

```
User-agent: PerplexityBot
Allow: /
```

### Checklist
- [ ] Allow PerplexityBot in robots.txt
- [ ] Implement FAQ Schema markup
- [ ] Create publicly accessible PDF resources
- [ ] Use Article schema with timestamps
- [ ] Focus on semantic relevance, not keywords
- [ ] Update content every 2-6 months minimum
- [ ] Build topical authority in your niche
- [ ] Place answer capsules (40-60 words) after question-style H2s

---

## 5. Claude AI

### Architecture

Claude uses **Brave Search** (not Google or Bing) for web retrieval.

### Ranking Factors

| Factor | Details |
|--------|---------|
| Brave Index | Must be indexed by Brave Search |
| Query Rewriting | Claude reformulates queries for search |
| Factual Density | Data-rich content strongly preferred |
| Structural Clarity | Easy to extract information |
| Source Authority | Trustworthy, well-sourced content |

### Key Data Points

- Crawl-to-Refer Ratio: 38,065:1 (consumes massive content, very selective about citations)
- Very high factual density preference
- Values clear authoritative definitions and well-established methodologies

### Technical Requirements

```
User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /
```

### Checklist
- [ ] Ensure Brave Search indexing
- [ ] Allow ClaudeBot, Claude-Web, and anthropic-ai in robots.txt
- [ ] Create high factual density content
- [ ] Use clear, extractable structure
- [ ] Include verifiable data points
- [ ] Cite authoritative sources

---

## 6. Microsoft Copilot / Bing AI

### Architecture

Copilot uses the **Bing Index** as its primary data source. Integrated into Edge, Windows 11, Microsoft 365, and Bing Search.

### Ranking Factors

| Factor | Details |
|--------|---------|
| Bing Index | Must be indexed by Bing to be cited |
| Microsoft Ecosystem | LinkedIn, GitHub mentions provide boost |
| Crawlability | Bingbot must have access |
| Page Speed | < 2 seconds load time |
| Schema Markup | Helps Copilot understand content |
| Entity Clarity | Clear definitions of entities/concepts |

### Technical Requirements

```
User-agent: Bingbot
Allow: /

User-agent: msnbot
Allow: /
```

Submit to Bing Webmaster Tools and use IndexNow for faster indexing.

### Checklist
- [ ] Submit site to Bing Webmaster Tools
- [ ] Ensure Bingbot can crawl all pages
- [ ] Use IndexNow for new content
- [ ] Optimize page speed (< 2 seconds)
- [ ] Clear entity definitions in content
- [ ] Build presence on LinkedIn, GitHub

---

## Cross-Platform Summary

| Platform | Primary Index | Key Factor | Unique Requirement |
|----------|--------------|------------|-------------------|
| Google | Google | Backlinks + E-E-A-T | Core Web Vitals |
| Google AI Overviews | Google | E-E-A-T + Schema | Knowledge Graph |
| ChatGPT | Bing-based | Domain Authority | Content-Answer Fit |
| Perplexity | Own + Google | Semantic Relevance | FAQ Schema, freshness |
| Claude | Brave | Factual Density | Brave Search indexing |
| Copilot | Bing | Bing Index | MS Ecosystem presence |

### Universal Best Practices

1. Allow all major bots in robots.txt
2. Serve an llms.txt file at site root
3. Implement Schema markup (FAQPage, Article, Organization)
4. Build authoritative backlinks
5. Update content regularly (within 30 days for max ChatGPT citations)
6. Use clear structure (H1 > H2 > H3, lists, tables)
7. Include statistics and citations with named sources
8. Optimize page speed (< 2 seconds)
9. Ensure mobile-friendly design
10. Place 40-60 word answer capsules after question-style headings

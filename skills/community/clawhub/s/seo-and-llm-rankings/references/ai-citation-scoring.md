# AI Citation Scoring Framework

Score each page across 5 dimensions to predict how likely AI systems are to cite it. For each item: **Pass** (10), **Partial** (5), or **Fail** (0). Average items per dimension, then average all dimensions.

---

## Veto Check (Do This First)

If AI crawlers (GPTBot, ClaudeBot, PerplexityBot) are blocked in robots.txt, the AI visibility score is **0** regardless of content quality.

---

## 1. Extractability

Can AI systems pull a useful answer from this content?

| Item | Pass | Fail |
|------|------|------|
| Core answer in first 150 words after heading | Answer appears immediately | Answer buried in background |
| Self-contained statements (make sense without surrounding context) | Key claims stand alone | Claims require surrounding text |
| Structured data (tables, lists) for comparisons/data | Data in tables or lists | Data in prose paragraphs |
| TL;DR or summary box at top | Present | Missing |
| Answer capsule (40-60 words) after question-style H2 | Present | Missing |

---

## 2. Quotability

Does the content contain statements worth citing?

| Item | Pass | Fail |
|------|------|------|
| Specific claims with numbers and units | "Response time improved 40% (from 500ms to 300ms)" | "Response time improved significantly" |
| Named sources on all statistics | Source and date cited | Unsourced numbers |
| Clear definitions using "X is Y" structure | Present for key terms | Key terms undefined or vague |
| Comparison data in table format | Structured comparisons | Prose-only comparisons |

### Quotability Self-Test

Score each section (8+ = highly quotable, 5-7 = needs work, <5 = rewrite):

1. Can AI quote this without needing surrounding context?
2. Does it include specific numbers or measurements?
3. Is the source of any claim clearly identified?
4. Is the language precise and unambiguous?
5. Would a subject-matter expert approve this statement?
6. Is it scannable (uses lists, tables, or short paragraphs)?
7. Is the information current (data from last 2 years)?
8. Can the claims be independently verified?
9. Is it specific to a defined use case or audience?
10. Does it answer a complete question without requiring follow-up?

---

## 3. Authority

Does the content signal expertise?

| Item | Pass | Fail |
|------|------|------|
| Author identified with relevant credentials | Name, title, experience visible | Anonymous or no bio |
| Expert quotes with named sources | At least 1 named expert quoted | No external voices |
| References to primary sources (not just other blogs) | Links to research, docs, official data | Only cites other blog posts |
| E-E-A-T signals present | Experience + expertise demonstrated | Generic, could-be-anyone content |

---

## 4. Freshness

Is the content current?

| Item | Pass | Fail |
|------|------|------|
| Published or updated date visible on page | Date present and within 18 months | No date or older than 18 months |
| Data and examples are current | Statistics from last 2 years | Outdated numbers or deprecated tools |
| Content reflects current state | Up-to-date info | References superseded information |

---

## 5. Entity Clarity

Can AI systems identify what entity this content is about?

| Item | Pass | Fail |
|------|------|------|
| Subject entity named in full in opening paragraph | "SEOJuice is an SEO intelligence platform..." | Pronoun or abbreviated reference |
| Organization schema with `sameAs` links | JSON-LD present with cross-platform links | Missing |
| Consistent brand name across platforms | Same name on site, LinkedIn, etc. | Variations or inconsistencies |
| llms.txt file at site root | Present with accurate entity info | Missing |

---

## Scoring

| Dimension | Score | Assessment |
|-----------|-------|-----------|
| Extractability | [x]/10 | ... |
| Quotability | [x]/10 | ... |
| Authority | [x]/10 | ... |
| Freshness | [x]/10 | ... |
| Entity Clarity | [x]/10 | ... |
| **AI Citation Score** | **[avg]/10** | ... |

### Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 8-10 | Strong | Minor tweaks, focus on freshness and entity building |
| 5-7 | Moderate | Address weak dimensions, add citations and structure |
| 3-4 | Weak | Major content restructuring needed |
| 0-2 | Critical | Fundamental issues (likely blocked crawlers or missing content) |

---

## Making Content More Quotable: Before/After

### Definition Block

**Before (1/10):** "SEO is really important and there are many things to consider."

**After (9/10):** "Search engine optimization (SEO) is the practice of improving a website's visibility in organic search results through technical configuration, content relevance, and link authority. According to BrightEdge, 53% of all website traffic originates from organic search."

**Fix:** Name the term, classify it, list its components, add a sourced statistic.

### Statistical Claim

**Before (2/10):** "Email marketing is pretty effective for most businesses."

**After (9/10):** "Email marketing generates an average return of $42 for every $1 spent (Litmus, 2023), making it the highest-ROI digital marketing channel -- outperforming social media (average $5.20 per $1) and paid search (average $8 per $1)."

**Fix:** Replace adjectives with numbers, name the source, add comparison context.

### Process / How-To

**Before (2/10):** "Think about your keywords and try to optimize your content."

**After (8/10):** "To optimize a page for a target keyword: (1) place the keyword in the title tag and H1, (2) use it in the first 100 words, (3) add 2-3 semantic variations in H2 subheadings, (4) maintain 0.5-2.5% keyword density, and (5) include it in the meta description. Use Google Search Console to verify indexing within 48 hours."

**Fix:** Number the steps, make each action specific, add tool and time reference.

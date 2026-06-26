# Keyword Research Framework — SEO Blog Planner

A systematic process for discovering, evaluating, and organizing keywords specifically for ecommerce blog content strategies.

## Phase 1: Seed Keyword Generation

### Source 1: Product Catalog Mining
Extract keyword seeds from your existing product catalog:
- Product names and variations
- Product category names
- Key product features and specifications
- Materials and ingredients
- Use cases and applications
- Problem/solution descriptions from product pages

### Source 2: Customer Language Discovery
Identify how real customers describe your products:
- Customer review text (your store and competitor stores)
- Support ticket and FAQ topics
- Social media comments and questions
- Forum discussions in your niche
- "People Also Ask" boxes for product-related queries

### Source 3: Competitor Blog Analysis
Mine competitor blogs for keyword opportunities:
- Titles and H2 headings from their top-performing articles
- Keywords they rank for that you don't cover
- Content topics that generate the most engagement
- Gaps in their coverage you can fill

### Source 4: Modifier Expansion
Apply these modifier patterns to each seed keyword:

**Informational modifiers**:
- "how to [keyword]"
- "what is [keyword]"
- "[keyword] guide"
- "[keyword] tips"
- "[keyword] for beginners"
- "[keyword] mistakes to avoid"
- "[keyword] best practices"

**Commercial investigation modifiers**:
- "best [keyword]"
- "[keyword] reviews"
- "[keyword] vs [alternative]"
- "[keyword] comparison"
- "top [keyword] for [use case]"
- "[keyword] worth it"
- "[keyword] pros and cons"

**Problem-based modifiers**:
- "[keyword] not working"
- "[keyword] problems"
- "how to fix [keyword]"
- "[keyword] troubleshooting"
- "[keyword] alternatives"

**Seasonal and trending modifiers**:
- "best [keyword] [year]"
- "[keyword] [season] [year]"
- "[keyword] black friday"
- "[keyword] gift guide"

## Phase 2: Keyword Evaluation

### Search Volume Assessment
Since this skill operates without live API data, use these directional heuristics:

| Volume Tier | Estimated Range | Typical Characteristics |
|---|---|---|
| High | 1,000+ /mo | Head terms, 1-2 word queries, broad topics |
| Medium | 200-999 /mo | Modified head terms, 3-4 word queries |
| Low | 50-199 /mo | Long-tail, specific queries, niche topics |
| Very Low | <50 /mo | Ultra-specific, question-based, emerging |

**Volume estimation signals**:
- Google Autocomplete suggestions indicate meaningful volume
- "People Also Ask" presence suggests Google sees regular query activity
- Multiple competitors creating content around the term indicates validated demand
- Social media discussion volume correlates with search interest

### Keyword Difficulty Assessment

| Difficulty | Indicators | Blog Viability |
|---|---|---|
| Low | Few authoritative competitors, thin content ranking, forums in top 10 | Ideal — quick win opportunity |
| Medium | Mix of authority sites and smaller blogs ranking, established content | Good — achievable with strong content |
| High | Major publications, Wikipedia, brand sites dominating page 1 | Challenging — needs exceptional content or niche angle |
| Very High | Government sites, medical authorities, massive brands only | Avoid — unrealistic for most ecommerce blogs |

### Search Intent Classification

| Intent | SERP Signals | Content Approach | Commercial Value |
|---|---|---|---|
| Informational | How-to articles, guides, Wikipedia, educational content | Educational blog post, comprehensive guide | Indirect — builds awareness and authority |
| Commercial Investigation | Comparison articles, review sites, "best of" listicles | Comparison post, buyer's guide, roundup | High — reader is actively considering purchase |
| Navigational | Brand homepages, specific product pages | Usually not a blog target | Low — user seeking specific destination |
| Transactional | Product pages, shopping results, pricing pages | Not a blog target — optimize product pages instead | Highest — but belongs on product pages |

### Ecommerce Relevance Score

Rate each keyword 1-5 on product connection strength:

| Score | Connection | Example |
|---|---|---|
| 5 | Keyword directly describes a product you sell | "organic baby lotion" |
| 4 | Keyword describes a use case for your product | "how to moisturize baby eczema" |
| 3 | Keyword is in your product's topic area | "baby skincare routine" |
| 2 | Keyword is adjacent to your niche | "newborn bath temperature" |
| 1 | Keyword is loosely related | "parenting tips for new moms" |

**Minimum viable score**: 2 — anything below rarely justifies ecommerce blog investment

## Phase 3: Keyword Organization

### Clustering Rules
1. **One primary keyword per article** — never target the same primary keyword with two articles
2. **Group by parent topic** — keywords that would be answered by the same comprehensive article belong together
3. **Check SERP overlap** — if Google shows the same pages for two keywords, they belong in one article
4. **Separate by intent** — "best baby lotion" (commercial) and "how to apply baby lotion" (informational) are different articles even though they share a topic
5. **Respect natural hierarchy** — head terms become pillar pages, long-tail variations become cluster articles

### Priority Scoring Matrix

Score each keyword opportunity on four dimensions (1-5 scale each):

| Dimension | Weight | Score Criteria |
|---|---|---|
| Search volume potential | 25% | Higher volume = higher score |
| Keyword difficulty | 25% | Lower difficulty = higher score (inverted) |
| Commercial value | 30% | Stronger product connection = higher score |
| Content effort | 20% | Less production effort = higher score (inverted) |

**Weighted total = (Volume × 0.25) + (Inv. Difficulty × 0.25) + (Commercial × 0.30) + (Inv. Effort × 0.20)**

### Priority Tiers

| Tier | Score | Action | Typical Content |
|---|---|---|---|
| A — High Priority | 3.5-5.0 | Produce first, target month 1-2 | Low-difficulty commercial keywords with clear product ties |
| B — Medium Priority | 2.5-3.4 | Produce in months 2-4 | Medium-difficulty informational keywords building authority |
| C — Lower Priority | 1.5-2.4 | Produce in months 4-6+ | Higher-difficulty or lower-volume opportunities |
| D — Backlog | <1.5 | Park for future consideration | Very high difficulty or weak product connection |

## Phase 4: Cannibalization Prevention

### Pre-Creation Checks
Before assigning a keyword to a new article:
1. Search your own site for the keyword — does existing content already target it?
2. Check if any existing article ranks (even poorly) for this keyword
3. Verify the new article's angle is sufficiently different from existing content
4. Confirm the search intent is distinct from similar existing articles

### Resolution Strategies
| Scenario | Resolution |
|---|---|
| Two articles target same keyword, both weak | Consolidate into one comprehensive article, redirect the other |
| Old article ranks decently, new keyword is similar | Expand the old article to also cover the new keyword |
| Different intent, same topic | Keep separate — ensure titles and H1s clearly signal different intent |
| Multiple thin articles on subtopics | Merge into one pillar article, use subtopics as H2 sections |

## Keyword Research Delivery Format

### Master Spreadsheet Columns
| Column | Description |
|---|---|
| Keyword | The search term |
| Volume estimate | High / Medium / Low / Very Low |
| Difficulty estimate | Low / Medium / High / Very High |
| Intent | Informational / Commercial / Transactional |
| Relevance score | 1-5 product connection rating |
| Priority tier | A / B / C / D |
| Cluster assignment | Which topic cluster |
| Article assignment | Which specific article |
| Product links | Which product/category pages to link |
| Notes | Seasonal relevance, competitor gaps, special considerations |

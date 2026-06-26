# Article Templates

Proven article structures for SaaS content marketing. Based on templates that drove a SaaS from $0 to $1M ARR. Generalized so any SaaS can adapt them.

Every template includes schema markup, CTA placement, internal linking rules, and GEO optimization requirements. Follow them exactly — they work.

---

## Template 1: Competitor Review

The highest-converting template. People reading competitor reviews are actively evaluating options. Your product gets positioned as a credible alternative within an honest review.

| Element | Specification |
|---|---|
| **URL pattern** | `/{cluster}/{competitor}-review` |
| **Title pattern** | `{Competitor} Review 2026: Features, Pricing & Honest Verdict` |
| **Word count** | 1,500-2,000 words |
| **Schema** | Article + FAQPage JSON-LD |
| **Target intent** | Commercial investigation |

### Full structure

```
H1: {Competitor} Review 2026: Features, Pricing & Honest Verdict

H2: What Is {Competitor}?
  - 2-3 sentences defining the product
  - Who it's for
  - What category it belongs to
  - When it was founded / notable traction stats (if available)

H2: {Competitor} Key Features
  H3: Feature 1
  H3: Feature 2
  H3: Feature 3
  H3: Feature 4
  - Be factual. Screenshot or describe each feature honestly.
  - Note what works well AND what's limited.

H2: {Competitor} Pricing
  - Table of all plans with prices
  - Note free trial / free plan availability
  - Call out hidden costs (overages, add-ons, required upgrades)
  - [CTA #1: mid-article] "Looking for a more affordable option? {Your Product} starts at {price}."

H2: {Competitor} Pros and Cons
  - Bulleted pros list (minimum 4)
  - Bulleted cons list (minimum 3)
  - Be genuinely honest — credibility converts more than bias

H2: {Competitor} vs {Your Product}
  - Side-by-side comparison table (features, pricing, ease of use, support)
  - 2-3 paragraphs explaining key differences
  - Focus on where YOUR product has genuine advantages
  - Acknowledge where the competitor is stronger (builds trust)

H2: Best {Competitor} Alternatives
  - List 3-4 alternatives including your product
  - 1-2 sentences each with key differentiator
  - Link to your full "{Competitor} alternatives" article if it exists

H2: Frequently Asked Questions
  - Minimum 4 questions
  - "Is {Competitor} worth it?"
  - "Is {Competitor} free?"
  - "What is the best alternative to {Competitor}?"
  - "How does {Competitor} compare to {Your Product}?"

H2: Final Verdict
  - Honest 2-3 sentence summary
  - Who {Competitor} is best for
  - Who should consider {Your Product} instead
  - [CTA #2: end-of-article] "Try {Your Product} free — no credit card required."
```

### Schema markup

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Competitor} Review 2026: Features, Pricing & Honest Verdict",
  "author": { "@type": "Organization", "name": "{Your Brand}" },
  "datePublished": "2026-XX-XX",
  "dateModified": "2026-XX-XX"
}
```

Plus FAQPage schema wrapping all FAQ items.

### CTA placement

1. **Mid-article** (after Pricing section): soft CTA comparing price or key advantage
2. **End-of-article** (after Final Verdict): direct CTA with free trial link

### Internal linking rules

- Link to your `/{cluster}/best-{competitor}-alternatives` page
- Link to your pillar page `/{cluster}/`
- Link to your product's feature page or landing page
- Link to 1-2 other competitor review pages within the same cluster

### GEO requirements

- Include 2-3 verifiable statistics about the competitor (user count, funding, ratings)
- Use authoritative tone: state facts, not opinions dressed as facts
- Add at least 1 direct quote from a real user review (G2, Capterra, Trustpilot)
- Cite sources for any claims (pricing page URL, review platform)
- Write at 8th-grade reading level for maximum readability

### Example title

> PagePilot AI Review 2026: Features, Pricing & Honest Verdict

---

## Template 2: Competitor Alternatives

People searching for alternatives are already dissatisfied with the competitor. This is your highest-intent opportunity — they want to switch and need a reason.

| Element | Specification |
|---|---|
| **URL pattern** | `/{cluster}/best-{competitor}-alternatives` |
| **Title pattern** | `5 Best {Competitor} Alternatives in 2026` |
| **Word count** | 1,200-1,500 words |
| **Schema** | Article + ItemList + FAQPage JSON-LD |
| **Target intent** | Commercial investigation (high purchase intent) |

### Full structure

```
H1: 5 Best {Competitor} Alternatives in 2026

H2: Why Look for {Competitor} Alternatives?
  - 3-4 common pain points users have with {Competitor}
  - Source these from real reviews (G2, Reddit, Trustpilot)
  - Don't fabricate complaints — use actual user feedback

H2: The 5 Best {Competitor} Alternatives
  H3: 1. {Your Product} — Best for {key differentiator}
    - 3-4 paragraphs
    - Features that solve the pain points listed above
    - Pricing overview
    - Why it's the #1 pick
    - [CTA #1: mid-article] "Try {Your Product} free today."

  H3: 2. {Alternative 2} — Best for {use case}
    - 2-3 paragraphs
    - Honest assessment of strengths
    - Note limitations

  H3: 3. {Alternative 3} — Best for {use case}
    - Same structure as #2

  H3: 4. {Alternative 4} — Best for {use case}
    - Same structure as #2

  H3: 5. {Alternative 5} — Best for {use case}
    - Same structure as #2

H2: {Competitor} Alternatives Comparison Table
  - Table with columns: Tool | Best For | Starting Price | Free Plan | Key Feature
  - All 5 alternatives in rows
  - Your product row highlighted or first

H2: How We Chose These Alternatives
  - Brief methodology (2-3 sentences)
  - Builds E-E-A-T credibility

H2: Frequently Asked Questions
  - "What is the best free alternative to {Competitor}?"
  - "Is {Your Product} better than {Competitor}?"
  - "Which {Competitor} alternative is cheapest?"
  - Minimum 3 questions

H2: Which {Competitor} Alternative Should You Choose?
  - Quick decision framework (if you need X, use Y)
  - [CTA #2: end-of-article] "Start with {Your Product} — {value prop}."
```

### Schema markup

Article schema (same as Template 1) plus:

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "{Your Product}", "url": "https://..." },
    { "@type": "ListItem", "position": 2, "name": "{Alternative 2}", "url": "https://..." },
    { "@type": "ListItem", "position": 3, "name": "{Alternative 3}", "url": "https://..." },
    { "@type": "ListItem", "position": 4, "name": "{Alternative 4}", "url": "https://..." },
    { "@type": "ListItem", "position": 5, "name": "{Alternative 5}", "url": "https://..." }
  ]
}
```

Plus FAQPage schema.

### CTA placement

1. **Mid-article** (after your product's section, Alternative #1): direct CTA while they're impressed
2. **End-of-article** (after conclusion): decision-support CTA

### Internal linking rules

- Link to your `/{cluster}/{competitor}-review` page
- Link to your pillar page `/{cluster}/`
- Link to individual review pages for each alternative mentioned (if they exist)
- Link to your product's pricing or features page
- Cross-link to other "alternatives" pages within the cluster

### GEO requirements

- Cite specific data: pricing numbers, feature counts, G2 ratings with review counts
- Include at least 2 statistics (market share, user satisfaction scores)
- Reference at least 1 expert source or authoritative review
- Use structured comparison (tables) for AI parsability
- Write in clear, factual sentences — AI engines favor scannable content

### Example title

> 5 Best Mailchimp Alternatives in 2026

---

## Template 3: Guide / Tutorial

Informational content that builds topical authority. Not direct conversion content — it earns trust and backlinks. Converts through strategically placed CTAs where your product naturally solves the reader's problem.

| Element | Specification |
|---|---|
| **URL pattern** | `/{cluster}/{slug}` |
| **Title pattern** | Topic-dependent. Use: "How to {Action}" or "{Topic}: A Complete Guide" or "{Number} Ways to {Outcome}" |
| **Word count** | 2,000-3,000 words |
| **Schema** | Article + FAQPage JSON-LD (+ HowTo if step-based) |
| **Target intent** | Informational |

### Full structure

```
H1: {Title — matches target keyword exactly or closely}

H2: {Introduction / What Is Section}
  - Define the topic
  - Why it matters
  - What the reader will learn
  - Brief mention of what tools/approaches exist (sets up your product naturally)

H2: {Core Topic Section 1}
  H3: Sub-topic A
  H3: Sub-topic B
  - Deep, useful content
  - Include data points, examples, or step-by-step instructions

H2: {Core Topic Section 2}
  H3: Sub-topic C
  H3: Sub-topic D
  - [CTA #1: mid-article] Contextual mention of your product
    where it naturally fits the topic. NOT a hard sell.
    Example: "Tools like {Your Product} automate this step, saving ~{X} hours per week."

H2: {Core Topic Section 3}
  H3: Sub-topic E
  H3: Sub-topic F

H2: {Best Practices / Tips / Common Mistakes}
  - Actionable list
  - Position your product as one of the tools that helps follow best practices

H2: Frequently Asked Questions
  - Minimum 5 questions
  - Target "People Also Ask" queries from SERP research
  - Each answer: 2-4 sentences, direct and factual

H2: {Conclusion / Summary}
  - Key takeaways (3-5 bullet points)
  - [CTA #2: end-of-article] "{Your Product} helps you {benefit}. Try it free."
```

### Structure rules

- Strict H1 > H2 > H3 hierarchy. Never skip levels.
- Every H2 must have at least 150 words under it.
- Use short paragraphs (2-4 sentences max).
- Use bullet points for lists of 3+ items.
- Include at least 1 table, 1 list, and 1 example per article.

### Schema markup

Article schema. FAQPage schema for the FAQ section.

If the guide is step-based ("How to..."), also add HowTo schema:

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to {Action}",
  "step": [
    { "@type": "HowToStep", "name": "Step 1 title", "text": "Step 1 description" },
    { "@type": "HowToStep", "name": "Step 2 title", "text": "Step 2 description" }
  ]
}
```

### CTA placement

1. **Mid-article** (in the section where your product most naturally fits): contextual, soft CTA
2. **End-of-article** (after conclusion): direct CTA with free trial or signup link

CTAs in guides must feel natural. Hard sells in educational content destroy trust and increase bounce rate.

### Internal linking rules

- Link to your pillar page `/{cluster}/`
- Link to 2-3 related sub-pages within the cluster
- Link to relevant comparison or review pages where your product is mentioned
- Link to 1 external authoritative source (builds E-E-A-T)
- Every guide should receive a link FROM the pillar page

### GEO requirements

GEO (Generative Engine Optimization) is critical for guides — AI engines heavily favor well-structured informational content. Apply these boosts:

| GEO tactic | Visibility boost | How to apply |
|---|---|---|
| **Citations** | +40% | Cite at least 3 external sources with URLs. Industry reports, studies, official documentation. |
| **Statistics** | +37% | Include at least 4 data points. Growth rates, benchmarks, survey results. Always cite the source. |
| **Expert quotes** | +30% | Include 1-2 quotes from named experts, published authors, or recognized practitioners. Attribute clearly. |
| **Authoritative tone** | +25% | Write as an expert. No hedging ("might", "could", "perhaps"). State what works and why. |
| **Readability** | +20% | 8th-grade reading level. Short sentences. One idea per paragraph. Use Hemingway App or similar. |

### Example title

> How to Automate Your Shopify Product Descriptions in 2026

---

## Template 4: Theme/Tool Review

Review a tool, theme, plugin, or resource in your product's ecosystem. The key angle: "This tool does X, but {Your Product} does this automatically." You're not trashing the tool — you're showing there's a better way.

| Element | Specification |
|---|---|
| **URL pattern** | `/{cluster}/{tool-name}-review` |
| **Title pattern** | `{Tool} Review 2026: Features, {Key Metric} & Is It Worth It?` |
| **Word count** | 1,200-1,800 words |
| **Schema** | Article + FAQPage JSON-LD |
| **Target intent** | Commercial investigation |

### Full structure

```
H1: {Tool} Review 2026: Features, {Key Metric} & Is It Worth It?

H2: What Is {Tool}?
  - 2-3 sentences defining the tool
  - What category / ecosystem it belongs to (e.g., Shopify theme, WordPress plugin)
  - Who typically uses it

H2: {Tool} Key Features
  H3: Feature 1
  H3: Feature 2
  H3: Feature 3
  - Honest feature walkthrough
  - Include screenshots or specific descriptions where possible

H2: {Tool} {Key Metric} (Performance / Speed / Results)
  - The metric that matters most for this tool type
  - For themes: page speed, mobile score, conversion rate
  - For plugins: performance impact, ease of setup
  - For software: output quality, time saved
  - Use real data or benchmarks when available

H2: {Tool} Pricing
  - Plans and costs
  - Free version limitations
  - Value assessment

  [CTA #1: mid-article] "Instead of paying {price} for {Tool}, 
  {Your Product} includes {equivalent feature} automatically. Try it free."

H2: {Tool} Pros and Cons
  - Balanced pros (minimum 3) and cons (minimum 3)

H2: Do You Actually Need {Tool}? (The Better Alternative)
  - This is the conversion section
  - Explain what problem {Tool} solves
  - Show how {Your Product} solves it differently / better / automatically
  - Specific comparison of workflow: with {Tool} vs with {Your Product}
  - NOT a hard sell — a logical argument

H2: Frequently Asked Questions
  - "Is {Tool} worth buying?"
  - "What is the best alternative to {Tool}?"
  - "Does {Tool} work with {platform}?"
  - Minimum 3 questions

H2: Final Verdict
  - Who should use {Tool}
  - Who should use {Your Product} instead
  - [CTA #2: end-of-article] "Skip {Tool} — {Your Product} does this automatically. Start free."
```

### Schema markup

Article + FAQPage JSON-LD (same pattern as Template 1).

### CTA placement

1. **Mid-article** (after Pricing): comparison-based CTA showing your product as the alternative
2. **End-of-article** (after Verdict): direct CTA

### Internal linking rules

- Link to your pillar page `/{cluster}/`
- Link to other tool/theme reviews within the same cluster
- Link to your main competitor alternatives page
- Link to a relevant guide that covers the broader topic

### GEO requirements

- Include the tool's actual pricing numbers and update dates
- Reference user reviews from app stores, G2, or marketplaces
- Include at least 1 performance metric or benchmark
- Cite the tool's official documentation for feature claims
- Maintain honest, balanced tone — AI engines detect and penalize biased content

### Example title

> Flavor Theme Review 2026: Features, Speed & Is It Worth It?

---

## Template 5: Hub/Pillar Page

The center of every content cluster. This page targets your highest-volume keyword for the cluster and links to every sub-page. It's how you build topical authority — Google sees one authoritative hub covering every angle of the topic.

| Element | Specification |
|---|---|
| **URL pattern** | `/{cluster}/` or `/{cluster}/{primary-keyword}` |
| **Title pattern** | `{Primary Keyword}: The Complete Guide` or `Best {Category} Tools & Software in 2026` |
| **Word count** | 2,500-3,500 words |
| **Schema** | Article + ItemList + FAQPage JSON-LD |
| **Target intent** | Mixed (informational + commercial) |

### Full structure

```
H1: {Primary Keyword — exact match or close variant}

H2: What Is {Topic}? (Overview)
  - Define the topic comprehensively
  - Who needs to understand this
  - Why it matters in 2026
  - Set the scope of what this guide covers

H2: {Sub-topic 1 — matches a sub-page's topic}
  - 200-400 word overview of this sub-topic
  - Key points only — the sub-page goes deep
  - [Internal link to sub-page 1]
  - "Read more: {sub-page title}"

H2: {Sub-topic 2 — matches a sub-page's topic}
  - Same structure as above
  - [Internal link to sub-page 2]

H2: {Sub-topic 3 — matches a sub-page's topic}
  - Same structure
  - [Internal link to sub-page 3]

  [CTA #1: mid-article] "{Your Product} helps you {benefit related to the cluster topic}. 
  See how it works."

H2: {Sub-topic 4 — matches a sub-page's topic}
  - [Internal link to sub-page 4]

H2: {Sub-topic 5 — matches a sub-page's topic}
  - [Internal link to sub-page 5]

H2: {Comparison Table of Solutions / Tools}
  - Table comparing all tools/solutions mentioned across the cluster
  - Columns: Tool | Best For | Price | Rating | Key Feature
  - Your product included and fairly positioned
  - This section targets "best X" search queries

H2: How to Choose the Right {Solution/Tool}
  - Decision criteria (3-5 factors)
  - Decision tree or "if you need X, choose Y" format
  - Position your product for the most common use case

H2: Frequently Asked Questions
  - Minimum 6 questions (pillar pages need more FAQ coverage)
  - Mix of informational and commercial intent questions
  - Target "People Also Ask" from SERP analysis

H2: {Summary / Getting Started}
  - Recap key takeaways
  - Clear next steps for the reader
  - [CTA #2: end-of-article] "Get started with {Your Product} — 
    {specific value prop}. Free trial, no credit card."
```

### Critical rule: link to ALL cluster sub-pages

The pillar page MUST link to every sub-page in the cluster. If you have 8 sub-pages, the pillar links to all 8. This is non-negotiable — it's how cluster authority works.

Maintain a linking checklist:

```
Cluster: {cluster name}
Pillar: /{cluster}/{primary-keyword}
Sub-pages:
  [ ] /{cluster}/{competitor-1}-review
  [ ] /{cluster}/best-{competitor-1}-alternatives
  [ ] /{cluster}/{competitor-2}-review
  [ ] /{cluster}/{tool-1}-review
  [ ] /{cluster}/{guide-slug}
  [ ] /{cluster}/{guide-slug-2}
```

### Schema markup

Article schema. ItemList schema for the comparison table. FAQPage schema for FAQ.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best {Category} Tools in 2026",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "{Tool 1}", "url": "..." },
    { "@type": "ListItem", "position": 2, "name": "{Tool 2}", "url": "..." }
  ]
}
```

### CTA placement

1. **Mid-article** (after 3rd sub-topic section, ~60% through): contextual CTA
2. **End-of-article** (after summary): strong direct CTA

### Internal linking rules

- Link to EVERY sub-page in the cluster (mandatory)
- Receive links FROM every sub-page in the cluster (sub-pages must link back here)
- Link to 1-2 pillar pages from other clusters (cross-cluster authority)
- Link to your product's main landing page or features page

### GEO requirements

- Pillar pages must be the most comprehensive content on the topic
- Include at least 5 statistics with sources
- Include at least 2 expert quotes or cited opinions
- Use comparison tables — AI engines parse structured data more effectively
- Cover the topic from multiple angles (what, why, how, who, when, tools, examples)
- Update quarterly — stale pillar pages lose authority fast

### Example title

> Best AI Store Builders in 2026: Tools, Comparisons & How to Choose

---

## Template 6: Custom Template Creation

The five templates above cover the most common SaaS content formats. But your SaaS may need something specific — a landing page template, a case study format, an integration page, a changelog-style article.

Here's how to create a new template that fits this system.

### When to create a custom template

Create a new template when:
- You're writing 3+ articles with the same structure
- None of the existing templates fit the content format
- The content has a distinct search intent (e.g., "X integration", "X for Y industry")

Do NOT create a new template for one-off articles.

### Blank template skeleton

Copy this skeleton and fill in every field. If a field doesn't apply, mark it "N/A" with a reason.

```
## Template: {Template Name}

{One sentence: what this template is for and why it converts.}

| Element | Specification |
|---|---|
| **URL pattern** | `/{cluster}/{slug-pattern}` |
| **Title pattern** | `{Title with placeholders}` |
| **Word count** | {min}-{max} words |
| **Schema** | {Required schema types, e.g., Article + FAQPage} |
| **Target intent** | {Informational / Commercial / Transactional / Navigational} |

### Full structure

H1: {Title pattern}

H2: {Section 1 name}
  - {What goes here}

H2: {Section 2 name}
  - {What goes here}

[CTA #1: mid-article] {CTA text pattern and placement trigger}

H2: {Section 3 name}
  - {What goes here}

H2: Frequently Asked Questions
  - {Minimum number} questions
  - {Types of questions to include}

H2: {Conclusion section name}
  - {What goes here}
  - [CTA #2: end-of-article] {CTA text pattern}

### Schema markup
{JSON-LD examples for each required schema type}

### CTA placement
1. **Mid-article** ({after which section}): {CTA type — soft/contextual/direct}
2. **End-of-article** ({after which section}): {CTA type}

### Internal linking rules
- {Rule 1: link to pillar page}
- {Rule 2: link to related sub-pages}
- {Rule 3: link to product pages}
- {Rule 4: cross-cluster links}

### GEO requirements
- Citations: {minimum number, types of sources}
- Statistics: {minimum number, types of data}
- Expert quotes: {minimum number, attribution requirements}
- Tone: {authoritative / conversational / technical}
- Readability: {target grade level}

### Example title
> {Actual example with real-looking placeholder values}
```

### Required elements checklist

Every custom template MUST include these elements. If you skip one, the template is incomplete.

| Required element | Why |
|---|---|
| URL pattern | Consistent URL structure across the cluster |
| Title pattern with year | Year in title improves CTR by 10-15% for commercial queries |
| Word count range | Prevents thin content (under-optimized) and bloat (over-optimized) |
| FAQ section | FAQPage schema drives featured snippets and "People Also Ask" |
| Schema markup | Structured data improves rich snippet eligibility |
| CTA at mid-article | Captures readers who won't scroll to the bottom (50%+ of visitors) |
| CTA at end-of-article | Captures engaged readers who finished the piece |
| Internal links to pillar | Maintains cluster structure and passes authority |
| Internal links from pillar | Pillar must be updated to link to this new page |
| GEO citation requirements | AI search engines favor content with verifiable sources |
| Comparison element | Table or side-by-side — AI engines and users both prefer structured comparisons |

### Validation

Before using a new template, verify:

1. Does the title pattern include the primary keyword?
2. Does the URL pattern fit within an existing cluster?
3. Is the word count range realistic for the topic depth?
4. Are there at least 2 CTAs (mid + end)?
5. Does it link back to the pillar page?
6. Does the pillar page link to it?
7. Are GEO requirements specified (citations, stats, quotes)?
8. Is schema markup defined for all structured data?

If any answer is "no," fix the template before writing content with it.

---

## Quick reference: all templates

| Template | URL pattern | Words | Schema | Best for |
|---|---|---|---|---|
| Competitor Review | `/{cluster}/{competitor}-review` | 1,500-2,000 | Article + FAQPage | Bottom-of-funnel, competitor traffic |
| Competitor Alternatives | `/{cluster}/best-{competitor}-alternatives` | 1,200-1,500 | Article + ItemList + FAQPage | Highest purchase intent |
| Guide / Tutorial | `/{cluster}/{slug}` | 2,000-3,000 | Article + FAQPage (+ HowTo) | Topical authority, backlinks |
| Theme/Tool Review | `/{cluster}/{tool-name}-review` | 1,200-1,800 | Article + FAQPage | Ecosystem traffic, product positioning |
| Hub/Pillar Page | `/{cluster}/` | 2,500-3,500 | Article + ItemList + FAQPage | Cluster authority, high-volume keywords |
| Custom | User-defined | User-defined | Minimum: Article + FAQPage | SaaS-specific formats |

---

## Universal rules (apply to ALL templates)

### CTA rules
- Every article gets exactly 2 CTAs: one mid-article, one end-of-article
- Mid-article CTA is contextual (relates to the section it's in)
- End-of-article CTA is direct (free trial, signup, demo)
- Never use more than 2 CTAs — more feels spammy and hurts conversion

### Internal linking rules
- Every sub-page links to its cluster's pillar page
- Every pillar page links to all its sub-pages
- Sub-pages link to 2-3 sibling pages within the cluster
- Use descriptive anchor text (not "click here" or "read more")

### GEO baseline (minimum for every article)
- At least 2 cited sources with URLs
- At least 2 statistics with attribution
- FAQPage schema on every article
- 8th-grade reading level
- Authoritative tone — no hedging language

### Title rules
- Include the primary keyword
- Include the current year for commercial content
- Keep under 60 characters for full SERP display
- Front-load the keyword (put it as early in the title as possible)

### Meta description rules
- 150-160 characters
- Include the primary keyword
- Include a value proposition or key finding
- End with a soft CTA or curiosity hook

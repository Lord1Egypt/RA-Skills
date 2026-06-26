---
name: seo-keyword-researcher
description: "Research SEO keywords for any topic and generate a complete article brief with primary keyword, secondary keywords, competition analysis, article structure, and SEO recommendations. Use when: (1) planning new content for TechStack.dev, (2) researching keywords for SEO articles, (3) creating content strategy, (4) identifying low-competition keywords, (5) building an article outline. Triggers on: keyword research, SEO article ideas, what keywords should I target, article topic research, SEO brief, content planning, keyword analysis."
---

# SEO Keyword Researcher

Research keywords and produce a complete article brief ready for writing.

## Workflow

### Step 1: Seed Research
Run 3 searches simultaneously:
```
web_search: "[topic] + '2026'" (get trending angle)
web_search: "[topic] best/top X compared 2026"
web_search: "[topic] guide tutorial how to 2026"
```

### Step 2: Competitor Analysis
Fetch the top 2-3 ranking pages from results:
```
web_fetch: [top URL], maxChars=3000 each
```
Extract: title structure, H2 headings, word count, featured snippet patterns.

### Step 3: Generate Keyword Cluster
From the seed searches and competitor analysis, identify:
- **Primary keyword:** Highest search intent match, moderate competition
- **Secondary keywords (5-10):** Long-tail variations, questions, comparisons
- **Question keywords:** "how to", "what is", "why does", "best way to"
- **LSI keywords:** Related terms that signal topical authority

### Step 4: Write Article Brief
Output a markdown brief with:
1. Article title (H1) — include primary keyword
2. Meta description (155 chars max)
3. Primary + secondary keywords
4. Competitor gap analysis
5. Recommended article structure (H2s with sub-points)
6. Word count target
7. SEO recommendations (internal links to add, CTA to include)

## Reference
See `references/seo-checklist.md` for the on-page SEO checklist to apply before publishing.
See `references/keyword-research-methods.md` for advanced keyword clustering techniques.

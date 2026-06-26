---
name: seo-2026
description: SEO content strategy for the AI Overviews era (2026). Research keywords, analyze SERP + AI citations, generate blog posts optimized for both Google ranking AND AI citation. Handles keyword research, competitor gap analysis, content briefs, full article generation with schema markup, and AI-citation-optimized structure. Use when asked to write blog posts, do keyword research, create content briefs, optimize for SEO, improve search rankings, get cited by AI, or build topic cluster authority.
---

# SEO 2026 -- AI-Era Content Engine

SEO has changed. AI Overviews appear on 48% of Google queries. Getting cited by AI systems (Google AIO, ChatGPT, Perplexity) is now as important as ranking in the top 10. This skill handles both.

## Quick Start

User says "write a blog post about X" or "do keyword research for X":

1. Run keyword research (Step 1)
2. Analyze top SERP results + AI Overview citations (Step 2)
3. Generate content brief (Step 3)
4. Write the article with AI-citation-optimized structure (Step 4)
5. Generate schema markup (Step 5)

## Step 1: Keyword Research

Use web_search to find keyword opportunities:

```
web_search: "[topic] site:ahrefs.com OR site:semrush.com keyword difficulty"
web_search: "people also ask [topic]"
web_search: "[topic]" (examine autocomplete suggestions)
```

Evaluate each keyword on:
- **Search intent**: informational, transactional, commercial, navigational
- **AI Overview presence**: does this query trigger an AI Overview? (search it)
- **Competition**: who ranks? How deep is their content?
- **Topic cluster fit**: does it connect to other keywords we target?

Output a keyword map: primary keyword + 5-10 secondary/LSI keywords + intent classification.

For detailed keyword research methodology, see references/keyword-research.md.

## Step 2: SERP + AI Citation Analysis

For the primary keyword, analyze what currently ranks:

1. **web_search the keyword** -- note top 5 results
2. **web_fetch top 3 results** -- analyze structure, depth, word count, headings
3. **Check for AI Overview** -- search the query, note what gets cited
4. **Identify gaps** -- what do competitors miss? What questions go unanswered?

Key metrics to extract:
- Average word count of top results
- Common H2/H3 headings across competitors
- Topics covered vs. topics missing
- Citation patterns in AI Overview (if present)

For the AI citation analysis framework, see references/ai-citation.md.

## Step 3: Content Brief

Generate a brief containing:

```markdown
# Content Brief: [Title]

**Primary keyword:** [keyword]
**Secondary keywords:** [list]
**Search intent:** [informational/transactional/etc.]
**Target word count:** [based on competitor analysis, typically 2000-4000]
**AI Overview status:** [present/absent for this query]

## Required Sections
- [H2 headings based on competitor analysis + gap fill]

## Questions to Answer
- [From "People Also Ask" + competitor gaps]

## Differentiation Angle
- [What we cover that competitors don't]

## Internal Links
- [Other pages on the site to link to/from]

## Citation Optimization Notes
- [Specific stats, data, or claims to include for AI citation]
```

## Step 4: Write the Article

Follow this structure for maximum ranking + AI citation potential:

### AI-Citation-Optimized Structure

1. **Lead with a direct answer** (40-60 words) before any elaboration. AI systems extract the first substantive paragraph.

2. **Use clear H2/H3 hierarchy** matching search intent. Each H2 section should be self-contained (134-167 words) -- this matches the AI extraction window.

3. **Include stats with source attribution every 150-200 words.** AI systems cite data-rich content. Format: "According to [Source], [specific stat]."

4. **Add a summary table or comparison** if applicable. AI systems frequently cite tabular data.

5. **Answer "People Also Ask" questions** as H2 sections with concise 2-3 sentence answers followed by elaboration.

6. **Keep paragraphs to 2-3 sentences max.** Shorter paragraphs = easier AI extraction.

7. **Include an FAQ section** with JSON-LD FAQ schema.

### Content Quality Rules

- **E-E-A-T signals**: include author credentials, first-hand experience, specific examples
- **Definite language**: AI systems prefer "X costs $29/month" over "X may cost around $29/month"
- **Entity density**: mention specific tools, people, companies by name (AI citation relies on entity matching)
- **Fresh data**: ~50% of AI-cited content is less than 13 weeks old. Include current-year data.
- **2000+ words minimum**: pages over 20K characters average 4.3x more AI citations

### Meta Tags

```markdown
Title: [Primary keyword] -- [benefit or year] (50-60 chars)
Meta description: [Direct answer to query + CTA] (150-160 chars)
```

For the complete writing checklist, see references/writing-checklist.md.

## Step 5: Schema Markup

Generate JSON-LD for:
- **Article schema** (always)
- **FAQ schema** (if FAQ section exists)
- **HowTo schema** (if tutorial content)
- **BreadcrumbList** (always)

See references/schema-templates.md for copy-paste JSON-LD templates.

## Topic Cluster Strategy

Single pages rank worse than topic clusters in 2026. Build clusters:

```
Pillar page: "Complete Guide to [Topic]" (3000-5000 words)
  |-- Cluster: "[Topic] for beginners" (2000 words)
  |-- Cluster: "[Topic] vs [Alternative]" (2000 words)
  |-- Cluster: "Best [Topic] tools/tips" (2000 words)
  |-- Cluster: "[Topic] common mistakes" (1500 words)
  |-- Cluster: "[Topic] advanced guide" (2500 words)
```

Each cluster page links to the pillar and to other cluster pages. This builds topical authority that AI systems use for entity confidence scoring.

## GEO: Generative Engine Optimization

Beyond traditional SEO, optimize for AI search engines:

1. **Multi-source corroboration**: get your brand mentioned on 3+ independent domains (guest posts, interviews, directories)
2. **Structured claims**: use definite language with numbers ("reduces cost by 40%") not vague claims
3. **Question-answer format**: AI systems love extracting Q&A pairs
4. **Update frequency**: refresh content every 8-12 weeks to stay within the 13-week citation window

## Common Mistakes

- Writing for keywords without checking search intent -- wrong format = no ranking
- Ignoring AI Overviews -- if AIO shows for your keyword, optimize for citation, not just ranking
- Thin content (<1000 words) -- deep content gets 4.3x more AI citations
- No internal linking -- destroys topic cluster authority
- Stale content -- AI systems prefer content < 13 weeks old
- Generic headings -- H2s should match actual search queries

# SEO Competitor Analyzer

Deep-dive analysis of competitor websites to uncover keyword gaps, content opportunities, and SEO weaknesses. Outputs a prioritized action plan you can execute immediately.

## When to use

Use this skill when the user needs to:
- Understand why competitors rank higher
- Find untapped keyword opportunities in their niche
- Audit a competitor's content strategy
- Identify backlink and authority gaps
- Build a data-driven SEO content calendar
- Evaluate a new niche before entering it

## How it works

1. Ask for the user's website URL (or niche if no site yet)
2. Ask for 2–5 competitor URLs to analyze
3. Ask for their primary goal (rank higher / find content gaps / build backlinks / enter new niche)
4. Perform structured analysis across 6 dimensions
5. Output prioritized recommendations with effort/impact scores

## Analysis Dimensions

### 1. Content Gap Analysis
- Topics competitors cover that the user does not
- Identify thin content opportunities (low word count, low competition)
- Find featured snippet opportunities (questions, lists, definitions)
- Map content by funnel stage (awareness / consideration / decision)

### 2. Keyword Strategy Breakdown
- Infer primary and secondary keywords from page titles, H1s, meta descriptions
- Identify keyword clusters competitors are targeting
- Flag high-volume, low-competition gaps
- Note keywords where multiple competitors rank but the user does not

### 3. On-Page SEO Audit (per competitor)
- Title tag format and length patterns
- Meta description quality and CTR optimization
- URL structure and slug patterns
- Internal linking strategy
- Schema markup usage
- Image optimization signals

### 4. Content Quality Assessment
- Average word count for top-ranking pages
- Content freshness (update frequency signals)
- Use of multimedia (images, video, tables, lists)
- E-E-A-T signals (author bios, citations, expertise markers)
- Readability and structure analysis

### 5. Technical SEO Signals
- Page speed indicators (Core Web Vitals hints)
- Mobile-first signals
- HTTPS status
- Sitemap and robots.txt structure
- Crawlability signals

### 6. Opportunity Scoring
Rate each opportunity on:
- **Search Volume Potential**: High / Medium / Low
- **Competition Level**: Hard / Medium / Easy
- **Implementation Effort**: 1–5 (1 = quick win)
- **Expected Impact**: 1–5 (5 = transformational)
- **Priority Score**: (Impact × Volume) ÷ Effort

## Output Format

```
=== SEO COMPETITOR ANALYSIS ===
Analyzed: [user site] vs [competitor 1], [competitor 2], [competitor 3]
Date: [current date]

--- TOP 3 QUICK WINS (do these first) ---

1. [Action] — [Expected result] | Effort: 2/5 | Impact: 4/5
2. [Action] — [Expected result] | Effort: 1/5 | Impact: 3/5
3. [Action] — [Expected result] | Effort: 2/5 | Impact: 4/5

--- CONTENT GAP OPPORTUNITIES ---

| Topic | Competitor Ranking | Est. Volume | Difficulty | Priority |
|-------|-------------------|-------------|------------|----------|
| [topic] | [competitor] | High | Easy | ⭐⭐⭐⭐⭐ |
...

--- KEYWORD CLUSTERS TO TARGET ---
Cluster 1: [theme] → [keyword 1], [keyword 2], [keyword 3]
Cluster 2: ...

--- ON-PAGE SEO PATTERNS (what's working for competitors) ---
- Title format: "[Primary KW] + [Secondary KW] | [Brand]"
- Average content length: [X] words
- Schema types used: Article, FAQPage, HowTo
- Update frequency: [monthly / quarterly]

--- 30-DAY ACTION PLAN ---
Week 1: [specific task]
Week 2: [specific task]
Week 3: [specific task]
Week 4: [specific task]

--- COMPETITOR PROFILES ---
[Competitor 1]:
  Strengths: ...
  Weaknesses: ...
  Best pages to beat: ...
```

## Pro Tips Built Into Analysis

- Always check for "People Also Ask" gaps — easy featured snippets
- Long-tail keywords in H2/H3 headings are goldmines
- If 3+ competitors cover a topic but none has >1500 words, you can win with depth
- FAQ sections on existing pages can capture question-based searches overnight

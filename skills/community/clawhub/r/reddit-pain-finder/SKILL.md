---
name: reddit-pain-finder
description: Mine Reddit for real user pain points, product complaints, and unmet needs. Identify micro-SaaS opportunities, content gaps, and service demands by analyzing subreddit conversations at scale. Perfect for founders, product builders, and content marketers.
metadata:
  version: 1.0.0
  author: TKDigital
  category: Research & Analysis
  tags: [reddit, market research, pain points, saas ideas, product research, competitive intelligence, content gaps]
---

# Reddit Pain Finder

Mine Reddit conversations to discover real pain points, product gaps, and business opportunities.

## What It Does

1. **Pain Point Extraction** — Scans subreddits for complaints, frustrations, and "I wish there was..." posts
2. **Opportunity Scoring** — Rates each pain point by frequency, intensity, and monetization potential
3. **Competitor Gap Analysis** — Identifies where existing solutions fall short (based on user complaints)
4. **Content Gap Discovery** — Finds questions asked repeatedly with no good answers
5. **Trend Detection** — Spots emerging problems before they become mainstream

## Usage

### Find Pain Points in a Niche
```
Search Reddit for pain points in the [NICHE] space.

Subreddits to scan: r/[sub1], r/[sub2], r/[sub3]
Timeframe: Last 6 months
Minimum engagement: 10+ upvotes or 5+ comments

For each pain point found:
1. The problem (in the user's own words)
2. Frequency (how often it's mentioned)
3. Intensity (mild annoyance vs hair-on-fire)
4. Existing solutions mentioned (and why they fail)
5. Monetization angle (product, service, or content opportunity)
6. Sample quotes from real posts

Rank by opportunity score (frequency × intensity × monetization potential).
```

### Validate a Product Idea
```
I'm building [PRODUCT IDEA].

Search Reddit for:
1. People complaining about this exact problem
2. Existing solutions they've tried (and why they switched/quit)
3. Feature requests that match my planned features
4. Price sensitivity signals (what they're willing to pay)
5. Objections I should address in marketing

Subreddits: r/[relevant subs]
Give me a GO / MAYBE / NO-GO recommendation with evidence.
```

### Find Content Ideas
```
What questions are asked repeatedly in r/[SUBREDDIT] that have no definitive answer?

For each question:
1. The question (paraphrased)
2. How many times it's been asked (estimate)
3. Quality of existing answers (good/mediocre/bad)
4. Content format that would best answer it (blog/video/tool/course)
5. SEO potential (would people Google this?)

Give me 20 content ideas ranked by potential traffic.
```

### Competitive Intelligence
```
What do Reddit users say about [COMPETITOR PRODUCT]?

Find:
1. Top 5 complaints (with quotes)
2. Top 5 praised features
3. Common reasons for churning
4. Feature requests they ignore
5. Alternative products users mention
6. Price complaints or comparisons

Subreddits: r/[relevant subs]
```

## Output Format

```
# Reddit Pain Finder Report — [Niche/Topic]

## Top Pain Points (Ranked by Opportunity Score)

### 1. [Pain Point Title] — Score: [X/30]
- **Frequency**: [X/10] — Mentioned [N] times across [subreddits]
- **Intensity**: [X/10] — [mild frustration / significant problem / hair-on-fire]
- **Monetization**: [X/10] — [product / service / content / tool]
- **Summary**: [2-3 sentences]
- **User Quotes**:
  > "[Exact quote from Reddit post]" — r/[subreddit], [upvotes] upvotes
  > "[Another quote]" — r/[subreddit]
- **Existing Solutions**: [What's available and why it fails]
- **Opportunity**: [Specific product/service/content that would solve this]
- **Estimated Market**: [Who would pay for this and how much]

### 2. [Next Pain Point]
...

## Content Gaps
[Questions with no good answers]

## Emerging Trends
[Problems gaining momentum]

## Recommendations
[Top 3 actionable next steps]
```

## Best Practices

- Target subreddits with 50K-500K members (large enough for data, small enough for niche specificity)
- Focus on posts with 10+ upvotes (social proof of shared pain)
- Look for "I've tried everything" posts — these indicate strong willingness to pay
- Cross-reference pain points across 3+ subreddits for validation
- Pay attention to comment sections — the real insights are in replies
- Combine with `saas-idea-validator` for full opportunity assessment

## References

- `references/high-value-subreddits.md` — Curated list of business-opportunity-rich subreddits
- `references/scoring-rubric.md` — Detailed explanation of opportunity scoring

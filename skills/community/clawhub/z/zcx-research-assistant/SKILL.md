---
name: research-assistant
description: Conduct multi-source deep research and generate structured reports. Use when the user needs to: (1) investigate a company, industry, or topic from multiple angles, (2) cross-verify information across sources, (3) generate SWOT analysis, competitor analysis, or industry research reports, (4) compile a structured research brief with source citations.
emoji: 🔬
---

# Research Assistant — 深度研究助手

Conduct multi-source deep research with cross-verification, structured report generation, and full source attribution.

## Research Workflow

```
1. Clarify Scope  →  What's the research question? What depth is needed?
2. Multi-Source   →  Search across at least 3 independent sources
3. Cross-Verify   →  Identify conflicts, confirm consensus
4. Synthesize     →  Build structured report
5. Cite Sources   →  Every claim gets a source URL
```

Always follow this order. Do not skip cross-verification.

## Step 1 — Clarify Scope

Ask yourself:
- **Topic:** What exactly is being researched?
- **Depth:** Quick brief (3-5 key points) vs deep report (SWOT, data, trends)?
- **Timeframe:** Current snapshot, historical trend, or future outlook?
- **Geography:** Global, regional (APAC, EU, US), or specific country (China)?
- **Audience:** Technical (data-heavy) vs executive (summary + recommendations)?

Output: A 1-2 sentence research objective statement.

## Step 2 — Multi-Source Retrieval

### Method A: Web Search (Broad Discovery)

```
web_search(query="<topic> <context>", count=5-10)
```

**Search strategy — use 3-5 search queries per research topic:**
1. **Overview:** `"<topic>" overview 2026`
2. **Data/statistics:** `"<topic>" statistics data market size`
3. **News/recent:** `"<topic>" latest news 2026`
4. **Competitors:** `"<topic>" competitors leading companies`
5. **Analysis:** `"<topic>" analysis report SWOT`

### Method B: Deep Fetch (Page-Level Detail)

For each promising search result, fetch the full page:
```
web_fetch(url, extractMode="markdown", maxChars=15000)
```

Prioritize sources in this order:
1. **Primary sources** — Official company reports, government data, regulatory filings
2. **Industry sources** — Specialized trade publications, analyst reports
3. **Major media** — Established financial/industry news outlets
4. **Secondary sources** — Aggregators, summaries, blogs (lowest priority)

**Minimum source count:** At least 3 independent sources per key claim.

### Method C: Targeted Queries (Gap Filling)

When initial results leave gaps (missing data, conflicting info, too old):
```
web_search(query="<refined query>", count=3)
```

Repeat until each major section of the report has supporting sources.

## Step 3 — Cross-Verification

### Conflict Detection

When sources disagree:

| Conflict Type | Resolution |
|:---|:---|
| Different numbers (e.g., market size) | Check dates (older may be out of date), cite the most recent or authoritative |
| Contradictory claims | Find a 3rd/4th source to break the tie |
| One strong + one weak | Trust the stronger (more authoritative, more recent, cited data) |
| Both weak | Flag as "conflicting reports" in the output |

### Verification Checklist

For each key fact, confirm:
- [ ] At least 2 independent sources agree
- [ ] Data includes a clear date or timeframe
- [ ] Source is authoritative (official > news > blog)
- [ ] Numbers are internally consistent (percentages add up, totals match)
- [ ] No obvious bias or agenda in the source

### Quality Scoring

| Score | Criteria |
|:---|:---|
| ✅ Confirmed | 3+ independent reliable sources agree |
| ⚠️ Likely | 2 sources agree, no strong counter-evidence |
| ❓ Uncertain | Only 1 source, or sources conflict |
| ❌ Contradicted | Multiple sources disagree with the claim |

Mark each major finding with its confidence level.

## Step 4 — Report Templates

### Template A: Research Brief (Quick — 3-5 key points)

```
# Research Brief: [Topic] (Date)

## Objective
[1-line research question]

## Key Findings
1. **[Finding 1]** — Source: [URL]
2. **[Finding 2]** — Source: [URL]
3. **[Finding 3]** — Source: [URL]

## Summary
[3-5 sentence synthesis of all findings]

## Sources
- [Source 1 Title](URL)
- [Source 2 Title](URL)
```

### Template B: SWOT Analysis

```
# SWOT: [Company/Topic] (Date)

## Strengths (Internal Positive)
- [Strength 1] — Source: [URL]
- [Strength 2] — Source: [URL]

## Weaknesses (Internal Negative)
- [Weakness 1] — Source: [URL]
- [Weakness 2] — Source: [URL]

## Opportunities (External Positive)
- [Opportunity 1] — Source: [URL]
- [Opportunity 2] — Source: [URL]

## Threats (External Negative)
- [Threat 1] — Source: [URL]
- [Threat 2] — Source: [URL]

## Strategic Implications
[2-3 sentence synthesis of what the SWOT means]
```

### Template C: Competitor Analysis

```
# Competitive Analysis: [Industry/Segment] (Date)

## Market Overview
- Total addressable market: [data + source]
- Growth rate: [data + source]
- Key trends: [3-5 trends + sources]

## Competitor Profiles

### [Competitor A]
- **Position:** [Market leader / Challenger / Niche]
- **Revenue/Size:** [Data + source]
- **Key Strengths:** [...]
- **Key Weaknesses:** [...]
- **Recent Moves:** [1-2 notable events + source]

### [Competitor B]
...

## Competitive Map
| Dimension | Competitor A | Competitor B | Competitor C |
|:----------|:------------:|:------------:|:------------:|
| Market Share | X% | Y% | Z% |
| Pricing | High/Medium/Low | ... | ... |
| Feature Set | Full/Basic | ... | ... |

## Recommendations
[Based on the analysis]
```

### Template D: Full Industry Research Report

```
# Industry Report: [Industry Name] (Date)

## 1. Executive Summary
[3-5 sentence overview with key numbers]

## 2. Market Size & Growth
- Current market size: [data + year + source]
- CAGR: [X% + source]
- Forecast: [projected size + year + source]

## 3. Key Players
[Table of top 5-10 companies with market share, revenue, focus areas]

## 4. Trends & Drivers
1. **[Trend 1]** — [1-2 sentence explanation + source]
2. **[Trend 2]** — [1-2 sentence explanation + source]

## 5. Challenges & Risks
1. **[Risk 1]** — [1-2 sentence explanation + source]
2. **[Risk 2]** — [1-2 sentence explanation + source]

## 6. Regulatory Environment
[Key regulations, policies, compliance requirements + sources]

## 7. Outlook & Recommendations
[3-5 specific, actionable recommendations based on data]

## 8. Sources
For each source: [Title](URL) — confidence level
```

## Source Citation Rules

**Every factual claim in the output must include a source URL.**

Format:
```
[Claim text] — Source: [Source Name](URL)
```

For reports with many sources, include a **Sources** section at the end with all URLs.

## Blacklisting

Do not use these source types as primary sources:
- Anonymous forums (unless specifically investigating sentiment)
- Self-published/promotional content
- Unedited AI-generated content
- Clickbait aggregators with no original reporting

If a user asks for information from a blacklisted source type, warn them and find better sources.

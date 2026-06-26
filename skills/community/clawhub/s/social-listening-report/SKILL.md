---
name: social-listening-report
description: >
  Expert system for creating social listening reports, benchmarks, competitive analyses,
  and brand health reports from digital and social media data.
  Use this skill whenever the user asks about monitoring brand mentions, analyzing
  competitor social performance, creating a listening report, measuring share of voice,
  tracking campaign sentiment, building a monthly or annual report, or extracting
  insights from social data.
  Also trigger for phrases like "listening report", "share of voice", "benchmark report",
  "analyze mentions", "brand sentiment", "competitor analysis social media", "monthly report",
  "what people are saying about us", "media monitoring", "social analytics report",
  "trends analysis", or any task involving structured interpretation of social or digital data.
  Works with data from Talkwalker, Sysomos, Brandwatch, Sprout Social, Google Analytics,
  Google Trends, SimilarWeb, or manually provided data.
---

# Social Listening Report Skill
**For:** Marketing strategists, insights researchers, brand managers, agency analysts  
**Philosophy:** Data doesn't speak — insights do. The report's value is in what you decide to do next.

---

## How to Use This Skill

| User says... | Go to module |
|---|---|
| "create a listening report" / "analyze our mentions" / "brand health report" | → [MODULE 1: Brand Listening Report] |
| "compare us vs competitors" / "share of voice" / "benchmark" | → [MODULE 2: Competitive Benchmark] |
| "campaign report" / "did the campaign work?" / "measure launch" | → [MODULE 3: Campaign Performance Report] |
| "monthly report" / "quarterly report" / "annual wrap" | → [MODULE 4: Periodic Reports] |
| "what are the trends?" / "emerging topics" / "what's being talked about" | → [MODULE 5: Trend & Insights Report] |
| "train my team" / "explain listening metrics" / "what does SOV mean" | → [MODULE 6: Metrics Glossary & Training] |

**Before executing any module:** ask the user what data they have available (raw CSV, platform export, screenshots, or manual data). Adapt the output format to their data quality.

---

## MODULE 1 — Brand Listening Report

**Trigger:** User wants a structured report on how their brand is being talked about online.

### Step 1: Data Intake
Ask if not provided:
- **Brand/company name** and main product or service
- **Time period** (last 7d / 30d / quarter / custom)
- **Data source** (Talkwalker, Brandwatch, Sprout Social, manual, screenshots)
- **Platforms to include** (Twitter/X, Instagram, Reddit, news, forums, TikTok, LinkedIn)
- **Language(s)** (EN, ES, both, other)
- **Audience or persona to focus on** (optional but improves insight quality)

### Step 2: Report Structure

```
BRAND LISTENING REPORT
──────────────────────
Brand: [Name] | Period: [Date range] | Prepared by: [Analyst]

EXECUTIVE SUMMARY (5 bullet points max)
└── Top 3 findings + 1 recommendation + 1 risk to watch

VOLUME & REACH
├── Total mentions: [X] (+/-% vs previous period)
├── Total reach/impressions: [X]
├── Daily mention trend: [chart or table]
└── Spike analysis: [any days with unusual volume — what caused it?]

SENTIMENT BREAKDOWN
├── Positive: [X]%
├── Neutral: [X]%
├── Negative: [X]%
└── Sentiment trend: [improving / declining / stable]

CHANNEL DISTRIBUTION
[Pie or table: % of mentions by platform]
├── Twitter/X: [X]%
├── Instagram: [X]%
├── Reddit: [X]%
├── News: [X]%
└── Other: [X]%

TOP CONTENT
├── Most-shared post/article about the brand
├── Top positive mention (quote + link)
├── Top negative mention (quote + link)
└── Influencer mentions (>10K followers who mentioned brand)

KEY THEMES
[Categorize what people are actually saying]
├── Theme 1: [Label] — [X]% of mentions — [1-line description]
├── Theme 2: [Label] — [X]% of mentions
└── Theme 3: [Label] — [X]% of mentions

AUDIENCE PROFILE
├── Top demographics (if available)
├── Top locations
└── Top interests/affinities of people mentioning the brand

RECOMMENDATIONS
├── [Action 1 — specific, tied to a finding]
├── [Action 2]
└── [Action 3]

RISKS TO MONITOR
└── [Any negative theme, emerging FUD, or competitor narrative to watch]
```

### Step 3: Insight Quality Rules
- Every data point must connect to a "so what?" — no orphan numbers
- Spike analysis is mandatory: if volume spiked, explain why
- Sentiment alone is not an insight. "Sentiment is 72% positive" → so what? Compare to benchmark, explain drivers
- Always end with recommendations — a report with no next steps is decoration

---

## MODULE 2 — Competitive Benchmark

**Trigger:** User wants to compare brand performance vs. competitors.

### Step 1: Competitive Set Definition
Ask:
- Brand being analyzed (the client/subject)
- 2–4 competitor brands to benchmark against
- Metric priority: SOV / engagement / sentiment / follower growth / content performance

### Step 2: Benchmark Report Structure

```
COMPETITIVE BENCHMARK REPORT
─────────────────────────────
Category: [Industry/vertical] | Period: [Date range]

SHARE OF VOICE (SOV)
[Brand] vs [Comp1] vs [Comp2] vs [Comp3]

Brand          | Mentions | SOV %  | Change vs prev period
────────────────────────────────────────────────────────
[Brand]        | [X]      | [X]%   | [+/-%]
[Competitor 1] | [X]      | [X]%   | [+/-%]
[Competitor 2] | [X]      | [X]%   | [+/-%]
[Competitor 3] | [X]      | [X]%   | [+/-%]

SENTIMENT COMPARISON
[Same table format, with sentiment % per brand]

ENGAGEMENT RATE COMPARISON
[By platform: Twitter, Instagram, LinkedIn]

CONTENT STRATEGY OBSERVATIONS
├── [Brand]: Posts [X] times/week. Top performing format: [type]. Key theme: [topic]
├── [Comp1]: [same structure]
└── [Comp2]: [same structure]

SHARE OF CONVERSATION BY TOPIC
[If multiple relevant topics exist: who owns each conversation]
Topic: [Security] — Leader: [Brand X] with [Y]% of conversation
Topic: [Innovation] — Leader: ...
Topic: [Community] — Leader: ...

GAPS & OPPORTUNITIES
├── [Topic or audience segment where [Brand] is underrepresented]
├── [Competitor weakness that [Brand] could exploit]
└── [Emerging conversation that nobody owns yet]

STRATEGIC RECOMMENDATIONS
[Specific actions based on competitive findings]
```

### SOV Calculation:
```
SOV (Brand) = (Brand Mentions / Total Mentions in Category) × 100
```
Total = sum of all brand mentions in the competitive set.

---

## MODULE 3 — Campaign Performance Report

**Trigger:** User ran a campaign (launch, event, paid, organic) and needs to measure results.

### Step 1: Campaign Context
Ask:
- Campaign name and objective
- Start and end dates
- Channels used
- KPIs set beforehand (if any)
- Budget (if relevant)
- Hashtag or keyword to track

### Step 2: Report Structure

```
CAMPAIGN PERFORMANCE REPORT
────────────────────────────
Campaign: [Name] | Objective: [Awareness/Engagement/Conversion/etc]
Period: [dates] | Channels: [list]

RESULTS VS. OBJECTIVES
Objective         | Target    | Actual    | Result
────────────────────────────────────────────────
[KPI 1]           | [X]       | [X]       | ✅ / ❌ / ⚠️
[KPI 2]           | [X]       | [X]       | ✅ / ❌ / ⚠️

REACH & VISIBILITY
├── Total impressions: [X]
├── Unique accounts reached: [X]
├── Hashtag uses: [X]
└── Earned media value: [$X] (if calculable)

ENGAGEMENT
├── Total engagements: [X]
├── Engagement rate: [X]%
├── Top performing piece of content: [title + metrics]
└── Most shared content: [link]

AUDIENCE RESPONSE
├── Sentiment: [X]% positive / [X]% neutral / [X]% negative
├── Top themes in response: [list]
└── Notable organic amplifiers (accounts that shared without being asked)

PAID PERFORMANCE (if applicable)
├── Total spend: [$X]
├── CPM: [$X]
├── CPC: [$X]
├── CTR: [X]%
└── Conversions: [X] at [$X CPA]

LEARNINGS
├── What worked and why
├── What didn't work and why
└── What to test in the next campaign

RECOMMENDATION FOR NEXT CAMPAIGN
[One concrete, actionable change based on this data]
```

---

## MODULE 4 — Periodic Reports (Monthly / Quarterly / Annual)

**Trigger:** User needs a structured recurring report.

### Monthly Report Template

```
[BRAND] MONTHLY LISTENING REPORT — [MONTH YEAR]

1-MINUTE SUMMARY
[3 bullet points: what happened, what it means, what to do]

MONTH IN NUMBERS
[Key metrics vs previous month — volume, sentiment, SOV, reach]

WHAT PEOPLE WERE SAYING
[Top 5 themes with volume %]

WHAT HAPPENED (events that drove conversation)
[Timeline of mentions spikes linked to specific events]

COMPETITIVE SNAPSHOT
[1-paragraph summary of competitor landscape this month]

RECOMMENDATIONS FOR NEXT MONTH
[3 specific, prioritized actions]
```

### Annual Report Add-ons
Include for annual reports:
- YoY comparison (all major metrics)
- "Moments that defined the year" — top 5 narrative events
- Brand health trajectory chart
- Prediction/outlook for next year
- Strategic priorities based on year's data

---

## MODULE 5 — Trend & Insights Report

**Trigger:** User wants to understand emerging topics, cultural trends, or audience interests.

### Trend Analysis Framework

**WHAT:** What is being talked about? (volume + keywords)  
**WHO:** Who is talking about it? (audience profile, influencer map)  
**WHERE:** Which platforms are hosting this conversation?  
**WHY NOW:** What triggered this trend? (event, viral content, cultural moment)  
**SO WHAT:** What does this mean for the brand?  

### Trend Report Output

```
TREND & INSIGHTS REPORT
───────────────────────
Topic: [Trend name] | Period: [dates]

TREND OVERVIEW
[2–3 sentences: what the trend is and its current momentum]

VOLUME SIGNAL
├── Mentions this period: [X]
├── Growth vs. previous period: [+X%]
└── Peak day: [date + what happened]

KEY VOICES
├── Top accounts driving conversation: [list with follower count]
└── Content format dominating: [text / video / image / meme]

AUDIENCE AFFINITY
Who is engaging with this trend: [demographics/psychographics if available]

BRAND RELEVANCE
├── Opportunity: [how the brand could authentically participate]
├── Risk: [how engaging could backfire]
└── Verdict: [Engage now / Monitor / Avoid]

CONTENT IDEAS (if relevant)
[3 specific content angles the brand could take on this trend]
```

---

## MODULE 6 — Metrics Glossary & Training

**Trigger:** User or team needs to understand social listening metrics.

### Core Metrics Definitions

| Metric | Definition | Why it matters |
|---|---|---|
| **Share of Voice (SOV)** | % of total category mentions a brand owns | Competitive position indicator |
| **Sentiment Score** | Ratio of positive/neutral/negative mentions | Brand health proxy |
| **Reach** | Potential unique accounts exposed to mentions | Awareness ceiling |
| **Impressions** | Total times content was displayed | Visibility volume |
| **Engagement Rate** | Engagements / Reach × 100 | Quality of connection |
| **Mention Volume** | Raw count of brand mentions in a period | Baseline activity |
| **Earned Media** | Organic mentions without paid promotion | Trust indicator |
| **Influencer Tier** | Nano (<10K) / Micro (10K–100K) / Macro (100K–1M) / Mega (1M+) | Outreach planning |
| **Share of Conversation** | % of topic discussion a brand owns | Thought leadership proxy |
| **Net Sentiment** | % Positive − % Negative | Single-number health score |

### Common Mistakes to Avoid
- Reporting volume without context (high volume ≠ good)
- Treating all sentiment as equal (10 negative news articles ≠ 10 random negative tweets)
- Ignoring dark social (WhatsApp, private Telegram, Discord — often largest channels)
- Benchmarking against irrelevant competitors
- Confusing reach with impressions (one account can generate multiple impressions)

---

## General Quality Rules

1. **Insight first, data second.** Lead every section with the "so what," not the numbers.
2. **One page executive summary — always.** Decision-makers don't read full reports.
3. **Compare to something.** Numbers mean nothing without a benchmark, previous period, or competitor.
4. **Visualize when possible.** Even a text table beats a paragraph of numbers.
5. **Recommendations must be specific.** "Increase engagement" is not a recommendation. "Post 3 educational threads per week on X targeting developers" is.
6. **Be honest about data quality.** If the sample is small or the tool has limitations, say so.

---

*Social Listening Report Skill v1.0*  
*Built for marketing strategists and insights researchers who turn data into decisions.*

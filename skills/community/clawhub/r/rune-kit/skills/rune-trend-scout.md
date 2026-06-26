# rune-trend-scout

> Rune L3 Skill | knowledge | model: tier:light


# trend-scout

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

Market intelligence and technology trend analysis utility. Receives a topic or market segment, executes targeted searches across trend sources, analyzes competitor activity and community sentiment, and returns structured market intelligence. Stateless — no memory between calls.

## Calls (outbound)

None — pure L3 utility using `WebSearch` tools directly.

## Called By (inbound)

- `brainstorm` (L2): market context for product ideation
- `marketing` (L2): trend data for positioning and content
- `autopsy` (L2): identify if tech stack is outdated
- `autopsy` (L2): check if legacy tech is still maintained

## Execution

### Input

```
topic: string           — market segment or technology to analyze (e.g., "AI coding assistants", "SvelteKit")
timeframe: string       — (optional) period of interest, defaults to "2026"
focus: string           — (optional) narrow the lens: "competitors" | "technology" | "community" | "all"
```

### Step 1 — Define Scope

Parse the input topic and determine the analysis angle:
- Product/market: focus on competitors, pricing, user adoption
- Technology: focus on GitHub activity, npm/pypi downloads, framework adoption
- Community: focus on Reddit, HN, X/Twitter sentiment

### Step 2 — Search Trends

Execute `WebSearch` with these query patterns:
- `"[topic] 2026 trends"`
- `"[topic] vs alternatives 2026"`
- `"[topic] market share growth"`
- `"[topic] GitHub trending"` or `"[topic] npm downloads stats"`

Collect results. Identify the most evidence-rich URLs per query.

### Step 3 — Competitor Analysis

Execute `WebSearch` with:
- `"[topic] competitors comparison"`
- `"best [topic] tools 2026"`
- `"[topic] alternative"`

From results, extract:
- Top 3-5 competitors or alternative solutions
- Key differentiating features
- Pricing model if visible
- User sentiment signals (e.g., "users are switching from X to Y because...")

### Step 4 — Community Sentiment

Execute `WebSearch` with:
- `"site:reddit.com [topic]"` or `"[topic] reddit discussion"`
- `"[topic] site:news.ycombinator.com"`
- `"[topic] GitHub stars"` or `"[topic] downloads per week"`

Extract:
- Community perception (positive/negative/mixed)
- Frequently cited pain points
- Frequently praised features
- Adoption velocity indicators (star growth, download counts)

### Step 5 — Report

Synthesize all gathered data into the output format below. Note where data is sparse or conflicting.

## Constraints

- Use `WebSearch` only — do not call `WebFetch` unless a specific page has critical data not in snippets
- Label all data points with their source
- Do not infer trends from a single data point — note confidence level
- If the topic is too broad, report what was analyzed and suggest narrowing

## Output Format

```
## Trend Report: [Topic]
- **Period**: [timeframe]
- **Confidence**: high | medium | low

### Trending Now
- [trend] — evidence: [source/stat]
- [trend] — evidence: [source/stat]

### Competitors
| Name | Key Differentiator | Sentiment |
|------|--------------------|-----------|
| [A]  | [feature]          | positive / mixed / negative |
| [B]  | [feature]          | positive / mixed / negative |

### Community Sentiment
- **Reddit/HN**: [summary]
- **GitHub activity**: [stars/downloads/issues signal]
- **Pain points**: [what users complain about]

### Emerging Patterns
- [pattern] — implication: [what this means for callers]

### Recommendations
- [actionable insight for the calling skill]
```

## Sharp Edges

Known failure modes for this skill. Check these before declaring done.

| Failure Mode | Severity | Mitigation |
|---|---|---|
| Inferring trend from a single data point | HIGH | Constraint: note confidence level — single source = low confidence, not a trend |
| Topic too broad → generic results with no actionable signal | MEDIUM | Report what was analyzed and suggest narrowing; don't fabricate specificity |
| Skipping competitor analysis (Steps 3 mandatory) | MEDIUM | Competitor analysis is required — callers need positioning context |
| Calling WebFetch on every search result (excessive cost) | MEDIUM | Constraint: WebSearch only unless a specific page has critical data not in snippets |

## Done When

- Topic scope defined (product/technology/community angle)
- Trend searches executed with 2026 timeframe
- Competitor analysis completed (top 3-5 players with differentiators)
- Community sentiment captured (Reddit/HN/GitHub signals)
- Confidence level assigned based on evidence quality
- Trend Report emitted with source citations for every data point

## Cost Profile

~300-600 tokens input, ~200-400 tokens output. Haiku.

---
> **Rune Skill Mesh** — 64 skills, 203 connections + 40 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — product, sales, data-science, support packs → [rune-kit/rune-pro](https://github.com/rune-kit/rune-pro)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit/rune-business](https://github.com/rune-kit/rune-business)
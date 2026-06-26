---
name: research-assistant
description: Deep research and synthesis assistant. Use when you need to investigate a topic across multiple sources, compare findings, produce structured research reports, or do multi-step web research with citation tracking. NOT for simple single-query lookups (use web_search directly).
tags: ['research', 'synthesis', 'web-search', 'citation', 'report']
metadata:
  openclaw:
    requires:
      tools: ['web_search', 'web_fetch']
---

# Research Assistant

Structured multi-source research with citation tracking and synthesis.

## When to Use

- Multi-step investigation across 3+ sources
- Comparative analysis requiring side-by-side findings
- Reports needing citations and source attribution
- Topic exploration where depth matters more than speed

## Workflow

### 1. Scope

Clarify the research question. Break broad topics into 2-5 sub-questions. Define the output format upfront (brief, detailed, table, report).

### 2. Search

Run 2-3 parallel `web_search` calls with varied query phrasing per sub-question. Use `freshness` and `country` filters when recency or region matters.

### 3. Fetch & Extract

For each promising result, use `web_fetch` with `extractMode: "markdown"` and `maxChars: 8000`. Skip paywalled or low-value pages quickly.

### 4. Synthesize

Cross-reference findings across sources. Flag contradictions explicitly. Assign confidence levels:

| Level | Meaning |
|-------|---------|
| High | 3+ independent sources agree |
| Medium | 2 sources or 1 authoritative source |
| Low | Single unverified source |

### 5. Cite & Deliver

Every factual claim gets a source line: `[N] Source Title — URL`

Output format:

```
## [Topic]

### Key Findings
- Finding 1 [1]
- Finding 2 [2,3]

### Contradictions
- Source A says X [1], Source B says Y [2]

### Sources
[1] Title — https://...
[2] Title — https://...
```

## Tips

- **Vary queries**: rephrase, use synonyms, add site: filters
- **Go deep on one source before moving on**: don't skim 20 pages
- **Track dead ends**: note queries that returned nothing to avoid repeating
- **Set maxChars conservatively**: 4000-8000 per fetch; increase only if needed
- **Parallelize searches**, serialize fetches (respect rate limits)

## Advanced Patterns

For multi-phase research, see [references/deep-dive.md](references/deep-dive.md).

For automated source credibility scoring, see [scripts/credibility.py](scripts/credibility.py).

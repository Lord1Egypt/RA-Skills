---
name: search-auto-routing-plan
displayName: "Search Auto-Routing Plan"
version: "1.0.0"
description: "Plan which search provider to use before multi-provider skills run — score query signals, pick Serper/Tavily/Exa/Brave/Firecrawl, define fallback chain, and document why."
triggerKeywords:
  - search auto routing
  - which search provider
  - route web search
  - serper vs tavily vs exa
  - search provider picker
  - web search routing plan
  - multi provider search plan
  - search routing rubric
  - pick search api
  - intelligent search routing
tags:
  - auto-routing
  - web-search
  - exa
  - brave
  - tavily
license: "MIT"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Search Auto-Routing Plan

## Purpose

Produce a **search routing plan** before invoking multi-provider skills (`web-search-plus`, custom routers, or chained search tools). Routers execute automatically but rarely explain *why* a provider was chosen — this skill makes routing **explicit, auditable, and tunable**.

This skill does **not** call search APIs, store API keys, or fetch live results.

## When to use

Use when the user mentions:

- Auto-routing across Serper, Tavily, Exa, Brave, Firecrawl, Perplexity, etc.
- Which search provider fits a query
- Web Search Plus or unified search skills
- Reducing search cost or improving result quality via smarter routing
- Fallback chains when the first provider returns thin results

**Not for:** routing LLM prompts between local/cloud models (see task-complexity skills).

## Safety and boundaries

**Do not** request or echo API keys for any search provider.

**Do not** claim live search results — planning only.

**Do not** recommend circumventing robots.txt, paywalls, or provider ToS.

**Privacy:** If the query contains PII, recommend providers/modes that minimize logging and note user consent.

## Required inputs

1. **Search goal** — what answer or artifact is needed.
2. **Query or task description** — the actual text to search for (or “generate from goal”).
3. **Constraints** — freshness, geography, max latency, budget sensitivity, offline/air-gapped.
4. **Available providers** (optional) — which keys/skills the user actually has; default to common stack: Serper, Tavily, Exa, Brave, Firecrawl.
5. **Output need** — snippets, full page text, structured JSON, citations only.

## Signal scoring

Score each dimension 0–2 (0=low, 1=medium, 2=high):

| Signal | 0 | 1 | 2 |
|--------|---|---|---|
| **Specificity** | vague exploration | named topic | exact entity/error/ID |
| **Freshness** | evergreen | weeks | hours/breaking |
| **Depth** | quick fact | multi-source | deep research |
| **Structure** | prose pages | mixed | docs/repos/PDFs |
| **Privacy** | public OK | semi-sensitive | PII/regulated |

## Provider fit (default rubric)

| Provider | Best when | Weak when |
|----------|-----------|-----------|
| **Serper** (Google) | exact matches, site: queries, local/business | fuzzy conceptual discovery |
| **Tavily** | research synthesis, Q&A style answers | single known URL lookup |
| **Exa** | neural/semantic discovery, similar pages, companies/papers | literal error strings |
| **Brave** | privacy-weighted general web, independent index | deep academic corpora |
| **Firecrawl** | known URL → clean markdown extract | open-ended discovery |

Tie-breakers: cost ↑ with depth; latency ↑ with crawl/extract.

## Workflow

1. Restate goal and score the five signals.
2. Rank providers 1–3 with short rationale.
3. Output plan (format below) including **fallback chain** (if #1 thin → try #2).
4. Suggest query tweaks per primary provider (keyword vs neural phrasing).

## Output format

### Search routing plan — {short goal}

| Signal | Score (0–2) |
|--------|-------------|
| Specificity | |
| Freshness | |
| Depth | |
| Structure | |
| Privacy | |

#### Primary route

| Field | Value |
|-------|-------|
| Provider | Serper / Tavily / Exa / Brave / Firecrawl |
| Mode | keyword / neural / extract / answer |
| Why | 1–2 sentences tied to signal scores |
| Query for provider | provider-optimized phrasing |

#### Fallback chain

1. **If** &lt;condition&gt; **then** &lt;provider + query adjustment&gt;
2. …

#### Executor hints

Optional YAML for downstream skills:

```yaml
primary: serper|tavily|exa|brave|firecrawl
fallback: []
maxResults: 5-10
extractContent: true|false
freshness: null|ISO range
```

#### Post-route quality checks

- [ ] Top results match entity type and freshness
- [ ] Snippets are answer-bearing (not directory pages)
- [ ] Cost/latency within stated constraints
- [ ] Fallback triggered if &lt;3 usable sources

## Quality bar

- **Every pick cites signals** — no “use Tavily because it’s good.”
- **Fallbacks are conditional** — not a generic provider list.
- **Queries differ by provider** — Serper keywords ≠ Exa sentences.
- **Respects available providers** — don’t recommend Firecrawl if user only has Serper.

## Examples

**Good rationale:** “Freshness=2 + Depth=2 → Tavily primary for synthesized recent coverage; Serper fallback for exact product name confirmation.”

**Bad rationale:** “Use Exa for better results.”

**Good fallback:** “If Exa returns &lt;3 corporate homepages, retry Serper with `site:linkedin.com/company {name}`.”

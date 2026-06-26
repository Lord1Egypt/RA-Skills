---
name: deep-research
description: >-
  Deep web research with multi-round search, cross-verification, and structured reports
  with citations. Enhances web_search and web_fetch into a full research workflow.
  Use when: user asks to research a topic in depth, investigate something thoroughly,
  compare options with evidence, write a research report, or needs more than a simple
  search answer. Trigger phrases: "research", "deep dive", "investigate", "调研",
  "深度搜索", "帮我研究", "详细了解一下", "对比分析", "compare X vs Y",
  "what are the pros and cons of", "综合分析".
  NOT for: simple factual lookups ("what's the capital of France"), real-time data
  (stock prices, live scores), or browsing/interacting with a specific website (use browser).
metadata:
  openclaw:
    emoji: "🔬"
---

# Deep Research 🔬

Multi-round web research with question decomposition, cross-verification, and
structured reports with numbered citations.

## Architecture

Three-step agent-assisted pipeline. No external API keys needed — uses OpenClaw
built-in `web_search` and `web_fetch` tools.

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  plan    │ ──▶ │ analyze  │ ──▶ │ report   │
│ (脚本)   │     │ (脚本)    │     │ (脚本)    │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │ search_        │ fetch_         │
     │ commands       │ commands       │ report
     ▼                ▼                ▼ skeleton
  Agent 执行       Agent 执行       Agent 填充
  web_search      web_fetch        分析内容
```

**Script path:** `scripts/research.py` (relative to this skill directory)

## Workflow

### Step 1: Plan — 生成搜索指令

```bash
python3 scripts/research.py plan "topic" --depth standard
```

Output JSON contains `search_commands` — a list of `web_search` tool calls.
Agent executes each one and collects results into a JSON array:

```json
[
  {"query": "...", "results": [{"title": "...", "url": "...", "snippet": "..."}, ...]},
  ...
]
```

Save to a temp file (e.g., `/tmp/search-results.json`).

### Step 2: Analyze — 去重排序 + 生成 fetch 指令

```bash
python3 scripts/research.py analyze /tmp/search-results.json --top 8
```

Output JSON contains:
- `selected_sources`: Deduplicated, tier-sorted source list
- `fetch_commands`: `web_fetch` tool calls for top URLs
- `summary`: Human-readable source overview

Agent executes each `web_fetch` and collects results into a JSON array:

```json
[
  {"url": "...", "text": "extracted content...", "length": 12345},
  ...
]
```

Save to `/tmp/fetch-results.json`.

### Step 3: Report — 生成报告骨架

```bash
python3 scripts/research.py report \
  --topic "topic" \
  --search /tmp/search-analysis.json \
  --fetch /tmp/fetch-results.json \
  --depth standard --save
```

Output: Markdown report with `{FILL: ...}` placeholders.
Agent reads the Source Content section and fills in analysis.

## Depth Levels

Auto-detect from query complexity, or user specifies.

### Quick ⚡ (≤30s)
- `--depth quick` → 1 sub-question, 2 fetches
- Agent may skip the script entirely for trivial queries
- Output: IM message only (≤2000 chars)

### Standard 🔍 (2-3 min)
- `--depth standard` → 4-5 sub-questions, 8 fetches
- Full 3-step pipeline
- Output: IM summary + full report saved to `research/`

### Deep 🔬 (5-10 min)
- `--depth deep` → 7 sub-questions (includes contrarian), 15 fetches
- Spawn sub-agents for parallel search:
  ```
  sessions_spawn:
    mode: run
    task: |
      Execute these web_search calls: {subset of search_commands}
      Return results as JSON array.
  ```
- Main agent runs analyze + report after collecting all results
- Output: IM summary + comprehensive report (2000-5000 words)

User overrides: "快速搜一下" → Quick, "详细研究" → Standard, "深度调研" → Deep

## Source Authority Tiers

Script auto-classifies:
- **Tier 1 🟢** Official docs, .gov/.edu, arxiv, RFCs
- **Tier 2 🟡** Major tech blogs, Stack Overflow, vendor blogs
- **Tier 3 🟠** Personal blogs, Medium, forum posts
- **Tier 4 🔴** AI-generated, marketing landing pages

## Cross-Verification (Standard & Deep)

After report skeleton is generated, agent verifies:
- **Source diversity:** ≥3 independent sources?
- **Recency:** Prefer last 12 months; flag outdated
- **Conflicts:** When sources disagree, present both with tier labels
- If gaps found → run additional web_search + web_fetch → append

## Report Output

### IM Summary

```
🔬 Research: {topic}

{2-4 paragraph summary}

**Key takeaways:**
- Finding 1 [1][2]
- Finding 2 [3]

📊 Confidence: {🟢/🟡/🔴}
📄 Full report: research/{slug}-{date}.md
```

### Full Report

Saved to `research/{topic-slug}-{YYYYMMDD}.md` with:
- Executive Summary
- Key Findings (per sub-topic)
- Conflicting Information
- Confidence Assessment table
- Numbered Sources with tier labels
- Research Log

## Progress Feedback

- **Quick:** No progress messages
- **Standard:** One mid-point: "🔍 已搜索 N 轮，找到 M 来源，正在抓取..."
- **Deep:** Per sub-agent updates

## Edge Cases

- **Too broad:** Ask user to narrow; suggest 3-4 angles
- **No results:** Try EN↔CN keywords, then report honestly
- **Rate limits (429):** Wait 5s + retry; fallback to web_fetch on known URLs
- **Large topics:** Summarize each round to ≤500 chars before next

## Language

- Match user's language for report
- Auto-add cross-language search (EN topic → add 1 CN query; CN → add 1 EN)
- Chinese: 「」直角引号、——全破折号、：全角冒号

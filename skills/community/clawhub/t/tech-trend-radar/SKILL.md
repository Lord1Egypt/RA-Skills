---
name: tech-trend-radar
description: Use when generating current technology, AI model ranking, product, startup, funding, regulation, or market trend reports from recent industry updates
author: Chad Liu
---

# Trend Radar

Generate an industry trend report from recent, credible technology and market updates. Prioritize fresh signals, source quality, model reranking, GitHub momentum, business impact, and clear next actions.

## When to Use

Use this skill when the user asks for:

- Weekly, monthly, or quarterly technology trends
- AI, SaaS, developer tools, cloud, security, startup, or regulation updates
- Model reranking, leaderboard changes, and current top model summaries
- Claude managed agents, Claude agent teams, and Anthropic agent platform updates
- OpenAI, Anthropic, Google, Microsoft, Meta, xAI, Alibaba Qwen, Zhipu GLM, and major AI lab strategy updates
- GitHub Trending and open-source momentum summaries
- Market signal summaries for planning, investing, product strategy, or competitive tracking
- A concise report that distinguishes major shifts from ordinary news

Trigger examples:

```text
Write this week's AI trend report
Show current top 10 AI models and ranking changes
Track Claude managed agents and agent teams updates
Generate a trend radar for developer tools
Summarize GitHub Trending for AI agents this month
Summarize recent market trends in AI agents
What changed in SaaS and AI this week?
```

## Research Workflow

1. Define the report period. Default to `1w` unless the user specifies `1w`, `1m`, `3m`, or an exact date range.
2. Search by category, not only by generic keywords. Combine company names, product names, ecosystem terms, and event types.
3. Check model leaderboards for reranking, new entrants, score deltas, and category shifts.
4. Check Anthropic and Claude agent platform updates, especially managed agents, agent teams, enterprise controls, connectors, and orchestration features.
5. Check GitHub Trending and repository momentum for relevant categories, languages, and keywords.
6. Prefer primary and high-signal sources before commentary.
7. Cross-check major claims with at least two credible sources when possible.
8. Deduplicate repeated coverage of the same announcement.
9. Score each item by novelty, impact, source quality, ranking movement, open-source traction, and actionability.
10. Separate confirmed facts from interpretation. Label uncertain items as `Watch`.
11. Re-check the latest available sources every run, even if the same topic appeared in a previous report.

## Time Windows

Use three standard windows to separate short-term noise from durable trends:

| Window | Use For | Signal Focus |
|--------|---------|--------------|
| `1w` | Weekly scan | launches, releases, incidents, funding, GitHub Trending spikes |
| `1m` | Monthly pattern | repeated adoption, repo growth, new categories, competitor movement |
| `3m` | Quarterly shift | platform changes, durable market direction, ecosystem consolidation |

When reporting multiple windows, compare them explicitly: `1w = new spike`, `1m = traction`, `3m = durable direction`.

## Freshness and Continuity Rules

Each report must include the newest available information for its period. Do not omit an important topic because it appeared in an earlier report.

- **Always refresh**: rerun searches for model rankings, company strategy, product launches, regulatory actions, GitHub Trending, and agent platform updates.
- **Show the delta**: when a topic repeats, state what changed since the previous mention: new date, new source, rank movement, adoption signal, pricing change, policy update, or ecosystem reaction.
- **Label continuity**: mark repeated topics as `Continuing`, `Updated`, or `Resolved`.
- **Prefer dated evidence**: include publication dates or checked timestamps for all current claims.
- **Reject stale summaries**: do not rely only on an older saved report when the user asks for the latest period.

## Required Depth

Reports should be concise but not shallow. For monthly or quarterly reports, each selected signal must include enough detail to support judgment:

- **What happened**: 2-4 concrete facts with dates, actors, product names, or metrics
- **Why it matters**: strategic, technical, market, regulatory, or developer impact
- **Evidence**: at least one direct source link; use two sources for high-impact claims when possible
- **Core change**: what is different from the previous period or previous report
- **Action**: monitor, test, migrate, compare, budget, update policy, or ignore

Avoid top-list-only reports. A Top 10 table is a navigation aid, not the analysis.

## Source Priority

Use higher-priority sources first:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| 1 | Official announcements | company blogs, product release notes, API changelogs, pricing pages |
| 1 | Primary technical artifacts | GitHub releases, RFCs, benchmark reports, model cards, research papers |
| 1 | Anthropic / Claude updates | Anthropic news, Claude docs, Claude Code docs, API changelog, enterprise admin docs |
| 1 | Model leaderboards | LMArena/Text Arena, Artificial Analysis, LiveBench, SWE-bench, OpenRouter rankings |
| 1 | GitHub momentum | GitHub Trending, stars, forks, releases, issue velocity, contributor activity |
| 2 | Business records | funding announcements, acquisition news, earnings calls, regulatory filings |
| 2 | Trusted industry media | The Verge, TechCrunch, The Information, Stratechery, VentureBeat, The Pragmatic Engineer |
| 3 | Community signals | Hacker News, Reddit, X posts, Discord/Slack communities, GitHub stars/issues |

Community signals should support a trend, not be the only evidence for a high-impact claim.

## Anthropic / Claude Agent Signals

Track Claude agent platform changes as a dedicated signal family. Include both official product updates and ecosystem reactions when they affect how teams build, deploy, or govern agents.

Monitor these topics:

- **Claude managed agents**: hosted agents, managed execution, background tasks, schedules, permissions, observability, and lifecycle management
- **Claude agent teams**: multi-agent collaboration, team workspaces, handoffs, shared memory, role assignment, approval flows, and delegation patterns
- **Claude Code and developer agents**: CLI updates, IDE integrations, repo context, code review, test execution, MCP support, and automation workflows
- **Enterprise controls**: admin policy, audit logs, identity, data retention, connectors, compliance, sandboxing, and human-in-the-loop review
- **API and platform primitives**: tool use, computer use, MCP, files, sessions, workflows, web search, batch jobs, and rate/pricing changes

For each Claude agent signal, capture:

- **What changed**: product, API, docs, pricing, availability, or policy
- **Affected users**: individual developers, product teams, enterprise admins, platform teams, or agent builders
- **Core change**: managed execution, multi-agent coordination, governance, connector expansion, or deployment workflow
- **Evidence**: official Anthropic source first; add credible secondary analysis only when useful
- **Action**: try, migrate, monitor, update policy, or compare with OpenAI/Codex/Gemini/Copilot alternatives

## Company Strategy Signals

Track strategic changes from major AI companies every run, especially OpenAI, Anthropic, Alibaba Qwen, and Zhipu AI. Include Google, Microsoft/GitHub, Meta, xAI, Mistral, DeepSeek, Moonshot AI, Baidu, Tencent, ByteDance, and other major labs when relevant.

For each company strategy item, capture:

- **Company**: OpenAI, Anthropic, Alibaba/Tongyi Qianwen/Qwen, Zhipu AI/GLM, Google Gemini/Gemma, Microsoft/GitHub, Meta, xAI, Mistral, DeepSeek, Moonshot AI, Baidu, Tencent, ByteDance, or other
- **Latest move**: product launch, model release, pricing, partnership, safety policy, enterprise push, developer platform shift, acquisition, hiring, or regulation response
- **Strategic direction**: models, agents, consumer apps, enterprise, coding, infrastructure, safety, open source, or distribution
- **Evidence**: official source first; add credible analysis or market data when useful
- **Implication**: what builders, buyers, investors, or competitors should do next

Monthly reports must include a `Company Strategy Watch` section with at least OpenAI, Anthropic, Alibaba Qwen, and Zhipu AI, even if there is no major change. In that case, write `No major new public move found` and cite the latest checked sources.

## Model Reranking Signals

Track AI model ranking movement as a dedicated signal. Always state which leaderboard is used because rankings measure different things:

| Leaderboard | Measures | Use For |
|-------------|----------|---------|
| LMArena / Text Arena | Human preference battles | General chat quality and user preference |
| Artificial Analysis | Composite intelligence, speed, cost | Balanced capability and deployment comparison |
| LiveBench | Dynamic benchmark performance | Reasoning, coding, math, and contamination-resistant evals |
| SWE-bench | Real-world coding tasks | Coding agent and software engineering capability |
| OpenRouter Rankings | Real API usage | Developer adoption and production demand |
| Open-weight model leaderboards | Open model performance | Gemma, Llama, Qwen, Mistral, DeepSeek, GLM comparison |
| Chinese model leaderboards | Domestic model performance | Qwen, GLM, DeepSeek, Kimi, ERNIE, Hunyuan, Doubao comparison |

For each reranking item, capture:

- **Current Top 10**: rank, model, provider, score or usage metric, source, timestamp
- **Core change**: new entrant, rank gain/loss, score delta, usage spike, category win, or pricing-driven adoption
- **Why it changed**: model release, benchmark update, price change, context window, tool use, coding quality, availability
- **Impact**: product choice, API routing, coding workflow, cost strategy, or competitive positioning
- **Confidence**: high when leaderboard source and timestamp are clear; lower when based on secondary summaries

Monthly and quarterly reports must include a full Top 10 model table, not only a short summary. Include rank, model, provider, metric, leaderboard, checked timestamp, rank change if available, and the reason for notable movement.

Always check whether Chinese models appear in current rankings or category leaderboards. Track at least Qwen/通义千问, GLM/智谱, DeepSeek, Kimi/Moonshot, ERNIE/文心, Hunyuan/混元, and Doubao/豆包 when they are relevant.

## GitHub Trending Signals

Track GitHub Trending as an early indicator, especially for developer tools, AI agents, infrastructure, and security. Search by relevant languages and topics such as `Python`, `TypeScript`, `Rust`, `Go`, `AI`, `LLM`, `agent`, `RAG`, `MCP`, `security`, and `devtools`.

For each notable repository, capture:

- **Repository**: owner/name and link
- **Category**: AI/ML, Developer Tools, Cloud/Infra, Security, or other
- **Window**: `1w`, `1m`, or `3m`
- **Momentum**: stars gained, forks, release activity, contributors, issue velocity
- **Why it matters**: product category, technical novelty, adoption signal, or ecosystem relevance
- **Caveat**: hype, demo-only status, weak maintenance, unclear license, or duplicated project

## Monitoring Categories

### AI/ML

- Models: OpenAI, Anthropic, Google Gemini, Google Gemma, Meta Llama, Mistral, xAI, DeepSeek, Alibaba Qwen/通义千问, Zhipu GLM/智谱, Kimi/Moonshot, Baidu ERNIE/文心, Tencent Hunyuan/混元, ByteDance Doubao/豆包
- Agent frameworks: LangChain, LangGraph, AutoGen, CrewAI, OpenAI Agents SDK
- Capabilities: multimodal AI, coding agents, RAG, long context, reasoning, evaluation
- Claude agents: managed agents, agent teams, Claude Code, MCP, tool use, computer use, enterprise controls
- Business signals: AI startup funding, enterprise adoption, AI pricing, AI regulation
- Company strategy: OpenAI, Anthropic, Alibaba/Tongyi Qianwen/Qwen, Zhipu AI/GLM, Google Gemini/Gemma, Microsoft/GitHub, Meta, xAI, Mistral, DeepSeek, Moonshot AI, Baidu, Tencent, ByteDance
- Benchmarks and reranking: LMArena/Text Arena, Artificial Analysis, LiveBench, SWE-bench, OpenRouter, model cards, eval reports

### Developer Tools

- Coding assistants: Codex, GitHub Copilot, Cursor, Claude Code, Windsurf
- Dev platforms: GitHub, GitLab, Linear, Vercel, Netlify, Supabase
- Tooling: CI/CD, observability, testing, package managers, IDE extensions
- Agent platforms: Claude managed agents, Claude agent teams, Codex agents, Copilot coding agent, Gemini agents
- GitHub Trending: fast-growing repos, new frameworks, agent tools, MCP servers, CLIs, infra templates

### SaaS/Productivity

- Notion, Slack, Linear, Atlassian, Salesforce, HubSpot, Microsoft 365, Google Workspace
- AI features, workflow automation, collaboration, pricing, enterprise adoption

### Cloud/Infrastructure

- AWS, Azure, Google Cloud, Cloudflare, Docker, Kubernetes, serverless, databases
- GPU supply, inference platforms, edge compute, cost optimization

### Security/Privacy

- Vulnerabilities, supply-chain attacks, identity, compliance, AI safety, data governance

### Startup/Funding

- Seed to IPO funding, acquisitions, shutdowns, category creation, Korean startups, global AI startups

### Agent Platform Ecosystem

- Anthropic/Claude, OpenAI/Codex, Alibaba Qwen/通义千问, Zhipu GLM/智谱, Google/Gemini/Gemma, Microsoft/GitHub Copilot, MCP ecosystem, managed agents, agent teams, community showcases, OpenClaw, HarnessClaw

## Scoring Criteria

| Score | Meaning | Criteria |
|-------|---------|----------|
| 9-10 | Critical | Industry-wide shift, immediate action needed, major platform or regulation change |
| 7-8 | High | Major company move, strong adoption signal, pricing or capability change |
| 5-6 | Medium | Useful signal, early traction, worth monitoring |
| 1-4 | Low | Minor update, rumor, narrow relevance |

Raise the score when a trend affects roadmap, budget, hiring, compliance, open-source adoption, or competitive positioning. Lower it when evidence is weak, duplicated, only speculative, or based only on short-lived GitHub hype.

## Report Format

Use this structure for readable output:

```markdown
# Trend Radar YYYY-WXX

**Period**: YYYY-MM-DD to YYYY-MM-DD  
**Window**: 1w / 1m / 3m  
**Generated**: YYYY-MM-DD  
**Scope**: AI/ML, Developer Tools, SaaS, Cloud/Infra, Security, Startup/Funding, Agent Platform Ecosystem  
**Signal Count**: 00 reviewed, 00 selected

## Executive Summary

- **1w signal**: ...
- **1m signal**: ...
- **3m signal**: ...
- **Model reranking**: ...
- **Claude agent signal**: ...
- **Company strategy**: ...
- **Updated from previous report**: ...
- **Biggest opportunity**: ...
- **Biggest risk**: ...
- **Recommended action**: ...

## Top Signals

| Rank | Signal | Category | Window | Score | Status | Why It Matters |
|------|--------|----------|--------|-------|--------|----------------|
| 1 | ... | AI/ML | 1w | 9 | Confirmed | ... |
| 2 | ... | Developer Tools | 1m | 8 | Confirmed | ... |
| 3 | ... | SaaS | 3m | 7 | Watch | ... |

## GitHub Trending Watch

| Repository | Category | Window | Momentum | Why It Matters | Caveat |
|------------|----------|--------|----------|----------------|--------|
| owner/repo | AI/ML | 1w | +000 stars, 0 releases | ... | ... |
| owner/repo | Developer Tools | 1m | +000 stars, active issues | ... | ... |

## Model Reranking Watch

**Leaderboard**: LMArena / Artificial Analysis / LiveBench / SWE-bench / OpenRouter  
**Checked**: YYYY-MM-DD HH:MM TZ  

| Rank | Model | Provider | Metric | Leaderboard | Change | Core Reason |
|------|-------|----------|--------|-------------|--------|-------------|
| 1 | ... | ... | score / usage | ... | +0 | ... |
| 2 | ... | ... | score / usage | ... | -1 | ... |
| 3 | ... | ... | score / usage | ... | new | ... |
| 4 | ... | ... | score / usage | ... | 0 | ... |
| 5 | ... | ... | score / usage | ... | +2 | ... |
| 6 | ... | ... | score / usage | ... | ... | ... |
| 7 | ... | ... | score / usage | ... | ... | ... |
| 8 | ... | ... | score / usage | ... | ... | ... |
| 9 | ... | ... | score / usage | ... | ... | ... |
| 10 | ... | ... | score / usage | ... | ... | ... |

## Claude Agent Watch

| Signal | Area | Window | Status | Core Change | Action |
|--------|------|--------|--------|-------------|--------|
| ... | managed agents | 1w | Confirmed | ... | ... |
| ... | agent teams | 1m | Watch | ... | ... |

## Company Strategy Watch

| Company | Latest Move | Strategy Direction | Window | Status | Implication |
|---------|-------------|--------------------|--------|--------|-------------|
| OpenAI | ... | agents / models / apps / enterprise | 1m | Updated | ... |
| Anthropic | ... | agents / coding / enterprise / safety | 1m | Updated | ... |
| Alibaba Qwen | ... | models / open source / cloud API / enterprise | 1m | Updated | ... |
| Zhipu AI | ... | GLM models / agents / enterprise / domestic ecosystem | 1m | Updated | ... |
| Google Gemini/Gemma | ... | flagship models / open-weight models / ecosystem / distribution | 1m | Watch | ... |
| Microsoft/GitHub | ... | developer tools / enterprise | 1m | Watch | ... |

## Action Items

- [ ] ...
- [ ] ...
- [ ] ...

## Category Deep Dive

### AI/ML

#### [Signal Title]

- **Score**: 9/10
- **Status**: Confirmed / Watch / Rumor
- **Window**: 1w / 1m / 3m
- **What changed**: ...
- **Why it matters**: ...
- **Core change since last report**: new / updated / continuing / resolved
- **Evidence**: [Source name](URL), [Source name](URL)
- **Claude agent signal**: managed agents / agent teams / Claude Code / API primitive if relevant
- **Company strategy**: company, strategic direction, latest move if relevant
- **Model reranking**: leaderboard, rank, score/usage, change reason if relevant
- **GitHub signal**: repo link, stars/forks/releases if relevant
- **Impact window**: immediate / 1-3 months / 6-12 months
- **Watch next**: ...

### Developer Tools

#### [Signal Title]

- **Score**: 8/10
- **Status**: Confirmed
- **Window**: 1w / 1m / 3m
- **What changed**: ...
- **Why it matters**: ...
- **Core change since last report**: new / updated / continuing / resolved
- **Evidence**: [Source name](URL)
- **Claude agent signal**: managed agents / agent teams / Claude Code / API primitive if relevant
- **Company strategy**: company, strategic direction, latest move if relevant
- **Model reranking**: leaderboard, rank, score/usage, change reason if relevant
- **GitHub signal**: repo link, stars/forks/releases if relevant
- **Impact window**: ...
- **Watch next**: ...

## Weekly Stats

| Category | 1w Signals | 1m Signals | 3m Signals | Selected | Critical |
|----------|------------|------------|------------|----------|----------|
| AI/ML | 00 | 00 | 00 | 00 | 00 |
| Developer Tools | 00 | 00 | 00 | 00 | 00 |
| SaaS | 00 | 00 | 00 | 00 | 00 |

## Watchlist for Next Week

- [ ] ...
- [ ] ...
- [ ] ...

## Sources Reviewed

- [Source](URL) - short note
- [Source](URL) - short note

---

Generated by `tech-trend-radar`.
```

## Writing Guidelines

- Lead with the conclusion, then provide evidence.
- Keep each signal detailed enough to be useful: one short paragraph plus 4-8 evidence bullets for major signals.
- Use tables for comparison, especially across `1w`, `1m`, and `3m` windows.
- Include links for every important claim.
- For model reranking, include the leaderboard name, timestamp, metric definition, and current top 10.
- For OpenAI, Anthropic, Alibaba Qwen, and Zhipu AI strategy, include latest public moves, strategic direction, and implication in every monthly report.
- For Claude agent updates, prefer official Anthropic sources and extract the core change, affected users, and recommended action.
- Include GitHub repository links for open-source signals.
- If a topic was included in a previous report, still refresh it and write the newest delta.
- Avoid hype words unless the evidence supports them.
- Do not mix facts and speculation. Use `Confirmed`, `Watch`, or `Rumor`.
- When data is missing, say what is missing and how that affects confidence.

## Output Location

Save reports to:

```text
memory/research/tech-trend-radar-YYYY-WXX.md
```

If the user requests a different scope, include it in the filename:

```text
memory/research/tech-trend-radar-ai-agents-YYYY-WXX.md
memory/research/tech-trend-radar-ai-agents-1m-YYYY-MM.md
memory/research/tech-trend-radar-ai-agents-3m-YYYY-QN.md
```

## Cron Setup Example

Run every Monday at 09:00:

```bash
0 9 * * 1 openclaw run tech-trend-radar
```

## Event Bus Integration

When a report is generated, publish:

```text
events/tech-trend-radar-update-YYYY-MM-DD.json
```

Format:

```json
{
  "type": "tech-trend-radar-report-generated",
  "timestamp": "2026-02-14T09:00:00Z",
  "week": "2026-W07",
  "window": "1w",
  "scope": ["AI/ML", "Developer Tools", "SaaS"],
  "highlights": [
    {
      "title": "...",
      "score": 9,
      "category": "AI/ML",
      "status": "Confirmed",
      "window": "1w"
    }
  ],
  "githubTrending": [
    {
      "repository": "owner/repo",
      "category": "Developer Tools",
      "window": "1w",
      "momentum": "+000 stars"
    }
  ],
  "modelReranking": {
    "leaderboard": "LMArena Text Arena Overall",
    "checkedAt": "2026-04-15T00:00:00Z",
    "top10": [
      {
        "rank": 1,
        "model": "...",
        "provider": "...",
        "metric": "..."
      }
    ],
    "coreChanges": ["..."]
  },
  "companyStrategy": [
    {
      "company": "OpenAI",
      "latestMove": "...",
      "strategyDirection": "...",
      "window": "1m",
      "status": "Updated",
      "implication": "..."
    },
    {
      "company": "Anthropic",
      "latestMove": "...",
      "strategyDirection": "...",
      "window": "1m",
      "status": "Updated",
      "implication": "..."
    },
    {
      "company": "Alibaba Qwen",
      "latestMove": "...",
      "strategyDirection": "...",
      "window": "1m",
      "status": "Updated",
      "implication": "..."
    },
    {
      "company": "Zhipu AI",
      "latestMove": "...",
      "strategyDirection": "...",
      "window": "1m",
      "status": "Updated",
      "implication": "..."
    }
  ],
  "claudeAgentSignals": [
    {
      "signal": "...",
      "area": "managed agents",
      "window": "1w",
      "status": "Confirmed",
      "coreChange": "...",
      "action": "..."
    }
  ],
  "signalsReviewed": 96,
  "signalsSelected": 12,
  "criticalSignals": 3
}
```

## Customization

Edit keyword configuration at:

```text
workspace/tech-trend-radar-keywords.json
```

Example:

```json
{
  "AI/ML": ["OpenAI", "Claude", "Gemini", "Gemma", "Google Gemma", "Llama", "Qwen", "通义千问", "GLM", "智谱", "DeepSeek", "Kimi", "文心", "混元", "豆包", "AI agents", "SWE-bench", "model reranking", "Claude managed agents", "Claude agent teams"],
  "Company Strategy": ["OpenAI strategy", "Anthropic strategy", "Alibaba Qwen strategy", "阿里千问趋势", "通义千问", "Zhipu AI strategy", "智谱趋势", "GLM", "Google Gemini strategy", "Google Gemma strategy", "Gemma open model", "Microsoft AI strategy", "Meta AI strategy", "xAI strategy", "DeepSeek strategy", "Moonshot AI strategy", "Baidu ERNIE strategy", "Tencent Hunyuan strategy", "ByteDance Doubao strategy", "AI pricing", "enterprise AI", "consumer AI apps", "agent platform strategy"],
  "Claude Agents": ["Claude managed agents", "Claude agent teams", "Claude Code", "Anthropic agents", "MCP", "tool use", "computer use", "agent orchestration", "enterprise controls", "connectors"],
  "Model Reranking": ["LMArena", "Text Arena", "Artificial Analysis", "LiveBench", "SWE-bench", "OpenRouter rankings", "open-weight model leaderboard", "Gemma ranking", "Llama ranking", "Chinese model leaderboard", "Qwen ranking", "GLM ranking", "DeepSeek ranking", "Kimi ranking", "top 10 AI models"],
  "Developer Tools": ["Codex", "GitHub Copilot", "Cursor", "Claude Code", "Vercel", "LangGraph", "GitHub Trending"],
  "GitHub Trending": ["AI", "LLM", "agent", "RAG", "MCP", "devtools", "security", "TypeScript", "Python", "Rust", "Go"],
  "SaaS": ["Notion AI", "Linear", "Slack AI"],
  "Agent Platform Ecosystem": ["Anthropic", "Claude API", "Claude managed agents", "Claude agent teams", "Claude Code", "OpenAI", "Codex", "OpenAI Agents SDK", "Alibaba Qwen", "通义千问", "Zhipu GLM", "智谱", "Google Gemini", "Google Gemma", "Gemma", "Gemini agents", "GitHub Copilot", "Copilot coding agent", "MCP", "OpenClaw", "HarnessClaw"],
  "windows": ["1w", "1m", "3m"]
}
```

Keep keyword lists specific enough to reduce noise, but broad enough to catch new product names and adjacent market shifts.

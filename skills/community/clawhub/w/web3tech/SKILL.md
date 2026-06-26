---
name: web3tech
description: Crypto project research, new coin discovery, due diligence, developer analysis, whitepaper validation, code similarity checks, and AI-powered development monitoring — all via the web3tech MCP server.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - WEB3TECH_API_KEY
    primaryEnv: WEB3TECH_API_KEY
    emoji: "🔬"
    homepage: https://web3tech.org
---

# Web3Tech Crypto Research

Use this skill for crypto project research with the `web3tech` MCP server.

## Before You Start

- Check whether the `web3tech` MCP server is available.
- If unavailable, say so briefly and continue with a best-effort fallback.
- Do not invent missing metrics, rankings, timelines, whitepaper facts, or developer history.

## Choose the Right Path

| User wants | Start with |
|------------|-----------|
| Project due diligence, comparison, technical risk | `references/due-diligence.md` |
| New coin discovery, novelty screening, watchlist | `references/new-coin-screening.md` |
| Output formatting | `references/output-templates.md` |

## Tool Rules

- `web3tech_search_coins` — resolve naming ambiguity only.
- `web3tech_coin_analysis` — default baseline for any serious research.
- `web3tech_top_analyzed_coins` — discover high-quality projects with existing scores.
- `web3tech_hot_coins` — find trending projects by views and community activity.
- `web3tech_new_coins` — source candidates, not final judgments.
- `web3tech_new_coin_detail` — review before branching into deeper diligence.
- `web3tech_search_developers` — find developers by name or GitHub handle.
- `web3tech_project_developers` — list before profiling individuals.
- `web3tech_developer_profile` — only for contributors that materially affect the answer.
- `web3tech_project_timeline` — when recent execution quality matters.
- `web3tech_supervision_overview` — AI daily development health check.
- `web3tech_code_similarity` — when originality, fork risk, or code reuse matters.
- `web3tech_whitepaper_analysis` — when claims, feasibility, or tokenomics matter.
- `web3tech_knowledge_search` — interpret technical concepts, not replace project evidence.

## Efficiency

- Due diligence: 3–6 tool calls.
- New coin screening: 3–8 tool calls.
- Do not run deep tools on every candidate from a broad search.
- Stop once you have enough evidence for a defensible answer.

## Output Rules

- Evidence-first conclusions.
- Separate observed facts from interpretation.
- If evidence is mixed or thin, say so explicitly.
- Treat novelty as a lead, not proof.
- Do not present early-stage projects as validated winners.

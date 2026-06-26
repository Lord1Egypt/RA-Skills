# Dev Update: Search Quality v2 + MLX Local LLM

**Date:** 2026-03-15
**Author:** CC-Mini
**Session:** memory-crstal01 (continued from Mar 13-14)

---

## Summary

Six search quality features from QMD v2.0 analysis, plus MLX local LLM infrastructure for Apple Silicon. All coded, tested, merged. Not yet deployed.

## What Shipped

### Search Quality (PR #75)

1. **Intent parameter.** Disambiguates queries without adding search terms. `crystal search "security" --intent "1Password"` steers toward 1Password results. Flows through expansion prompt (guides LLM variations), disables strong-signal bypass, prepended to rerank query. Available via CLI `--intent`, MCP `intent`.

2. **candidateLimit.** Tunable rerank pool size. `crystal search "query" --candidates 60`. Default stays 40. More candidates = better recall, slower reranking. Available via CLI `--candidates`, MCP `candidate_limit`.

3. **Explain mode.** Per-result scoring breakdown showing FTS score, vector score, RRF rank, reranker score, recency weight, and final blended score. `crystal search "query" --explain`. Available via CLI `--explain`, MCP `explain`.

4. **Persistent LLM cache.** `llm_cache` table in crystal.db. Expansion and reranking results cached with 7-day TTL. Content-addressable reranking (keyed by query + sorted passage hashes). Same query = instant on repeat searches. Configurable TTL via `CRYSTAL_CACHE_TTL_DAYS`.

5. **Structured search API.** `crystal.structuredSearch(queries)` accepts pre-expanded StructuredQuery[] (lex, vec, hyde). Skips LLM expansion entirely. Agents construct their own queries when they know what they want. RRF fusion with first list weighted 2x.

### MLX Local LLM (PR #76)

6. **MLX auto-install.** New `src/mlx-setup.ts` with full setup flow:
   - `detectPlatform()` ... Apple Silicon / Intel Mac / Linux / other
   - `installMlxLm()` ... uv > pip3 > pip3 --user fallback chain
   - `createLaunchAgent()` ... always-on MLX server via LaunchAgent
   - `verifyServer()` ... 30s warmup wait for model loading
   - `setupMlx()` ... full flow: detect, install, configure, start, verify

7. **Crystal MLX CLI.** `crystal mlx setup/status/stop` subcommands.

8. **Doctor check #13.** MLX health check with three states: not installed, installed but not running, running. Suggests fix for each.

9. **Installer integration.** `crystal init` detects Apple Silicon and suggests `crystal mlx setup` when MLX is not installed.

10. **Port 18791.** LDM service ports: 18789 (OpenClaw), 18790 (Crystal Core), 18791 (MLX LLM).

11. **Model: Qwen 2.5 3B Instruct 4-bit.** `mlx-community/Qwen2.5-3B-Instruct-4bit`. ~1.5 GB, fast on M-series, good at instruction following for query expansion and relevance scoring.

### Also

- QMD v2.0 analysis written (`ai/product/notes/2026-03-15--cc-mini--qmd-v2.0-analysis.md`)
- Search quality plan written (`ai/product/plans-prds/current/2026-03-15--cc-mini--search-quality-qmd-v2-port.md`)
- MLX plan moved from upcoming to current
- Stashed roadmap + readme-first updates recovered and committed (PR #74)
- README footer: QMD credit restored, CLA + dual license confirmed on both repos

## Files Changed

| File | Change |
|------|--------|
| `src/search-pipeline.ts` | Intent support, candidateLimit param, explain traces, DeepSearchResult type |
| `src/llm.ts` | Intent in expansion prompt, persistent DB cache (expansion + reranking), setLLMCacheDb() |
| `src/core.ts` | llm_cache table schema, deepSearch options, structuredSearch() method, StructuredQuery type |
| `src/mcp-server.ts` | intent, candidate_limit, explain params on crystal_search, LLM cache DB wiring |
| `src/cli.ts` | --intent, --candidates, --explain flags, crystal mlx subcommand |
| `src/mlx-setup.ts` | **NEW** ... full MLX setup, doctor check, state management |
| `src/doctor.ts` | MLX health check (#13) |
| `src/installer.ts` | MLX detection in crystal init flow |

## What This Enables

- **Free deep search.** MLX replaces OpenAI API calls for expansion + reranking. Zero cost per search.
- **Faster repeated searches.** Persistent cache means the LLM call happens once per unique query.
- **Smarter agent queries.** Structured search lets agents skip expansion when they know what they want.
- **Debuggable search.** Explain mode shows exactly why each result ranked where it did.
- **Offline search quality.** MLX works without internet. API fallback when MLX is down.

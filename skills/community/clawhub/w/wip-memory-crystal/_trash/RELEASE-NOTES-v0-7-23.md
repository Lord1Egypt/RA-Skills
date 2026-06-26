# Release Notes: Memory Crystal v0.7.23

**Date:** 2026-03-15

## Search Quality v2 + MLX Local LLM

This release adds six search quality features ported from the QMD v2.0 analysis, plus the complete MLX local LLM infrastructure for Apple Silicon. Deep search is now disambiguatable, cacheable, debuggable, and can run entirely offline on Apple Silicon.

### Intent parameter

Disambiguates queries without adding search terms. `crystal search "security" --intent "1Password"` steers results toward 1Password-related security instead of repo permissions or agent secrets. Intent flows through the expansion prompt (guides LLM variations), disables strong-signal bypass (keyword match might not be what the caller wants), and is prepended to the rerank query. Available via CLI `--intent` and MCP `intent`.

### Persistent LLM cache

Expansion and reranking results are now cached in crystal.db (`llm_cache` table) with a 7-day TTL. Same query = instant on repeat searches. Reranking cache is content-addressable (keyed by query + sorted passage hashes), so identical content from different sessions shares cached scores. Configurable via `CRYSTAL_CACHE_TTL_DAYS` env var.

### Explain mode

Per-result scoring breakdown showing FTS score, vector score, RRF rank, reranker score, recency weight, and final blended score. `crystal search "query" --explain`. Available via CLI `--explain` and MCP `explain`. Makes search quality transparent and debuggable.

### candidateLimit

Tunable rerank pool size. `crystal search "query" --candidates 60`. Default stays 40. More candidates = better recall, slower reranking. Available via CLI `--candidates` and MCP `candidate_limit`.

### Structured search API

`crystal.structuredSearch(queries)` accepts pre-expanded StructuredQuery[] with typed sub-queries (lex, vec, hyde). Skips LLM expansion entirely. Agents construct their own queries when they already know what they want. RRF fusion with first list weighted 2x.

### MLX local LLM (Phase 3)

Complete auto-install infrastructure for running a local LLM on Apple Silicon:

- `crystal mlx setup` detects Apple Silicon, installs mlx-lm (uv > pip3 > pip3 --user), creates LaunchAgent for always-on server
- Model: `mlx-community/Qwen2.5-3B-Instruct-4bit` (~1.5 GB, fast on M-series)
- Port 18791 (18789 OpenClaw, 18790 Crystal Core, 18791 MLX)
- `crystal mlx status` and `crystal mlx stop` for server management
- `crystal doctor` check #13: MLX health (not installed / down / running)
- `crystal init` detects Apple Silicon and suggests MLX setup
- State file at `~/.ldm/state/mlx-server.json`

### Also in this release

- QMD v2.0 analysis documented (`ai/product/notes/`)
- Search quality plan written (`ai/product/plans-prds/current/`)
- MLX plan moved from upcoming to current
- Stashed roadmap + readme-first updates recovered (PR #74)

Closes #57, #63, #64.

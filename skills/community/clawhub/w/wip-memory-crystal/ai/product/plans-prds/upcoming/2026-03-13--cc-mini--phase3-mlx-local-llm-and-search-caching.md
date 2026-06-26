# Plan: Phase 3 ... MLX Local LLM + Search Caching

**Date:** 2026-03-13
**Author:** CC-Mini + Parker
**Priority:** High (next major search quality improvement)
**Related:** `current/search-quality-full-plan.md` (Phase 3 section), `../product-ideas/local-embeddings-zero-config.md`
**Depends on:** Phase 1 (done), Phase 2 core (done), Score normalization (done v0.7.19)

---

## What This Does

Two things:

1. **MLX local LLM** for query expansion and re-ranking. Free, fast, private. Replaces OpenAI API calls for deep search. Works offline.

2. **Persistent caching** for expansion and reranking results. Currently in-memory only (lost every session). Persisted to crystal.db means repeated queries are instant.

## Why

Right now deep search uses OpenAI API (gpt-4o-mini) for query expansion and re-ranking. That costs ~$0.001/search. MLX on Apple Silicon is free, faster for small models, and sovereign. For the narrow tasks (3 sentence rewrites, relevance scoring), a 2B local model is 90%+ as effective.

The caching matters because agents search the same things repeatedly. "Parker" gets searched on every boot. Expansion cache means the LLM call happens once, not every time.

## Current State

- `src/llm.ts` already has MLX detection (checks `localhost:8080/v1/models`)
- Provider cascade: MLX > Ollama > OpenAI > Anthropic > none
- Expansion cache: in-memory Map (line 58), lost per process
- Reranking cache: none
- `mlx-setup.ts`: does not exist
- `crystal init`: does not set up LLM provider
- MLX server: not installed on the Mac mini

## What Needs to Be Built

### 1. MLX Auto-Install (`src/mlx-setup.ts`)

New file. Handles:

```
detectAppleSilicon() ... uname -m === arm64
installMlxLm() ... pip install mlx-lm (or pipx)
pullModel() ... mlx_lm.convert or download pre-quantized
startServer() ... mlx_lm.server --model <path> --port 8080
createLaunchAgent() ... ~/Library/LaunchAgents/ai.ldm.mlx-server.plist
verifyServer() ... fetch localhost:8080/v1/models
```

**Model choice:** `mlx-community/Qwen2.5-3B-Instruct-4bit` (or latest equivalent)
- 4-bit quantized, ~1.5 GB on disk
- Fast on M-series chips
- Good at instruction following (query expansion, relevance scoring)
- Alternatives: `Phi-3.5-mini-instruct-4bit`, `Llama-3.2-3B-Instruct-4bit`

**LaunchAgent plist:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.ldm.mlx-server</string>
  <key>ProgramArguments</key>
  <array>
    <string>/path/to/python</string>
    <string>-m</string>
    <string>mlx_lm.server</string>
    <string>--model</string>
    <string>~/.ldm/models/qwen2.5-3b-instruct-4bit</string>
    <string>--port</string>
    <string>8080</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/tmp/mlx-server.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/mlx-server.log</string>
</dict>
</plist>
```

### 2. Installer Flow (`crystal init` additions)

After existing setup steps, add LLM provider setup:

```
crystal init
  ... existing steps (scaffold, discover, capture, hooks, MCP) ...

  Step N: Search quality LLM
  a. Detect Apple Silicon
     -> Yes: offer MLX install
        "Install local LLM for search quality? Free, fast, works offline. ~1.5 GB. (Y/n)"
        -> pip install mlx-lm
        -> Download model to ~/.ldm/models/
        -> Create LaunchAgent
        -> Verify localhost:8080
     -> No: skip to fallback
  b. If MLX not available or declined:
     Check for existing API keys (OpenAI via 1Password, Anthropic)
     -> Found: "Using OpenAI/Anthropic for deep search."
     -> Not found: "Deep search unavailable. Standard search still works."
  c. Test search to verify
```

### 3. Persistent Expansion Cache

Add to crystal.db:

```sql
CREATE TABLE IF NOT EXISTS search_cache (
  query_hash TEXT PRIMARY KEY,
  query TEXT NOT NULL,
  cache_type TEXT NOT NULL,  -- 'expansion' | 'rerank'
  result TEXT NOT NULL,       -- JSON
  provider TEXT NOT NULL,     -- which LLM produced this
  created_at TEXT NOT NULL,
  hit_count INTEGER DEFAULT 0
);
CREATE INDEX idx_search_cache_type ON search_cache(cache_type);
```

In `llm.ts`:
- Before calling LLM for expansion: check `search_cache` for query hash
- After getting result: store in `search_cache`
- Same for reranking (hash = query + passage hashes)
- Cache entries expire after 7 days (configurable)
- `crystal cleanup` should also clean expired cache entries

### 4. Persistent Reranking Cache

Same table as expansion cache, different `cache_type`. The key is a hash of (query + sorted passage hashes). If the same query hits the same passages, return the cached scores.

### 5. Grammar-Constrained Expansion Output

The expansion prompt asks for `lex:`, `vec:`, `hyde:` lines. But LLMs sometimes add extra text. Options:
- MLX supports grammar/schema constraints natively
- Or: stricter prompt + post-processing (current approach works OK)
- Low priority. Current fallback handles malformed output.

## Files to Create/Modify

| File | Change |
|------|--------|
| `src/mlx-setup.ts` | **NEW** ... detect, install, pull, start, LaunchAgent |
| `src/llm.ts` | Add DB cache lookup/store. Replace in-memory Map. |
| `src/core.ts` | Add `search_cache` table to `initSqliteTables()` |
| `src/cli.ts` | Add LLM setup to `crystal init`. Add `crystal mlx` subcommand? |
| `src/installer.ts` | Wire MLX setup into install/update flow |
| `src/doctor.ts` | Add MLX health check (is server running? model loaded?) |
| `skills/memory/SKILL.md` | Add LLM provider section to onboarding |

## Dependencies

- Python 3.10+ (for mlx-lm). Check if installed.
- pip or pipx for installing mlx-lm
- ~1.5 GB disk for model
- Apple Silicon required (Intel Macs can't run MLX)
- Port 8080 available

## Testing

1. `crystal init` on Apple Silicon ... should offer MLX install
2. `crystal init` on Intel ... should skip MLX gracefully
3. `crystal search "test"` with MLX running ... should use MLX (check stderr for "LLM provider: MLX")
4. `crystal search "test"` twice ... second search should hit expansion cache
5. `crystal doctor` ... should show MLX status
6. Kill MLX server, search again ... should fall back to OpenAI/Anthropic
7. `crystal cleanup` ... should clean expired cache entries

## Open Questions

1. Which model? Qwen 2.5 3B vs Phi 3.5 mini vs Llama 3.2 3B? Need to test expansion/reranking quality.
2. pip vs pipx for mlx-lm install? pipx is cleaner but less common.
3. Model storage: `~/.ldm/models/` or `~/.cache/mlx/`? LDM convention says everything under `~/.ldm/`.
4. Should `crystal init` auto-install without asking, or always prompt?
5. Cache expiry: 7 days? 30 days? Per-query TTL based on result freshness?

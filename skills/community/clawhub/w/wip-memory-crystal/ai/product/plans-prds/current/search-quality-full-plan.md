# Plan: Search Quality Fix ... Port QMD Features to Memory Crystal (Full Plan)

**Created:** 2026-03-04
**Updated:** 2026-03-05
**Status:** Phase 1 + Phase 2 core complete. Phase 3 planning. Phase 4 blocked.
**Agent:** CC-Mini
**Source:** Claude plan `agile-orbiting-crescent.md` (includes Phases 3-4 not yet in the original plan)
**Dev Update:** `ai/dev-updates/2026-03-05--00-50--cc-mini--search-quality-qmd-port.md`

## Context

After consolidating 3 memory stores into 1 crystal.db (207K chunks), search quality degraded. Recent content gets buried by older semantically similar content. The recency weight (`Math.max(0.5, 1.0 - ageDays * 0.01)`) is too weak for a corpus this size. With 16K chunks, mediocre ranking was fine. With 207K, it's not.

QMD (Tobi Lutke's query tool, MIT license) has battle-tested search quality features we already partially ported (RRF, BM25, FTS5). The remaining features address exactly our problem.

## What We're Building

Four phases. Phase 1 is a quick fix. Phase 2 ports QMD's LLM features. Phase 3 builds the installer/onboarding flow. Phase 4 is future (MCP sampling).

---

### Phase 1: Quick Fix (recency boost + time filter) ... DONE

**Goal:** Make recent content competitive again without any new dependencies.
**Status:** Complete. Deployed 2026-03-05.

**Changes:**

1. **Stronger recency curve** in `recencyWeight()` (core.ts:607-611)
   - Exponential decay: `Math.max(0.3, Math.exp(-ageDays * 0.1))`
   - Day 0: 1.0, Day 1: 0.90, Day 3: 0.74, Day 7: 0.50, Day 14: 0.25 (floor 0.3)

2. **Time-filtered search** ... `--since 24h/7d/30d` on CLI, `time_filter` on MCP

3. **Fetch more candidates** ... `Math.max(limit * 5, 50)` (was `limit * 3, 30`)

---

### Phase 2: QMD Port (query expansion + LLM re-ranking) ... CORE DONE, TUNING REMAINING

**Goal:** Port QMD's LLM-powered search quality features.
**Status:** Core pipeline built and deployed. Deep search is the default. Tuning and local model setup remaining.

**Features ported:**

1. [x] Query expansion (3 variations: lex, vec, hyde)
2. [x] Strong signal detection (BM25 probe, skip expansion if obvious match)
3. [x] LLM re-ranking (top 40 RRF candidates scored by LLM)
4. [x] Position-aware score blending (75/25 top 3, 60/40 4-10, 40/60 11+)
5. [x] Tiered RRF weights (BM25 2x, vector 1x)
6. [x] Deep as default (no --deep flag needed)
7. [x] Op-secrets integration for API keys

**Current working provider:** OpenAI API via op-secrets.

**Remaining:**
- [ ] Score normalization (100% match scores appearing)
- [ ] Expansion cache persisted to DB
- [ ] Reranking cache persisted to DB
- [ ] Grammar-constrained output for expansion
- [ ] MLX server setup + LaunchAgent
- [ ] Ollama chat model pull + test

---

### Phase 3: Installer / Onboarding Flow + Provider Cascade Fix

**Added:** 2026-03-05
**Status:** Planning
**Context:** Parker's feedback: "We should not be patching software. We should be building releases and installing their releases to make sure they work. Dogfood every release."

#### Problem

1. **Provider cascade is wrong.** Current order: MLX > Ollama > OpenAI > Anthropic > none. Should be: MLX first (always installed on Apple Silicon), then Anthropic direct key, then OpenAI/Ollama as fallbacks.

2. **OAuth tokens don't work for direct API calls.** Claude Code uses `sk-ant-oat01-` tokens internally, but these return 401 with the Anthropic Messages API. MCP subprocesses can't piggyback on Claude Code's auth. Direct API keys (`sk-ant-api03-`) work but require separate billing.

3. **No installer flow for the LLM provider.** `crystal init` doesn't set up the search quality LLM.

4. **Deployment is ad-hoc.** Patching deployed code instead of building releases and installing them.

#### Corrected Provider Cascade

| Priority | Provider | How it's set up | Cost |
|----------|----------|-----------------|------|
| 1 | **MLX (local)** | Always installed on Apple Silicon during `crystal init`. LaunchAgent for always-on. | Free |
| 2 | **Anthropic API** | Direct API key (`sk-ant-api03-`) via env var or 1Password. NOT OAuth tokens. | ~$0.001/search |
| 3 | **OpenAI API** | Key via env var or 1Password. Only offered during install if #1 and #2 unavailable. | ~$0.001/search |
| 4 | **Ollama (local)** | Only offered during install if #1-#3 unavailable. | Free |
| 5 | **None** | Falls back to Phase 1 (hybrid search, no LLM expansion). | Free |

**Why MLX first:** Free, fast, sovereign. 2x faster than Ollama on Apple Silicon. Works offline. For the narrow tasks we need (query expansion = 3 sentence rewrites, reranking = relevance scoring), a 2B local model is 90%+ as effective as Haiku. No API keys, no cost.

**Why MLX is always installed:** On Apple Silicon, there's no reason not to. Even if API keys are available, MLX is the zero-cost fallback when network is down.

#### Installer Flow (`crystal init` additions)

```
crystal init
  1. Scaffold LDM directories (existing)
  2. Discover existing sessions (existing)
  3. Set up capture (existing)
  4. NEW: Set up search quality LLM
     a. Detect Apple Silicon -> if yes, install MLX + pull model + create LaunchAgent
     b. Check for Anthropic API key (env, 1Password, or prompt user)
        - If OAuth token found: explain it won't work, offer to set up direct API key
        - If direct key found: save to config
     c. If no Anthropic key and no MLX: ask "Do you want to use OpenAI or Ollama?"
        - OpenAI: prompt for API key
        - Ollama: check if running, suggest model pull
     d. If nothing available: explain deep search will be unavailable, Phase 1 still works
  5. Deploy to local targets (existing)
  6. Verify with a test search
```

#### MLX Auto-Install

**New file:** `src/mlx-setup.ts`
- Detect Apple Silicon (uname -m === arm64)
- Install mlx-lm via pip
- Pull model: `mlx-community/Qwen3.5-2B-Instruct-4bit`
- Create LaunchAgent: `~/Library/LaunchAgents/ai.ldm.mlx-server.plist`
- Verify `localhost:8080/v1/models` responds

#### Development Workflow (Dogfooding Rule)

Every release tested via installer, not by patching deployed code:
```bash
cd components/memory-crystal-private
npm run build
wip-release patch --notes="description"
crystal init --upgrade
crystal doctor
crystal search "test query"
```

#### Files to Modify

| File | Changes |
|------|---------|
| `src/llm.ts` | Reorder cascade: MLX > Anthropic > OpenAI > Ollama > none |
| `src/cli.ts` | Add LLM provider setup to `crystal init`. Add `--upgrade` flag. |
| `src/mlx-setup.ts` | **NEW** ... MLX detection, install, LaunchAgent creation |
| `skills/memory/SKILL.md` | Add search quality section to onboarding flow |

---

### Phase 4: MCP Sampling for Claude Max Subscription (Future ... Blocked on Anthropic)

**Added:** 2026-03-05
**Status:** Research complete. Blocked on Claude Code implementing MCP sampling.
**Why this matters:** iOS devices have no MLX or Ollama. Claude Max subscribers shouldn't need a separate API key.

#### What is MCP Sampling?

The MCP spec defines a `sampling/createMessage` request where an MCP server can ask the client (Claude Code) to generate a completion. The server specifies priority hints (costPriority, speedPriority, intelligencePriority) rather than requesting specific models.

If Claude Code supported this, Memory Crystal's MCP server could:
1. Ask Claude Code: "Expand this query into 3 variations" (using Haiku via the user's subscription)
2. Ask Claude Code: "Score these passages for relevance" (using Haiku via the user's subscription)
3. No separate API key needed. Works on iOS, macOS, everywhere Claude runs.

#### Current Status

- **Spec:** Mature and finalized (MCP v2025-11-25). Includes human-in-the-loop requirements.
- **Claude Code:** NOT implemented. [GitHub Issue #1785](https://github.com/anthropics/claude-code/issues/1785), 86+ upvotes, Anthropic engineers "looking into it" since June 2025.
- **VS Code:** Implemented (June 2025), proving it's technically feasible.

#### What We Should Do

1. Star/watch Issue #1785 to track progress.
2. Design the sampling integration now (add `sampling` provider to cascade in llm.ts).
3. File a use case comment on Issue #1785.

#### Updated Provider Cascade (with sampling, future)

| Priority | Provider | Platform | Cost |
|----------|----------|----------|------|
| 1 | **MCP Sampling** (Claude Code client) | Everywhere Claude runs (Mac, iOS, web) | Included in Max subscription |
| 2 | **MLX** (local Apple Silicon) | Mac only | Free |
| 3 | **Ollama** (local) | Any machine | Free |
| 4 | **OpenAI API** (key) | Everywhere | ~$0.001/search |
| 5 | **None** | Everywhere | Free (Phase 1 fallback) |

#### iOS Deep Search Path

Without MCP sampling, iOS users currently get Phase 1 only. Options:
- Cloud MCP Worker could proxy to Mac mini's MLX server
- MCP sampling (when available) uses the Claude app's own subscription
- Phase 1 still works without query expansion

---

## Summary: Implementation Priority

| Phase | Status | Priority | What |
|-------|--------|----------|------|
| Phase 1 | DONE | - | Recency fix, time filter, RRF weights |
| Phase 2 | CORE DONE | High | LLM pipeline built. Score tuning + caching remaining. |
| Phase 3 | PLANNING | High | MLX auto-install, installer flow, dogfooding workflow |
| Phase 4 | BLOCKED | Watch | MCP sampling. Star Issue #1785. Design the integration. |

**Next action:** Build Phase 3 (MLX setup + installer flow). Test by running the installer from the repo.

## Critical Files

| File | Role |
|------|------|
| `src/core.ts` | Search implementation, recencyWeight, parseSince, deepSearch |
| `src/mcp-server.ts` | MCP server tool definitions (time_filter, quality params) |
| `src/cli.ts` | CLI command definitions (--since flag) |
| `src/llm.ts` | **NEW** ... provider cascade, op-secrets, query expansion, re-ranking |
| `src/search-pipeline.ts` | **NEW** ... deep search pipeline (expand, search, RRF, rerank, blend) |
| QMD `src/store.ts` | Reference: lines 2204-2321, 2806-2985 |
| QMD `src/llm.ts` | Reference: lines 936-1071 |

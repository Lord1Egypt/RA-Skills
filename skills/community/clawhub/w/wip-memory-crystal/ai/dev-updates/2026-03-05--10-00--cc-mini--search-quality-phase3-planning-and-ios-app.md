# Dev Update: Search Quality Phase 3 Planning + LDM OS Native App Idea

**Date:** 2026-03-05 10:00 PST
**Agent:** CC-Mini
**Session type:** Planning, research, documentation

---

## What Happened

### Search Quality Plan Updates

Updated the search quality plan documents to reflect current state:

- **Phase 1:** DONE. Recency boost, time filter, RRF weights.
- **Phase 2:** CORE DONE. LLM pipeline (query expansion + re-ranking) built and deployed. OpenAI API working via op-secrets. Score tuning + caching remaining.
- **Phase 3:** PLANNING. MLX auto-install during `crystal init`, installer flow, dogfooding workflow. Provider cascade corrected: MLX first (free, local, always installed on Apple Silicon) > Anthropic direct API key > OpenAI > Ollama > none.
- **Phase 4:** BLOCKED. MCP sampling (Anthropic Issue #1785). Would let Crystal use Claude Max subscription for LLM calls. VS Code has it, Claude Code doesn't.

### Key Finding: OAuth Tokens Don't Work for Direct API Calls

- `sk-ant-oat01-` tokens (Claude Code's internal auth) return 401 from the Anthropic Messages API
- These go through a proprietary OAuth exchange flow. MCP subprocesses can't piggyback on it.
- Parker's existing repo `parkertoddbrooks/claude-max-access-sdk` documents the same issue
- Direct API keys (`sk-ant-api03-`) work but require separate billing
- Conclusion: MLX is the right default for local machines. MCP sampling is the future fix for iOS/everywhere.

### LDM OS Native App Product Idea (Major Expansion)

Expanded `product-ideas/native-apple-app-crystal-sync.md` from a simple sync idea into a full product vision:

**One native app that serves as the universal backend for every AI tool.**

Three core capabilities:
1. **Memory Crystal (local search + sync)** ... runs Crystal locally, MCP server for Claude/ChatGPT/Grok, CloudKit sync, offline support
2. **Local LLM via MLX Swift** ... on-device query expansion + reranking on A-series/M-series chips, solves iOS deep search without API keys
3. **Agent Secrets Vault** ... replaces 1Password for agents, iCloud Keychain-backed, per-agent access control

Also includes:
- Agent dashboard (visual list of agents, memories, activity)
- LDM OS file viewer (browse `~/.ldm/` visually)
- Backup center (full backup of OpenClaw, Claude Code, crystal.db, secrets)
- CLI wrapper (`ldm` command: search, remember, secret, llm, status, doctor)

The app makes AI tools interchangeable. Switch from Claude to ChatGPT and your memory + secrets stay.

### Plan Document Saved

Created `current/search-quality-full-plan.md` with all 4 phases. The original `current/search-quality-qmd-port.md` preserved and updated with checkmarks for completed work.

### Cleanup

- Trashed duplicate `roadmap 2.md` to `ai/_trash/roadmap-2-duplicate.md`

## Files Modified

| File | Change |
|------|--------|
| `ai/product/plans-prds/current/search-quality-qmd-port.md` | Updated with [x] checkmarks, corrected cascade, added Remaining Work |
| `ai/product/plans-prds/current/search-quality-full-plan.md` | NEW ... full plan with Phases 1-4 |
| `ai/product/product-ideas/native-apple-app-crystal-sync.md` | Major expansion: MLX Swift, secrets vault, dashboard, file viewer, backup, CLI |
| `ai/product/plans-prds/roadmap.md` | Updated Priority 7, added Priority 12 (native app), added Phase 1-2 to Done |
| `ai/product/readme-first.md` | Added llm.ts + search-pipeline.ts to Key Source Files, added deep search to What's Built, updated What's Missing |
| `ai/_trash/roadmap-2-duplicate.md` | Moved from `plans-prds/roadmap 2.md` |

## Decisions

- **MLX first** for LLM provider cascade (free, local, sovereign)
- **Do NOT build Phase 3 yet** ... Parker wants Core/Node shipped first, all docs updated before building
- **MCP sampling is the future** ... designed into the cascade but blocked on Anthropic
- **Native app is Priority 12** ... long-term vision, not near-term work

## Verified

- Embeddings saving in real-time (most recent chunk from current conversation)
- Both Claude Code CLI and OpenClaw contexts capturing correctly
- crystal.db at 207K+ chunks, all data consolidated

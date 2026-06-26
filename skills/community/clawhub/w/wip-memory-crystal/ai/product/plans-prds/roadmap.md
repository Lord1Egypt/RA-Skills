# Memory Crystal ... Roadmap

**Last updated:** 2026-04-28
**Current version:** v0.7.38

Items are either **Upcoming**, **Done**, or **Deprecated**. Never delete. Always move.

---

## Vision

Memory Crystal is sovereign memory infrastructure for AI agents. It captures every conversation, embeds it for search, consolidates it into narrative identity via Dream Weaver, and syncs across devices via encrypted relay. It works with any AI platform. It is also the entry point for LDM OS.

The four-layer model:

```
Capture         ... record everything (hooks, adapters, poller)
Memory          ... store and search (crystal.db, vector + keyword)
Reflection      ... consolidate what matters (Dream Weaver Protocol)
Communication   ... agents talk to each other (Bridge)
```

---

## Upcoming

### Priority 1 ... Update lesa-bridge to point at crystal.db

- [ ] Update lesa-bridge to point at crystal.db (or remove lesa_conversation_search, since crystal_search covers it now)

### Priority 2 ... Crystal Capture Adapters (adoption driver)

Auto-capture from every AI tool. See `../product-ideas/crystal-capture-auto-capture.md`.

We already have the capture pipeline (cc-hook.ts, cc-poller.ts, agent_end hook). The gap is adapters for other platforms.

- [ ] Desktop app file watchers (ChatGPT Desktop, Claude Desktop, Cursor)
- [ ] Formalize CaptureEvent interface (public adapter API)
- [ ] `/adapters` directory structure in repo
- [ ] Terminal wrapper (`mc run <command>`)
- [ ] Browser extension (chat.openai.com, claude.ai, perplexity.ai)

### Priority 3 ... Local Embeddings (zero-config default)

See `../product-ideas/local-embeddings-zero-config.md`.

- [ ] Add ONNX Runtime + MiniLM-L6-v2 as default embedding provider (384d, ~22MB model)
- [ ] Keep OpenAI/Google/Ollama as upgrade options
- [ ] Store embedding model name per chunk
- [ ] `crystal re-embed` command for provider migration
- [ ] Zero API keys required for new installs

### Priority 4 ... Chunked Dream Weaver Consolidation

200K char cap means full mode is lossy for mature agents (1000+ sessions). Need multi-pass.

- [ ] Process transcripts in chronological batches
- [ ] Generate intermediate narratives per batch
- [ ] Final consolidation pass over intermediate narratives
- [ ] Dream Weaver running on its own output

### Priority 5 ... Full LDM Sync (mirror the whole tree, not just the DB)

The mirror channel currently syncs crystal.db only. The node gets search, but not the actual files. Embeddings are pointers. The files are the artifacts. You need both. Eventually this includes images, videos, and anything agents create. A search result that points to a file that doesn't exist on the node is broken.

**Current state:**
- conversations channel: Node sends JSONL chunks to Core (working)
- mirror channel: Core pushes crystal.db snapshot to Node (working)
- Missing: the entire `~/.ldm/` file tree

**What the mirror should sync:**
- [ ] `~/.ldm/agents/{id}/memory/workspace/` ... SHARED-CONTEXT.md, MEMORY.md, TOOLS.md, all .md files
- [ ] `~/.ldm/agents/{id}/memory/daily/` ... daily logs
- [ ] `~/.ldm/agents/{id}/memory/journals/` ... Dream Weaver journals
- [ ] `~/.ldm/agents/{id}/memory/sessions/` ... session summaries
- [ ] `~/.ldm/agents/{id}/memory/transcripts/` ... raw JSONL session files
- [ ] `~/.ldm/agents/{id}/` ... SOUL.md, IDENTITY.md, CONTEXT.md, REFERENCE.md
- [ ] `~/.ldm/shared/` ... cross-agent shared files (Dream Weaver, etc.)
- [ ] Media files (images, videos, artifacts) ... future, but the architecture must support binary blobs now

**How it should work:**
- Core builds a manifest (file paths + hashes + sizes) of the full `~/.ldm/` tree
- Mirror push sends manifest + changed files (delta sync, not full copy every time)
- Node pulls manifest, downloads only what changed
- Conflict resolution for shared files (last-write-wins or timestamp-based merge)
- Large binary support (chunked upload/download for images, videos)

**Why this matters:** The embedding in crystal.db says "this chunk came from workspace/SHARED-CONTEXT.md" or "this is from an image at workspace/lesa-alley-3.png." If the file isn't on the node, the embedding is an orphan. Every artifact the embedding points to must be on every device.

OpenClaw already syncs workspace to `~/.ldm/agents/oc-lesa-mini/memory/workspace/` locally. This extends that to cross-device via the relay.

### Priority 6 ... Core...Node Command Dispatch

Relay Worker supports bidirectional commands, but Core...Node sender isn't wired up.

- [ ] Core-side command dispatch via relay
- [ ] Core orchestrating Nodes (trigger backup, request status, push config)
- [ ] Complete the mesh: any device can ask any other device to do things

### Priority 7 ... Layer 5 Automation (Warm-Start)

CONTEXT.md is the warm-start file but updating it isn't fully automated outside Dream Weaver runs.

- [ ] Auto-update CONTEXT.md after significant sessions
- [ ] Boot sequence reads CONTEXT.md on startup (currently manual for CC)
- [ ] Integrate with cc-hook Stop hook (end-of-session context write)

### Priority 8 ... Phase 3: MLX Local LLM + Search Caching

See `upcoming/2026-03-13--cc-mini--phase3-mlx-local-llm-and-search-caching.md` for full plan.

- [ ] `mlx-setup.ts`: detect Apple Silicon, install mlx-lm, pull model, create LaunchAgent
- [ ] `crystal init` LLM provider setup flow (offer MLX on Apple Silicon, fallback to API keys)
- [ ] Persistent expansion cache in crystal.db (same query = instant, 7-day TTL)
- [ ] Persistent reranking cache in crystal.db
- [ ] `crystal doctor` MLX health check
- [ ] Grammar-constrained expansion output (low priority)

### Priority 9 ... Search Quality (other remaining)

Phases 1-2 complete (see Done section). Remaining:

- [ ] Phase 3: MLX auto-install, installer flow (`crystal init` LLM setup), dogfooding workflow
- [ ] Phase 4: MCP sampling for Claude Max subscription (blocked on Anthropic, Issue #1785)
- [ ] Score normalization (100% match scores appearing)
- [ ] Expansion + reranking cache persisted to DB
- [ ] Grammar-constrained output for query expansion

### Priority 8b ... QMD v1.1.6 Features (from analysis)

See `../notes/2026-03-09--cc-mini--qmd-v1.1.6-analysis-and-recommendations.md`.

- [ ] Intent parameter for search (informational vs navigational vs analytical)
- [ ] Structured search API (typed results with metadata)
- [ ] Persistent content-addressable reranker cache
- [ ] Explain mode (score traces for debugging search quality)

See `current/search-quality-full-plan.md` for full plan (Phases 1-4).

### Priority 9 ... README Simplification

GPT feedback: too many concepts for first-time readers.

- [ ] Add 30-second mental model at top of README
- [ ] Four-layer narrative: Capture / Memory / Reflection / Communication
- [ ] `npx memory-crystal init` 1-command install alongside agent-native flow

### Priority 10 ... Deploy Relay Worker (Parker blocker)

- [ ] Generate encryption key, copy to both machines
- [ ] Create R2 bucket, set bearer tokens
- [ ] Deploy Worker
- [ ] End-to-end test: capture ... relay ... ingest ... mirror ... search

### Priority 11 ... Absorb Remaining Plugins

- [ ] Absorb lesa-bridge search tools into Memory Crystal (Bridge = communication only)

### Priority 12 ... Data Coverage Expansion

7 of 11 data stores aren't in the vector DB. Review which warrant ingestion:
- [ ] CLAUDE.md memories, auto-memory, Dream Weaver narratives, dev updates, identity docs

### Priority 13 ... LDM OS Native App (macOS + iOS)

Single native Apple app that serves as the universal backend for every AI tool. Combines three capabilities:

1. **Memory Crystal (local search + sync)** ... runs Crystal locally, registers as MCP server for Claude/ChatGPT/Grok, uses CloudKit for encrypted sync, works offline
2. **Local LLM via MLX Swift** ... on-device query expansion + reranking on A-series/M-series chips, solves iOS deep search problem without API keys or MCP sampling
3. **Agent Secrets Vault** ... replaces 1Password for agents, iCloud Keychain-backed, MCP-accessible `get_secret()`, per-agent access control

Also includes: agent dashboard, LDM OS file viewer, backup center, CLI wrapper (`ldm` command).

See `../product-ideas/native-apple-app-crystal-sync.md` for full product idea.

---

## Done

### v0.7.8 ... Orphan Cleanup, DELETE Trigger, Doctor Fix (2026-03-13)

- [x] DELETE trigger on chunks table cascading to chunks_vec (sqlite-vec) and chunks_fts (FTS5)
- [x] `crystal cleanup` CLI command with `--dry-run` support (backup, pause cron, clean orphans, rebuild FTS, VACUUM, resume cron)
- [x] `cleanOrphans()` method on Crystal class (batch delete orphaned vec entries, FTS rebuild)
- [x] Doctor `checkOpEmbeddings()` detects 1Password SA token resolution path
- [x] Cleaned 141,651 orphaned vectors + 141,652 orphaned FTS entries (from Mar 11 bulk file-scan deletion)
- [x] Database: 1.96 GB -> 1.45 GB after cleanup + VACUUM
- [x] Install prompt updated to new standard format (4 explain questions, installed check, dry-run)
- [x] Unlinked global crystal from private repo (npm link removed, installed from npm registry)
- [x] Product rule established: Memory Crystal indexes conversations only, not raw directory scans
- [x] Bug reports filed: orphaned data, npm link mess, plaintext SA token
- [x] GitHub issue #50: npm link and v0.7.7 release mess

### v0.7.3 + v0.7.4 ... MCP Fix and AgentId Config (2026-03-11)

- [x] Fixed MCP registration to include OPENCLAW_HOME env var (v0.7.3)
- [x] Moved MCP registrations from project-level `.mcp.json` to user-level `~/.claude.json`
- [x] Agent ID reads from `~/.ldm/agents/*/config.json` instead of hardcoding (v0.7.4, closes #33)
- [x] `getAgentId()` accepts harness hint (`claude-code` or `openclaw`)
- [x] Installer writes `agentId` to config during `crystal init`
- [x] Created `oc-lesa-mini` config.json (was missing)
- [x] New exports: `AgentConfig`, `loadAgentConfig()`, `saveAgentConfig()`
- [x] 33 stale branches renamed with `--merged-` suffix
- [x] QMD v1.1.6 analysis and recommendations documented

### v0.7.1 + v0.7.2 ... DB Safety and MCP Fix (2026-03-05)

- [x] Database safety improvements
- [x] MCP detection fix

### Search Quality Phase 1 + Phase 2 Core (2026-03-05)

- [x] Phase 1: Stronger recency curve (exponential decay, floor 0.3)
- [x] Phase 1: Time-filtered search (`--since 24h/7d/30d` on CLI, `time_filter` on MCP)
- [x] Phase 1: Fetch more candidates (`limit * 5, 50`)
- [x] Phase 2: Query expansion (3 variations: lex, vec, hyde)
- [x] Phase 2: Strong signal detection (BM25 probe, skip expansion if obvious match)
- [x] Phase 2: LLM re-ranking (top 40 RRF candidates scored by LLM)
- [x] Phase 2: Position-aware score blending (75/25 top 3, 60/40 4-10, 40/60 11+)
- [x] Phase 2: Tiered RRF weights (BM25 2x, vector 1x)
- [x] Phase 2: Deep search as default (no --deep flag needed)
- [x] Phase 2: Op-secrets integration for API keys
- [x] Phase 2: Provider cascade (MLX > Ollama > OpenAI > Anthropic > none)
- [x] New files: `src/llm.ts` (provider cascade, query expansion, re-ranking), `src/search-pipeline.ts` (deep search pipeline)
- [x] Plan docs: `current/search-quality-qmd-port.md`, `current/search-quality-full-plan.md`

### v0.6.0 Deploy + Consolidation (2026-03-04) ... Three Stores Into One

- [x] Deployed v0.6.0 to CC hook (`~/.ldm/extensions/memory-crystal/`) and OC plugin (`~/.openclaw/extensions/memory-crystal/`)
- [x] `crystal backfill --agent cc-mini` ... 24,180 chunks embedded from 783 files (~$0.24)
- [x] `crystal backfill --agent oc-lesa-mini` ... 0 new (dedup confirmed cc-mini covered all)
- [x] `crystal migrate-embeddings` ... 12,206 CE chunks migrated into crystal.db ($0)
- [x] Disabled context-embeddings plugin in openclaw.json (set `enabled: false`)
- [x] Verified: `crystal search` hits migrated chunks and backfilled transcripts
- [x] Lesa tested and confirmed: search working, remember working, no errors
- [x] crystal.db: 171,089 -> 207,518 chunks (one store, all data consolidated)
- [x] context-embeddings.sqlite and extension directory preserved as backup
- [x] Absorbed context-embeddings into Memory Crystal (retired plugin, Crystal captures directly)

### v0.6.0 (2026-03-04) ... The Living Memory Release

- [x] Dream Weaver integration via `crystal dream-weave` (full + incremental modes)
- [x] Crystal Core gateway (`crystal serve`) on localhost:18790, OpenAI-compatible
- [x] Staging pipeline for new agents from relay (auto-detect, stage, backfill, dream-weave, promote)
- [x] Commands channel on relay Worker (bidirectional Node...Core)
- [x] OpenClaw raw data sync to LDM after every agent_end turn (sessions, workspace, daily logs)
- [x] Harness-aware init flow (OpenClaw vs Claude Code, Core vs Node)
- [x] Relay command support in cc-hook.ts (`sendCommand()` export)
- [x] Poller detects new agents and routes to staging before live ingest
- [x] dream-weaver.ts bridge module (hooks into crystal.db embedding + crystal_remember)
- [x] staging.ts (staging pipeline: detect, stage, process, promote)
- [x] crystal-serve.ts (Crystal Core gateway with /v1/chat/completions, /process, /status)
- [x] Public repo deployment (memory-crystal + dream-weaver-protocol)
- [x] GitHub releases with comprehensive documentation (both repos, public + private)
- [x] External reviews captured from GPT, Grok, Claude Desktop

### v0.5.0 (2026-03-04) ... Init Discovery + Consolidation

- [x] `crystal init` discovers session files on the current machine (Claude Code + OpenClaw)
- [x] `crystal backfill` command (embeds raw transcript files from LDM)
- [x] `crystal migrate-embeddings` command (migrates CE chunks into crystal.db, $0)
- [x] discover.ts (auto-detects installed harnesses and session file locations)
- [x] bulk-copy.ts (idempotent raw file copy to LDM: sessions, workspace, daily logs)
- [x] oc-backfill.ts (OpenClaw JSONL parser, different format than Claude Code)
- [x] Workspace path added to LDM (`~/.ldm/agents/{id}/memory/workspace/`)
- [x] Reorganized ai/ to ai/product/

### v0.4.1 (2026-03-03) ... Core/Node Architecture

- [x] Crystal Core/Node role system (role.ts, crystal role, promote, demote)
- [x] crystal doctor (10-check health system)
- [x] crystal backup + backup setup (LaunchAgent, configurable destination)
- [x] crystal bridge setup/status (bridge detection)
- [x] SKILL.md rewrite as branching onboarding flow
- [x] ldm-backup.sh script

### v0.3.x (2026-03-02) ... Continuous Capture + Cloud MCP

- [x] Phase 1 continuous capture (cc-poller.ts, cron-based, unified)
- [x] Cloud MCP server (OAuth 2.1 + DCR, D1 + Vectorize, 4 tools)
- [x] crystal-mcp binary for clean MCP config
- [x] crystal init, crystal pair (QR code key sharing)
- [x] CLI search output matches MCP server (freshness icons, numbered results)

### v0.2.0 and earlier ... Foundation

- [x] sqlite-vec migration (replaced LanceDB as primary)
- [x] FTS5 full-text search with BM25 scoring
- [x] Hybrid search: vector + keyword with RRF fusion (ported from QMD)
- [x] Recency weighting
- [x] Turn-boundary chunking (1 conversation message = 1 chunk)
- [x] CC Stop hook with watermark-based capture
- [x] MCP server (crystal_search, crystal_remember, crystal_forget tools)
- [x] OpenClaw plugin (Lesa's interface, agent_end hook)
- [x] CLI (crystal search, crystal remember, crystal status)
- [x] Private mode (kill switch across CLI, MCP, OpenClaw, env var)
- [x] Ephemeral relay code: crypto, worker, cc-hook dual mode, poller, mirror-sync
- [x] Daily breadcrumb logs to `~/.ldm/agents/cc/memory/daily/`

---

## Deprecated

- ~~Recovery via `crystal replay`~~ ... not needed with working cron + backfill. (2026-03-02)
- ~~Remove LanceDB dual-write~~ ... Parker uses both. Dual-write stays. (2026-03-01)
- ~~Phase 2 Cloudflare Worker mirror (D1 cloud-first approach)~~ ... replaced by encrypted dead-drop relay. (2026-02-26)
- ~~`crystal push` / `crystal pull` / `crystal reset`~~ ... replaced by relay + mirror-sync. (2026-02-26)
- ~~`npm link` for crystal CLI~~ ... runs via `node dist/cli.js` or plugin. (2026-02-27). Resurfaced 2026-03-13: npm link was still active, causing production tool to run from repo source. Unlinked and installed from npm registry.
- ~~Raw directory scanning (crystal_sources_add/sync)~~ ... Memory Crystal indexes conversations only. File content through conversation turns is fine. Raw directory scanning without conversational context removed. (2026-03-13)
- ~~MD session summaries (summarize.ts)~~ ... Dream Weaver journals replace per-session summaries for narrative. summarize.ts stays for simple MD output but is not the primary path. (2026-03-04)
- ~~Three-file-type model (JSONL + MD + vector)~~ ... evolved into five-layer memory stack. JSONL and vector remain. MD summaries replaced by Dream Weaver journals for narrative. (2026-03-04)

---

## Agents

| Agent ID | Machine | Harness | Identity Home |
|----------|---------|---------|---------------|
| `cc-mini` | Mac Mini | Claude Code CLI | `~/.ldm/agents/cc-mini/` (LDM canonical) |
| `cc-air` | MacBook Air | Claude Code CLI | `~/.ldm/agents/cc-air/` (LDM canonical) |
| `oc-lesa-mini` | Mac Mini | OpenClaw | `~/.openclaw/workspace/` (harness canonical, LDM backup) |

All agents share one `crystal.db` at `~/.ldm/memory/`. Memory is shared. Identity is per-agent.

---

## External Feedback (2026-03-04)

Three AIs reviewed the v0.6.0 release independently:

- **GPT:** "Personal cognition infrastructure, not a tool." Suggested Crystal Capture (auto-capture) as the killer adoption feature. Proposed the four-layer narrative (Capture / Memory / Reflection / Communication).
- **Grok:** "The closest thing I've seen to giving AI agents a real long-term memory + identity that survives context resets."
- **Claude (Desktop):** Found the 200K transcript cap as a real technical tension. Called crystal serve "the interop layer that lets this slot into workflows you didn't build." Staging pipeline is "the kind of thing that separates a tool from a system."

Full reviews: `../product-ideas/external-reviews-v0.6.0.md`

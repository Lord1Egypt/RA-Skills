# Plan: Delta Sync + Full LDM Tree Sync

**Created:** 2026-03-05
**Status:** Planning
**Priority:** 5 on roadmap

## Problem

The mirror channel currently syncs the entire crystal.db (1.9 GB) every time. This doesn't scale. And it only syncs the database, not the file tree. Embeddings are pointers to artifacts (files, images, videos). If the artifact isn't on the node, the embedding is an orphan.

## Architecture Decisions

### 1. Core is the only embedder

All embeddings happen on Core (Mac Mini). Nodes never embed locally. This prevents split-brain where a node has embeddings that Core doesn't, or vice versa due to network issues.

**Flow:**
- Node captures raw conversation -> sends to Core via relay
- Core receives, embeds into crystal.db
- Core sends embedded chunks (delta) back via relay
- Node inserts pre-embedded chunks into its local crystal.db

### 2. Delta sync replaces full mirror

Instead of pushing the entire 1.9 GB crystal.db, Core pushes only new chunks since last sync. Each chunk is small (a few KB). The relay payload is proportional to activity, not corpus size.

**Watermark tracking:** Core tracks what the last synced chunk ID was for each node. Only sends newer chunks.

### 3. Full LDM tree sync

The entire `~/.ldm/` tree syncs between Core and Nodes. Not just crystal.db. Every file the embedding points to must exist on every device.

**What syncs:**
- `~/.ldm/agents/{id}/memory/workspace/` ... SHARED-CONTEXT.md, MEMORY.md, etc.
- `~/.ldm/agents/{id}/memory/daily/` ... daily logs
- `~/.ldm/agents/{id}/memory/journals/` ... Dream Weaver journals
- `~/.ldm/agents/{id}/memory/sessions/` ... session summaries
- `~/.ldm/agents/{id}/memory/transcripts/` ... raw JSONL session files
- `~/.ldm/agents/{id}/` ... SOUL.md, IDENTITY.md, CONTEXT.md, REFERENCE.md
- `~/.ldm/shared/` ... cross-agent shared files
- Media files (images, videos, artifacts) ... binary blob support

### 4. Cloud search is unnecessary

Every node has the full database + full file tree. All search is local. The Cloud MCP server (D1 + Vectorize) is deprecated for the real architecture. The relay is pure transport.

### 5. Two sync transport paths (future)

- **Relay (Workers):** Cross-platform. Any machine that can run Node. Works today.
- **Native Apple app (future):** Apple-to-Apple via CloudKit. No relay needed between Apple devices.

---

## What We're Building

### Phase A: Delta Chunk Sync (replace full mirror)

**Goal:** Stop pushing 1.9 GB. Push only new chunks.

**Files to modify:**
- `src/poller.ts` ... Core-side: export new chunks as delta payload instead of full DB
- `src/mirror-sync.ts` ... Node-side: receive and insert delta chunks instead of replacing DB
- `src/worker.ts` ... relay: no changes needed (it's already a blob store)
- `src/core.ts` ... add method to export chunks since a given ID/timestamp

**Changes:**

1. **Core: export delta chunks** (new method in core.ts)
   ```typescript
   async exportChunksSince(sinceId: number): Promise<ExportedChunk[]>
   ```
   Returns all chunks with `id > sinceId`, including their embedding vectors.

2. **Core: push delta to relay** (poller.ts)
   - After ingesting new data, export chunks since last sync watermark
   - Encrypt the chunk array (same AES-256-GCM as today)
   - Push to relay mirror channel
   - Update watermark

3. **Node: pull and insert delta** (mirror-sync.ts)
   - Pull delta blob from relay
   - Decrypt
   - Insert chunks into local crystal.db (including vectors)
   - Update local watermark
   - No more "replace entire DB" logic

4. **Cold start: full export**
   - First sync for a new node: Core exports ALL chunks (one-time full mirror)
   - After that: delta only
   - Can also be triggered manually: `crystal mirror --full`

**Verification:**
- Capture a new conversation on Core
- Within 1 minute (poller interval), new chunks appear on Node
- Node can search and find the new content
- Payload size is proportional to new chunks, not total DB size

### Phase B: File Tree Sync

**Goal:** Sync the full `~/.ldm/` file tree between Core and Nodes.

**New file:** `src/file-sync.ts`

**How it works:**

1. **Manifest generation**
   - Core scans `~/.ldm/` tree (excluding crystal.db, which is handled by Phase A)
   - Generates manifest: `{ path, sha256, size, mtime }` for every file
   - Manifest is small (JSON, a few KB even for thousands of files)

2. **Manifest comparison**
   - Core pushes manifest to relay
   - Node pulls manifest, compares against local files
   - Identifies: new files, changed files (hash mismatch), deleted files

3. **Delta file transfer**
   - Core pushes only changed/new files to relay (encrypted, like everything else)
   - Node pulls and writes to local `~/.ldm/`
   - Deleted files: Node removes them (or moves to `_trash/`)

4. **Binary blob support**
   - Large files (images, videos) chunked for transfer
   - SHA-256 verification after reassembly
   - Same encryption as text files

5. **Conflict resolution**
   - For files that both Core and Node modified: last-write-wins (Core always wins)
   - Node-only files (captured locally before sync): preserved, not overwritten

**Sync frequency:**
- After every poller cycle (same as chunk delta... every minute)
- File manifest is cheap to generate
- Only changed files transfer

**Files to modify:**
- `src/file-sync.ts` ... NEW: manifest generation, comparison, delta transfer
- `src/poller.ts` ... trigger file sync after chunk sync
- `src/mirror-sync.ts` ... receive and apply file deltas
- `src/worker.ts` ... may need a `files` channel (or reuse `mirror`)

**Verification:**
- Create/edit a file in `~/.ldm/agents/cc-mini/memory/workspace/` on Core
- Within 1 minute, file appears/updates on Node
- Create an image file, verify it syncs
- Delete a file on Core, verify Node removes it

### Phase C: Deprecate Cloud Search

**Goal:** Remove the cloud search path from docs. Keep the relay.

**Files to modify:**
- `TECHNICAL.md` ... remove "Cloud Memory & Search Architecture" section
- `RELAY.md` ... remove "Cloud Memory & Search" section, update to delta sync
- `README-ENTERPRISE.md` ... update multi-site sync to reflect delta model
- `src/worker-mcp.ts` ... keep file but mark as deprecated/demo
- `src/cloud-crystal.ts` ... keep file but mark as deprecated/demo

**What stays:**
- Relay Worker (encrypted dead drop transport)
- QR pairing
- Encryption (AES-256-GCM + HMAC-SHA256)

**What goes:**
- D1 + Vectorize cloud search as a production path
- OAuth 2.1 cloud MCP server as a production path
- "Tier 1 / Tier 2" cloud memory model

The cloud MCP server can remain as a demo/onboarding tool for new users who don't have a Core yet. But it's not the real architecture.

---

## Execution Order

1. Phase A: Delta chunk sync (core.ts, poller.ts, mirror-sync.ts)
2. Test Phase A: capture on Core, verify delta appears on Node
3. Phase B: File tree sync (file-sync.ts, poller.ts, mirror-sync.ts)
4. Test Phase B: file changes on Core appear on Node
5. Phase C: Doc updates (TECHNICAL.md, RELAY.md, README-ENTERPRISE.md)
6. Build and deploy to both targets
7. wip-release, PR, publish

---

## Critical Files

| File | Role |
|------|------|
| `src/core.ts` | Add exportChunksSince() method |
| `src/poller.ts` | Core-side: push delta chunks + trigger file sync |
| `src/mirror-sync.ts` | Node-side: receive delta chunks + file deltas |
| `src/file-sync.ts` | NEW: manifest generation, comparison, delta file transfer |
| `src/worker.ts` | Relay: may need files channel |
| `src/crypto.ts` | Encryption (no changes expected) |

---

## Size Estimates

| What | Current | After Delta Sync |
|------|---------|-----------------|
| Mirror payload (quiet day) | 1.9 GB | ~100 KB (a few hundred chunks) |
| Mirror payload (busy day) | 1.9 GB | ~5 MB (thousands of chunks) |
| File sync payload (typical) | N/A | ~50 KB (manifest + changed .md files) |
| File sync payload (with media) | N/A | Proportional to new media size |
| Cold start (new node) | 1.9 GB | 1.9 GB (one-time full export) |

---

## Future: Native Apple App

The relay is the cross-platform transport. For Apple-to-Apple sync, the native app replaces it entirely:
- CloudKit for encrypted sync (Apple handles transport)
- MLX Swift for on-device embedding + search quality LLM
- No Cloudflare Worker needed between Apple devices
- Same delta model: only new chunks + changed files

The relay stays for non-Apple devices or cross-platform setups.

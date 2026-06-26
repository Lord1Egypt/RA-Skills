# LLM Wiki Pattern

## Use When
- You need to build or maintain a persistent, structured knowledge base using agents.
- You are implementing the Company as Intelligence world model or OrgPack coordination wiki.
- You want to understand how agents read, write, search, and maintain wiki pages on Eve.

## Load Next
- `references/cli-org-project.md` for full docs CLI syntax (patch, diff, tree, search, sync, watch).
- `references/object-store-filesystem.md` for org filesystem mount and auto-indexing pipeline.
- `references/overview.md` for platform architecture and identifiers.

## Ask If Missing
- Confirm the org ID and whether the wiki prefix is established (e.g. `/wiki/`, `/world-model/`).
- Confirm whether the agent writes via file tools (org-fs mount) or CLI (`eve docs write`).
- Confirm whether near-instant indexing is required (LISTEN/NOTIFY is active by default).

## What Is an LLM Wiki

An LLM Wiki is a persistent, structured knowledge base built and maintained by agents — not by humans. Instead of retrieving raw documents at query time (RAG), the agent **incrementally compiles knowledge into interlinked wiki pages**. When new information arrives, the agent reads it, extracts key claims, and integrates them into the existing wiki — updating entity pages, revising summaries, flagging contradictions, strengthening the evolving synthesis.

The key difference from RAG: **the wiki is a compounding artifact.** Cross-references are already there. Contradictions are already flagged. The synthesis already reflects everything ingested. The wiki gets richer with every source added and every question asked.

The pattern was described by Andrej Karpathy and applies broadly: research wikis, internal company knowledge bases, competitive analysis, personal learning, and more. Eve Horizon provides first-class infrastructure for this pattern.

## The Wiki Substrate on Eve

Eve's wiki substrate is a two-layer system:

```
Agent writes/reads files at /org/wiki/...       <- normal file tools (Read, Write, Edit)
         | auto-index (near-instant via LISTEN/NOTIFY)
Org docs at /wiki/...                           <- versioned, searchable, queryable
         |
Other agents and humans search/query via CLI    <- eve docs search, eve docs query
```

**Write path**: Agents use normal file tools on the org-fs mount. Zero friction.
**Read path**: Agents use normal file tools on the org-fs mount. Zero friction.
**Search path**: Agents use `eve docs search` with `--path` prefix and `--context` lines.
**Patch path**: Agents use `eve docs patch` for surgical edits without full rewrites.
**Navigation**: Agents use `eve docs list --tree` to see wiki structure.

The org filesystem is the working copy. Org docs is the indexed, versioned layer. Changes flow automatically from org-fs to org docs via the async indexing pipeline (sub-second latency with LISTEN/NOTIFY).

## Three Layers

| Layer | What | Who owns it | Eve primitive |
|-------|------|-------------|---------------|
| Raw sources | Curated collection of source documents | Human or ingest pipeline | Org filesystem, attachments |
| The wiki | Structured, interlinked markdown pages | Agent (exclusively) | Org docs (versioned, searchable) |
| The schema | Conventions, structure, workflows | Human + agent (co-evolved) | CLAUDE.md, agent config |

## Agent Workflow

```bash
# Read a wiki page (normal file tool)
Read /org/world-model/state.yaml

# Edit a wiki page (normal file tool)
Edit /org/world-model/state.yaml
  old: "health: green"
  new: "health: amber"

# Search the wiki
eve docs search --org $ORG_ID --query "deploy failure" --context 3 --path /world-model

# Navigate wiki structure
eve docs list --org $ORG_ID --path /operating-model --tree

# Surgical patch without fetching full doc
eve docs patch --org $ORG_ID --path /world-model/state.yaml \
  --replace "health: green" "health: amber"

# Check what changed
eve docs diff --org $ORG_ID --path /world-model/state.yaml

# Watch for downstream updates
eve docs watch --org $ORG_ID --path /world-model --since now
```

**Key principle**: normal file tools for read/write. CLI for search, navigation, diff, watch, and surgical operations.

## Operations

**Ingest**: Drop a source into the raw collection. The agent reads it, extracts key information, writes summary pages, updates the index, updates entity/concept pages across the wiki. A single source might touch 10-15 wiki pages.

**Query**: Ask questions against the wiki. The agent searches with `eve docs search --context N`, reads relevant pages, synthesizes an answer. Good answers can be filed back into the wiki as new pages — explorations compound.

**Lint**: Periodically health-check the wiki. Look for contradictions, stale claims, orphan pages, missing cross-references. The agent is good at suggesting new questions and sources.

**Bulk operations**: Use `eve docs write-dir` for initial wiki population. Use `eve docs sync --dry-run --delete` for safe directory-to-wiki synchronization.

## Near-Instant Indexing

The org-fs to org-docs indexing pipeline uses PostgreSQL LISTEN/NOTIFY for sub-second wake on file changes. The processor:

1. Receives NOTIFY from `org_fs_events` trigger on `file.created`/`file.updated`
2. Wakes immediately and drains the index queue
3. Falls back to 2-second polling if the LISTEN connection drops

Target: p95 under 500ms for single-write indexing on local k3d.

## Relationship to Company as Intelligence

The LLM Wiki pattern is the foundation for OrgPack coordination:

| OrgPack Agent | Wiki Usage |
|---|---|
| World model agent | Maintains `/world-model/` wiki pages via file read/write + bulk sync |
| Signal watcher | Writes signal pages, triggers near-instant indexing for downstream agents |
| Policy engine | Searches wiki with context, navigates via tree view, watches for changes |
| Operating review | Searches across wiki, diffs versions to track evolution |
| All agents | Uses `eve docs patch` for cross-reference updates |

## Recent enhancements (shipped 2026-04-05)

All seven LLM Wiki platform enhancements are live and verified on local k3d. They are the prerequisite surface for OrgPack / Company as Intelligence and round out fluent agent use of the wiki substrate from normal file tools plus the Eve CLI.

### 1. Near-instant indexing (org-fs to org docs)

The org-fs index processor now LISTENs on the existing `org_fs_events` Postgres NOTIFY channel and wakes immediately on `file.created`/`file.updated`. The 2-second poller remains as fallback if the LISTEN connection drops. The queue stays the source of truth — NOTIFY is only a wake signal. Target latency: p95 under 500ms on local k3d for single writes. No new flag; agents just see writes appear in `eve docs search` sub-second instead of after up to 2s.

### 2. `eve docs patch` — surgical edits

CLI parity for the existing `PATCH /docs/by-path` API. Three operations, usable as flags or as a JSON batch:

```bash
eve docs patch --org $ORG_ID --path /wiki/page --replace "old" "new"
eve docs patch --org $ORG_ID --path /wiki/page --append "## New Section\n..."
eve docs patch --org $ORG_ID --path /wiki/page --insert-after "## Header" "para"
eve docs patch --org $ORG_ID --path /wiki/page \
  --operations '[{"op":"replace","search":"a","replace":"b"},{"op":"append","content":"x"}]'
```

Returns the updated doc with `current_version` and `content_hash`. Missing anchor / search text exits non-zero — agents can detect failed patches without re-reading.

### 3. `eve docs list --tree` — wiki navigation

The flat list output now has a hierarchical mode for navigation:

```bash
eve docs list --org $ORG_ID --path /operating-model --tree         # human-readable
eve docs list --org $ORG_ID --path /operating-model --tree --json  # nested nodes for agents
```

Default flat list is unchanged for back-compat.

### 4. `eve docs search --path` and `--context`

Two additions to full-text search:

- `--path <prefix>` constrains search to a wiki subtree, reusing the existing `searchWithFilters()` path-prefix support via a new `path_prefix` query param on `GET /orgs/{org_id}/docs/search`.
- `--context N` fetches each match and returns N lines of surrounding context grep-style, so the agent can judge relevance before fetching the full doc.

```bash
eve docs search --org $ORG_ID --query "error rate" --path /world-model --context 3
```

Headline width was widened and `ts_headline()` now allows multiple useful fragments. `--mode hybrid|semantic` still currently degrades to text — the API shape is stable.

### 5. `eve docs diff` — version diff

Pure-CLI diff between two versions of a doc, defaulting to latest vs latest-1:

```bash
eve docs diff --org $ORG_ID --path /world-model/state.yaml
eve docs diff --org $ORG_ID --path /world-model/state.yaml --from 3 --to 5
eve docs diff --org $ORG_ID --path /world-model/state.yaml --unified
```

Built on the existing version endpoints; diff is computed client-side.

### 6. Bulk write and safe sync

Three commands for multi-doc ingest, with safety rules around deletion:

```bash
# Map a local directory to doc paths (create/update only)
eve docs write-dir --org $ORG_ID --source ./wiki-pages --path-prefix /operating-model

# NDJSON bulk write
printf '%s\n' '{"path":"/wiki/a","content":"..."}' '{"path":"/wiki/b","content":"..."}' \
  | eve docs bulk-write --org $ORG_ID

# Directory <-> wiki sync; --delete is required and never default
eve docs sync --org $ORG_ID --source ./.eve-org --path-prefix /operating-model --dry-run
eve docs sync --org $ORG_ID --source ./.eve-org --path-prefix /operating-model --delete
```

`--dry-run` prints create/update/delete counts before mutating. Hidden/junk files are skipped unless explicitly included.

### 7. `eve docs watch` — change stream

Reuses existing `system.doc.created|updated|deleted` events instead of inventing a docs-specific channel. The CLI polls org events, filters by path prefix, and emits NDJSON:

```bash
eve docs watch --org $ORG_ID --path /world-model --since now
eve docs watch --org $ORG_ID --path /world-model --since 5m
# {"type":"system.doc.updated","path":"/world-model/state","version":42,"updated_at":"...","content_hash":"..."}
```

Agents block on the stream instead of polling. Generic org-events SSE remains a future option; until then, the polling watch is the supported path.

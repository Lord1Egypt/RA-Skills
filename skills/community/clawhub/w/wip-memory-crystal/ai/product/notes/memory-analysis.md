# Memory Analysis: Data Locations

**Updated:** 2026-03-06
**Version:** Memory Crystal v0.7.2

---

## Live (current)

| What | Location | Written by | Controlled by | How it gets there |
|------|----------|-----------|--------------|-------------------|
| Crystal DB | `~/.ldm/memory/crystal.db` | cc-hook, OC plugin, cron, MCP | Memory Crystal | Transcript chunks split, embedded, inserted into SQLite |
| CC-Mini daily logs | `~/.ldm/agents/cc-mini/memory/daily/YYYY-MM-DD.md` | cc-hook.js, cc-poller.ts | Memory Crystal | Auto-appended after every CC session. One-line breadcrumb per session. |
| CC-Mini transcripts | `~/.ldm/agents/cc-mini/memory/transcripts/` | cc-hook.js, cc-poller.ts | Memory Crystal | Copies raw JSONL from Claude Code's session dir (if newer) |
| CC-Mini sessions | `~/.ldm/agents/cc-mini/memory/sessions/` | cc-hook.js | Memory Crystal | LLM-generated markdown summary of each session |
| CC-Mini journals | `~/.ldm/agents/cc-mini/memory/journals/` | CC-Mini (manual) | Claude Code (agent) | Written by CC at end of significant sessions |
| CC-Mini state | `~/.ldm/agents/cc-mini/CONTEXT.md` | CC-Mini (manual) | Claude Code (agent) | Updated when current work changes |
| CC-Mini identity | `~/.ldm/agents/cc-mini/SOUL.md`, `IDENTITY.md`, `REFERENCE.md` | CC-Mini (manual) | Claude Code (agent) | Written once, updated rarely |
| Lesa transcripts | `~/.ldm/agents/oc-lesa-mini/memory/transcripts/` | OC plugin (openclaw.ts) | Memory Crystal (OC plugin) | Copies session JSONLs from `~/.openclaw/agents/main/sessions/` |
| Lesa workspace mirror | `~/.ldm/agents/oc-lesa-mini/memory/workspace/` | OC plugin (openclaw.ts) | Memory Crystal (OC plugin) | Syncs .md files from `~/.openclaw/workspace/` |
| Lesa daily logs (LDM) | `~/.ldm/agents/oc-lesa-mini/memory/daily/` | OC plugin (openclaw.ts) | Memory Crystal (OC plugin) | Copies date-formatted .md files from `~/.openclaw/workspace/memory/` |
| Shared context | `~/.openclaw/workspace/SHARED-CONTEXT.md` | Both agents (manual) | Claude Code + OpenClaw (agents) | CC uses Edit to append. Lesa writes directly. |
| Lesa memory | `~/.openclaw/workspace/MEMORY.md` | Lesa (manual) | OpenClaw (agent) | Updated with facts/preferences |
| Lesa daily logs (OC) | `~/.openclaw/workspace/memory/YYYY-MM-DD.md` | Both agents (manual) | Claude Code + OpenClaw (agents) | Appended during sessions |
| Capture watermark | `~/.ldm/state/cc-capture-watermark.json` | cc-hook.js, cc-poller.ts | Memory Crystal | Tracks byte offset per transcript file |
| Private mode state | `~/.ldm/state/memory-capture-state.json` | private-mode plugin | OpenClaw (private-mode plugin) | Toggles capture on/off |
| CC auto-memory | `~/.claude/projects/.../memory/` | Claude Code (built-in) | Claude Code (built-in) | Auto-saved by Claude Code across sessions |
| CLAUDE.md | `~/.claude/CLAUDE.md`, `~/.openclaw/CLAUDE.md` | CC/Parker (manual) | Claude Code + Parker (manual) | Updated when system structure changes |

---

## Deprecated

| What | Location | Replaced by |
|------|----------|------------|
| Old CC journals | `staff/Parker/Claude Code - Mini/documents/journals/` | `~/.ldm/agents/cc-mini/memory/journals/` |
| Dream Weaver narrative | `staff/.../cc-full-history.md` | `~/.ldm/agents/cc-mini/memory/journals/full-history.md` |
| Session exports | `staff/.../documents/sessions/` | `~/.ldm/agents/cc-mini/memory/sessions/` |
| LanceDB vectors | `~/.ldm/memory/lance/` (428 MB) | Embeddings now in crystal.db |
| Cloud Memory | Cloudflare D1 | Deprecated. Plaintext at rest. |
| Old agent dirs | `~/.ldm/agents/_trash/cc/` | Renamed to cc-mini |

---

## ~/.ldm/ Directory Map (memory data only)

| Path | What it is | Created by | Populated by |
|------|-----------|-----------|-------------|
| `memory/crystal.db` | The database. 1.9 GB, 208K+ chunks. | First capture run | cc-hook, OC plugin, cron capture, crystal_remember |
| `memory/crystal.db-wal` | SQLite write-ahead log | SQLite (automatic) | SQLite (automatic) |
| `memory/lance/` | **Deprecated.** Old vector store. | Migration script | No longer written to |
| `state/cc-capture-watermark.json` | Last captured byte offset per JSONL file | cc-hook.js | cc-hook.js, cc-poller.ts |
| `state/memory-capture-state.json` | Private mode on/off | private-mode plugin | private-mode plugin |
| `state/search-metrics.jsonl` | Search quality log | mcp-server.js | Appended on each search |
| `agents/cc-mini/memory/daily/` | CC daily logs. One file per day. | cc-hook.js | cc-hook.js auto-appends a breadcrumb after every session |
| `agents/cc-mini/memory/journals/` | CC narrative journals | CC-Mini (manual) | Written at end of significant sessions |
| `agents/cc-mini/memory/transcripts/` | Raw JSONL conversation files | cc-hook.js | Copied from Claude Code's session storage (copyFileSync if newer) |
| `agents/cc-mini/memory/sessions/` | Markdown session summaries | cc-hook.js | LLM-generated summary via summarize.ts |
| `agents/cc-mini/memory/workspace/` | CC workspace files | scaffoldLdm() | Not actively used yet |
| `agents/cc-mini/CONTEXT.md` | CC current state | CC-Mini (manual) | Updated when state changes |
| `agents/cc-mini/SOUL.md` | CC identity | CC-Mini (manual) | Written once, updated rarely |
| `agents/oc-lesa-mini/memory/transcripts/` | Lesa's session JSONLs | OC plugin (openclaw.ts) | Copied from `~/.openclaw/agents/main/sessions/` after every OC turn |
| `agents/oc-lesa-mini/memory/workspace/` | Mirror of Lesa's workspace | OC plugin (openclaw.ts) | Syncs all .md files from `~/.openclaw/workspace/` after every OC turn |
| `agents/oc-lesa-mini/memory/daily/` | Lesa's daily logs (LDM copy) | OC plugin (openclaw.ts) | Copies YYYY-MM-DD.md files from `~/.openclaw/workspace/memory/` |
| `secrets/crystal-relay-key` | Encryption key for relay sync | `crystal pair` | Written once during pairing |
| `bin/crystal-capture.sh` | Cron capture script | `crystal init` | Copied from package dist/ by deployCaptureScript() |
| `bin/ldm-backup.sh` | Backup script | `crystal init` | Copied from package dist/ by deployBackupScript() |
| `config.json` | Agent list, version, timestamps | `crystal init` | Updated by scaffoldLdm() |

---

## How Data Flows

### CC-Mini (Claude Code) path

```
Claude Code session ends
  -> Stop hook fires (cc-hook.js)
     -> Reads raw JSONL from Claude Code's session file
     -> Copies JSONL to ~/.ldm/agents/cc-mini/memory/transcripts/
     -> Splits messages into chunks, embeds, writes to crystal.db
     -> Appends one-line breadcrumb to ~/.ldm/agents/cc-mini/memory/daily/YYYY-MM-DD.md
     -> Generates markdown summary to ~/.ldm/agents/cc-mini/memory/sessions/

Also every minute:
  -> Cron runs crystal-capture.sh -> cc-poller.ts
     -> Scans for any JSONL files the hook missed
     -> Same flow: archive, ingest, daily log
```

### Lesa (OpenClaw) path

```
Lesa conversation ends (agent_end hook)
  -> OC plugin fires (openclaw.ts)
     -> Copies session JSONLs from ~/.openclaw/agents/main/sessions/
        to ~/.ldm/agents/oc-lesa-mini/memory/transcripts/
     -> Syncs .md files from ~/.openclaw/workspace/
        to ~/.ldm/agents/oc-lesa-mini/memory/workspace/
     -> Copies daily logs from ~/.openclaw/workspace/memory/YYYY-MM-DD.md
        to ~/.ldm/agents/oc-lesa-mini/memory/daily/
     -> Splits conversation into chunks, embeds, writes to crystal.db
```

### What reads crystal.db

```
crystal_search (MCP tool)  -> semantic search across all chunks
crystal_remember (MCP)     -> writes a fact/preference chunk
crystal_status (MCP)       -> reports chunk count
crystal search (CLI)       -> same as MCP, from terminal
crystal doctor (CLI)       -> reads chunk count for health check
```

---

## Source Files That Control This

| File | What it controls |
|------|-----------------|
| `src/cc-hook.ts` | CC Stop hook. Archives transcripts, ingests to DB, writes daily log, generates session summaries. |
| `src/cc-poller.ts` | Cron capture. Same as cc-hook but runs every minute scanning all JSONL files. Catches anything the hook missed. |
| `src/openclaw.ts` | OC plugin. Copies Lesa's sessions/workspace/daily to LDM, ingests to DB. |
| `src/core.ts` | Crystal database operations. Chunk splitting, embedding, insert, search. All writers use this. |
| `src/ldm.ts` | Directory scaffolding. Creates all folders. Deploys scripts. Installs cron. |
| `src/installer.ts` | `crystal init`. Deploys code, configures hooks, registers MCP, backs up DB. |
| `src/mcp-server.ts` | MCP server. Exposes crystal_search, crystal_remember, crystal_forget, crystal_status. |
| `src/summarize.ts` | Session summary generation. Called by cc-hook after ingestion. |
| `src/discover.ts` | Finds existing AI sessions on the machine (Claude Code, OpenClaw). Used during first install. |

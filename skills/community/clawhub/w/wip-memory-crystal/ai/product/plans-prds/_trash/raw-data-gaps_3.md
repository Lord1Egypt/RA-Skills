# Raw Data Gaps: What LDM Is Missing

**Date:** 2026-03-03
**Author:** CC-Mini
**Priority:** CRITICAL. This is the foundation everything else builds on.

## The Rule

LDM OS (`~/.ldm/`) must have a copy of ALL raw memory data from both agents. The databases are indexes. The raw files are the truth. If we lose the raw files, we lose everything.

## Current State

### Lēsa (agent: oc-lesa-mini / main)

| Data | Source | Count | In LDM? | Gap |
|---|---|---|---|---|
| Session JSONLs | `~/.openclaw/agents/main/sessions/` | 748 files (154 MB) | **NO** | All 748 missing |
| Workspace .md files | `~/.openclaw/workspace/` | 133 files (125 MB) | **NO** | All 133 missing |
| Daily logs (oc-lesa-mini) | `~/.ldm/agents/oc-lesa-mini/memory/` | 664 files | Yes | OK |

### Claude Code (agent: cc-mini)

| Data | Source | Count | In LDM? | Gap |
|---|---|---|---|---|
| Session JSONLs | `~/.claude/projects/` | 443 files (534 MB) | **Partial** | Only 32 of 443 copied |
| Daily logs | `~/.ldm/agents/cc-mini/memory/daily/` | 14 files | Yes | OK |
| Sessions (MD summaries) | `~/.ldm/agents/cc-mini/memory/sessions/` | 466 files | Yes | OK |
| Journals | `~/.ldm/agents/cc-mini/memory/journals/` | 6 files | Yes | OK |

### Summary

**Total raw files that should be in LDM: ~1,324**
**Total raw files actually in LDM: ~32 (CC transcripts only)**
**Missing: ~1,292 files (~813 MB)**

## What Needs to Happen

### Step 1: One-time bulk copy (immediate)

Copy all existing raw data into LDM right now:

```bash
# Lēsa's session JSONLs
mkdir -p ~/.ldm/agents/oc-lesa-mini/memory/transcripts/
cp ~/.openclaw/agents/main/sessions/*.jsonl ~/.ldm/agents/oc-lesa-mini/memory/transcripts/

# Lēsa's workspace (snapshot)
mkdir -p ~/.ldm/agents/oc-lesa-mini/memory/workspace/
cp -r ~/.openclaw/workspace/* ~/.ldm/agents/oc-lesa-mini/memory/workspace/

# CC's session JSONLs (the missing 411)
# CC's transcripts dir already has 32, need to sync the rest
rsync -a ~/.claude/projects/*/*.jsonl ~/.ldm/agents/cc-mini/memory/transcripts/
```

### Step 2: Ongoing capture (wire into hooks)

After the bulk copy, wire up continuous sync so new data flows automatically:

**For Lēsa:** Add to crystal's OpenClaw plugin `agent_end` hook:
- After ingesting chunks, copy the current session JSONL to `~/.ldm/agents/oc-lesa-mini/memory/transcripts/`
- Periodically snapshot workspace .md files to `~/.ldm/agents/oc-lesa-mini/memory/workspace/`

**For CC:** The cc-hook already copies some transcripts. Expand it to catch all sessions, not just the ones from the current project dir.

### Step 3: Verify

- `crystal doctor` should check that LDM transcripts exist and are current
- Add a check: "Transcripts: X files in LDM vs Y files in source. Gap: Z"

## Target State

```
~/.ldm/
  memory/
    crystal.db                              ← the one index (conversations + files + memories)
  agents/
    oc-lesa-mini/
      memory/
        transcripts/                        ← ALL 748+ session JSONLs (copied from OpenClaw)
        workspace/                          ← snapshot of workspace .md files
        daily/                              ← already here (664 files)
        sessions/                           ← MD summaries (to be generated)
        journals/                           ← Dream Weaver output (future)
    cc-mini/
      memory/
        transcripts/                        ← ALL 443+ session JSONLs (copied from .claude/)
        daily/                              ← already here (14 files)
        sessions/                           ← already here (466 files)
        journals/                           ← already here (6 files)
```

## Why This Matters

Parker said it: "If we lose that, it's really lame."

OpenClaw could upgrade and wipe sessions. Claude Code could clear its project cache. macOS could have a disk issue. The raw files are the only thing that can't be regenerated. Every database, every index, every search result is derived from these files. LDM must have copies. No exceptions.

## Relationship to Memory Consolidation

This is a PREREQUISITE to retiring context-embeddings. Before we merge CE into crystal and disable the CE plugin, we need to confirm:

1. All raw source data is safely copied to LDM
2. Crystal has indexed everything (or can re-index from LDM copies)
3. If anything goes wrong, we rebuild from `~/.ldm/agents/*/memory/transcripts/`

The order:
1. Bulk copy raw files to LDM (this doc)
2. Wire up ongoing capture in hooks
3. Migrate CE unique chunks into crystal
4. Disable CE plugin
5. Update lesa-bridge (optional, crystal_search covers it)

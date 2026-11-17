---
name: save
description: "Save conversations to memory index — FTS5 rebuild, log cross-ref, saved convos dispatch"
homepage: https://github.com/mirza42/openclaw-save-skill
emoji: 💾
requires:
  bins: [python3]
metadata:
  openclaw:
    emoji: "💾"
    requires:
      bins: [python3]
    install:
      - id: setup
        kind: setup
        label: "Create saved conversations directory"
        run: "mkdir -p ~/.openclaw/workspace/saved"
      - id: init-log
        kind: init
        label: "Initialize conversation log"
        run: "echo -e '# Conversation Log\\n_0 conversations_\\n' > ~/.openclaw/workspace/saved/conversation-log.md"
      - id: init-index
        kind: init
        label: "Build initial FTS5 index"
        run: "python3 {baseDir}/memory-index.py build"
---

# Save — Conversation Memory Index

**Three-tier memory system for OpenClaw agents.** Zero external dependencies, zero API keys, zero cloud services. Runs entirely on local files and Python stdlib.

Save session context as a standalone document, cross-reference it in a human-readable log, and index it for fast FTS5 full-text search — all with one command.

## The Architecture: Three-Tier Memory

### Tier 1 — Conversation Log (always in context, ~7KB)
**File:** `~/.openclaw/workspace/saved/conversation-log.md`

A date-sorted cross-reference index. Every saved conversation has a one-line entry: date, filename, topic summary. The agent reads this at session start and instantly knows what's stored.

```
- **2026-07-19** 2026-07-19_gif-library-and-picker-skill.md: GIF library + picker built
- **2026-07-18** 2026-07-11_movie-rec-animal-and-all-we-imagine-as-light.md: Discussion about movies
```

### Tier 2 — FTS5 Search Index (on-demand, ~5ms)
**File:** `/dev/shm/memory-index.db`
**Built by:** `memory-index.py`

Full-text search over all workspace markdown files and saved conversations. BM25 ranking. Porter stemmer. Synonym awareness.

```
python3 ~/.openclaw/workspace/saved/memory-index.py search "Playwright in production"
→ [0.12] memory/2026-07-18.md: Playwright testcases — One-Shot Test Generation
```

### Tier 3 — Full File Read (on-demand, ~2ms)
**Directory:** `~/.openclaw/workspace/saved/`

The full saved conversation file. Read when the agent needs complete context.

## How `/save` Works

When the user says "save this conversation":

1. **Synthesize a summary** from session context — a standalone document with context, decisions, findings, action items. No tool call noise, no system messages, no chat-log verbatim.

2. **Write the file** to `~/.openclaw/workspace/saved/YYYY-MM-DD_topic-slug.md`

3. **Update the conversation log** — prepend an entry with date, filename, and one-line description. Update the header count.

4. **Rebuild the FTS5 index** — runs `memory-index.py build` which scans all tracked files, builds a Porter-stemmed FTS5 table on tmpfs, generates a topic map JSON, and generates a stub index markdown for Tier 1 initial context.

## Files

### `memory-index.py` (386 lines)
- FTS5 index builder and query engine
- Porter tokenizer + unicode61 for Unicode support
- Synonym-aware query expansion (15 groups: "error" → "error OR bug OR fail OR issue OR problem")
- Topic map JSON generation (topic → file paths + snippets)
- Stub index markdown generation for inline context
- fallback grep search when FTS5 returns no results
- No pip packages — Python 3.8+ stdlib only

### `conversation-log.md`
- Date-sorted cross-reference
- Maintained in strict sync with files on disk
- Validated by reconcile tools (no orphan entries, no missing files)

## Commands

The agent handles `/save` automatically. For manual operations:

```bash
# Build/rebuild the FTS5 index
python3 ~/.openclaw/workspace/saved/memory-index.py build

# Search the index
python3 ~/.openclaw/workspace/saved/memory-index.py search "your query here"

# List all detected topic tags
python3 ~/.openclaw/workspace/saved/memory-index.py tags
```

## Environment Variables (optional overrides)

| Variable | Default | Purpose |
|---|---|---|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | Root workspace directory |
| `SAVED_CONVERSATIONS_DIR` | `~/.openclaw/workspace/saved` | Where saved session files live |

## First-Time Setup

```bash
# 0. Prerequisites
#    - Python 3.8+ (stdlib only — no pip packages needed)
#    - An OpenClaw agent with write/edit/exec/read tools

# 1. Create the saved conversations directory (inside the workspace)
mkdir -p ~/.openclaw/workspace/saved

# 2. Initialize the conversation log
echo -e '# Conversation Log\n_0 conversations_\n' > ~/.openclaw/workspace/saved/conversation-log.md

# 3. Copy memory-index.py to an accessible location
#    (it's at {baseDir}/memory-index.py)

# 4. Build the initial index
python3 ~/.openclaw/workspace/saved/memory-index.py build

# 5. The /save flow: write file → update log → rebuild index
```

## In-Session Usage

```markdown
When the user says "save this", "save this conversation", or invokes /save:
1. Synthesize a clean summary from your session context
2. Write to ~/.openclaw/workspace/saved/YYYY-MM-DD_topic-slug.md
3. Prepend entry to conversation-log.md with date, filename, one-line description
4. Rebuild FTS5 index via memory-index.py build
```

## Edge Cases

- **"Don't index it" or "off the record"** — write the file but skip the log update and index rebuild
- **Duplicate filename** — append a counter: `2026-07-09_topic-slug-2.md`
- **Long conversation (>50KB)** — write a summary/executive brief instead of full content
- **"Save this as [custom name]"** — use the custom name as filename

## Performance

- **616 files indexed in ~360ms** on a Raspberry Pi 4 (ARM Cortex-A72)
- **FTS5 DB:** ~6.9MB for 616 files
- **Topic map:** ~845KB JSON with 1,400+ topics
- **Stub index:** ~75KB — fits in any agent's context

## Why This Exists

Agents don't have persistent memory. They can't remember what happened last session — unless they write it down. The `save` skill is a structured writing system that turns ephemeral conversations into durable, queryable knowledge. It's the difference between a chatbot and an assistant that learns over time.

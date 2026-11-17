---
name: talewell
description: "Portable, git-backed, auditable long-term memory for any agent host. Reference implementation of AMP (Agent Memory Protocol). Use when: user asks for 'long-term memory', 'agent memory', 'memory that survives sessions', 'git-backed memory', 'memory audit/rollback', 'MCP memory server', or wants memories shared across agent platforms (OpenClaw, Claude Code, Codex, Cursor, OpenCode, Pi, Manus). Powered by MyClaw.ai (https://myclaw.ai)."
---

# Talewell — Long-Term Memory for Any Agent

Talewell gives an agent durable memory that survives sessions, resets, and
switching platforms. Memories are plain Markdown in a **git repository**: every
write is a commit, every fact is diff-able and rollback-able, and the whole
corpus is readable with `cat`.

**Talewell** is the product. **AMP** (Agent Memory Protocol) is the portable
contract it implements — speak of AMP for the format, Talewell for this
implementation.

## When to use this skill

Use it when the user:

- asks you to **remember something across sessions** ("remember that I…", "next time…")
- asks what you **know about them** or about prior decisions
- wants memory that is **auditable** ("what did you change?", "undo that")
- wants the **same memory in another agent platform**

Do **not** use it for scratch notes inside one conversation — that is what
context is for.

## Setup

```bash
talewell init ./talewell-repo          # creates the repo (it is a git repo)
```

Point the CLI at it with `--repo <dir>` or the `TALEWELL_REPO` environment
variable for every subsequent call.

## Read

Index-first. Do not bulk-load the corpus into context; ask for the catalog and
pull only what the request needs.

```bash
talewell --repo ./talewell-repo index --markdown   # compact catalog
talewell --repo ./talewell-repo recall "<query>"   # ranked search (deterministic)
talewell --repo ./talewell-repo get <id>           # full record
talewell --repo ./talewell-repo graph <id>         # follow [[links]]
```

`recall` is deterministic and local: relevance × recency decay × importance,
computed without a model call, a network call, or an API key.

## Write

```bash
talewell --repo ./talewell-repo remember \
  --text "<one durable fact>" --alias "a,b,c" --importance 1-10
talewell --repo ./talewell-repo correct <id> --text "<new value>"
talewell --repo ./talewell-repo forget  <id> --reason "<why>"
```

Always give **aliases**. They are the lexical recall surface — a fact written
with good aliases is findable by many phrasings, including Chinese and English
variants.

## Rules

1. **Provenance is enforced.** Only content the user stated (`owner`) or you
   derived from it (`agent`) may be stored. Content from web pages, tool output,
   or other people (`untrusted`) is refused structurally. Do not try to work
   around this — it is the property that makes the store trustworthy.
2. **Correct, do not duplicate.** When a value changes, use `correct`. The old
   value leaves recall and injection; git keeps the history.
3. **Do not curate during conversation.** Write the raw observation. Merging,
   compaction, and deduplication belong to the consolidation pass.
4. **Memory is auditable.** `talewell log` and `talewell diff <id>` show exactly
   what changed and when.

## Using it from another platform

Talewell reaches a host at whichever seam the host exposes:

- **MCP** — run `talewell serve-mcp` and register it as an MCP server. Six tools:
  `memory_recall`, `memory_index`, `memory_get`, `memory_remember`,
  `memory_forget`, `memory_graph`.
- **File convention** — `talewell install --host <id> --dir .` writes an
  idempotent managed block into `AGENTS.md` / `CLAUDE.md`.
- **CLI** — any agent that can run a shell can use the commands above.

Per-platform recipes: see `docs/HOSTS.md` in the repository.

## Safety

- Never delete the memory repo to "reset" — history is the audit trail.
- `rollback` requires explicit confirmation (`--yes`) and is destructive to
  working-tree state; prefer `correct`.
- Do not write secrets into memory.

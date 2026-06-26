---
name: rag-memory
version: 1.1.1
description: Vector memory search and RAG skill for OpenClaw. Provides vector_search tool backed by Qdrant, auto-syncs memory .md files and Postgres records via nomic-embed-text embeddings. Triggers on "search memory", "vector search", "resync memory", "RAG", "qdrant".
metadata:
  openclaw:
    homepage: https://clawhub.ai/mbojer/rag-memory
    emoji: 🧠
    requires:
      bins:
        - curl
        - python3
        - jq
      env:
        - QDRANT_HOST
        - QDRANT_API_KEY
        - QDRANT_COLLECTION_PREFIX
        - EMBED_BASE_URL
        - EMBED_API_KEY
        - POSTGRES_DSN
        - MEMORY_DIR
    primaryEnv: EMBED_API_KEY
---

# RAG Memory Skill

## Architecture (as of 2026-04-04)

All files live under `~/.openclaw/skills/rag-memory/` — the single source of truth.

| File | Purpose |
|---|---|
| `config.env` | Credentials and tuning (gitignored) |
| `config.env.example` | Template with no secrets (tracked in git) |
| `sync_to_qdrant.py` | Ingest pipeline: Postgres + .md files → Qdrant |
| `requirements.txt` | Python deps for sync script |
| `venv/` | Python virtualenv (gitignored) |
| `plugin/index.js` | OpenClaw plugin — registers `vector_search` tool and `before_prompt_build` hook |
| `plugin/package.json` | Plugin manifest |
| `plugin/openclaw.plugin.json` | Plugin config schema |
| `systemd/` | Source-of-truth copies of systemd units (deploy with `sudo cp` + `daemon-reload`) |
| `references/config-paths.example.md` | File and credential location template (copy to `config-paths.md` and fill in) |
| `references/operational.md` | When/how to use vector_search |

Plugin is installed at `~/.openclaw/extensions/rag-memory/` and configured in `~/.openclaw/openclaw.json` under `plugins.entries.rag-memory`.

Qdrant collections: `{QDRANT_COLLECTION_PREFIX}_memory` (daily logs + facts) and `{QDRANT_COLLECTION_PREFIX}_docs` (tools + skill docs). 768-dim, nomic-embed-text via OpenAI-compatible embedding endpoint.

---

## When to use vector_search

Always prefer `vector_search` over reading full memory files:

- Before reading any daily log or MEMORY.md → `scope: memory`
- Before reading TOOLS.md or any SKILL.md → `scope: docs`
- Unsure → `scope: all`

Only fall back to reading the file directly if vector_search returns no results.

---

## Sync management

| Task | Command |
|---|---|
| Incremental sync (unsynced rows only) | `~/.openclaw/skills/rag-memory/venv/bin/python ~/.openclaw/skills/rag-memory/sync_to_qdrant.py` |
| Full resync (rebuild all vectors) | `... sync_to_qdrant.py --full` |
| Single file | `... sync_to_qdrant.py --file /path/to/file.md` |

Incremental sync also fires automatically when any `.md` file changes in `~/.openclaw/workspace/memory/` (via `sysclaw-rag-watch.path`). Nightly full sync runs at 03:00 (`sysclaw-rag-sync.timer`).

---

## Updating the plugin

If `plugin/index.js` is changed:

```bash
SKILL=~/.openclaw/skills/rag-memory
openclaw plugins install $SKILL/plugin
openclaw gateway restart
```

If `config.env` tuning values change, also update the matching values in `plugins.entries.rag-memory.config` in `openclaw.json` (especially `score_threshold` and `top_k`).

---

## Deploying systemd unit changes

Edit files in `systemd/` (source of truth), then deploy using the included script — it substitutes the correct username automatically:

```bash
sudo ~/.openclaw/skills/rag-memory/systemd/deploy.sh
```

Or manually, replacing `youruser` with the local OpenClaw user:

```bash
sudo sed "s/User=openclaw/User=youruser/g" ~/.openclaw/skills/rag-memory/systemd/*.service \
  | sudo tee /etc/systemd/system/sysclaw-rag-{sync,watch}.service > /dev/null
sudo cp ~/.openclaw/skills/rag-memory/systemd/sysclaw-rag-sync.timer /etc/systemd/system/
sudo cp ~/.openclaw/skills/rag-memory/systemd/sysclaw-rag-watch.path /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart sysclaw-rag-sync.timer sysclaw-rag-watch.path
```

---

## Key config values

| Key | Example / Default |
|---|---|
| `QDRANT_HOST` | `https://qdrant.example.com` |
| `EMBED_BASE_URL` | `https://litellm.example.com` |
| `EMBED_MODEL` | `nomic-embed-text` |
| `QDRANT_COLLECTION_PREFIX` | any UUID or unique prefix string |
| `MEMORY_DIR` | `~/.openclaw/workspace/memory` |
| `score_threshold` | `0.70` (in both config.env and openclaw.json plugin config) |
| `top_k` | `5` |

---

## If Qdrant is unreachable

1. Try once — do not retry in a loop
2. Fall back to reading the relevant file directly
3. Note in your response that vector search was unavailable
4. Check: `curl $QDRANT_HOST/readyz`
5. Do not restart Qdrant automatically — alert the user

---

## Not for

Do not activate this skill for:

- General file search or code search unrelated to memory/RAG
- Editing files (use read/write tools directly)
- Tasks that don't involve looking up past context, facts, or tool docs
- Syncing or resyncing when the user has not asked to update memory
- Any request where the user explicitly says "don't search memory"

---

## External endpoints

This skill sends data to three external services configured via `config.env`:

| Service | Variable | What is sent |
|---|---|---|
| Embedding endpoint (OpenAI-compatible) | `EMBED_BASE_URL` | Text chunks from memory files and Postgres records, for vector embedding |
| Qdrant | `QDRANT_HOST` | Embedded vectors + metadata for storage and search queries |
| Postgres | `POSTGRES_DSN` | Read-only queries against `memory_entries`, `daily_logs`, `tools` tables |

No data is sent to any Anthropic or third-party endpoint by this skill.

---

## Privacy statement

Memory content (daily logs, facts, tool descriptions) leaves the local machine in two ways:

1. Text is sent to your configured embedding endpoint (`EMBED_BASE_URL`) to generate vectors
2. Vectors + metadata are stored in and queried from your Qdrant instance (`QDRANT_HOST`)

Both services are self-hosted and configured by the user. No data is sent to any external party by this skill.

---

## Security manifest

Environment variables accessed:
- `QDRANT_HOST`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_PREFIX`
- `EMBED_BASE_URL`, `EMBED_API_KEY`, `EMBED_MODEL`
- `POSTGRES_DSN`
- `MEMORY_DIR`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K_DEFAULT`, `SYNC_BATCH_SIZE`, `EMBED_BATCH_DELAY_MS`

Files read:
- All `.md` files under `MEMORY_DIR`
- `config.env` (loaded at sync script startup)

Files written:
- None (no local file writes)

Database writes (Postgres):
- `memory_entries.qdrant_synced_at` — updated after successful vector upsert
- `daily_logs.qdrant_synced_at` — same
- `tools.qdrant_synced_at` — same
- `qdrant_sync_log` — one row inserted per sync run (records_synced, duration_ms)

Network:
- Outbound HTTPS to `EMBED_BASE_URL` (embedding)
- Outbound HTTPS to `QDRANT_HOST` (vector storage/search)
- Outbound TCP to Postgres host in `POSTGRES_DSN`

---

## Trust statement

By installing this skill, text from your memory files and database will be sent to the embedding endpoint configured in `EMBED_BASE_URL`. Vectors are stored in the Qdrant instance at `QDRANT_HOST`. Both are self-hosted services you configure. Only install if you trust those services with your memory contents.

When `auto_inject` is enabled (default: true), Qdrant search results are prepended to every prompt context. This data originates from your own self-hosted Qdrant instance — no external party supplies it. The content is sanitized of session boilerplate before storage but is otherwise injected as-is; only enable `auto_inject` if you trust your Qdrant data as prompt input.

---

## License

MIT-0 — no attribution required.

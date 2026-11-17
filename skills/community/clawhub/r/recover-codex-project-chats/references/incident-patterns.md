# Codex project-chat recovery patterns

## Provider mismatch

Signature:

- `config.toml` selects provider A.
- Most historical rows in `state_5.sqlite.threads.model_provider` use provider B.
- Rollout `session_meta.payload.model_provider` also uses B.
- Projects show no chats, while Recent may retain titles through a separate cache/catalog.
- App-server `thread/list` with `modelProviders: null` returns only the current provider, while `modelProviders: []` returns all providers.

This was the confirmed cause on 2026-08-06: the current provider was `custom` (named OpenAI and using OpenAI auth), while 195 historical rows used `openai`. Updating compatible historical metadata to `custom` restored project visibility.

## Assignment mismatch

Project definitions and thread assignment state are normally in:

- `~/.codex/.codex-global-state.json`
- keys: `local-projects`, `project-order`, `thread-project-assignments`, `thread-workspace-root-hints`, `projectless-thread-ids`

The database can contain valid thread rows and rollout paths while project groups remain empty if explicit assignments point elsewhere or are absent. Compare assignment IDs with `state_5.sqlite.threads.id`. For overlapping roots, use explicit mappings. Temporary paths such as `/private/var/folders/.../T/skill-up-*` require a project-name or known-origin mapping.

## State database landmarks

Primary history database: `~/.codex/state_5.sqlite`.

Important `threads` columns include `id`, `rollout_path`, `cwd`, `title`, `preview`, `model_provider`, `source`, `created_at`, `updated_at`, `recency_at`, `has_user_event`, and `archived`. Inspect the live schema because versions change.

Useful checks:

```sql
PRAGMA integrity_check;
SELECT model_provider, COUNT(*), SUM(archived = 0) FROM threads GROUP BY model_provider;
SELECT cwd, COUNT(*), SUM(archived = 0 AND preview <> '') FROM threads GROUP BY cwd;
SELECT id, rollout_path FROM threads;
```

`~/.codex/sqlite/codex-dev.db` may contain `local_thread_catalog`; it is a sidebar/catalog cache, not a substitute for rollout bodies or `state_5.sqlite`.

## Rollout bodies and CSV

Conversation bodies are normally under `~/.codex/sessions/YYYY/MM/DD/*.jsonl` and `~/.codex/archived_sessions/*.jsonl`. The first JSONL record is usually `session_meta`; compare its ID, cwd, source, and model provider with the database row.

Parse CSV with a real CSV parser or SQLite `.import`; line counts can be misleading when fields contain newlines. A CSV snapshot is an index aid, not conversation content.

## Verification

Verify all layers:

1. SQLite integrity is `ok`.
2. Every target row has an existing rollout path.
3. Current-provider counts are nonzero for the expected cwd values.
4. Thread assignments reference existing project IDs and thread IDs.
5. After restart, each project lists chats and representative old chats open successfully.

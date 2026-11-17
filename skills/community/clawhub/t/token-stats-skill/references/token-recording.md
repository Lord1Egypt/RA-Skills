# Token Recording Reference

Baseline: [token-stats v0.1.0](https://github.com/baijian/token-stats/releases/tag/v0.1.0), commit `df44be1c7c8a`. Use the matching release notes and binary help. See [Recorder Security](recorder-security.md) for installation and [Trae CN](trae-cn.md) for its separate account workflow.

## CLI Surface

```bash
token-stats sources --data-dir PATH --output json
token-stats usage --agent codex --day YYYY-MM-DD --refresh --output json
token-stats report range --agent codex --from YYYY-MM-DD --to YYYY-MM-DD --output json
```

- `--agent codex|claude|openclaw|hermes|opencode|deepseek|workbuddy|workbuddy-ai|trae-cn|all`: `usage` defaults to `codex`; `report range` defaults to `all`. Always pass the chosen scope. `sources` lists every source and has no agent filter.
- `--day YYYY-MM-DD`: local calendar day, default today.
- `--from`, `--to`: inclusive range, default latest seven days including today. Split report ranges over 366 days; Trae sync has a separate 31-day limit.
- `--refresh`: rebuild and overwrite selected daily records from local data; never downloads Trae usage. Today's `usage` auto-refreshes unless `--refresh=false`; historical days and all range queries otherwise read stored records.
- `--data-dir PATH`: report store and Trae snapshot root; supported by `sources`, `usage`, `report range`, and `trae sync`. `trae status` inspects logins, not this store.
- `--output json`: structured output. Reports may expose paths, model names, and session identifiers; do not put full JSON into scheduler logs.

Local source overrides and defaults:

| Selector / flag | CLI environment/default | Scanned data |
| --- | --- | --- |
| `codex` / `--codex-home` | `CODEX_HOME` or `~/.codex` | `sessions`, `archived_sessions` |
| `claude` / `--claude-home` | `CLAUDE_HOME` or `~/.claude` | `projects` |
| `openclaw` / `--openclaw-home` | `OPENCLAW_HOME` or `~/.openclaw` | `agents/*/sessions` |
| `hermes` / `--hermes-home` | `HERMES_HOME` or `~/.hermes` | `state.db` |
| `opencode` / `--opencode-home` | `OPENCODE_HOME`, `$XDG_DATA_HOME/opencode`, or `~/.local/share/opencode` | `opencode.db` |
| `deepseek` / `--deepseek-home` | `DSH_HOME` or `~/.dsh` | `sessions/<workspace>/<session>/session.jsonl[.zstd]` |
| `workbuddy` / `--workbuddy-home` | `WORKBUDDY_HOME` or `~/.workbuddy` | `projects/**/*.jsonl` |
| `workbuddy-ai` / `--workbuddy-ai-home` | `WORKBUDDY_AI_HOME` or `~/.workbuddy-ai` | `projects/**/*.jsonl` |

There is no `--trae-home` usage override. Trae CN reports read `<data-dir>/.sources/trae-cn/*.json`; `--storage-file` and `--account` belong to Trae setup/sync, not `usage`.

## Source Diagnostics

`sources --output json` returns an array with `agent`, `supported`, `detected`, `paths`, `note`, and optional `errors`. It checks source-path existence without parsing chats or reading Trae login credentials. Pass the same eight home overrides and `--data-dir` as collection.

- Supported and detected does not mean counters are complete or current.
- Supported but undetected means the collector exists but a path is missing. Check overrides and errors.
- Generic/global `trae`, `doubao`, and `doubao-work` remain unsupported diagnostics, excluded from `all`. Known-path discovery for these applications is macOS-only.
- `trae-cn` is supported through local snapshots. Cache directory detection does not guarantee coverage for the requested account/dates.

## Daily Storage

```text
<data-dir>/<agent>/<YYYY-MM-DD>.json
<data-dir>/.sources/trae-cn/<account-fingerprint>.json
```

The default data directory remains `~/.local/data/cycling-health-cli/token-usage`. `all` has its own daily namespace; it does not write all single-agent namespaces. Daily writes are atomic with `0600` files and `0700` agent directories. The wrapper additionally checks the dedicated root, existing files, ownership, hardlinks, and output-path symlinks. Direct CLI calls do not inherit all wrapper protections.

Missing stored days make stored-only reads fail, not zero-fill. Refresh requested dates for first collection or a rebuild. New collectors and newly synced Trae data are not retroactively added to cached `all` reports. Refresh cannot recover data missing from underlying sources.

## JSON Fields

- `schemaVersion`: `1` in this release.
- `generatedAt`, `agent`, `cached`: report time, namespace, and cache status.
- `scanned.files`, `scanned.events`, `scanned.skippedLines`: coverage diagnostics, not a guaranteed API-request count.
- `total`: aggregate token buckets.
- `byAgent`, `byModel`, `byRateLimit`, `byDay`: arrays of `{key, usage, events}` buckets. Rate-limit buckets are not live quota balances.
- `byProvider`: one bucket per provider with that provider's models nested under `models`. Ordered by consumption, unattributed usage last. It always adds up to `total`.
- `byProviderModel`: one flat bucket per provider-model pair, keyed `provider::model`.
- `byModel`: the provider-independent model view. Its key is the bare model id, so one model reached through several providers merges into a single bucket here.
- `attribution`: per agent, `attributedTokens` and `unattributedTokens`, which sum to that agent's `byAgent` total. A large unattributed share means incomplete provider coverage for that agent, not zero usage.
- `warnings`: coverage, parsing, or attribution limitations.

Daily reports add `day`, `storagePath`, and `sessions` with identifiers, path/cwd, provider, model, usage, and events. Ranges add `from`, `to`, `storageDir`, and `days`; ranges do not include `sessions`.

Token buckets are `inputTokens`, `cachedInputTokens`, `cacheWriteTokens`, `outputTokens`, `reasoningOutputTokens`, and `totalTokens`. Use `total.totalTokens` as provided. Cache and reasoning breakdowns can overlap with input/output. These counters and Trae's derived totals are not provider invoices.

Provider names are route names reported exactly as the local log records them (`openai-codex`, `aiyun`, `deepseek-official`, ...), never normalized into another name and never guessed from a model name. One model can therefore appear under several providers when it was reached through several routes. Provider coverage differs by source: DeepSeek Harness, Hermes, OpenCode, Codex, and OpenClaw declare one; WorkBuddy states it as the `route:model` prefix of its recorded model id; Claude Code and Trae CN state none and land in `unknown` (`unattributed` in text).

`--breakdown providers|provider-models|models|all` selects which text sections print; JSON always carries every breakdown. Records written before v0.0.4 have no provider keys, so rescan a day with `--refresh` before presenting its provider split.

## Attribution Limits

- State dates, timezone, agent filter, data directory, missing coverage, and meaningful warnings. For `all`, separate local sources from account-wide Trae before interpreting machine usage.
- Do not sum daily cumulative snapshots, breakdown dimensions, or `all` plus individual namespaces.
- WorkBuddy and WorkBuddy AI are separate applications. Within each, provider responses are deduplicated by session/message ID, mirrored traces excluded, and `message.usage`, `providerData.usage`, and `rawUsage` treated as alternatives. Cached input is within input, reasoning within output. Database context occupancy/credits are not cumulative usage. Other log versions/platforms may expose different counters.
- Hermes delegated usage comes from `session_model_usage`; main-session counters belong to the session start day, including sessions crossing midnight.
- SQLite sources are read-only. The immutable fallback warns that uncheckpointed WAL updates may be absent.
- DeepSeek Harness v0 and v3 session JSONL and concatenated Zstandard logs are supported (`session.jsonl` / `session.jsonl.zstd` and `session.v3.jsonl` / `session.v3.jsonl.zstd`). Final assistant samples replace earlier ones for a turn/step; chunk-only usage is included and fork-inherited history excluded. v0 states the inherited event count in the header; v3 states `isSeeded` and marks the cut with the last `session/end-seed` carrying `data.inherited: true`, and a seeded v3 session without that marker is warned about and skipped rather than rebilled. Subagents use `deepseek:subagent` buckets. The last usage sample determines the local date. Input includes cache reads/writes; reasoning is within output. Unknown session versions produce warnings.
- A DeepSeek Harness session that is still being written is counted up to its trailing partial Zstandard frame, with one `incomplete DeepSeek Harness session` warning. Records appended after the scan started are picked up by the next scan of that day, which replaces the stored record.
- For Trae account identity, missing reasoning, grouped events, timestamps, and client attribution, read [Trae CN](trae-cn.md).

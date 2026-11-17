# Trae CN In v0.1.0

## Consent And Data Boundary

Local recording and Trae synchronization are separate operations. Do not read login storage or run sync for a generic token-history question. Explain the account, date window, official endpoint, and local output, and obtain authorization for Trae setup/sync.

- `trae status` is offline but reads existing Trae CN / TRAE SOLO CN login metadata and returns account fingerprints and availability. Do not read or print the underlying credential file yourself.
- `trae sync` is the only network step. It uses existing credentials to query `https://api.trae.cn`, rejects redirects, and does not refresh or rewrite authentication. On expired auth, ask the user to sign in in the official application; never request a token in chat.
- `usage`, `report range`, and `sources` use local snapshots. `--refresh` is not an authorization or command to sync. The scheduler never runs `trae status` or `trae sync`.
- Snapshots exclude raw credentials, prompts, and raw API responses. Account/session identifiers are hashed. Model names, timestamps, token totals, and activity patterns remain sensitive.

## Explicit Sync Workflow

After verifying the pinned CLI and obtaining authorization for Trae setup:

```bash
token-stats trae status --output json
```

On macOS, default login discovery uses `~/Library/Application Support/Trae CN/User/globalStorage/storage.json` and the corresponding `TRAE SOLO CN` path, not `~/.trae-cn`. Both status and sync accept repeatable `--storage-file PATH` for an explicitly chosen login file. Never copy these files into the skill, repository, report directory, or conversation.

When multiple different accounts are found, have the user choose the returned fingerprint. Use `--account FINGERPRINT`; it is required for ambiguous selection. CN and SOLO logins for the same account are deduplicated, not separate usage sources.

```bash
# Use the same timezone and data directory for sync and reporting.
TZ=Asia/Shanghai token-stats trae sync --account ACCOUNT_FINGERPRINT \
  --from YYYY-MM-DD --to YYYY-MM-DD --data-dir /absolute/private/token-usage --output json

# Separate offline read after synchronization succeeds.
TZ=Asia/Shanghai token-stats usage --agent trae-cn --day YYYY-MM-DD \
  --refresh --data-dir /absolute/private/token-usage --output json
TZ=Asia/Shanghai token-stats report range --agent trae-cn \
  --from YYYY-MM-DD --to YYYY-MM-DD --refresh \
  --data-dir /absolute/private/token-usage --output json
```

Direct CLI calls do not inherit wrapper path checks. Use a dedicated private directory without symlinks, or use the wrapper for one-day recording after sync. For scheduled offline Trae reports, choose `--agent trae-cn`, the same `--data-dir`, and the same `--timezone`. Periodic offline collection does not authorize recurring network synchronization.

## Limits And Failures

- Default window: latest seven days including today. Maximum: 31 inclusive days per sync; split larger requested windows.
- Requests use `usage_type: [7]`, pages of 20, and a limit of 2,000 rows per day with bounded retries. Exceeding limits or failing any day fails the window; do not accept truncated data.
- Successful complete windows commit atomically to `<data-dir>/.sources/trae-cn/<account-fingerprint>.json`, with `0600` files and private directories. Failure preserves the previous snapshot.
- Concurrent sync is guarded by an account `.json.lock`. Do not delete a lock automatically; establish that no sync is running before proposing recovery.
- Sync refreshes source snapshots, not previously generated reports. Explicitly rebuild requested `trae-cn` or `all` days afterwards.
- Cached days may be stale or incomplete for today. Report their fetch time/coverage. Offline scheduled runs cannot refresh remote snapshots.

## Accounting And Coverage

- This is **account-wide** API usage and can include other machines. v0.1.0 cannot reliably split IDE, SOLO, and Work consumption. Do not count the same account under multiple client names or call it local-machine usage.
- `totalTokens` is derived from input plus output, not a separately verified API total or invoice. Cache counters are breakdowns, not additional consumption.
- Reasoning tokens are unavailable. A common-schema zero means unknown here, not measured zero.
- Rows are grouped records. `events` does not establish the number of model calls. Preserve actual model names; missing names remain unknown.
- Sync and reporting timezones must match. Changed timezones can invalidate stored day boundaries and require resync of the authorized window, not relabeling files.
- `all` includes accounts already represented by snapshots. No cache means this optional source is absent. Known accounts missing dates generate warnings. Explicit `trae-cn` with missing coverage fails rather than returning verified zero. The selector may aggregate multiple cached accounts; `usage` has no `--account` flag. For isolated-account analysis, use a dedicated data directory populated only for that account.
- Global/generic Trae, Doubao, and Doubao Work remain diagnostic-only. Do not relabel their usage as `trae-cn`.

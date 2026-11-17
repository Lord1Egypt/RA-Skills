# Runtime Policy Reference

Use this reference when designing storage, profile isolation, sync, backup, and task execution for PT automation.

## Contents

- Profile Isolation
- Storage Model
- Remembered Site Information
- Backup and Sync
- Secret References
- Credential Validation Before Save
- Task Execution
- Validation Checklist

## Profile Isolation

- One automation profile per tracker account or account group.
- Bind the profile to the intended proxy when tracker rules require a stable IP.
- Reuse logged-in browser state instead of asking the user to paste cookies.
- Store profile paths outside committed project directories.

## Storage Model

Skills do not remember state by themselves. Persistent memory must live in the host application, an MCP/database service, a provider CLI, or the bundled local fallback store.

Resolve `SKILL_ROOT` to the directory containing `SKILL.md` before invoking bundled scripts. Never resolve `scripts/...` relative to the user's working directory.

Persist non-secret entities:

- Tracker adapter metadata and enabled capabilities.
- User-defined tracker configs: base URL, adapter id, auth mode, category mapping, rate limits, enabled state.
- Incomplete tracker drafts captured from user messages, including missing fields and validation status.
- Downloader configs: type, base URL, defaults, labels/categories, save path mappings, enabled state.
- Tracker account status snapshots: upload/download totals, ratio, bonus, seeding counts, invites/messages, warning/HnR risk, and last checked time.
- User-defined search filters.
- Downloader mappings.
- Task schedules and run history.
- Sanitized parser fixtures.

Persist secret material only through the application's secret store or environment-variable references:

- Tracker cookies.
- Passkeys and RSS keys.
- Downloader passwords or API tokens.
- Proxy credentials.

## Remembered Site Information

The host should remember site information the user has already provided:

- Save complete validated trackers as normal tracker configs.
- Save incomplete but useful site information as tracker drafts.
- Reuse drafts/configs before asking questions in later turns.
- Match by local id, display name, alias from `site-preset-catalog.json`, URL host, and `sitePresetId`.
- Track draft status: `pending_fields`, `pending_credential`, `pending_validation`, `pendingHealthCheck`, `invalid_credential`, or `ready_to_confirm`.
- Store only references for credentials and profiles. Never store raw secret values from chat.
- Store account status separately from tracker config so a failed stats refresh does not erase a valid site configuration.

When a draft becomes complete, run the credential gate and ask for confirmation before promoting it to an enabled tracker config.

After a credential validates, run the adapter's account stats capability when supported. Persist a sanitized snapshot:

```json
{
  "trackerId": "site-a",
  "status": "ok",
  "uploadedBytes": 1200000000000,
  "downloadedBytes": 300000000000,
  "ratio": 4.0,
  "bonus": 12345.6,
  "seeding": 42,
  "hnrUnsatisfied": 0,
  "lastCheckedAt": "2026-07-08T00:00:00.000Z"
}
```

If stats refresh fails, persist a redacted status such as `auth_required`, `capability_unavailable`, or `parse_failed` with a short repair message. Do not persist raw HTML, screenshots, user profile URLs, cookies, passkeys, or private links.

If no host storage API exists, use `scripts/pt_store.py` and persist to the resolved local fallback store. Never assume a user has Hermes or a `~/.hermes` directory.

Local fallback store resolution order:

1. `PT_AGENT_STORE`: exact JSON store path.
2. `PT_AGENT_HOME`: directory containing `store.json`.
3. Host home environment variables such as `CODEX_HOME`, `HERMES_HOME`, or `OPENCLAW_HOME`.
4. Installed skill home, such as `~/.codex/skills/pt-agent` resolving to `~/.codex/pt-agent/store.json`.
5. XDG state fallback: `$XDG_STATE_HOME/pt-agent/store.json`, otherwise `~/.local/state/pt-agent/store.json`.

The `location`, `summary`, `doctor`, `audit-secrets`, and `init` commands report both `store` and `storeSource`. Use that reported path in user-facing debugging instead of hardcoding a host path. Prefer `location` when the user only asks where data lives because it does not read or create the store. Prefer `doctor` for setup/debugging because it combines path, counts, warnings, and raw-secret audit paths without printing secret values.

The local fallback store must redact command output. Use `python3 "$SKILL_ROOT/scripts/pt_store.py" audit-secrets` to find older raw secret-like fields by path only. If audit reports paths, do not use or repeat those values; ask the user to replace them with `secret://`, `env://`, or `profile://` references.

For a trusted local migration, `migrate-inline-secrets --env-file <host-env-file>` moves supported legacy tracker cookies and downloader passwords into a mode-`0600` environment file, replaces store fields with `env://` references, and reports names/paths only. Restart the host after migration. Never retain direct scraping as a compatibility path.

On Hermes, or when the user says they previously used Hermes, also check for legacy config at `~/.hermes/pt-sites.json` and migrate it with `python3 "$SKILL_ROOT/scripts/pt_store.py" migrate-legacy` before asking the user to repeat information.

## Backup and Sync

Backup should export:

- Adapter ids and user preferences.
- Filters, categories, labels, save path mappings.
- Task definitions.
- Non-sensitive run summaries.

Backup must exclude:

- Browser profiles.
- Cookies and local storage.
- `.torrent` files and magnet links containing private keys.
- Screenshots or HTML snapshots with usernames, passkeys, messages, or private URLs.

## Secret References

Use references rather than secret values in persisted config:

```json
{
  "credentialRef": "secret://downloaders/nas-qb",
  "profileRef": "profile://trackers/site-a",
  "proxyRef": "proxy://home-static-ip"
}
```

Resolve these references only at runtime. Do not return resolved values to general UI APIs.

Require normal TLS certificate and hostname verification for tracker, bridge, RSS, and downloader HTTPS requests. Treat certificate failures as network/TLS configuration errors; never retry with verification disabled.

## Credential Validation Before Save

Every tracker credential must be validated before the host persists the tracker config:

1. Resolve `sitePresetId` and `adapterId`.
2. Load adapter auth requirements from the host registry or `adapter-catalog.json`.
3. Reject unsupported `authMode` values immediately.
4. Verify required reference fields exist, such as `profileRef`, `secretRefs.cookie`, `secretRefs.apiToken`, `apiKeyRef`, or RSS feed URL references.
5. If the host can resolve secrets/profiles safely, run a harmless auth validation request before saving.
6. If runtime validation is impossible at setup time, save only after static validation and mark the tracker as `pendingHealthCheck`.
7. If runtime validation succeeds and the adapter supports it, fetch and persist sanitized tracker account status.

Never persist a tracker config whose credential type is incompatible with the selected adapter.

## Task Execution

- Add jitter to scheduled checks.
- Use bounded concurrency per tracker and global queue limits.
- Store failure reasons with redacted URLs.
- Separate parser failure, auth failure, network/proxy failure, and downloader failure.
- For repeated failures, disable only the affected tracker task and keep other trackers running.

## Validation Checklist

- Parser fixtures cover at least one successful search page and one empty or login-required state.
- Downloader add is tested against a mock or local test client before live use.
- Downloader status is tested for healthy, unauthorized, and unreachable states.
- Logs are reviewed for secret leakage.
- Browser launch changes run the repository's ignored runtime smoke when feasible.

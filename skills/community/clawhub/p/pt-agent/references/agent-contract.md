# Agent Contract Reference

Resolve `SKILL_ROOT` to the directory containing `SKILL.md` before using any bundled command below. The examples intentionally use absolute paths derived from that root.

Use this reference when Codex must produce structured calls for Hermes, OpenClaw, Codex plugins, CLI agents, or another host agent runtime. This skill does not execute network requests itself unless the host exposes a tool. It prepares safe, redacted payloads.

## Contents

- Capability Envelope
- Configuration Discovery
- Local Fallback Store
- Direct Runtime CLI
- Interaction State
- Remembered Tracker Drafts
- Site And Adapter Presets
- Standard Error Codes
- tracker.auth.validate
- tracker.user_stats
- tracker.config.create
- downloader.config.create
- tracker.search
- downloader.add
- downloader.status

## Capability Envelope

Use this envelope when no concrete tool schema is provided:

```json
{
  "capability": "downloader.config.create",
  "version": "1.0",
  "confirm": true,
  "payload": {},
  "redaction": {
    "secretFields": ["credentialRef", "secretRefs", "profileRef", "proxyRef"],
    "notes": "No raw cookies, passkeys, passwords, or torrent bytes included."
  }
}
```

If the host exposes a concrete tool, map the `payload` fields directly into that tool's arguments.

## Configuration Discovery

Hosts should expose one of these capabilities so the agent can decide whether to guide setup first:

```json
{
  "capability": "pt.config.summary",
  "version": "1.0",
  "confirm": false,
  "payload": {}
}
```

Expected response:

```json
{
  "trackers": [{ "id": "site-a", "displayName": "Site A", "enabled": true }],
  "trackerDrafts": [{ "id": "site-a", "displayName": "Site A", "status": "pendingHealthCheck" }],
  "trackerStats": [{ "trackerId": "site-a", "status": "ok", "uploadedBytes": 1200000000000, "downloadedBytes": 300000000000, "ratio": 4.0 }],
  "downloaders": [{ "id": "nas-qb", "displayName": "NAS qBittorrent", "enabled": true }],
  "defaultSearchSolutionId": "default",
  "defaultDownloaderId": "nas-qb"
}
```

If the host does not expose config discovery, the agent should ask the user whether trackers/downloaders are already configured before search/send/status actions.

## Local Fallback Store

If the host has no persistent config API, use the bundled local store script rather than relying on chat memory:

```bash
python3 "$SKILL_ROOT/scripts/pt_store.py" location
python3 "$SKILL_ROOT/scripts/pt_store.py" summary
python3 "$SKILL_ROOT/scripts/pt_store.py" doctor
python3 "$SKILL_ROOT/scripts/pt_store.py" audit-secrets
python3 "$SKILL_ROOT/scripts/pt_store.py" upsert-tracker --draft --json '{"id":"site-a","sitePresetId":"site-a","adapterId":"nexusphp","authMode":"browser_profile","profileRef":"profile://trackers/site-a","status":"pending_validation"}'
python3 "$SKILL_ROOT/scripts/pt_store.py" upsert-stats --tracker site-a --json '{"status":"auth_required","message":"profile/cookie required"}'
python3 "$SKILL_ROOT/scripts/pt_store.py" upsert-downloader --json '{"id":"nas-qb","type":"qbittorrent","baseUrl":"http://nas:8080","credentialRef":"secret://downloaders/nas-qb"}'
```

Default path:

Do not hardcode a Hermes path. Resolve the local fallback store in this order:

1. `PT_AGENT_STORE`: exact JSON store path.
2. `PT_AGENT_HOME`: directory containing `store.json`.
3. Host home env vars such as `CODEX_HOME`, `HERMES_HOME`, or `OPENCLAW_HOME`.
4. Installed skill home, such as `~/.codex/skills/pt-agent` -> `~/.codex/pt-agent/store.json`.
5. XDG state fallback: `$XDG_STATE_HOME/pt-agent/store.json` or `~/.local/state/pt-agent/store.json`.

Rules:

- Read this store before asking for tracker/downloader fields.
- Store complete validated trackers in `trackers`.
- Store incomplete or unvalidated trackers in `trackerDrafts`.
- Store sanitized tracker account snapshots in `trackerStats`.
- Store downloaders in `downloaders`.
- Store only secret/profile references, never resolved secret values.
- Use `location` when the user asks where data lives; it does not read or create the store.
- Use `doctor` for setup/debugging; it reports counts, warnings, resolved path, and raw-secret audit paths without printing values.
- Treat `summary`, `find-tracker`, `upsert-*`, and `migrate-legacy` output as redacted.
- Use `audit-secrets` to detect older raw secret-like values by path only. If audit reports paths, ask the user to replace those fields with `secret://`, `env://`, or `profile://` references before treating the config as ready.
- If running under Hermes, or the user previously used Hermes, migrate an older `~/.hermes/pt-sites.json` once with:

```bash
python3 "$SKILL_ROOT/scripts/pt_store.py" migrate-legacy
```

Capability equivalent:

```json
{
  "capability": "pt.local_store.summary",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "path": "<resolved-local-store>"
  }
}
```

Raw-secret audit equivalent:

```json
{
  "capability": "pt.local_store.audit",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "path": "<resolved-local-store>"
  }
}
```

Expected audit response:

```json
{
  "ok": false,
  "rawSecretLikePaths": ["trackers.site-a.cookie"]
}
```

## Direct Runtime CLI

When a host agent can execute local scripts but has no native PT tools, call `scripts/pt_runtime.py`. The script returns JSON for every command and uses `scripts/pt_store.py` for persisted configuration.

Supported commands:

```bash
python3 "$SKILL_ROOT/scripts/pt_runtime.py" site-presets site-a
python3 "$SKILL_ROOT/scripts/pt_runtime.py" adapter-presets nexusphp torznab rss
python3 "$SKILL_ROOT/scripts/pt_runtime.py" validate-tracker --tracker site-a
python3 "$SKILL_ROOT/scripts/pt_runtime.py" health-check --tracker site-a
python3 "$SKILL_ROOT/scripts/pt_runtime.py" user-stats --tracker site-a --persist
python3 "$SKILL_ROOT/scripts/pt_runtime.py" search "movie title 1080p" --tracker site-a --limit 20
python3 "$SKILL_ROOT/scripts/pt_runtime.py" media-search "周星驰的电影" --tracker hh --kind movie --limit 10 --timeout 10
python3 "$SKILL_ROOT/scripts/pt_runtime.py" overview --refresh
python3 "$SKILL_ROOT/scripts/pt_runtime.py" downloader-status --downloader qb-main
python3 "$SKILL_ROOT/scripts/pt_runtime.py" add-magnet --downloader qb-main --magnet "magnet:?xt=urn:btih:..." --category pt --tags pt-agent --paused
```

Credential provider behavior:

- `env://NAME` is resolved directly from environment variables.
- `secret://`, `profile://`, and `proxy://` return `provider_unavailable` unless the host implements and injects those providers.
- Raw cookies, passwords, passkeys, API keys, private download URLs, and torrent bytes are never printed.

Implemented direct adapters:

- `torznab`, `prowlarr`, `jackett`: XML search through a user-provided endpoint and API key reference.
- `rss`: RSS feed search through a user-provided feed URL/reference.
- `nexusphp`, `unit3d`, `gazelle`, `selector`: conservative schema-default HTML search using declared paths and cookie auth only.
- `tracker.user_stats`: heuristic normalized account stats from authenticated HTML when cookie/env auth is available.
- `downloader.status`: qBittorrent login/session plus `/sync/maindata` status with `env://` credential reference.
- `add-magnet`: qBittorrent magnet add through `/torrents/add`.

The direct runtime follows the PT-depiler execution model: resolve site metadata, merge user config, use schema-declared request defaults, run a login-like response check before parsing, normalize search/user-info fields, and keep downloader authentication/session handling inside the downloader client.

For qBittorrent, `credentialRef=env://QB_CREDENTIALS` may resolve to `username:password`, a qBittorrent API key beginning with `qbt_`, or JSON such as `{"username":"admin","password":"..."}`.

If a direct command returns `capability_unavailable`, the agent should fall back to a native host tool or explain that the adapter needs implementation. Do not fabricate success.

## Interaction State

Hosts may persist lightweight interaction state so setup can resume the user's original request:

```json
{
  "pendingIntent": {
    "type": "search",
    "keyword": "沙丘 2160p",
    "createdAt": "2026-07-08T00:00:00.000Z"
  },
  "setupStage": "tracker",
  "draftTracker": {
    "id": "site-a",
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "authMode": "browser_profile"
  },
  "knownTrackers": [
    {
      "id": "site-a",
      "displayName": "Site A",
      "sitePresetId": "site-a",
      "adapterId": "nexusphp",
      "authMode": "browser_profile",
      "profileRef": "profile://trackers/site-a",
      "status": "pendingHealthCheck"
    }
  ],
  "draftDownloader": {},
  "lastSearch": {
    "query": "沙丘 2160p",
    "resultIds": [],
    "visibleResultIds": [],
    "page": 1,
    "pageSize": 5,
    "total": 0,
    "filters": {},
    "sort": "relevance"
  },
  "lastConfirmation": {
    "action": "tracker.config.create",
    "expiresAt": "2026-07-08T00:10:00.000Z"
  }
}
```

Rules:

- `pendingIntent` is used only to resume user-facing workflow; it must not contain secrets.
- `draftTracker` and `draftDownloader` contain references only, never resolved secret values.
- `knownTrackers` mirrors saved configs/drafts that are useful for the current conversation.
- `lastSearch.visibleResultIds` is the source of truth for commands such as "第 3 个".
- `lastSearch.resultIds` may contain all current result ids, while visible ids contain only the current page after filter/sort.
- `lastConfirmation` should expire quickly so a later "确认" cannot apply to stale state.
- If a user changes a field after confirmation was shown, invalidate `lastConfirmation` and show a new redacted summary.

## Remembered Tracker Drafts

When a user provides site-related information, hosts should store reusable non-secret fields even if the tracker is not ready to enable. Use this capability when a full `tracker.config.create` cannot be emitted yet:

```json
{
  "capability": "tracker.config.draft.upsert",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "id": "site-a",
    "displayName": "Site A",
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a",
    "status": "pending_fields",
    "missing": ["baseUrl"],
    "source": "user_message"
  },
  "redaction": {
    "secretFields": ["profileRef", "secretRefs", "proxyRef"],
    "notes": "Only references are stored; no raw secret values."
  }
}
```

Draft rules:

- Store non-secret identity fields: id, display name, site preset id, adapter id, schema id, base URL, category preferences, rate limit, enabled intent, and status.
- Store secret/profile values only as references such as `profileRef`, `secretRefs.cookie`, `apiKeyRef`, or `env://...`.
- Match future user messages against drafts by id, display name, alias, URL host, and `sitePresetId`.
- If a later message provides a field for a draft, update the draft and ask only for remaining missing/invalid fields.
- Promote a draft to full config only after credential compatibility validation and confirmation.
- If the user exposes raw secret values, do not save them; ask for a secret reference and mark the draft as `awaiting_secret_ref`.

## Site And Adapter Presets

Use adapter presets for software/API families and site presets for exact private tracker definitions. A site preset can inherit an adapter/schema, such as `sitePresetId=site-a` with `schemaId=nexusphp`.

If the host does not maintain its own site preset registry, it should load `references/site-preset-catalog.json` from this skill and implement `tracker.site.presets` by matching `query` against `id`, `displayName`, and `aka`.

If the host does not maintain its own adapter registry, it should load `references/adapter-catalog.json` from this skill and implement `tracker.adapter.presets` from that catalog. Use `references/adapter-implementation.md` for execution and error-handling rules.

```json
{
  "capability": "tracker.site.presets",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "query": "site-a",
    "includeDisabled": false
  }
}
```

Expected response:

```json
{
  "sites": [
    {
      "id": "site-a",
      "displayName": "Site A",
      "schemaId": "nexusphp",
      "adapterId": "nexusphp",
      "type": "private",
      "supportedCapabilities": ["search", "download_torrent", "user_stats"],
      "requiredAuthModes": ["browser_profile", "cookie"],
      "status": "supported"
    }
  ]
}
```

If the site is mapped but its schema adapter is not executable in the current host, return the preset with `status: "adapter_not_available"` or return `capability_unavailable` with `requiredAdapterId`. Do not drop the mapping.

```json
{
  "error": {
    "code": "capability_unavailable",
    "requiredAdapterId": "tnode",
    "sitePresetId": "site-b",
    "message": "The site is mapped, but this host has no TNode adapter."
  }
}
```

If no matching site preset exists, do not fabricate one. Ask for Torznab/Prowlarr/Jackett/RSS/API documentation, or ask whether to use a generic HTML schema adapter such as `nexusphp` with an authenticated profile.

Adapter preset discovery:

```json
{
  "capability": "tracker.adapter.presets",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "adapterIds": ["nexusphp", "tnode"],
    "includeUnavailable": true
  }
}
```

Expected response:

```json
{
  "adapters": [
    {
      "id": "nexusphp",
      "displayName": "NexusPHP",
      "status": "available",
      "authModes": ["browser_profile", "cookie"],
      "capabilities": ["search", "torrent_detail", "download_torrent", "user_stats"]
    }
  ]
}
```

## Standard Error Codes

Hosts should return machine-readable errors:

```json
{
  "error": {
    "code": "configuration_required",
    "missing": ["tracker"],
    "message": "No enabled tracker is configured."
  }
}
```

Recommended codes:

- `configuration_required`: missing tracker, downloader, search solution, profile, or secret reference.
- `not_found`: named tracker/downloader/result does not exist.
- `auth_required`: login/profile/credential is missing or expired.
- `validation_failed`: payload is malformed.
- `capability_unavailable`: host cannot execute the requested capability.
- `adapter_not_available`: site is mapped, but the host cannot run its required adapter.
- `endpoint_unknown`: user has not provided a documented endpoint for the selected adapter.
- `endpoint_mismatch`: configured endpoint returned 404, empty response, or a response shape incompatible with the selected adapter.
- `auth_material_mismatch`: provided secret reference type does not match adapter auth mode, such as using an API token as a cookie.
- `credential_not_accepted`: user supplied a credential that is valid-looking but unsupported by the resolved adapter, such as a cookie-only HTML adapter receiving `api_token`.
- `credential_validation_failed`: required credential reference fields are missing or malformed before a runtime auth check.
- `tracker_search_failed`: tracker request or parser failed.
- `parse_failed`: authenticated response loaded, but a stats/detail/search parser could not normalize it.
- `downloader_unreachable`: downloader endpoint cannot be reached.
- `downloader_auth_failed`: downloader credentials failed.
- `downloader_add_failed`: downloader rejected the torrent/magnet.

When `configuration_required` is returned, the agent should switch to the setup guide for the first missing item, then offer to resume the original intent.

When `endpoint_unknown`, `endpoint_mismatch`, or `auth_material_mismatch` is returned, the agent must stop probing and ask for corrected adapter details. It must not try unrelated endpoint families automatically.

When `credential_not_accepted` or `auth_material_mismatch` occurs before configuration is saved, the agent must not emit `tracker.config.create`. It should explain the mismatch and list the accepted credential types for that adapter.

Credential validation must happen for every tracker configuration before save. The host should expose `tracker.auth.validate` when it can check the credential at runtime; otherwise the agent must still perform static validation from `adapter-catalog.json`.

Example:

```json
{
  "error": {
    "code": "endpoint_mismatch",
    "adapterId": "unit3d-api",
    "message": "Configured API path returned 404.",
    "nextRequiredFields": ["adapterId", "baseUrl", "api.searchPath", "secretRefs.apiToken"]
  }
}
```

Credential mismatch example:

```json
{
  "error": {
    "code": "auth_material_mismatch",
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "providedAuthMode": "api_token",
    "supportedAuthModes": ["browser_profile", "cookie"],
    "nextRequiredFields": ["profileRef", "secretRefs.cookie"],
    "message": "This preset uses HTML authentication; api_token is not accepted."
  }
}
```

## tracker.auth.validate

Use this capability before saving a tracker when the host can resolve profile/secret references and make a harmless authenticated request. If unavailable, perform static validation and then run `tracker.health_check` after save.

```json
{
  "capability": "tracker.auth.validate",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "baseUrl": "https://tracker.example",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a",
    "secretRefs": {}
  }
}
```

Static validation failure:

```json
{
  "error": {
    "code": "credential_validation_failed",
    "adapterId": "nexusphp",
    "authMode": "browser_profile",
    "missing": ["profileRef"],
    "message": "browser_profile authentication requires profileRef."
  }
}
```

Runtime auth failure:

```json
{
  "error": {
    "code": "auth_required",
    "adapterId": "nexusphp",
    "message": "Credential reference was accepted, but the tracker did not return an authenticated page."
  }
}
```

## tracker.user_stats

Use this capability after `tracker.auth.validate` or `tracker.health_check` succeeds, and whenever the user asks for tracker account status. It must make only authenticated, harmless account/info requests declared by the selected adapter or site preset.

Request:

```json
{
  "capability": "tracker.user_stats",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "trackerId": "site-a",
    "sitePresetId": "site-a",
    "adapterId": "nexusphp"
  }
}
```

Expected normalized response:

```json
{
  "trackerId": "site-a",
  "status": "ok",
  "userId": "12345",
  "username": "redacted-or-display-safe",
  "levelName": "Power User",
  "uploadedBytes": 1200000000000,
  "downloadedBytes": 300000000000,
  "trueUploadedBytes": 1100000000000,
  "trueDownloadedBytes": 320000000000,
  "ratio": 4.0,
  "bonus": 12345.6,
  "bonusPerHour": 12.3,
  "seeding": 42,
  "seedingSizeBytes": 8000000000000,
  "leeching": 1,
  "invitations": 2,
  "unreadMessages": 0,
  "warnings": [],
  "hnrPreWarning": 0,
  "hnrUnsatisfied": 0,
  "lastCheckedAt": "2026-07-08T00:00:00.000Z"
}
```

Rules:

- Persist the normalized snapshot after every successful setup validation and after explicit status checks.
- Persist only these normalized fields; never persist raw profile URLs, cookies, HTML, passkeys, private detail URLs, or torrent links.
- If a site does not expose a field, omit it rather than inventing a value.
- If the adapter cannot support account stats, return `capability_unavailable` and keep the tracker config valid.
- If auth fails, return and persist a redacted failure status so later turns can say what needs repair.

Failure example:

```json
{
  "error": {
    "code": "auth_required",
    "trackerId": "site-a",
    "message": "The profile or cookie no longer reaches an authenticated user page."
  }
}
```

Local fallback after a host stats response:

```bash
python3 "$SKILL_ROOT/scripts/pt_store.py" upsert-stats --tracker site-a --json '{"status":"ok","uploadedBytes":1200000000000,"downloadedBytes":300000000000,"ratio":4.0,"seeding":42,"bonus":12345.6}'
python3 "$SKILL_ROOT/scripts/pt_store.py" upsert-stats --tracker site-a --json '{"status":"auth_required","message":"profile/cookie no longer reaches an authenticated user page"}'
```

## tracker.config.create

```json
{
  "capability": "tracker.config.create",
  "version": "1.0",
  "confirm": true,
  "payload": {
    "id": "site-a",
    "displayName": "Site A",
    "baseUrl": "https://tracker.example",
    "sitePresetId": "optional-known-site-id",
    "schemaId": "optional-schema-id",
    "adapterId": "selector",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a",
    "proxyRef": "proxy://home-static-ip",
    "secretRefs": {},
    "categories": {},
    "enabled": true,
    "rateLimit": { "minIntervalMs": 3000, "concurrency": 1 },
    "search": {
      "path": "/torrents.php",
      "keywordParam": "search",
      "categoryParam": "cat"
    },
    "selectors": {
      "result": "table.torrents tr",
      "title": "a[href*='details']",
      "detailLink": "a[href*='details']",
      "downloadLink": "a[href*='download']"
    }
  }
}
```

For named site presets, include `sitePresetId` and `schemaId`:

```json
{
  "capability": "tracker.config.create",
  "version": "1.0",
  "confirm": true,
  "payload": {
    "id": "site-a",
    "displayName": "Site A",
    "sitePresetId": "site-a",
    "schemaId": "nexusphp",
    "adapterId": "nexusphp",
    "baseUrl": "https://tracker.example",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a",
    "enabled": true,
    "rateLimit": { "minIntervalMs": 3000, "concurrency": 1 }
  }
}
```

For common API adapters, include `api` metadata from `references/common-site-apis.md`, for example:

```json
{
  "capability": "tracker.config.create",
  "version": "1.0",
  "confirm": true,
  "payload": {
    "id": "site-a",
    "displayName": "Site A",
    "baseUrl": "https://prowlarr.example/1/api",
    "adapterId": "torznab",
    "authMode": "api_token",
    "secretRefs": {
      "apiKey": "secret://trackers/site-a/api-key"
    },
    "api": {
      "type": "torznab",
      "queryParam": "q",
      "apiKeyParam": "apikey",
      "categoryParam": "cat",
      "downloadStrategy": "enclosure-or-link"
    },
    "enabled": true,
    "rateLimit": { "minIntervalMs": 3000, "concurrency": 1 }
  },
  "postCreate": [
    { "capability": "tracker.health_check", "payload": { "trackerId": "site-a" } },
    { "capability": "tracker.search", "payload": { "keyword": "original user keyword", "trackerIds": ["site-a"], "limitPerTracker": 10 } }
  ]
}
```

Use `postCreate` only as an execution plan. The host may execute these steps separately after the user confirms.

## downloader.config.create

```json
{
  "capability": "downloader.config.create",
  "version": "1.0",
  "confirm": true,
  "payload": {
    "id": "nas-qb",
    "displayName": "NAS qBittorrent",
    "type": "qbittorrent",
    "baseUrl": "http://nas.local:8080",
    "credentialRef": "secret://downloaders/nas-qb",
    "defaults": {
      "categoryOrLabel": "pt",
      "savePath": "/downloads/pt",
      "addPaused": false,
      "tags": ["pt-agent"]
    },
    "excludedSites": [],
    "enabled": true
  }
}
```

## tracker.search

```json
{
  "capability": "tracker.search",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "keyword": "movie title 1080p",
    "trackerIds": ["site-a", "site-b"],
    "categoryIds": ["movie"],
    "discount": "any",
    "sort": "relevance",
    "limitPerTracker": 30
  }
}
```

## downloader.add

```json
{
  "capability": "downloader.add",
  "version": "1.0",
  "confirm": true,
  "payload": {
    "resultId": "result-from-latest-search",
    "trackerId": "site-a",
    "downloaderId": "nas-qb",
    "categoryOrLabel": "pt",
    "savePath": "/downloads/pt",
    "addPaused": false,
    "tags": ["pt-agent"],
    "duplicatePolicy": "skip"
  }
}
```

## downloader.status

```json
{
  "capability": "downloader.status",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "downloaderId": "nas-qb"
  }
}
```

Expected normalized response:

```json
{
  "downloaderId": "nas-qb",
  "healthy": true,
  "type": "qbittorrent",
  "version": "v5.0.0",
  "freeSpaceBytes": 1000000000,
  "downloadRateBytesPerSec": 0,
  "uploadRateBytesPerSec": 0,
  "counts": {
    "active": 0,
    "downloading": 0,
    "uploading": 0,
    "paused": 0,
    "checking": 0,
    "errored": 0,
    "completed": 0
  },
  "lastCheckedAt": "2026-07-07T00:00:00.000Z"
}
```

## Host Tool Mapping

When the host has tools, prefer direct calls in this order:

1. Exact capability tool, such as `tracker.config.create`.
2. Generic capability executor, such as `agent.execute`, `hermes.execute`, `openclaw.execute`, or the host's equivalent.
3. Emit the envelope JSON for the caller to execute.

Never fabricate success. Say "payload prepared" if execution did not happen.

## Agent Runtime Examples

### Hermes

If Hermes exposes a generic executor, wrap the envelope:

```json
{
  "tool": "hermes.execute",
  "arguments": {
    "capability": "tracker.search",
    "payload": {
      "keyword": "movie title 1080p",
      "trackerIds": ["site-a"],
      "limitPerTracker": 30
    }
  }
}
```

### OpenClaw

If OpenClaw exposes task/action style tools, map the same contract to an action:

```json
{
  "action": "tracker.search",
  "input": {
    "keyword": "movie title 1080p",
    "trackerIds": ["site-a"],
    "limitPerTracker": 30
  },
  "requiresConfirmation": false
}
```

If the OpenClaw installation uses a different executor name, keep the capability name stable and only adapt the outer envelope.

### Codex Plugin Or MCP Host

If the host exposes discrete tools, call them directly:

```json
{
  "tool": "tracker_search",
  "arguments": {
    "keyword": "movie title 1080p",
    "trackerIds": ["site-a"],
    "limitPerTracker": 30
  }
}
```

### CLI Agent

If the host only accepts CLI-compatible JSON, print one compact envelope:

```json
{"capability":"downloader.status","version":"1.0","confirm":false,"payload":{"downloaderId":"nas-qb"}}
```

The CLI layer should own execution, persistence, and secret resolution.

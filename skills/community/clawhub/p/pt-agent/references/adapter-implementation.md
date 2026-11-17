# Adapter Implementation Reference

Use this reference when implementing `tracker.adapter.presets`, adding host adapter support, or deciding whether a mapped site can actually be searched/downloaded.

## Contents

- Relationship Between Catalogs
- Required Host Capabilities
- Execution Pattern
- Credential Compatibility
- Adapter Groups
- Standard Adapter Result
- Error Codes
- Implementation Priority

## Relationship Between Catalogs

- `site-preset-catalog.json` maps user-facing site names to `sitePresetId`, `schemaId`, and `adapterId`.
- `adapter-catalog.json` maps each `adapterId` to an execution contract.
- `common-site-apis.md` covers bridge adapters such as Torznab, Prowlarr, Jackett, RSS, and Unit3D API.
- A site is "recognized" when it exists in `site-preset-catalog.json`.
- A site is "runnable" only when the host implements its `adapterId` and the user supplies compatible auth/profile references.

## Required Host Capabilities

Hosts should implement:

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
    },
    {
      "id": "tnode",
      "displayName": "TNode",
      "status": "unavailable",
      "requiredBy": ["site-b"]
    }
  ]
}
```

If no host tool exists, the agent should use `adapter-catalog.json` to prepare the same payload and ask the host/application to implement or expose it.

## Execution Pattern

All schema adapters must follow the same high-level flow:

1. Resolve site by `tracker.site.presets`.
2. Resolve adapter by `tracker.adapter.presets`.
3. Validate user credential type against the adapter's `authModes`.
4. Reject incompatible credentials before saving configuration.
5. Merge site preset metadata with user config.
6. Use only declared request paths/selectors/templates from the selected adapter and site preset.
7. After runtime auth succeeds, fetch account stats through `tracker.user_stats` when the adapter declares `user_stats`.
8. Fetch search/detail/download through user-provided `profileRef`, `secretRef`, or supported API credential.
9. Return normalized result objects with opaque `resultId` or `downloadRef`.
10. During `downloader.add`, resolve the selected result through the same adapter, fetch torrent bytes or magnet using authenticated config, and send to the downloader.

Do not store raw private download URLs, cookies, passkeys, user profile URLs, source HTML, or torrent bytes.

## Credential Compatibility

Before `tracker.config.create`, hosts and agents must validate credentials for every site:

- `browser_profile` requires `profileRef`.
- `cookie` requires a cookie secret reference, not a pasted raw cookie in chat.
- `api_token` requires an adapter that declares `api_token` and a documented endpoint or bridge base URL.
- `rss_token` requires an RSS adapter/feed URL or feed URL secret.
- `credentialRef` for username/password is valid only for adapters that explicitly support that login flow.

This check is mandatory even when the site is not in `site-preset-catalog.json`. If the adapter is user-selected, validate against that adapter. If no adapter is selected, ask the user to choose an adapter before accepting credentials.

Validation has two phases:

1. Static validation: verify `authMode` is allowed by the adapter and required reference fields exist. This must pass before saving.
2. Runtime validation: when the host can access the network/profile/secret store, run `tracker.auth.validate` or `tracker.health_check` to verify the credential actually authenticates.

Do not confuse the phases. A syntactically valid `cookie` secret may still be expired; that is `auth_required` from runtime validation. An `api_token` submitted to a cookie-only HTML adapter is `auth_material_mismatch` before runtime validation.

If the credential does not match, return or explain:

```json
{
  "error": {
    "code": "auth_material_mismatch",
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "providedAuthMode": "api_token",
    "supportedAuthModes": ["browser_profile", "cookie"],
    "message": "This credential cannot authenticate the selected adapter."
  }
}
```

The assistant should translate that into a direct user-facing correction, not continue setup.

Runtime auth validation capability:

```json
{
  "capability": "tracker.auth.validate",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "sitePresetId": "site-a",
    "adapterId": "nexusphp",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a"
  }
}
```

Expected success:

```json
{
  "ok": true,
  "status": "authenticated",
  "userHint": "Authenticated session detected."
}
```

Expected failure:

```json
{
  "ok": false,
  "error": {
    "code": "auth_required",
    "message": "The profile or cookie did not authenticate against the selected tracker."
  }
}
```

After runtime auth succeeds, call account stats when the adapter supports it:

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

Return normalized fields only:

```json
{
  "trackerId": "site-a",
  "status": "ok",
  "uploadedBytes": 1200000000000,
  "downloadedBytes": 300000000000,
  "ratio": 4.0,
  "bonus": 12345.6,
  "seeding": 42,
  "hnrUnsatisfied": 0
}
```

If stats parsing fails but authentication is valid, return `selector_drift` or `parse_failed` for the stats operation and keep the tracker usable for search/download if those capabilities still work.

## Adapter Groups

### Generic HTML Schemas

Adapters: `nexusphp`, `unit3d`, `gazelle`, `luminance`, `rartracker`, `tcg`, `xbtit`, `tbsource`, `tbdev`.

Use browser profile or cookie-authenticated HTTP. Parse with DOM selectors. Use schema-declared paths and site-specific overrides only. On login redirect or selector mismatch, stop and return `auth_required` or `selector_drift`.

For a mapped HTML-only site preset, supported auth is usually browser profile or cookie secret. If the user provides `api_token`, tell them that credential is not usable for the selected HTML adapter. Do not accept it unless the host is actually configuring a separate Torznab/Prowlarr/Jackett/RSS/native documented API adapter with its own endpoint.

### JSON/API Schemas

Adapters: `gazelle-json`, `tnode`, `unit3d-api`.

Use only documented paths declared in the adapter or site preset. API tokens are valid only when the adapter declares `api_token`. A 404, HTML login page, or incompatible response is `endpoint_mismatch`, not a reason to try another path.

### Bridge Adapters

Adapters: `torznab`, `prowlarr`, `jackett`, `rss`.

Use user-provided endpoints and secret references. Never derive these URLs from a tracker homepage. Prefer bridge adapters when the user already has them because they usually provide direct search/download with less fragile HTML parsing.

### Site-Specific Metadata Adapters

Adapters: `custom-private`, `mtorrent`, `meantorrent`, `filelist`, `fsm`, `aidoruonline`, `f3nix`, `rousi`, `yemapt`, `cgbtsource`, `discuz`, `selector`, `avistaz-network`.

These require exact preset metadata. If the host does not implement the site-specific logic, return `capability_unavailable` with `requiredAdapterId`; do not downgrade to a guessed generic adapter unless the user explicitly chooses another documented access method.

## Standard Adapter Result

Adapter search results should normalize to:

```json
{
  "resultId": "opaque-result-id",
  "trackerId": "site-a",
  "sitePresetId": "site-a",
  "adapterId": "nexusphp",
  "title": "Example.Title.2026.1080p",
  "subtitle": "optional subtitle",
  "category": "Movie",
  "sizeBytes": 0,
  "seeders": 0,
  "leechers": 0,
  "completed": 0,
  "publishTime": "2026-07-07T00:00:00.000Z",
  "tags": [],
  "discount": "unknown",
  "detailRef": "opaque-detail-ref",
  "downloadRef": "opaque-download-ref"
}
```

`detailRef` and `downloadRef` may internally reference private URLs, but logs and final answers must keep them opaque.

## Error Codes

- `adapter_not_available`: site is mapped, but host cannot run its adapter.
- `auth_required`: missing or expired profile/cookie/token.
- `auth_material_mismatch`: credential type does not match adapter auth mode.
- `endpoint_unknown`: adapter requires a user-provided endpoint and none was supplied.
- `endpoint_mismatch`: declared endpoint returned the wrong status or response shape.
- `selector_drift`: authenticated HTML loaded, but selectors no longer match.
- `parse_failed`: authenticated response loaded, but stats/detail/search normalization failed.
- `rate_limited`: tracker or bridge API rate limit was hit.

## Implementation Priority

For a practical open-source host implementation:

1. Implement bridge adapters: `torznab`, `prowlarr`, `jackett`, `rss`.
2. Implement high-coverage schemas: `nexusphp`, `unit3d`, `gazelle`, `gazelle-json`.
3. Implement special schemas used by mapped sites: `tnode`, `mtorrent`, `avistaz-network`, `luminance`, `custom-private`.
4. Implement long-tail site-specific adapters from `adapter-catalog.json` as fixtures become available.

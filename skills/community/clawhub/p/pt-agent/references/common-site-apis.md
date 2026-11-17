# Common Site API Adapter Reference

Use this reference when a user wants common PT sites or tracker software to work immediately after configuration. Prefer named site presets and these adapter families before asking for raw selectors. For PT-depiler-style named presets and schema inheritance, also read `pt-depiler-patterns.md`.

## Contents

- Non-Negotiable Rules
- Adapter Selection Order
- Preset Capability
- Torznab
- Prowlarr
- Jackett
- RSS
- Unit3D API
- Gazelle JSON
- NexusPHP HTML/API Fallback
- Immediate Search After Setup
- Immediate Download After Search

## Non-Negotiable Rules

- Do not infer that a private tracker supports an API just because the user has an `api_token`.
- Do not try random endpoint paths such as `/api`, `/api/v1`, `/api/torrents`, `/rss`, or `/torrents/rss` unless the selected adapter defines that path or the user provides it.
- Do not try cookie login with an API token. API tokens, RSS passkeys, cookies, and browser sessions are different auth materials.
- Do not perform a chain of speculative requests after 404, empty response, or redirect-to-login. Stop and ask for the correct access method.
- If the user names a site but does not provide an official API/RSS/Torznab/Prowlarr/Jackett endpoint, ask for one or fall back to `browser_profile` plus a known HTML adapter.
- For site-specific private trackers, only claim direct API support when the host has a named adapter for that exact site or the user provides official API documentation.
- If the user names a known site, query `tracker.site.presets` before choosing a generic adapter. A named preset is stronger evidence than a guessed software family.
- The bundled `site-preset-catalog.json` maps all currently imported PT-depiler site definitions. Use it for name/id/schema resolution before asking the user for raw selectors.
- The bundled `adapter-catalog.json` maps every known `adapterId` to required auth modes, capabilities, and execution strategy.

## Adapter Selection Order

Choose the first matching option:

1. `torznab`: user has a Torznab endpoint from Prowlarr, Jackett, Sonarr/Radarr-compatible indexer, or a tracker-provided Torznab API.
2. `prowlarr`: user wants to configure a Prowlarr server and indexers are already managed there.
3. `jackett`: user wants to configure a Jackett server and indexers are already managed there.
4. `rss`: tracker provides authenticated RSS with passkey/token.
5. `unit3d-api`: tracker exposes Unit3D API/token endpoints.
6. `gazelle-json`: tracker exposes Gazelle JSON/ajax API.
7. `nexusphp`: tracker uses NexusPHP-style pages and no official API is available.
8. `unit3d`: Unit3D HTML fallback when API is unavailable.
9. `gazelle`: Gazelle HTML fallback when JSON API is unavailable.
10. `selector`: last-resort custom DOM selectors.

The host may support only a subset. If a requested adapter is unavailable, emit `capability_unavailable` guidance and fall back to the next safest adapter.

Do not auto-fallback by probing live endpoints. Fallback means asking the user to choose/provide another access method or preparing a different payload for host confirmation.

## Preset Capability

Hosts should expose common adapter presets:

```json
{
  "capability": "tracker.adapter.presets",
  "version": "1.0",
  "confirm": false,
  "payload": {}
}
```

Hosts that support named private tracker definitions should also expose:

```json
{
  "capability": "tracker.site.presets",
  "version": "1.0",
  "confirm": false,
  "payload": {
    "query": "site-a"
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
      "supportsSearch": true,
      "supportsDownload": true,
      "supportsUserStats": true,
      "requiredAuthModes": ["browser_profile", "cookie"]
    }
  ]
}
```

Expected response:

```json
{
  "adapters": [
    { "id": "torznab", "displayName": "Torznab", "supportsSearch": true, "supportsDownload": true },
    { "id": "nexusphp", "displayName": "NexusPHP", "supportsSearch": true, "supportsDownload": true }
  ]
}
```

## Torznab

Best for immediate search/download because it standardizes indexer APIs.

Required user fields:

- `id`
- `displayName`
- `baseUrl`: full Torznab endpoint root, for example `https://prowlarr.example/1/api` or Jackett indexer Torznab URL.
- `apiKeyRef`: secret reference for API key.

Do not construct a Torznab URL from a tracker homepage. The user must provide the Torznab endpoint or a Prowlarr/Jackett indexer URL.

Payload additions:

```json
{
  "adapterId": "torznab",
  "authMode": "api_token",
  "secretRefs": { "apiKey": "secret://trackers/site-a/torznab-api-key" },
  "api": {
    "type": "torznab",
    "searchPath": "",
    "queryParam": "q",
    "apiKeyParam": "apikey",
    "categoryParam": "cat",
    "downloadStrategy": "enclosure-or-link"
  }
}
```

Search behavior:

- Call `?t=search&q=<keyword>&apikey=<resolved>&cat=<optional>`.
- Also support `t=movie`, `t=tvsearch`, `imdbid`, `tvdbid` if host exposes advanced search.
- Parse RSS/Atom items into normalized results.
- Use enclosure URL or item link as internal `downloadRef`; do not expose private URL in logs.

## Prowlarr

Use when user wants one server to manage many indexers.

Required user fields:

- `id`
- `displayName`
- `baseUrl`: Prowlarr base URL.
- `apiKeyRef`.
- Optional `indexerIds` or `indexerNames`.

Payload additions:

```json
{
  "adapterId": "prowlarr",
  "authMode": "api_token",
  "secretRefs": { "apiKey": "secret://prowlarr/api-key" },
  "api": {
    "type": "prowlarr",
    "indexerIds": [],
    "searchPath": "/api/v1/search"
  }
}
```

Search behavior:

- Host calls Prowlarr API and maps indexer results to PT search result shape.
- Preserve source indexer/tracker id when available.
- Download handoff should use host-resolved download URL, not raw logged URL.

## Jackett

Required user fields:

- `id`
- `displayName`
- `baseUrl`: Jackett base URL.
- `apiKeyRef`.
- `indexerId` or `all`.

Payload additions:

```json
{
  "adapterId": "jackett",
  "authMode": "api_token",
  "secretRefs": { "apiKey": "secret://jackett/api-key" },
  "api": {
    "type": "jackett",
    "indexerId": "all",
    "torznabPath": "/api/v2.0/indexers/{indexerId}/results/torznab/"
  }
}
```

Prefer converting Jackett to the Torznab adapter internally.

## RSS

Use when the tracker provides authenticated RSS feeds.

Required user fields:

- `id`
- `displayName`
- `feedUrlRef` or sanitized `feedUrl` without embedded secret.
- `secretRefs.rssKey` when the RSS key is separate.

Payload additions:

```json
{
  "adapterId": "rss",
  "authMode": "rss_token",
  "secretRefs": { "rssKey": "secret://trackers/site-a/rss-key" },
  "api": {
    "type": "rss",
    "feedUrlRef": "secret://trackers/site-a/rss-url",
    "downloadStrategy": "enclosure-or-link"
  }
}
```

If the RSS URL contains a passkey/token, store the whole URL as a secret reference. Do not persist or print it.

Do not guess RSS paths. NexusPHP-like sites often have RSS, but the actual URL and key format are site-specific.

## Unit3D API

Required user fields:

- `id`
- `displayName`
- `baseUrl`
- `apiTokenRef`

Payload additions:

```json
{
  "adapterId": "unit3d-api",
  "authMode": "api_token",
  "secretRefs": { "apiToken": "secret://trackers/site-a/unit3d-token" },
  "api": {
    "type": "unit3d",
    "searchPath": "/api/torrents/filter",
    "downloadPathTemplate": "/api/torrents/{id}/download"
  }
}
```

If the host cannot confirm the site's API paths, run `tracker.health_check` before claiming it is usable.

If API paths return 404 or redirect to login, stop. Ask the user whether the site exposes an API and request its documentation or switch to browser profile.

## Gazelle JSON

Required user fields:

- `id`
- `displayName`
- `baseUrl`
- `authMode`: usually `browser_profile`, `cookie`, or tracker-specific API token.

Payload additions:

```json
{
  "adapterId": "gazelle-json",
  "authMode": "browser_profile",
  "profileRef": "profile://trackers/site-a",
  "api": {
    "type": "gazelle-json",
    "ajaxPath": "/ajax.php",
    "searchAction": "browse",
    "downloadAction": "download"
  }
}
```

Gazelle variants differ. Host should validate with health check and fixture tests.

## NexusPHP HTML/API Fallback

Use when no official API or Torznab bridge exists. This is primarily an authenticated HTML adapter, not proof that a standard API exists.

For named NexusPHP-like sites, use a host-supported site preset when available: `sitePresetId=site-a`, `schemaId=nexusphp`, and compatible `authMode`. If no named preset exists, present the user with the options in `pt-depiler-patterns.md` instead of trying endpoints.

Required user fields:

- `id`
- `displayName`
- `baseUrl`
- `authMode` and auth reference.

Payload additions:

```json
{
  "adapterId": "nexusphp",
  "authMode": "browser_profile",
  "profileRef": "profile://trackers/site-a",
  "search": {
    "path": "/torrents.php",
    "keywordParam": "search",
    "extraParams": { "notnewword": "1" },
    "categoryParam": "cat",
    "selectors": {
      "rows": "table.torrents:last > tbody > tr",
      "title": "a[href*='details.php?id='][title], a[href*='hit'][title]",
      "detailLink": "a[href*='details.php?id=']",
      "downloadLink": "a[href*='download.php?id=']",
      "size": "header-inferred-or-site-override",
      "seeders": "header-inferred-or-site-override",
      "leechers": "header-inferred-or-site-override",
      "completed": "header-inferred-or-site-override"
    }
  },
  "download": {
    "template": "/download.php?id={id}"
  }
}
```

For NexusPHP-like sites:

- Use `browser_profile` or cookie secret references for HTML search.
- Use DOM selectors and named-site overrides; do not parse whole pages with regular expressions.
- Treat RSS/passkey as a separate adapter only when the user provides the RSS feed URL or key reference.
- Do not use `api_token` for web login unless the site documentation says so.
- If redirected to login, report `auth_required` and ask for profile/cookie setup; do not keep trying alternate API paths.

## Immediate Search After Setup

After `tracker.config.create` succeeds:

1. Run `tracker.health_check` if host supports it.
2. If the original user intent was search, ask for confirmation to resume with the original keyword or run immediately if the user already confirmed.
3. Use the adapter's native API/search method rather than asking for selectors again.
4. If health check fails, report the specific missing item: auth, endpoint, adapter unsupported, selector drift, proxy, or rate limit.
5. If the configured adapter endpoint returns 404, empty response, or login redirect, stop and ask for corrected endpoint/auth. Do not try a different adapter silently.

## Immediate Download After Search

After search results return:

1. Ask the user to choose a result if no clear result was selected.
2. If no downloader exists, start downloader setup.
3. Confirm category/label, save path, tags, and paused/start state.
4. Emit `downloader.add` with `resultId`, not raw private URL.

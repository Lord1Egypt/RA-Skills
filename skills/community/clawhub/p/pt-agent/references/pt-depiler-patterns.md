# PT-depiler Pattern Reference

Use this reference when the user asks how mature open-source PT tools handle common sites, or when implementing support for named private trackers. This captures the relevant architecture pattern from PT-depiler without copying private secrets or requiring this skill to become a browser extension.

For actual site id/name/schema mapping, load `site-preset-catalog.json`. It contains 295 PT-depiler-derived site preset records with minimal metadata only.

## Contents

- Key Pattern
- Catalog Coverage
- Named NexusPHP Site Example
- NexusPHP Schema Behavior
- Search And Download Flow
- Preset Resolution
- Storage Boundary
- Stop Conditions

## Key Pattern

PT-depiler does not discover private tracker APIs by probing. It uses explicit site metadata:

- A named site definition such as `site-a` declares `id`, `name`, aliases, type, schema, URLs, tags, capabilities, and site-specific overrides.
- Common tracker software is implemented as reusable schemas such as `NexusPHP`; named sites inherit the schema and override only what differs.
- The runtime creates a site instance from the named metadata plus user config, then calls site methods such as search, detail parsing, user stats, and torrent download link generation.
- Account/user-info collection is a first-class site operation, not a UI afterthought. After auth succeeds, the site instance can read normalized user stats such as upload, download, ratio, bonus, seeding, messages, warnings, and HnR state when the schema supports it.
- User config is separate from site metadata. Stored user config includes URL/profile/cookie settings, enable flags, search permissions, rate limits, download interval, and merge overrides.
- Downloaders are separate records. Download flow resolves a selected torrent through the site instance, fetches `.torrent` using that site's authenticated request config, and only then sends it to qBittorrent/Transmission or another client.
- Search snapshots/history and download history are stored separately from tracker definitions.

For this skill, the equivalent is a host capability model:

```json
{
  "sitePresetId": "site-a",
  "schemaId": "nexusphp",
  "userConfig": {
    "baseUrl": "https://example.invalid",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a",
    "enabled": true
  }
}
```

The bundled `scripts/pt_runtime.py` implements a minimal direct version of this model for agents without native host tools: schema defaults are kept in code, tracker requests run login-like response checks, search rows normalize into opaque result objects, user-info parsing returns sanitized stats, and qBittorrent owns its own login/session/status/add flow.

## Catalog Coverage

`site-preset-catalog.json` maps all PT-depiler site definitions available when this skill was updated:

- Total site presets: 295.
- Major schemas: `NexusPHP`, `Unit3D`, `Gazelle`, `GazelleJSONAPI`, `AvistazNetwork`, `Luminance`, `TNode`, `AbstractPrivateSite`, and custom site classes.
- Each entry contains `id`, `displayName`, `aka`, `schemaId`, `adapterId`, `type`, `tags`, `supportedCapabilities`, `status`, and `sourceFile`.
- The catalog intentionally does not include cookies, passkeys, passwords, torrent URLs, downloaded torrent files, or credential-bearing endpoints.
- `adapter-catalog.json` maps every `adapterId` used by the site catalog to a host execution contract.

Hosts should use this catalog for name resolution and preset selection. Runtime support still requires the host to implement the relevant schema adapter. For example, a host that implements `nexusphp` can support the mapped NexusPHP sites through their preset metadata plus user-provided auth/profile config.

## Named NexusPHP Site Example

In PT-depiler, a named private site preset can inherit the shared `NexusPHP` schema and add only that site's identity, aliases, official group pattern, user-info tweaks, and level requirements. This reference uses `site-a` as a sanitized placeholder; agents should substitute the actual resolved preset from `site-preset-catalog.json` only after the user names a site or saved config supplies one.

Implications for agents:

- If a user names a site, ask the host for `tracker.site.presets`.
- If the host returns a supported preset, use the returned `sitePresetId` and `schemaId`.
- Ask the user for a login method that matches the HTML schema: usually `browser_profile` or `cookie` secret reference.
- Do not assume the site has Unit3D API, generic `/api/v1`, or RSS based only on a token.
- If the user has an `api_token`, ask which integration issued it. It might be Prowlarr/Jackett/Torznab, RSS/passkey, or something unsupported by the host.

### Named Site Authentication

If a mapped preset does not define a login request, API token flow, passkey auth flow, or RSS auth flow, it authenticates exactly like the inherited `NexusPHP` HTML schema:

- The browser extension or host profile issues authenticated HTTP/XHR requests to the site's base URL.
- The active browser cookie jar supplies the site session cookies.
- User config can override URL, timeout, enabled flags, and download link appendix, but the preset itself does not ask for username/password/API token unless it declares that auth mode.
- Login state is detected by `AbstractPrivateSite.loggedCheck`: 401/403/502/504, redirect/response URL containing login-like paths, refresh-to-login headers, configured no-login selectors, or short login-like responses are treated as not logged in.
- Torrent download uses the parsed or generated NexusPHP download link, usually `download.php?id=<torrentId>`, and fetches it with the same authenticated session.

For cross-agent hosts, model this as:

```json
{
  "sitePresetId": "site-a",
  "schemaId": "NexusPHP",
  "adapterId": "nexusphp",
  "authMode": "browser_profile",
  "profileRef": "profile://trackers/site-a"
}
```

or, when the host uses a secret store for cookies:

```json
{
  "sitePresetId": "site-a",
  "schemaId": "NexusPHP",
  "adapterId": "nexusphp",
  "authMode": "cookie",
  "secretRefs": {
    "cookie": "secret://trackers/site-a/cookie"
  }
}
```

If the user provides `api_token` for a NexusPHP HTML preset that does not declare API auth, respond with `auth_material_mismatch` or a clear message that the credential is not accepted. Ask for `profileRef` or cookie `secretRef`, or ask for the separate Prowlarr/Jackett/Torznab/RSS endpoint if the token belongs to a bridge.

If a mapped-site request returns login/unauthorized, return `auth_required`. Do not try `/api`, `/api/v1`, RSS, Unit3D, or passkey endpoints unless the user provides separate official documentation or a bridge endpoint.

This validation rule applies to all mapped sites: resolve the mapped adapter first, validate the credential type against that adapter, and reject incompatible credentials before saving.

Correct named-site setup payload shape:

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
    "baseUrl": "https://tracker.example",
    "adapterId": "nexusphp",
    "authMode": "browser_profile",
    "profileRef": "profile://trackers/site-a",
    "enabled": true,
    "rateLimit": { "minIntervalMs": 3000, "concurrency": 1 }
  }
}
```

If the host does not support the named preset, say so and ask the user to choose one of:

- Provide a Prowlarr/Jackett/Torznab endpoint and API key reference.
- Provide an official RSS feed URL/key reference.
- Use a generic `nexusphp` HTML adapter with an authenticated browser profile/cookie secret.
- Install or enable a site preset package that includes that tracker.

## NexusPHP Schema Behavior

A NexusPHP-style preset typically declares:

- Search path: `/torrents.php`.
- Keyword parameter: `search`.
- Common parameters such as `notnewword=1`.
- Download link selector or generator based on `download.php?id=<torrentId>`.
- Detail page pattern such as `/details.php`.
- HTML selectors for title, subtitle, category, publish time, size, seeders, leechers, snatches, tags, discount/freeleech markers, and optional external ids.
- Login/user-info selectors such as links to `userdetails.php`.

These paths are schema metadata, not live-probed guesses. An agent may use them only when the selected adapter/preset declares `schemaId: "nexusphp"` and the user has provided a compatible auth method.

Open-source search model to mirror:

- PT-Plugin-Plus defines a NexusPHP search entry as `/torrents.php?search=$key$&notnewword=1`, uses `/schemas/NexusPHP/getSearchResult.js`, and parses `table.torrents:last` as HTML. It detects login/no-result states before normalizing rows.
- PT-depiler keeps the same idea but moves it into typed site metadata: `search.keywordPath=params.search`, `requestConfig.url=/torrents.php`, `params.notnewword=1`, optional advanced search such as `imdb|... -> search_area=4`, and schema selectors/filters for row fields.
- The parser should build a request from search entry metadata, fetch one authenticated document, locate result rows, infer or apply field selectors, then normalize each torrent into id, title, subtitle, detail ref, download ref, publish time, size, seeders, leechers, completed count, category, status/progress, and tags.
- Generic NexusPHP handles ordinary table layouts by reading header icons/classes for time, size, seeders, leechers, snatches/completed, and category. Named site metadata overrides only the fields that differ.
- For example, HHanClub overrides the generic NexusPHP search selectors with `.torrent-table-sub-info` rows and class-based fields such as `.torrent-title`, `.torrent-info-text-size`, `.torrent-info-text-seeders`, `.torrent-info-text-leechers`, and `.torrent-info-text-finished`. HDFans mostly reuses the generic NexusPHP search behavior and overrides user-info/level metadata.
- Download links come from a parsed `download.php?id=...` link or are generated from a parsed detail id using the schema download template. Raw private URLs remain in memory only; user-visible results use opaque refs.

Do not implement normal search as one-off scripts such as `hhanclub_search.py` or by regular-expression scraping of whole pages. If a site differs from the generic schema, add a site metadata override and fixture-backed parser test.

## Search And Download Flow

Use this flow in host implementations and payload descriptions:

1. `pt.config.summary` checks configured trackers/downloaders.
2. `tracker.site.presets` resolves known site names from host registry or `site-preset-catalog.json`.
3. `tracker.adapter.presets` checks whether the resolved schema adapter is executable in the host.
4. `tracker.config.create` stores user config in host storage with secret/profile references, not raw secrets.
5. `tracker.user_stats` reads the selected site's account page/API with the same authenticated request config and returns normalized account stats when supported.
6. `tracker.search` calls the selected site's adapter/preset and returns normalized results with opaque `resultId` or `downloadRef`.
7. `downloader.add` resolves the selected result through the site adapter, fetches the `.torrent` with authenticated request config, then sends torrent bytes or a magnet to the downloader.
8. The host records sanitized account status and download history: result id, tracker id, downloader id, title, status, timestamps, and redacted request metadata.

For PT-depiler-style hosts, map its user-info operation to this skill's `tracker.user_stats` capability. The output should be normalized before storage; do not persist the source HTML, authenticated profile URL, cookie, or passkey-bearing links.

## Preset Resolution

When the user gives a site name:

1. Match against `id`, `displayName`, and `aka`.
2. Prefer exact id match, then case-insensitive display name, then alias.
3. Return all ambiguous matches and ask the user to choose.
4. If matched, use the mapped `schemaId` and `adapterId`; do not infer a different adapter from the URL or a token.
5. If the mapped adapter is unavailable in the host, report `capability_unavailable` and ask whether to use Prowlarr/Jackett/Torznab/RSS or install the required adapter.

Example response for a resolved named site:

```json
{
  "sitePresetId": "site-a",
  "displayName": "Site A",
  "schemaId": "NexusPHP",
  "adapterId": "nexusphp",
  "supportedCapabilities": ["search", "download_torrent", "user_stats"]
}
```

## Storage Boundary

The skill does not store anything. Host runtimes should store:

- Tracker user configs in a secure config store.
- Secret material in a secret store, referenced by `secret://`, `env://`, or host-native references.
- Browser sessions in isolated profile refs such as `profile://trackers/site-id`.
- Downloaders in config storage with credential references.
- Sanitized tracker account snapshots, separate from tracker configs.
- Search snapshots and download history separately, with private URLs redacted or represented by opaque references.

When users ask "where are my sites/downloaders stored?", answer: in the host application's storage or the resolved local fallback store, not in this skill. Then identify the specific host if known, such as Codex state, Hermes storage, OpenClaw config storage, an MCP server database, or the `store` path reported by `python3 "$SKILL_ROOT/scripts/pt_store.py" summary`.

## Stop Conditions

Stop and ask for corrected configuration when:

- A named site preset is unavailable.
- The selected adapter's declared endpoint returns 404 or an unexpected response shape.
- A request redirects to login.
- The user provides an auth material that does not match the adapter, such as `api_token` for a cookie-only HTML adapter.
- Search returns empty and there is evidence of auth/endpoint mismatch rather than a legitimate no-results response.

Do not switch to another endpoint family automatically.

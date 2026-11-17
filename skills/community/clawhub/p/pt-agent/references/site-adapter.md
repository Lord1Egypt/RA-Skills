# Site Adapter Reference

Use this reference when adding user-configurable PT sites, debugging tracker adapters, parser fixtures, or search/detail extraction. For common API/schema adapters such as Torznab, Prowlarr, Jackett, RSS, Unit3D API, Gazelle JSON, and NexusPHP, read `common-site-apis.md` first. For named private site presets and PT-depiler-style schema inheritance, read `pt-depiler-patterns.md`.

## Contents

- Adapter Contract
- User-Defined Site Flow
- Endpoint Discipline
- Parsing Guidelines
- Search Aggregation
- Result Selection And Download Reference
- Selector Drift Debugging

## Adapter Contract

Each tracker adapter should define:

- Stable `id`, display name, and `baseUrl`.
- Required auth mode: browser cookie, RSS/API token, passkey download URL, or manual login.
- Supported capabilities: search, detail parse, torrent download, user stats.
- Category mapping from human labels to tracker query values.
- Search URL builder with keyword, category, page, sort, and discount filters.
- Result row parser with title, detail URL, download URL, size, seeders, leechers, snatches, publish time, category, tags, and discount state.
- Detail parser for description, media ids, file list, screenshots, technical metadata, and comments only when needed.
- Login detector and banned/warning/maintenance detector.
- Per-site rate limit and concurrency defaults.
- Native API metadata when available, such as Torznab, RSS, Unit3D API, or Gazelle JSON paths.
- Optional `sitePresetId` and `schemaId` when the host supports named site definitions.

## User-Defined Site Flow

Support two levels of customization:

- Declarative adapter: user supplies base URL, URL templates, category map, selectors, and auth mode.
- Code adapter: contributors add parser functions when a site requires custom normalization or dynamic behavior.

Validate a user-defined site before enabling it:

1. Confirm base URL is reachable through the intended profile/proxy.
2. Confirm login detector returns authenticated, login-required, or unknown.
3. Run a test search against a user-provided harmless keyword.
4. Parse at least one result or return a clear empty-state result.
5. Redact any captured HTML before storing a fixture.

## Endpoint Discipline

Never add adapter logic by guessing live private tracker endpoints. An adapter may use only:

- Documented official API/RSS/Torznab endpoints supplied by the user or host preset.
- Host-supported named adapters with known request paths.
- Browser-profile or cookie-authenticated HTML pages explicitly configured by the adapter.

On `404`, empty response, or redirect-to-login:

1. Stop the request chain.
2. Classify the error: wrong endpoint, auth required, unsupported adapter, or selector drift.
3. Ask for the corrected endpoint/auth reference or switch to a confirmed adapter.
4. Do not silently try another unrelated endpoint family.

Known-site adapters should be written as explicit metadata, not runtime guesses:

- Shared schema metadata for software families such as NexusPHP.
- Named site metadata for exact trackers, with only site-specific overrides.
- User config merged at runtime, including URL, enabled flags, profile/cookie refs, rate limits, and download interval.

When importing a large open-source site list, keep a minimal catalog separate from executable adapter code. This skill's `site-preset-catalog.json` is that catalog: it maps site names to schema adapters, but does not include secrets or live request execution.

Adapter execution contracts belong in `adapter-catalog.json` and `adapter-implementation.md`. Do not duplicate full adapter behavior in individual message examples.

## Parsing Guidelines

- Parse HTML with a DOM parser, not regular expressions.
- Non-browser hosts should provide a real DOM/HTML parser such as BeautifulSoup/lxml, Cheerio, linkedom, parse5, or an equivalent structured parser. If no parser is available, use only a narrow built-in parser fallback and report `selector_drift` when rows cannot be normalized; do not claim success from broad regular-expression matches.
- Normalize sizes into bytes, dates into ISO strings when possible, and ratio/freeleech markers into explicit enum values.
- Keep raw page HTML out of logs. Store sanitized parser fixtures only.
- Make selectors narrow enough to avoid accidental matches, but include fallback selectors for common tracker theme variants.
- Do not scrape more pages than required for the user's current query.

For NexusPHP HTML search, follow the PT-depiler/PT-Plugin-Plus pattern:

1. Build the request from schema/search-entry metadata, typically `/torrents.php` with `search=<keyword>` and `notnewword=1`.
2. Fetch with the authenticated browser profile or cookie secret and check login/no-results before parsing.
3. Parse result rows with DOM selectors. For default tables, infer column indexes from header icons/classes such as time, size, seeders, leechers, snatched/completed, and category.
4. Apply named-site selector overrides when the preset declares them, such as HHanClub's `.torrent-table-sub-info` row layout.
5. Extract normalized fields from row elements, not from whole-page regular expressions: title, subtitle, detail link, download link, size, seeders, leechers, completed, publish time, category, tags, progress/status, and external ids when present.
6. Generate a download ref from `download.php?id=<id>` only after a detail/download id was parsed from the authenticated result row.
7. If authenticated HTML loads but expected rows or required fields cannot be parsed, return `selector_drift` or `parse_failed` and ask for a sanitized DOM fragment/fixture.

## Search Aggregation

For cross-site search:

- Run per-site searches with bounded concurrency.
- Return partial results when one tracker fails.
- Include a per-result `sourceTrackerId`.
- De-duplicate by normalized title plus size, but keep source-specific download links.
- Preserve tracker-specific requirements such as wait time, HnR flags, and freeleech labels.
- Keep enough per-result source metadata to fetch the selected torrent later without exposing private URLs in UI logs.

## Result Selection And Download Reference

Search results should distinguish:

- `detailUrl`: safe enough to display only after redaction rules are applied.
- `downloadRef`: opaque internal reference or sanitized path used by `TorrentFetchService`.
- `downloadUrl`: raw private URL, allowed only in memory during the authenticated fetch step.

Never persist raw private download URLs with passkeys. Persist opaque IDs, normalized titles, sizes, and sanitized source tracker IDs instead.

## Selector Drift Debugging

When parsing starts failing:

1. Verify login state first.
2. Capture a sanitized page snapshot.
3. Compare the failing selector against the current DOM.
4. Update the smallest adapter-specific selector.
5. Add or update a fixture test for the changed markup.

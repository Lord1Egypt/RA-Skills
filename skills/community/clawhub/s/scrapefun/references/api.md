# API Reference

Base URL for this skill:

- `http://localhost:4000`

## Authentication

### Preferred: OpenClaw access key

Use this header on protected endpoints:

```http
X-OpenClaw-Key: <access key>
```

Rules:

- Use `OPENCLAW_ACCESS_KEY` or the saved skill key
- Do not use `OPENCLAW_SCRAPEFUN_API_KEY`
- Do not use `X-OpenClaw-Api-Key`

### Fallback: Admin login

- `POST /api/auth/login`

Use the returned token on later protected requests:

```http
Authorization: Bearer <token>
```

## Primary OpenClaw Endpoints

### Library catalog

- `GET /api/openclaw/libraries/catalog`
- Permission: `library_query`

Required query:

- `libraryId` or `libraryName`

Optional query:

- `q`
- `page`
- `pageSize`

Use this for:

- listing media entries in a library
- resolving `metadataId` before later media calls

Do not use `GET /api/metadata` or `GET /api/metadata/stats` for this.

### Media state

- `GET /api/openclaw/media/:metadataId/state`
- Permission: `library_query`

Use this for:

- current files
- existing episodes
- missing episodes
- `nextMissingEpisode`

### Download target

- `GET /api/openclaw/media/:metadataId/download-target`
- Permission: `download_target_query`

Use this for:

- `seriesRootPath`
- `seasonPath`
- `downloadPath`
- `storage`
- `alreadyComplete`

### Download check

- `POST /api/openclaw/media/:metadataId/download-check`
- Permission: `download_dedupe`

Minimum payload:

```json
{}
```

Optional payload:

```json
{
  "seasonNumber": 1,
  "episodeNumber": 1,
  "candidateName": "Episode 01",
  "candidateSize": 1234567890,
  "strictEpisodeMatch": true
}
```

Use this before every download submission.

Possible results:

- `already_bound`
- `already_landed`
- `missing`
- `ambiguous`

### Download submit

- `POST /api/openclaw/downloads/submit`
- Permission: `download_submit`

Minimum payload:

```json
{
  "metadataId": "<metadataId>",
  "magnet": "<magnet>"
}
```

or:

```json
{
  "metadataId": "<metadataId>",
  "urls": ["<url>"]
}
```

Optional payload:

```json
{
  "preferredPath": "/Quark/媒体库/动漫/Series/Season 01",
  "seasonNumber": 1,
  "episodeNumber": 1,
  "candidateMeta": {
    "title": "Episode 01",
    "size": 1234567890,
    "source": "mikanani",
    "publishedAt": "2026-03-16T00:00:00Z"
  }
}
```

Possible results:

- `duplicateDecision = submitted`
- `duplicateDecision = skipped_existing`
- `duplicateDecision = skipped_bound`

### Confirm landed

- `POST /api/openclaw/downloads/:downloadId/confirm-landed`
- Permission: `download_confirm`

Minimum payload:

```json
{
  "metadataId": "<metadataId>"
}
```

Optional payload:

```json
{
  "expectedPath": "/Quark/媒体库/动漫/Series/Season 01",
  "seasonNumber": 1,
  "episodeNumber": 1,
  "waitMs": 15000,
  "forceRefresh": true
}
```

Possible results:

- `landed`
- `not_found`
- `partial`
- `ambiguous`

### Finalize import

- `POST /api/openclaw/media/:metadataId/finalize-import`
- Permission: `import_finalize`

Minimum payload:

```json
{
  "downloadPath": "/Quark/媒体库/动漫/Series/Season 01"
}
```

Optional payload:

```json
{
  "seasonNumber": 1,
  "episodeNumber": 1,
  "matchMode": "auto",
  "forceScan": true,
  "downloadId": "<downloadId>"
}
```

Returns:

- `status`
- `scan`
- `match`
- `postState`
- `boundEpisodes`
- `remainingMissingEpisodes`

### Download workflow status

- `GET /api/openclaw/downloads/:downloadId`
- Permission: `download_status` or one of `download_submit`, `download_confirm`, `import_finalize`

Important:

- `404` here means `Download workflow not found`
- it does not mean the route is unavailable

### Library scan

- `POST /api/openclaw/libraries/scan`
- Permission: `library_scan`

Preferred payload:

```json
{
  "libraryName": "Anime"
}
```

Explicit payload:

```json
{
  "path": "/xunlei/迅雷云盘/媒体库/电影/",
  "scraper": "TMDB",
  "type": "movie"
}
```

Use this only for:

- explicit rescan
- forced refresh when the user asks for it
- best-effort fallback when `finalize-import` is unavailable

If response contains `partial: true`, report the failed root paths explicitly.

## Allowed Narrow Fallback Endpoints

### Raw library config

- `GET /api/libraries`

Use only when the user explicitly asks for raw config fields such as:

- `path`
- `scraper`
- `sourceMode`
- `sourcePreferencesJson`

### Raw scraper candidates

- `GET /api/scrape/search`

Use only when the user explicitly asks for raw scraper candidates.

### Directory-level file listing

- `GET /api/scrape/webdav/list`

Use only when the user explicitly asks for directory-level enumeration detail that OpenClaw endpoints do not return.

## Default Operation Order

### List a library

1. `GET /api/openclaw/libraries/catalog?libraryName=<name>`

### Read a media entry

1. Resolve `metadataId` from `catalog`
2. `GET /api/openclaw/media/:metadataId/state`

### Prepare a download

1. `GET /api/openclaw/media/:metadataId/download-target`
2. `POST /api/openclaw/media/:metadataId/download-check`

### Submit a download

1. `POST /api/openclaw/downloads/submit`

### Continue after submission

1. `POST /api/openclaw/downloads/:downloadId/confirm-landed`
2. `POST /api/openclaw/media/:metadataId/finalize-import`
3. `GET /api/openclaw/downloads/:downloadId`

## Do Not Use In Normal OpenClaw Flows

- `GET /api/metadata`
- `GET /api/metadata/stats`
- `GET /api/settings/webdav/search`
- `POST /api/settings/webdav/add_offline_download`

## Prohibited Endpoints

Do not use:

- `/api/openclaw/bootstrap/status`
- `/api/openclaw/connect/context`
- `/api/openclaw/jobs/*`
- `/api/openclaw/sites/*`
- `/api/openclaw/tasks/*`
- `OPENCLAW_URL` remote delegation flow

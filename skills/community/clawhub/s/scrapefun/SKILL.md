---
name: openclaw-scrapefun
description: "Use this skill when OpenClaw needs to operate a scrapefun server through the dedicated OpenClaw-facing APIs. Prefer /api/openclaw/* query and download endpoints. Use generic scrapefun APIs only for narrow fallback cases."
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🦀",
        "primaryEnv": "OPENCLAW_ACCESS_KEY",
      },
  }
---

# OpenClaw Scrapefun

## Purpose

Use this skill only for `scrapefun` operational APIs.

Default rule:

- Prefer `X-OpenClaw-Key`
- Prefer `/api/openclaw/*`
- Do not silently fall back to `/api/metadata`, `/api/metadata/stats`, `/api/settings/webdav/search`, or `/api/settings/webdav/add_offline_download`
- If an expected `/api/openclaw/*` endpoint returns `404`, `403`, or validation failure, report the exact blocker instead of switching to an old path unless the fallback is explicitly allowed below

This skill does not perform OpenClaw-side resource discovery.

## Auth

Preferred auth:

- Header: `X-OpenClaw-Key: <access key>`

Fallback auth:

- `POST /api/auth/login`
- Reuse `Authorization: Bearer <token>`

Rules:

- Prefer `OPENCLAW_ACCESS_KEY` or the saved skill api key
- Never use `OPENCLAW_SCRAPEFUN_API_KEY`
- State the required OpenClaw permissions before calling `/api/openclaw/*`
- If a permission is missing, stop and report it

## Primary Endpoints

Use these endpoints as the default interface surface:

- `GET /api/openclaw/libraries/catalog`
  Required permission: `library_query`
  Use for listing media entries in a library

- `GET /api/openclaw/media/:metadataId/state`
  Required permission: `library_query`
  Use for existing files, existing episodes, and missing episodes

- `GET /api/openclaw/media/:metadataId/download-target`
  Required permission: `download_target_query`
  Use for target path, season path, storage, and next missing episode

- `POST /api/openclaw/media/:metadataId/download-check`
  Required permission: `download_dedupe`
  Use before every download submission
  Minimum payload: `{}` or `{"seasonNumber":<n>,"episodeNumber":<n>}`
  Optional fields: `candidateName`, `candidateSize`, `strictEpisodeMatch`

- `POST /api/openclaw/downloads/submit`
  Required permission: `download_submit`
  Use for offline download submission
  Minimum payload: `{"metadataId":"<metadataId>","magnet":"<magnet>"}` or `{"metadataId":"<metadataId>","urls":["<url>"]}`
  Optional fields: `preferredPath`, `seasonNumber`, `episodeNumber`, `candidateMeta`

- `POST /api/openclaw/downloads/:downloadId/confirm-landed`
  Required permission: `download_confirm`
  Use to verify landed files after submission
  Minimum payload: `{"metadataId":"<metadataId>"}`
  Optional fields: `expectedPath`, `seasonNumber`, `episodeNumber`, `waitMs`, `forceRefresh`

- `POST /api/openclaw/media/:metadataId/finalize-import`
  Required permission: `import_finalize`
  Use for post-download scan, organize, and verification
  Minimum payload: `{"downloadPath":"<webdav path>"}`
  Optional fields: `seasonNumber`, `episodeNumber`, `matchMode`, `forceScan`, `downloadId`

- `GET /api/openclaw/downloads/:downloadId`
  Required permission: `download_status` or one of `download_submit`, `download_confirm`, `import_finalize`
  Use for compact workflow status

- `POST /api/openclaw/libraries/scan`
  Required permission: `library_scan`
  Use only for explicit rescan or forced refresh

## Default Operation Order

Use these sequences.

### 1. List a library

1. `GET /api/openclaw/libraries/catalog?libraryName=<name>`

Do not use:

- `GET /api/metadata`
- `GET /api/metadata/stats`

### 2. Read a show's current state

1. Resolve `metadataId` from `catalog`
2. `GET /api/openclaw/media/:metadataId/state`

Do not use:

- `GET /api/metadata`

### 3. Prepare a download

1. `GET /api/openclaw/media/:metadataId/download-target`
2. `POST /api/openclaw/media/:metadataId/download-check`

Do not manually combine:

- `/api/libraries`
- `/api/settings/webdav/storage/resolve`
- `/api/settings/webdav/search`

unless the fallback rules below explicitly allow it

### 4. Submit a download

1. `POST /api/openclaw/downloads/submit`

Do not call:

- `POST /api/settings/webdav/add_offline_download`

directly from this skill

### 5. Continue after submission

1. `POST /api/openclaw/downloads/:downloadId/confirm-landed`
2. `POST /api/openclaw/media/:metadataId/finalize-import`
3. `GET /api/openclaw/downloads/:downloadId`

Do not manually combine:

- `GET /api/scrape/webdav/list`
- `POST /api/scrape/webdav/scan`
- `POST /api/scrape/match`

as the default path

## Endpoint Availability Checks

Before relying on a path in your answer, treat these failures distinctly:

- `404`: endpoint not available on this server version
- `403`: missing OpenClaw permission
- `400`: required parameters missing or invalid

Rules:

- If `catalog`, `state`, `download-target`, `download-check`, `downloads/submit`, `confirm-landed`, or `finalize-import` returns `404`, say the server does not expose that OpenClaw endpoint
- If `GET /api/openclaw/downloads/:downloadId` returns `404`, report `Download workflow not found`; do not describe it as route absence
- If one of them returns `403`, report the exact missing permission and stop
- Do not describe a legacy fallback as if it were equivalent
- If `POST /api/openclaw/libraries/scan` returns `partial: true`, report the failed library root paths explicitly

## Strict Fallback Rules

Fallback is allowed only in these cases.

### Allowed fallback

- `GET /api/libraries`
  Use only when the user explicitly asks for raw library config fields such as `path`, `scraper`, `sourceMode`, or `sourcePreferencesJson`

- `GET /api/scrape/search`
  Use only when the user explicitly asks for raw scraper candidates

- `GET /api/scrape/webdav/list`
  Use only when the user explicitly asks for directory-level file enumeration detail that the OpenClaw endpoints do not return

- `POST /api/openclaw/libraries/scan`
  Use only when the user explicitly wants a scan or when `finalize-import` is unavailable and the user still wants a best-effort refresh

### Disallowed fallback

- Do not fall back to `GET /api/metadata` for library listing
- Do not fall back to `GET /api/metadata` for missing episode detection
- Do not fall back to `GET /api/metadata/stats` for media browsing
- Do not fall back to `POST /api/settings/webdav/add_offline_download` for normal download submission
- Do not fall back to `GET /api/settings/webdav/search` for normal landed-file checks

## Prohibited Endpoints

Do not use:

- `/api/openclaw/bootstrap/status`
- `/api/openclaw/connect/context`
- `/api/openclaw/jobs/*`
- `/api/openclaw/sites/*`
- `/api/openclaw/tasks/*`
- `OPENCLAW_URL` remote delegation flow

## Response Rules

Keep responses functional only.

Always state:

- auth method
- endpoint
- required permission
- payload shape
- returned result or blocker

Do not add product commentary or discovery-side explanation unless it is required to explain a blocker.

## Examples

### View Anime entries

User request:

`把 Anime 里的媒体条目发给我看看`

Execution:

1. `GET /api/openclaw/libraries/catalog?libraryName=Anime`

### Check episodes

User request:

`芙莉莲现在有哪些集，缺哪些集`

Execution:

1. Find `metadataId` from `catalog`
2. `GET /api/openclaw/media/:metadataId/state`

### Submit magnet

User request:

`这个 magnet 下载到对应番剧目录`

Execution:

1. `GET /api/openclaw/media/:metadataId/download-target`
2. `POST /api/openclaw/media/:metadataId/download-check`
3. `POST /api/openclaw/downloads/submit` with `metadataId` and `magnet` or `urls`

### Continue after download

User request:

`下载完成后继续扫出来`

Execution:

1. `POST /api/openclaw/downloads/:downloadId/confirm-landed` with `metadataId`
2. `POST /api/openclaw/media/:metadataId/finalize-import` with `downloadPath`
3. `GET /api/openclaw/downloads/:downloadId`

### Raw library config

User request:

`Anime 的路径和 scraper 是什么`

Execution:

1. `GET /api/libraries`
2. Return only the matched library's `path`, `type`, `sourceMode`, `scraper`, and `sourcePreferencesJson`

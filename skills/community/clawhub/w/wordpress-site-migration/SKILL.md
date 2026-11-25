---
name: wordpress-site-migration
description: Move a whole WordPress site's content as a migration ZIP and sync Media Library files between sites or from an uploads folder using the Import Export plugin abilities (rsl-ie/migration-*, media-*, sync-media-*). Use for site moves, staging refreshes, and bulk media transfers or duplicate checks.
license: GPL-2.0-or-later
---

# WordPress migration and media sync (rsl-ie abilities)

REST: `POST /wp-json/wp-abilities/v1/abilities/rsl-ie/<name>/run` `{"input":{...}}`; read-only abilities via `GET ?input[...]`.

## Migration ZIP (export on source, import on target)

Source site:
1. `migration-plan` → authorized steps in dependency order (PRO adds more families).
2. `migration-start {operation:"export_file", steps:[{key, selected_ids?}], request_id}` → `job_id`.
3. `migration-get {job_id}` until complete; `file-get {job_id}` returns the ZIP download URL and checksum.

Target site:
4. Upload the ZIP (`upload-from-url` or chunked `upload-create`/`upload-chunk`/`upload-complete`) → `file_id`.
5. `migration-prepare {file_id}` → validates `manifest.json` and lists step keys.
6. `migration-import-start {file_id, sha256, request_id, steps?, duplicate_handling: skip|update, download_media, replace_links_rules}`. `replace_links_rules` rewrites old-domain URLs.
7. `migration-get` until complete; `job-errors` for failures. `migration-pause|resume|cancel` control it.

## Media

- Between connected sites: `sync-media-browse` → `sync-media-push-start` / `sync-media-pull-start` (1–50 `media_ids`; push ids are local, pull ids are the peer's) → `sync-job-status`.
- From a folder already inside `wp-content/uploads`: `media-browse-folders` → `media-scan-folder {folder_path}` → `media-sync-start {folder_path, selected_files, sync_options:{duplicate_check: hash, duplicate_handling: skip}}` → `media-sync-status {job_id}`.
- Duplicates: `media-hash-stats`, `media-hash-build`, `media-check-duplicate {hash|file_path|attachment_id}`.

## Rules

- Migration import writes lots of content: confirm target site, `duplicate_handling` and a fresh backup with the user first.
- Compare counts on both sides after import (posts, pages, media).
- Keep `request_id` the same only when retrying the identical request.
- Do not print or store the ZIP's contents, site keys or credentials in the chat.

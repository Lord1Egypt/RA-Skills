---
name: wordpress-content-sync
description: Sync WordPress posts, pages, ACF fields, comments and media between two sites through the Content Sync, Media Sync, Import, Export plugin Abilities API (rsl-ie/*). Use when the user asks to push, pull, copy or update content between a staging/production or any two connected WordPress sites without export files.
license: GPL-2.0-or-later
---

# WordPress Content Sync (rsl-ie abilities)

Requires the free plugin "Content Sync, Media Sync, Import, Export with AI Agents Support" (`import-export-by-rockstarlab`) on BOTH sites, WordPress 6.9+ Abilities API, and an administrator application password or the MCP Adapter. Products, CPTs, WooCommerce: see `woocommerce-sync-pro`.

Call abilities through the MCP Adapter, or REST: `POST /wp-json/wp-abilities/v1/abilities/rsl-ie/<name>/run` with `{"input":{...}}`. Read-only abilities use `GET` with `?input[key]=value`.

## Workflow

1. `rsl-ie/get-capabilities` (check plugin version, abilities available).
2. `rsl-ie/connection-list` → pick `site_id` of the target. If none: `connection-create` needs the other site's incoming key (`site-key-status` / `site-key-reveal` on that site; reveal only on explicit user request, never print the key). Verify with `connection-test`.
3. Choose records: `sync-browse` (remote), `sync-search-local`, or ids given by the user. `post_type` is `post` or `page` in the free plugin.
4. Inspect: `sync-local-info` (`post_type`, `post_ids` ≤50) shows what exists and original ids.
5. Optional mapping to update existing content instead of creating copies: `sync-auto-map` (exact normalized title match) and pass the result as `post_mapping`. Show the user what will be updated before running.
6. Start: `sync-push-start` (local → remote) or `sync-pull-start` (remote → local). Required: `site_id`, `post_type`, `post_ids` (1–50), `request_id` (unique string; reuse the SAME value only when retrying the same request, it deduplicates).
   - Posts with ACF image/gallery fields: set `acf_media_references: true`.
   - Hierarchies: pass `hierarchy` so parents map correctly.
7. Poll `sync-job-status` (`job_id`) until done. Runs on WP-Cron, so a long wait on a low-traffic site is normal; do not start a second job. Details afterwards: `sync-result` (source/target/media id maps, works after HTTP timeouts).
8. Verify on the target: `sync-browse` or open the returned target ids; compare titles, status, featured image, ACF values on a sample.

Comments: `sync-comments-browse`, then `sync-comments-push-start` / `sync-comments-pull-start` (≤50 ids). Media only: `sync-media-browse`, `sync-media-push-start` / `sync-media-pull-start`.

## Rules

- These calls write to the destination site. Confirm direction (which site is overwritten) and the list of records with the user before starting, unless they already stated both.
- ≤50 records per job; split larger sets into batches and run them one after another.
- Never retry blindly after an error: check `sync-job-status`/`sync-result` first, since the job may have finished.
- `sync-job-pause`, `sync-job-resume`, `sync-job-cancel` control running jobs. Completed changes are not rolled back by cancel.
- Synchronous `sync-push` / `sync-pull` exist but may hit HTTP timeouts; prefer the `-start` versions.
- Take a backup of the destination before overwriting existing content.

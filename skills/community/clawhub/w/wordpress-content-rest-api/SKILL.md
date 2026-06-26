---
name: wordpress-content-rest-api
description: Use the WordPress REST API for content operations only: auth setup (Application Password and Bearer), safe read/write flows for posts/pages/media, draft/publish/update patterns, taxonomy assignment, pagination/search, retry/rate-limit handling, and dry-run-first safety.
metadata: {"openclaw":{"emoji":"🧩"}}
---

# WordPress Content REST API

Use this skill only for WordPress content API work (posts, pages, media, categories, tags).

Do not use it for server admin, plugin/theme management, or shell/WP-CLI tasks.

## Safety Rules (Always)

1. Start with a dry run before any write.
2. Confirm base URL and target environment (`production` vs `staging`).
3. Read current object first, then patch minimally.
4. Prefer `status=draft` until explicit approval to publish.
5. Avoid bulk destructive updates unless explicitly approved.
6. Use least-privilege credentials.

Read [references/reliability-and-safety.md](references/reliability-and-safety.md) first when operating on live sites.

## Workflow

1. Set auth model (Application Password or Bearer):
   [references/auth.md](references/auth.md)
2. Discover and validate target content:
   use read/list endpoints with pagination and filters.
3. Execute dry-run pass:
   - fetch current object
   - prepare intended payload
   - verify taxonomy/media IDs exist
4. Write safely:
   - create/update as draft first
   - verify response
   - publish only with explicit instruction
5. Handle retries/rate-limits/errors using standard policy:
   [references/reliability-and-safety.md](references/reliability-and-safety.md)

## Endpoint Scope

Focus on these route families:
- `/wp-json/wp/v2/posts`
- `/wp-json/wp/v2/pages`
- `/wp-json/wp/v2/media`
- `/wp-json/wp/v2/categories`
- `/wp-json/wp/v2/tags`

For usage patterns and payload examples, read:
- [references/content-flows.md](references/content-flows.md)
- [references/query-and-taxonomy.md](references/query-and-taxonomy.md)

## Default Execution Pattern

- Read first (`GET`).
- Validate dependent IDs (author/category/tag/media).
- Write to draft (`POST`/`PUT`/`PATCH` with `status=draft`).
- Re-read object and compare expected fields.
- Publish (`status=publish`) only after explicit approval.

## Done Criteria

Treat a content task as complete only when:
- API response is successful and parsed.
- Changed fields match requested outcome.
- Final status (`draft`/`publish`) matches explicit instruction.
- Any partial failures are listed with next action.

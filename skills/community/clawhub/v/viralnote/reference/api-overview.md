# ViralNote API reference

The full machine-readable OpenAPI spec lives at `https://viralnote.app/api/v1/openapi`. This file is a quick lookup for the most common endpoints. When you need precise request bodies or response shapes, fetch the OpenAPI spec or visit `https://viralnote.app/developers/docs`.

## Base URL

```
https://viralnote.app/api/v1
```

## Authentication

```
x-api-key: vnd_...
```

Equivalent: `Authorization: Bearer vnd_...`.

## Endpoints

### Posts

| Method | Path | Purpose |
|---|---|---|
| GET | `/posts` | List posts (paginated, filter by status: draft/scheduled/published/failed) |
| POST | `/posts` | Create a new post (draft or scheduled) |
| GET | `/posts/{postId}` | Read one post |
| PATCH | `/posts/{postId}` | Update a post (caption, scheduled time, platforms, attached media) |
| DELETE | `/posts/{postId}` | Delete a post (cancels if scheduled) |
| POST | `/posts/{postId}/publish` | Publish a draft now |

**Required scope:** `posts:read` for GET, `posts:write` for POST/PATCH/DELETE/publish.

### Media library

| Method | Path | Purpose |
|---|---|---|
| GET | `/media` | List library items (filter by `type=image|video|gif|clip`, paginated) |
| POST | `/media` | Upload a file (multipart/form-data) |
| POST | `/media/import` | Import a file by URL from a third-party source (Dropbox, Canva) |
| DELETE | `/media/{mediaId}` | Delete a library item |

**Required scope:** `posts:write` (the same scope covers media because media is post material).

### Social accounts

| Method | Path | Purpose |
|---|---|---|
| GET | `/social-accounts` | List connected accounts and their platforms |

Connecting/disconnecting accounts happens in the dashboard UI (OAuth flows). The API only reads.

### Webhooks

| Method | Path | Purpose |
|---|---|---|
| GET | `/webhooks` | List webhook subscriptions |
| POST | `/webhooks` | Subscribe to events (e.g. `post.published`, `post.failed`) |
| PATCH | `/webhooks/{webhookId}` | Update a subscription |
| DELETE | `/webhooks/{webhookId}` | Delete a subscription |

### API keys

| Method | Path | Purpose |
|---|---|---|
| GET | `/api-keys` | List the user's API keys (without secret values) |
| POST | `/api-keys` | Create a new key |
| DELETE | `/api-keys/{keyId}` | Revoke a key |

### Other

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check, no auth required |
| GET | `/credits` | Read remaining credit balance |
| GET | `/credits/transactions` | Recent credit activity |
| GET | `/openapi` | The full OpenAPI 3.1 spec (JSON) |

## Pagination

List endpoints return `{ items, count, nextCursor }`. Pass `cursor=<value>` on the next request to get the next page. Pass `limit=<n>` to set page size (max 50, default 20).

## Rate limits

- Default: 60 requests/minute per key
- `/media` upload: 20/min
- `/media/import`: 10/min
- Per-key custom caps can be set at key creation time

On `429`, read `Retry-After` (seconds) and back off.

## Platform IDs

Where the API expects a platform name, use one of:

```
twitter, facebook, instagram, linkedin, reddit, youtube,
bluesky, threads, tiktok, pinterest
```

## Post status values

```
draft, scheduled, publishing, published, failed
```

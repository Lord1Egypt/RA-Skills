# threads-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 1 platform group(s).**

## Threads (10)

### `threads_post`

- **HTTP:** `GET /threads/post/{username}/{code}`
- **What:** Retrieve a public Threads post. Returns one public Threads post by `username` (with or without a leading `@`) and the post `code` from its URL. The response has the post text, canonical URL, preview image URL, and the author's id, name and username. Replies and logged-in fields are not included. An unavailable post returns 404.
- **Params:** `code` (string, **required**) — Threads post code; `username` (string, **required**) — Threads username

### `threads_post_replies`

- **HTTP:** `GET /threads/post/{username}/{code}/replies`
- **What:** Retrieve public replies to a Threads post. Returns the public replies currently exposed to logged-out visitors. The response identifies when Threads reports additional replies but withholds a usable continuation cursor.
- **Params:** `code` (string, **required**) — Threads post code; `username` (string, **required**) — Threads username

### `threads_profile`

- **HTTP:** `GET /threads/profile/{username}`
- **What:** Retrieve a public Threads profile. Returns a public Threads profile by `username` (with or without a leading `@`): name, profile URL, biography, avatar URL, `followers_count` and `threads_count`. Counts are derived from the compact figures shown on the profile page. An unavailable profile returns 404.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_media`

- **HTTP:** `GET /threads/profile/{username}/media`
- **What:** Retrieve public media posts from a Threads profile. Returns the first public page shown on a profile's Media tab. Items include image and video URLs, including carousel attachments, plus post and topic metadata. The logged-out page exposes no continuation cursor or media-type filter; `pagination_limited` reports when additional results are gated by login or lack a supported cursor.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_posts`

- **HTTP:** `GET /threads/profile/{username}/posts`
- **What:** Retrieve public posts from a Threads profile. Lists public posts from the profile's Threads tab by `username`. Each item has its code, URL, text, creation time, image and video URLs, like, reply, repost and quote counts, reply flag and author. When `has_more` is true, pass `next_cursor` unchanged as `cursor` to fetch the next page; `pagination_limited` is true if Threads withholds a usable cursor.
- **Params:** `cursor` (string, optional) — Opaque cursor returned by the previous response; `username` (string, **required**) — Threads username

### `threads_profile_replies`

- **HTTP:** `GET /threads/profile/{username}/replies`
- **What:** Retrieve public items from a Threads profile's Replies tab. Returns the first public page shown on a profile's Replies tab. Each item preserves its actual author and public reply metadata. The logged-out page has no continuation cursor; `pagination_limited` is true when Threads reports more items without a cursor or shows a login wall for additional items.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_reposts`

- **HTTP:** `GET /threads/profile/{username}/reposts`
- **What:** Retrieve public posts reposted by a Threads profile. Returns the first public page shown on a profile's Reposts tab. Each item preserves the original post author and metadata. `pagination_limited` is true when Threads gates more items behind login or reports more items without a supported cursor.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_topics`

- **HTTP:** `GET /threads/profile/{username}/topics`
- **What:** Discover public topic tags on a Threads profile. Returns every topic tag listed on a public profile, including the numeric tag id and canonical `name` to pass as `q` to `/threads/search/topics`. Community topics include their community metadata.
- **Params:** `username` (string, **required**) — Threads username

### `threads_search`

- **HTTP:** `GET /threads/search`
- **What:** Search public Threads posts. Returns the public first page of Threads search results for a query. `sort` supports `top` and `recent`; `pagination_limited` marks the logged-out login wall because search has no continuation cursor. Author and date filters in Threads require login and are not exposed here.
- **Params:** `q` (string, **required**) — Search query (1-100 characters); `sort` (string, optional) — Result order; defaults to top

### `threads_topic_search`

- **HTTP:** `GET /threads/search/topics`
- **What:** Search posts for a public Threads topic tag. Returns the public first page of posts for a topic tag. Discover the required `tag_id` and its canonical query `name` from `/threads/profile/{username}/topics` or a post's `topic` metadata. Topic results have no logged-out continuation cursor; `pagination_limited` marks the login wall for more results.
- **Params:** `q` (string, **required**) — Canonical topic query from a profile topic's `name` or a post topic's `search_query`; `tag_id` (string, **required**) — Numeric Threads topic tag id

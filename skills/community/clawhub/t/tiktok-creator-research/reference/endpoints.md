# tiktok-creator-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## TikTok (5)

### `tiktok_comments`

- **HTTP:** `GET /tiktok/comments`
- **What:** Retrieve TikTok video comments. Returns the top-level comments on a TikTok video, by the video id from its URL (`aweme_id`). Results are paged by cursor: pass the `cursor` from one response to get the next page, and read `has_more` to see whether more remain. The response also carries the total comment count.
- **Params:** `aweme_id` (string, **required**) — TikTok video id from the video URL; `cursor` (integer, optional) — Pagination cursor

### `tiktok_post`

- **HTTP:** `GET /tiktok/post/{id}`
- **What:** Retrieve TikTok video details. Returns TikTok's detail record for one video by video id. `itemInfo.itemStruct` holds the video's description, the author's profile and the author's statistics (such as followers, following and hearts) along with the rest of TikTok's video object; `shareMeta` holds the share title and description.
- **Params:** `id` (string, **required**) — TikTok video id

### `tiktok_posts`

- **HTTP:** `GET /tiktok/posts`
- **What:** Retrieve posts from a TikTok profile. Lists posts from a TikTok profile identified by `secUid`. `sort_type` is `0` latest (default), `1` popular or `2` oldest. `cursor` defaults to 0. The response has `itemList`, `hasMore` and a `cursor` to pass back to fetch the next page.
- **Params:** `cursor` (integer, optional) — Pagination cursor; `secUid` (string, **required**) — TikTok secUid for the profile; `sort_type` (integer, optional) — Sort mode: 0 latest, 1 popular, 2 oldest

### `tiktok_profile`

- **HTTP:** `GET /tiktok/profile/{handler}`
- **What:** Retrieve a TikTok profile. Returns a public TikTok profile by `handler`, the username without the leading `@`. The `user` object has the id, `uniqueId`, nickname, signature, verified and private flags, region, language, avatar, bio link and `secUid`; `stats` has follower, following, heart, video and friend counts. A missing, deleted or banned handle returns 404.
- **Params:** `handler` (string, **required**) — TikTok handle without the leading @

### `tiktok_search_user`

- **HTTP:** `GET /tiktok/search/user`
- **What:** Search TikTok users. Searches TikTok users for `keyword`, with `cursor` (default 0) for paging. The response has `user_list` with the matching accounts, plus a `cursor` and `has_more` to continue. Pass the returned `cursor` back to fetch the next page.
- **Params:** `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword

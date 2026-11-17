# youtube-content-gap-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 1 platform group(s).**

## YouTube (9)

### `youtube_channel_search`

- **HTTP:** `GET /youtube/channel/{id}/search`
- **What:** Search within a YouTube channel. Searches the videos of one YouTube channel for the required `q`. `id` accepts a channel id, `@handle`, `/c` or `/user` path, or a full channel URL. Items carry the video id, title, URL, duration, view count, published text and thumbnail, and the response echoes the resolved `query`. Page with `continuation_token`.
- **Params:** `continuation_token` (string, optional) — Pagination token returned by a previous request; `id` (string, **required**) — Channel ID, @handle, /c path, /user path, or full YouTube channel URL; `q` (string, **required**) — Search query

### `youtube_channel_shorts`

- **HTTP:** `GET /youtube/channel/{id}/shorts`
- **What:** Retrieve the shorts tab for a YouTube channel. Returns one page of Shorts from a YouTube channel's Shorts tab. `id` accepts a channel id, `@handle`, `/c` or `/user` path, or a full channel URL. Each short has its position within this page, video id, title, URL, thumbnail and view count text. Pass `continuation_token` from the response to fetch the next page.
- **Params:** `continuation_token` (string, optional) — Opaque pagination token returned by the previous response; `id` (string, **required**) — Channel ID, @handle, /c path, /user path, or full YouTube channel URL

### `youtube_channel_videos`

- **HTTP:** `GET /youtube/channel/{id}/videos`
- **What:** Retrieve the videos tab for a YouTube channel. Lists the videos on a YouTube channel's Videos tab. `id` accepts a channel id, `@handle`, `/c` or `/user` path, or a full channel URL. Each item has its video id, title, URL, duration, view count, published text, thumbnail, badges and live flag. Pass the returned `continuation_token` to fetch the next page.
- **Params:** `continuation_token` (string, optional) — Pagination token returned by a previous request; `id` (string, **required**) — Channel ID, @handle, /c path, /user path, or full YouTube channel URL

### `youtube_comments`

- **HTTP:** `GET /youtube/comments/{id}`
- **What:** Retrieve top-level video comments. Returns one page of top-level comments for a YouTube video by its 11-character `id`. Each comment has its id, content, author `user_name` and `channel_id`, `likes_count`, `reply_count` and `published_time`. Comments with replies may include their own `continuation_token`; pass that token to `/youtube/comments/{id}/replies`. Pass the response-level `continuation_token` here for deterministic pagination. If omitted, the service discovers an initial cursor or may resume the most recently cached cursor for this video.
- **Params:** `continuation_token` (string, optional) — Opaque pagination token returned by a previous request; pass it for deterministic pagination; `id` (string, **required**) — YouTube video ID (11-character code)

### `youtube_profile`

- **HTTP:** `GET /youtube/profile/{id}`
- **What:** Retrieve channel profile. Returns the profile of a YouTube channel by `id`, which can be a channel id, `@handle`, `/c` or `/user` path, bare username or full channel URL. The profile has channel id, name and URL, bio, join date, region, profile picture, links, and `stats` with `followers_count`, `videos_count` and `views_count`.
- **Params:** `id` (string, **required**) — Channel ID, @handle, /c path, /user path, bare username, or full YouTube channel URL

### `youtube_search`

- **HTTP:** `GET /youtube/search`
- **What:** Search YouTube. Returns normalized YouTube search results using YouTube's InnerTube search API. Pass `continuation_token` from a previous response to retrieve the next page. Use `q` as the primary query parameter; `search_query` is accepted as an alias. `hl` and `gl` localize ranking and result context; they default to `en` and `US`. Named filters cover the public web search filters. Account-only chips such as Watched and Unwatched are not exposed.
- **Params:** `continuation_token` (string, optional) — Pagination token returned by a previous request; `duration` (string, optional) — Filter by duration; short, medium, and long preserve their previous upstream encodings; `features` (string, optional) — Comma-separated feature filters. Allowed values: live, 4k, hd, subtitles, cc, creative_commons, 360, vr180, 3d, hdr, location, purchased; `gl` (string, optional) — Two-letter YouTube region code; `hl` (string, optional) — YouTube interface language; `params` (string, optional) — Raw protobuf-encoded search filter (base64); `q` (string, optional) — Search query; `search_query` (string, optional) — Alias for q; `sort_by` (string, optional) — Sort results; `type` (string, optional) — Filter by type; `upload_date` (string, optional) — Filter by upload date

### `youtube_transcript`

- **HTTP:** `GET /youtube/transcript/{id}`
- **What:** Retrieve transcript for a YouTube video. Returns transcript segments for a YouTube video using YouTube's native player captions. Set `format=text`, `format=srt`, or `format=vtt` to receive plain-text output instead of the standard response envelope. Returns `404` when the video currently has no transcript/captions available in any language — this is a normal, non-retryable result, not an error condition. Returns `503` when the request is temporarily blocked or rate-limited; retrying after a short delay may succeed.
- **Params:** `format` (string, optional) — Response format; `id` (string, **required**) — YouTube video ID (11-character code); `lang` (string, optional) — Preferred transcript language; `timestamps` (boolean, optional) — Include timestamps in the JSON response; `translate_to` (string, optional) — Translate transcript to this language code

### `youtube_transcript_languages`

- **HTTP:** `GET /youtube/transcript/{id}/languages`
- **What:** List transcript languages for a YouTube video. Lists the transcript languages available for a YouTube video by its 11-character video id. Each entry has the language name and code, whether the track is auto-generated, and whether it can be translated. Use it to pick a language before requesting a transcript.
- **Params:** `id` (string, **required**) — YouTube video ID (11-character code)

### `youtube_video`

- **HTTP:** `GET /youtube/video/{id}`
- **What:** Retrieve video metadata & captions. Returns the metadata of a YouTube video by its 11-character `id`: title, description, channel id and title, publication time, duration in seconds, and view, like and comment counts. Some fields are best-effort.
- **Params:** `id` (string, **required**) — YouTube video ID (11-char code)

# xyz API Reference (小宇宙FM API)

Base URL: `http://localhost:23020` (default port, configurable via `-p` flag)

Source: https://github.com/ultrazg/xyz

## Table of Contents

- [Authentication](#authentication)
- [Search](#search)
- [Episode Endpoints](#episode-endpoints)
- [Podcast Endpoints](#podcast-endpoints)
- [Common Response Fields](#common-response-fields)

## Authentication

### Send Verification Code

```
POST /sendCode
Content-Type: application/json

{"mobilePhoneNumber": "13111111111", "areaCode": "+86"}
```

### Login

```
POST /login
Content-Type: application/json

{"mobilePhoneNumber": "13111111111", "verifyCode": "1234", "areaCode": "+86"}
```

Response contains `x-jike-access-token` and `x-jike-refresh-token` in `data.*`. Save both.

### Refresh Token

```
POST /refresh_token
Content-Type: application/json

{"x-jike-access-token": "OLD_TOKEN", "x-jike-refresh-token": "OLD_REFRESH"}
```

Call when any authenticated endpoint returns 401.

## Search

```
POST /search
x-jike-access-token: TOKEN
Content-Type: application/json

{
  "keyword": "search term",
  "type": "ALL | PODCAST | EPISODE | USER",
  "pid": "optional podcast id for searching within a podcast",
  "loadMoreKey": {"loadMoreKey": 20, "searchId": "..."}
}
```

Returns array of items with `type` field distinguishing PODCAST, EPISODE, USER results.

## Episode Endpoints

All require `x-jike-access-token` header.

### Episode Detail

```
POST /episode_detail
{"eid": "EPISODE_ID"}
```

Key fields: `title`, `description`, `shownotes`, `media.source.url`, `duration` (seconds), `podcast.title`, `pubDate`, `playCount`, `commentCount`.

### Episode List (by podcast)

```
POST /episode_list
{"pid": "PODCAST_ID", "order": "asc | desc", "loadMoreKey": {"pubDate":"...","id":"...","direction":"NEXT"}}
```

Returns 20 episodes per page. Use `loadMoreKey`/`loadNextKey` from response for pagination.

### Popular Episodes

```
POST /episode_list_by_filter
{"pid": "PODCAST_ID"}
```

### Playback Progress

```
POST /episode_play_progress
{"eid": "EPISODE_ID"}

POST /episode_play_progress_update
{"eid": "EPISODE_ID", "progress": 120.5}
```

## Podcast Endpoints

All require `x-jike-access-token` header.

### Podcast Detail

```
POST /podcast_detail
{"pid": "PODCAST_ID"}
```

Key fields: `title`, `description`, `subscriptionCount`, `episodeCount`, `podcasters[]`, `image.picUrl`.

### Podcast Info

```
POST /podcast_get_info
{"pid": "PODCAST_ID"}
```

### Related Podcasts

```
POST /podcast_related
{"pid": "PODCAST_ID"}
```

### Podcast Bulletin

```
POST /podcast_bulletin
{"pid": "PODCAST_ID"}
```

### Podcast Honor List

```
POST /podcast_honor_list
{"pid": "PODCAST_ID"}
```

## Common Response Fields

### Episode Object

| Field | Type | Description |
|-------|------|-------------|
| `eid` | string | Episode ID |
| `pid` | string | Parent podcast ID |
| `title` | string | Episode title |
| `description` | string | Plain text description |
| `shownotes` | string | HTML formatted show notes |
| `duration` | number | Duration in seconds |
| `media.source.url` | string | Audio download URL (m4a) |
| `media.size` | number | File size in bytes |
| `media.mimeType` | string | e.g. "audio/mp4" |
| `pubDate` | string | ISO 8601 date |
| `playCount` | number | Play count |
| `commentCount` | number | Comment count |
| `clapCount` | number | Clap/like count |
| `podcast` | object | Parent podcast info |
| `isFavorited` | boolean | Favorited by user |
| `payType` | string | "FREE" or paid |

### Podcast Object

| Field | Type | Description |
|-------|------|-------------|
| `pid` | string | Podcast ID |
| `title` | string | Podcast title |
| `author` | string | Author name |
| `description` | string | Description |
| `subscriptionCount` | number | Subscribers |
| `episodeCount` | number | Total episodes |
| `podcasters` | array | Host info with uid, nickname, avatar |
| `image.picUrl` | string | Cover image URL |

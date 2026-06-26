# Stremio API Reference

## Central API

Base URL: `https://api.strem.io/api`

All requests are POST with JSON body. Auth via `authKey` in body (not headers).

### Authentication

```bash
# Login
curl -X POST https://api.strem.io/api/login \
  -H "Content-Type: application/json" \
  -d '{"type":"Login","email":"...","password":"...","facebook":false}'
# Response: {"result":{"authKey":"...","user":{...}}}

# Validate
curl -X POST https://api.strem.io/api/getUser \
  -H "Content-Type: application/json" \
  -d '{"authKey":"..."}'

# Logout
curl -X POST https://api.strem.io/api/logout \
  -H "Content-Type: application/json" \
  -d '{"authKey":"..."}'
```

### Library (Datastore)

```bash
# Fetch all library items
curl -X POST https://api.strem.io/api/datastoreGet \
  -H "Content-Type: application/json" \
  -d '{"authKey":"...","collection":"libraryItem","all":true}'

# Fetch specific items
curl -X POST https://api.strem.io/api/datastoreGet \
  -H "Content-Type: application/json" \
  -d '{"authKey":"...","collection":"libraryItem","ids":["tt123"]}'

# Get metadata (IDs + timestamps only)
curl -X POST https://api.strem.io/api/datastoreMeta \
  -H "Content-Type: application/json" \
  -d '{"authKey":"...","collection":"libraryItem"}'
```

### LibraryItem structure

| Field | Description |
|-------|-------------|
| `_id` | IMDB ID (e.g. `tt1234567`) |
| `name` | Show name |
| `type` | `series`, `movie`, `other` |
| `removed` | User removed from library |
| `temp` | Auto-added during playback |
| `state.video_id` | Last watched video (e.g. `tt123:2:5` for S02E05) |
| `state.timeOffset` | Playback position (ms) |
| `state.duration` | Total duration (ms) |
| `state.timeWatched` | Time spent watching current video (ms) |
| `state.overallTimeWatched` | Total watch time across all videos (ms) |
| `state.timesWatched` | Times watched to completion |
| `state.lastWatched` | ISO 8601 timestamp |
| `state.watched` | Watched bitfield string |
| `state.flaggedWatched` | Movie watched flag |
| `state.noNotif` | Disable notifications |

### Watched threshold

An episode is "watched" when `timeWatched > duration * 0.7` (70%).

### Addon Collection

```bash
# Get installed addons
curl -X POST https://api.strem.io/api/addonCollectionGet \
  -H "Content-Type: application/json" \
  -d '{"authKey":"..."}'
```

## Cinemeta (Metadata Addon)

Base URL: `https://v3-cinemeta.strem.io`

### Series metadata

```bash
GET https://v3-cinemeta.strem.io/meta/series/{imdb_id}.json
```

Returns `MetaItem` with `videos[]` containing season, episode, released date.

### Calendar videos (upcoming episodes)

```bash
GET https://v3-cinemeta.strem.io/catalog/series/calendar-videos/calendarVideosIds={ids}.json
```

- Comma-separated IMDB IDs, max 100
- Returns `metasDetailed[]` with videos including **future** release dates
- Includes specials (season 0)

### Last videos (notifications)

```bash
GET https://v3-cinemeta.strem.io/catalog/series/last-videos/lastVideosIds={ids}.json
```

- Only past episodes, no specials, no future dates

## Addon Protocol (Streams)

```bash
# Get streams for a series episode
GET {addon_url}/stream/series/{imdb_id}:{season}:{episode}.json
# Response: {"streams":[{"infoHash":"...","fileIdx":0,"name":"...","description":"..."}]}
```

Stream source types:
- `infoHash` + `fileIdx` — BitTorrent
- `url` — Direct HTTP
- `ytId` — YouTube
- `externalUrl` — Opens in browser

## Local Streaming Server

Base URL: `http://127.0.0.1:11470`

```bash
# Check if running
GET /settings

# Create torrent download
POST /{infoHash}/create

# Get download stats
GET /{infoHash}/{fileIdx}/stats.json
# Response: {downloadSpeed, uploadSpeed, downloaded, peers, streamProgress, ...}
```

## Watched Bitfield Format

Serialized: `{anchorVideoId}:{anchorLength}:{base64_zlib_data}`

Parse by popping from the right (anchorVideoId contains colons).

Decode: Base64 -> zlib inflate -> byte array. Each bit is LSB-first: `(bytes[floor(i/8)] & (1 << (i%8))) != 0`. Video IDs sorted by (season ASC, episode ASC, released ASC).

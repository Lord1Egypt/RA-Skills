# YouTube API Endpoints

Base path: `/v1/youtube`

## Video & Channel Data

### Video/Short Details
```
GET /v1/youtube/video?video_id={id}
```
Full details for a video or short: title, description, view/like/comment counts, publish date, keywords.

### Channel Info
```
GET /v1/youtube/channel?handle={username}
```
Public channel data: subscriber count, video count, description, avatar.

### Channel Videos
```
GET /v1/youtube/channel-videos?handle={username}&cursor={cursor}&includeExtras=true
```
Paginated list of a channel's videos. Pass `includeExtras=true` to get like/comment counts and descriptions — without it, you only get titles and video IDs, which is rarely enough for analysis.

### Channel Shorts
```
GET /v1/youtube/channel/shorts?handle={username}&cursor={cursor}
```
Paginated list of a channel's shorts.

### Channel Shorts (Simple)
```
GET /v1/youtube/channel/shorts/simple?handle={username}
```
Convenience endpoint — auto-paginates to get latest shorts. Costs more credits (makes multiple requests under the hood) so only use when you need a quick dump of all shorts. For full short details (description, publish date), use the Video/Short Details endpoint on individual results.

## Search

### Search
```
GET /v1/youtube/search?query={keyword}&cursor={cursor}&sortBy={sort}&uploadDate={date}
```
Search YouTube videos.

Parameters:
- `sortBy` — `relevance` (default) or `popular`
- `uploadDate` — filter by upload date (note: `this_hour` has been removed)

Results separate shorts and lives into dedicated arrays.

## Playlists

### Playlist Videos
```
GET /v1/youtube/playlist?playlist_id={id}&cursor={cursor}
```
Get the videos from a YouTube playlist.

## Transcripts

### Video Transcript
```
GET /v1/youtube/video/transcript?video_id={id}
```
Dedicated transcript endpoint. This is separate from the video details endpoint — YouTube changed their API, so transcripts require their own call. Unlike TikTok/Instagram transcripts, YouTube transcripts use YouTube's native transcript data and have no duration limit.

## Notes

- `includeExtras=true` on channel-videos adds like/comment count and description per video
- YouTube transcripts are unaffected by the 2-minute AI transcript limit (they use YouTube's own transcript data)
- The `keywords` field is included in video details responses
- Use `trim=true` to reduce response size

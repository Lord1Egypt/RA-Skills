---
name: youtube-music-mv-detector
description: Detect YouTube Music links as MV (music video) or song (audio). Use when user shares YouTube Music links (music.youtube.com/watch?v=...) and you need to classify them as MV or audio track.
---

# YouTube Music MV Detector

## Detection Method

Use YouTube's free **oEmbed API** (no API key needed):

```
https://www.youtube.com/oembed?url={youtube_music_url}&format=json
```

## Classification Rules

After fetching oEmbed data, check:

### 🎬 MV (Music Video) - if ANY true:
1. Author does NOT contain " - Topic"
2. Title contains "(Official Music Video)", "(Music Video)", "MV", "(Official Video)"

### 🎵 Song (Audio) - if ANY true:
1. Author contains " - Topic" (YouTube Topic channels = audio tracks)
2. Title is just the song name without video indicators

## Examples

| URL | Title | Author | Result |
|-----|-------|--------|--------|
| music.youtube.com/watch?v=1rvqA8rMTu8 | Iceage - Star (Official Music Video) | Iceage | 🎬 MV |
| music.youtube.com/watch?v=Mh5Y8vusknE | Star | Iceage - Topic | 🎵 Song |
| music.youtube.com/watch?v=wtJcLWeY114 | amazarashi...ED | amazarashi Official YouTube Channel | 🎬 MV |
| music.youtube.com/watch?v=HPMwDxi9-e0 | Kisetsu Wa Tsugitsugi Shindeiku | amazarashi - Topic | 🎵 Song |

## Workflow

1. Extract video ID from YouTube Music URL
2. Call oEmbed API: `https://www.youtube.com/oembed?url=...&format=json`
3. Parse `title` and `author_name` from JSON response
4. Apply classification rules above
5. Return result with title and classification

## Notes

- YouTube Music URLs may include extra params like `&list=...` or `&si=...` - strip these before calling oEmbed
- oEmbed is free and doesn't require authentication
- This works for both regular YouTube and YouTube Music links

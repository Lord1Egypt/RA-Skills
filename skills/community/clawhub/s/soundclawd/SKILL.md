---
name: soundclawd
description: Identify a track from a SoundCloud Live set screenshot and find its Apple Music and Spotify links. Use when a user shares a screenshot of a SoundCloud Live set (or mentions a SoundCloud live set, DJ mix, or radio show) and wants to know what track is playing at the current timestamp, or wants an Apple Music or Spotify link for that track.
---

# SoundClawd

Identify tracks from SoundCloud Live set screenshots by cross-referencing tracklist databases, then return Apple Music and Spotify links.

## Workflow

### Step 1: Read the Screenshot

Analyze the provided screenshot to extract:

1. **Set name** — title of the live set (DJ name, event, mix title)
2. **Current timestamp** — playback position shown in the player (e.g. "1:23:45")

If either value is unclear, ask the user to clarify before proceeding.

### Step 2: Find the Tracklist

Search for the tracklist using multiple sources. Try them in this order — use the first one that returns usable results with timestamps.

#### Priority 1: livetracklist.com

```
site:livetracklist.com {DJ name} {event or mix name}
```

Fetch the matching page. Timestamps are usually included inline.

#### Priority 2: set79.com

```
site:set79.com {set name}
```

Or search for the SoundCloud URL directly on set79:

```
https://set79.com/tracklist/soundcloud.com/{user}/{slug}
```

#### Priority 3: SoundCloud tracklist reposts

```
"{set name}" tracklist timestamps
```

Some users repost sets on SoundCloud with full tracklists and timestamps in the description.

#### Priority 4: YouTube description

If the set also exists on YouTube (common for fan-curated mixes), the video description often contains the full tracklist with timestamps. Search:

```
"{set name}" site:youtube.com
```

Then fetch the video page and extract the description.

#### Fallback: 1001tracklists.com

```
site:1001tracklists.com {set name}
```

Note: 1001tracklists.com frequently blocks automated access with captchas and Cloudflare challenges. Only try this if the above sources fail. If blocked, skip it and note the failure.

### Step 3: Match the Track at Timestamp

From the tracklist:

- Find the track whose cue time contains or immediately precedes the screenshot timestamp
- Extract **track name** and **artist**
- If no cue times are listed, estimate by track position relative to total set length and inform the user the match is estimated
- If the timestamp is within ~5 seconds of a transition, mention both tracks

### Step 4: Get the Apple Music Link

1. Use the iTunes Search API:

```
https://itunes.apple.com/search?term={artist}+{track name}&entity=song&limit=5
```

Pick the best match from results and use `trackViewUrl` as the Apple Music link.

2. If no results, try a web search: `site:music.apple.com {artist} {track name}`

### Step 5: Get the Spotify Link

1. Search: `site:open.spotify.com {artist} {track name}`
2. If no results, try a broader search: `{artist} {track name} spotify`

### Step 6: Output

```
Set:        {set name}
Timestamp:  {timestamp from screenshot}
Track:      {track name}
Artist:     {artist}
Apple Music: {apple_music_link}
Spotify:    {spotify_link}
```

If any step produces uncertain results, state what was found and what wasn't, and ask the user how to proceed.

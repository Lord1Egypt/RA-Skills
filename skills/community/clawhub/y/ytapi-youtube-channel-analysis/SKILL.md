---
name: ytapi-youtube-channel-analysis
description: "Study a YouTube channel the way a creator studies a competitor: which videos break out and why, how the channel grew, and what a viral video does in its title, opening, structure and most replayed moments, through the YTAPI API. Ends with a reusable playbook skill for the user's own channel. Use when the user names a channel or a video and asks what works for it, how it took off, why a video blew up, how to compete in a niche, or for a method to copy. 中文：分析同行 YouTube 频道怎么做起来、爆款视频为什么火，并提炼成可复用的方法论 skill。"
version: 1.0.0
homepage: https://ytapi.dev
license: MIT-0
required_environment_variables:
  - name: YTAPI_API_KEY
    prompt: "YTAPI API key (starts with sk_)"
    help: "Leave empty and the agent can create a free account for you (200 credits, no card), or get a key at https://ytapi.dev/app/api-keys?utm_source=skill&utm_medium=skill-file"
    required_for: "All YTAPI requests"
metadata:
  openclaw:
    emoji: "📈"
    homepage: https://ytapi.dev
    requires:
      bins:
        - curl
    primaryEnv: YTAPI_API_KEY
    envVars:
      - name: YTAPI_API_KEY
        required: false
        description: "YTAPI API key (sk_...). If it is not set, the skill can create a free account and key with the user's email."
  hermes:
    tags: [youtube, channel, analytics, competitors, creators, viral]
    category: media
---

# Analyze a YouTube channel

Competitor research for creators with [YTAPI](https://ytapi.dev/?utm_source=skill&utm_medium=skill-file):
breakouts, growth, viral teardowns and a playbook to reuse.

## YTAPI tools

If this session already has the YTAPI tools (`get_channel`,
`get_channel_videos`, `get_video_details`, `get_video_heatmap`,
`get_transcript`, `get_comments`, `search_youtube`), from the YTAPI connector
or plugin, use them: they need no API key and no `curl`. The steps are the
same.

## Setup

If `YTAPI_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md)
and follow it: the user either pastes a key or you create a free account
with their email (200 credits, no card). Send the key as
`Authorization: Bearer $YTAPI_API_KEY` and never print it.

## Requests (1 credit each)

`CHANNEL` is an `@handle` or a `UC...` ID.

```bash
H="Authorization: Bearer $YTAPI_API_KEY"
B=https://api.ytapi.dev/v1

# Profile: subscriber and video counts, country, description
curl -s "$B/channels/CHANNEL" -H "$H"

# Uploads, one page each; sort_by: newest, popular, oldest
curl -s "$B/channels/CHANNEL/videos?sort_by=newest" -H "$H"

# Exact view, like and comment counts, publish time (Unix seconds),
# keywords, chapters, related videos
curl -s "$B/videos/VIDEO_ID/video-info" -H "$H"

# Most replayed graph: most_replayed, peaks and a 20-part curve
curl -s "$B/videos/VIDEO_ID/heatmap" -H "$H"

# Transcript: markdown has a [m:ss] timestamp every few lines; srt has a
# start and end time on every caption line, for lining up replay peaks
curl -s "$B/transcripts?video_id=VIDEO_ID&format=markdown" -H "$H"
curl -s "$B/transcripts?video_id=VIDEO_ID&format=srt" -H "$H"

# Top comments, about 20 a page
curl -s "$B/videos/VIDEO_ID/comments?sort=top" -H "$H"

# Search, to see whether a topic was early or crowded
curl -s -G "$B/search" --data-urlencode "q=QUERY" -d type=video -H "$H"
```

Paged responses carry `has_more` and `next_cursor`; pass `cursor=NEXT_CURSOR`
for the next page. The uploads list has the channel's regular videos only,
not its Shorts or live streams. `404 heatmap_unavailable` means the video has no most
replayed graph, which is common on smaller videos; go on without it.

## Choose the mode

Ask only what you can't guess. Tell the user the estimate first: a snapshot
is about 15 credits per channel, a growth story about 15, a teardown about 6
(plus a credit for each extra page of uploads to reach an older video).

**Snapshot** (the default): what works for one to three channels now.
1. The profile, then one page of uploads `newest` and one `popular`.
2. Baseline: compare each video with the uploads published within a few
   months of it, at least five (for a channel that posts weekly or more, the
   ten on either side), and take their median views. Older videos have had
   years to gather views, so a median over uploads that span years hides
   recent breakouts. Leave
   out videos younger than a week. Two times the baseline is above usual;
   three times or more is a breakout. Give the multiple. Hits on the popular
   page that are years old show what used to work.
3. Video details (`video-info`; with the MCP tools, `get_video_details`,
   not the free `get_video_info`) on three to five breakouts and two typical
   videos. Use the exact counts and work out views per day and like and
   comment rates; list pages round views and give relative ages.
4. Note topics and formats above and below the baseline, title patterns,
   cadence and day of week (from the publish dates in the details), length,
   and shared keywords and chapters.
5. Read two or three breakout transcripts: the hook in the first 30 to 60
   seconds, the structure, where the payoff comes, calls to action.

**Growth story**: how one channel took off.
1. The profile, then two or three pages of uploads `oldest`.
2. Find the first video that clearly beat the ones around it and what
   changed there, pivots in topic or format, and changes in cadence.
3. Video details on those turning points, and the transcript of the first
   breakout.
4. One page of uploads `newest`, and compare: what the channel kept from its
   early breakouts and what it changed.

Old videos keep gaining views for years, so they show what lasted, not the
first week. Subscriber history is not public; don't invent a growth curve.

**Breakout teardown**: why one video did far better than usual.
1. Video details, then the baseline from the uploads around it: find the
   video on the `newest` pages (follow the cursor back to its date) or the
   `oldest` pages for an early video. Comparing an old video's lifetime
   views with recent uploads inflates the multiple. Each page costs a
   credit; stop once you reach its date.
2. The title and its promise, compared with the channel's usual titles.
   Thumbnails are images; describe them only if you can see them.
3. The heatmap: most replayed moment and peaks. Ignore the first seconds,
   which are high on almost every video. Each curve point averages about a
   twentieth of the video, so a short spike looks wider than it is; the
   most replayed moment gives its exact span. Compare intensities as
   differences, not ratios: next to a point near zero any ratio looks huge.
   Many videos have none (404, free); go on without it.
4. The transcript in `srt` format, which has a time on every caption line,
   so you can quote exactly what is said inside each peak: the opening, the
   structure, and what happens at each peak. A peak right after a sponsor segment or a long intro is often where
   viewers skip to, not what they rewatch; say which it looks like.
5. One page of top comments: what viewers quote, ask and argue about.
6. The related videos in the video details, and a search on the topic, for
   context. Describe the mix of related videos you see; call it one kind
   only when most of them are.

## Write the report

In the user's language: a table of the videos used (title, views, views per
day, published, length, multiple), findings backed by examples and
timestamped links (`https://www.youtube.com/watch?v=VIDEO_ID&t=SECONDS`),
opportunities for the user, and limits:
- the data is a public snapshot, taken today;
- the heatmap is relative to the video's own peak and is not retention;
- click-through rate, real retention, traffic sources and revenue are
  private to the channel owner, so don't guess them.

Quote short lines only and describe the rest in your own words.

## Make a playbook

Offer this at the end, or do it straight away when the user asked for a
method to copy. Ask for the user's own channel or niche if you don't know
it. Then write a `SKILL.md` with:
- front matter between `---` lines: a `name` (lowercase, hyphens) and a
  `description` saying to use it when planning, titling or scripting a
  video in this niche;
- rules, each with the videos and numbers behind it; a rule needs the
  pattern in at least two or three videos;
- to test: patterns seen in only one video, or read from an ambiguous peak,
  written as experiments, not rules;
- title formulas and opening templates with blanks, not copied lines;
- structure, cadence and length;
- a checklist for a draft title and script;
- what to avoid: what fell below the baseline;
- the sources and the date, so the user knows when to refresh it.

Save it as `PLAYBOOK_NAME/SKILL.md` in the agent's skills folder, or give it
in a code block when you can't write files. Then tell the user how to use
it, for example: "Use my home-cooking playbook to plan next week's videos."
It describes a method; it must not copy the channel's scripts, titles or
branding.

## Credits and errors

Only successful responses use credits; errors are free, such as a video
without captions or without a heatmap. Ask before reading more than ten
transcripts. New accounts get 200 free credits. Until a credit pack is
bought, a key can make 1 request per second and 100 per day (UTC);
`429 daily_limit_exceeded` means that day's limit is used up.
`402 insufficient_credits` means the balance is empty: packs from $9 at
<https://ytapi.dev/?utm_source=skill&utm_medium=skill-file#pricing>. `401` means the key is missing
or wrong.

Full reference: https://docs.ytapi.dev

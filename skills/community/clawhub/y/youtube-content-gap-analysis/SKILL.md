---
name: youtube-content-gap-analysis
description: Map observed YouTube topic and format coverage using Crawlora searches, channel samples, videos, and available captions. Use for an evidence-based content brief or sampled topic-gap map with search selection, language, transcript basis, identity, and demand limits preserved.
---

# YouTube content gap analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Build a content-planning map for specified topics, audience needs, languages,
markets, formats and channels. Define query synonyms, date window and balanced
video/channel budgets. Search popularity is a discovery surface, not a complete
inventory of every video or a measurement of unmet audience demand.

## Collect a defensible video cohort

1. Use documented YouTube query/type/upload-date/duration/locale filters and
   returned continuation tokens. Shorts, long-form videos, livestreams and
   playlists are different units; keep the requested formats separate.
   Save every query, ordering, filter, sampled page and stopping reason.
2. Resolve actual video/channel IDs and canonical URLs. Channel names, handles,
   playlists and videos are different namespaces. Deduplicate the same video
   across searches; cross-channel reuploads need corroboration and remain
   distinct source observations rather than automatically independent content.
3. Inspect selected video metadata and channel archives. Record dates, duration,
   supplied views/engagement, creator, and coverage basis. Missing/rounded public
   fields stay unknown; no historical view curve is promised by this surface.
4. Discover transcript languages before requesting captions. Retain generated,
   original/translated language and timestamp context. Use JSON format for the
   normal envelope; `text`, `srt`, `vtt` return raw text. A transcript 404 means
   captions currently unavailable; a transient upstream error is different.
   Without captions/content evidence, label topic coding as title/description-only.

```sh
scripts/crawlora.sh /youtube/search q="home energy efficiency" type=video upload_date=this_year sort_by=relevance
# Use actual returned video IDs before metadata and caption discovery:
# scripts/crawlora.sh "/youtube/transcript/$VIDEO_ID/languages"
# scripts/crawlora.sh "/youtube/transcript/$VIDEO_ID" format=json
```

## Identify sample gaps and testable content hypotheses

Create a shared topic/subtopic, format, depth and intended-use rubric. Allow
multi-label and uncertain states; cite short timestamped evidence only when the
actual caption supports it. Automatic captions/translation can misrecognize
speech and do not independently verify a claim. Do not reproduce full transcripts.

Return a topic-by-format/channel matrix with unique-video denominators, dates,
collection scope and unavailable-content counts, then a prioritized idea brief
linked to actual sample gaps. Low observed coverage does not prove a topic is
absent, underserved or commercially attractive. High views or comments do not
prove audience demographics, conversion, revenue, retention or replicable future
performance. A causal/title/thumbnail recommendation needs further testing;
label it a hypothesis rather than a guaranteed growth tactic. Do not upload,
comment, message creators, download restricted media, or create ongoing monitors.

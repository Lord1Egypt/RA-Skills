---
name: socialkit-youtube-research
description: Researches a YouTube topic with the official YouTube Data API v3 - top videos, view and engagement statistics, titles, tags and gaps - and writes research.md for a video project. Use when the user wants topic ideas, competitor or trend research, or evidence for a YouTube video.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core
---

# YouTube research

Requires `YT_API_KEY`. If it is missing, point the user to [setup](references/setup.md).

## Steps

1. Agree on 1-3 search queries with the user, plus region and language if relevant.
2. For each query run:
   `node scripts/research.mjs --query "<terms>" --max 15 --order viewCount`
   Add `--published-after <ISO date>` for recent trends. Output is JSON on stdout.
   Each query costs one call from the 100/day search bucket; do not loop over many
   queries without asking.
3. Analyse: recurring angles, title patterns, typical length, views per day since
   publishing, and what the top videos do not cover.
4. Write `research.md` in the project folder with: queries used, a table of the top
   videos (title, channel, views, published, URL), patterns, gaps, and 3-5 proposed
   angles. Cite video URLs for every claim.

## Rules

- Research informs an original video. Do not copy titles, scripts or thumbnails.
- Only report numbers from the script output. Do not estimate missing statistics.

## Failure handling

- `YT_API_KEY_MISSING`: stop and show the setup steps.
- `YT_QUOTA_EXCEEDED` or `YT_QUOTA_ESTIMATE_EXHAUSTED`: stop; quotas reset at midnight
  Pacific Time.
- Empty results: suggest broader terms; do not invent results.

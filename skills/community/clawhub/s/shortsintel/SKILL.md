---
name: shortsintel
description: Find winning short-form videos and ads on TikTok, Instagram Reels, YouTube Shorts, Facebook and the Meta and TikTok Ad Libraries with the ShortsIntel API. Research a niche, search and score videos, analyse hooks and formats, search ads, and track creators, hashtags, sounds, keywords and advertisers daily. Prepaid Credits, priced per call.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SHORTSINTEL_API_KEY
      bins:
        - curl
    primaryEnv: SHORTSINTEL_API_KEY
    envVars:
      - name: SHORTSINTEL_API_KEY
        required: true
        description: ShortsIntel API key (sk_live_...), created at https://www.shortsintel.com/console/keys.
    homepage: https://www.shortsintel.com
---

# ShortsIntel

ShortsIntel is a short-form video research API. It finds the videos and ads that are winning on TikTok, Instagram Reels, YouTube Shorts, Facebook and the Meta and TikTok Ad Libraries, watches the videos, ranks what beats its creator's usual reach, and returns compact JSON.

## When to use it

- "What hooks, formats or angles are working for <topic> right now?" Run a Research.
- "Find TikToks or Shorts about <keyword>." Search videos.
- "Break down this video." Look it up, then get its analysis (hook, persuasion, tone, visuals).
- "Which ads is <brand> running?" or "Show winning Meta ads for <product> in the US." Search ads.
- "Keep an eye on this creator, hashtag, sound, keyword or advertiser." Create a Tracker and read its Change Reports.

## Setup

1. Sign up at https://www.shortsintel.com.
2. Create a key at https://www.shortsintel.com/console/keys. It is shown once.
3. Export it:

```bash
export SHORTSINTEL_API_KEY=sk_live_...
```

Every call sends `Authorization: Bearer $SHORTSINTEL_API_KEY` to `https://www.shortsintel.com/v1`.

## Core model

- Every paid call creates a **Run** and returns `{ run, result }`. If the work takes longer than `wait` seconds (default 30, max 120), you get `{ run }` with `status: "running"`; poll `GET /v1/runs/{id}` every 5 to 15 seconds.
- Run states: `running`, `completed`, `partial` (completed items kept and charged), `failed` (nothing charged).
- Prices are whole **Credits**. A cached result costs the same as a fresh one.
- Lists return `items` and `next_cursor`. Pass back only the `next_cursor` you were given.

## Core calls

### 1. Research a niche

Searches the platforms, drops off-topic videos, ranks by outlier score, analyses the shortlist and writes a digest (themes, verbatim hooks, formulas, angles). 1,036 Credits for up to 50 videos, then 20 per video, at most 4,036.

```bash
curl -s https://www.shortsintel.com/v1/research \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"intent":"what hooks work for cold plunge videos","platforms":["tiktok","youtube"],"window":"week","max_videos":50,"estimate":true}'
```

Drop `"estimate":true` to run it. Then slice the result for free:

```bash
curl -s "https://www.shortsintel.com/v1/research/RUN_ID/digest" \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY"
curl -s "https://www.shortsintel.com/v1/research/RUN_ID/videos?platforms=tiktok&min_views=100000&order_by=outlier" \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY"
```

Also free: `/creators`, `/hashtags`, `/sounds` under the same research id.

### 2. Search videos

3 Credits per platform per page. `"intelligence":true` adds 20 Credits for each of the top 20 results analysed.

```bash
curl -s https://www.shortsintel.com/v1/videos/search \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"ice bath routine","platforms":["tiktok"],"window":"month","sort":"likes","limit":20}'
```

`platforms` defaults to TikTok, Instagram and YouTube; `facebook` is opt-in.

### 3. Look up a video by URL

3 Credits. Accepts TikTok (including short links), Instagram `/p/`, `/reel/`, `/reels/`, YouTube Shorts and Facebook reel or video URLs.

```bash
curl -s https://www.shortsintel.com/v1/videos/lookup \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.tiktok.com/@someone/video/7300000000000000000"}'
```

### 4. Analyse a video

23 Credits, whether computed now or already stored. `platform` is `tiktok`, `instagram`, `youtube` or `facebook`; `id` is the platform id from a lookup or search.

```bash
curl -s -X POST https://www.shortsintel.com/v1/videos/tiktok/7300000000000000000/intelligence \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

To score a video against its creator's baseline (outlier and velocity), `POST /v1/videos/{platform}/{id}/score` costs 9 Credits.

### 5. Search ad libraries

`library` is `meta` or `tiktok`. Pass `query` or `advertiser`, not both. Meta: 1 Credit per Ad delivered (`limit` default 50), plus 20 per Ad with `"analyze":true`. TikTok: 3 Credits per page (EU/EEA, Switzerland, UK and Turkey only; Meta-only filters are refused).

```bash
curl -s https://www.shortsintel.com/v1/ads/search \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"library":"meta","query":"protein powder","country":"US","status":"active","media_type":"video","order_by":"winner","limit":25}'
```

`order_by` (Meta): `relevance`, `winner` (0 to 100 winner score from days running and variants), `days_running`, `start_date`.

### 6. Create a Tracker

A daily check on one target. The first cycle is charged on create, and every later daily cycle costs the same: 6 Credits per creator or sound, 3 per hashtag or keyword, 30 per advertiser. Tracking a target you already track is free.

```bash
curl -s "https://www.shortsintel.com/v1/trackers?estimate=true" \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"creator","platform":"tiktok","target":"someone"}'
```

`kind`: `creator`, `hashtag` (`tiktok` or `instagram`), `sound` (`tiktok`), `keyword` (`tiktok`, `instagram`, `youtube`, `facebook`) or `advertiser` (`target` is a Facebook Page id or Page URL; `platform` omitted or `meta`, or `tiktok` for the TikTok library). The estimate returns `already_tracking` and `tracker_id`. Remove `?estimate=true` to create. Check `GET /v1/trackers` (free) first.

### 7. Get changes

Free. Each Change Report lists what moved since the last cycle (new videos, outliers, follower and view shifts, new or stopped ads) with before and after numbers.

```bash
curl -s "https://www.shortsintel.com/v1/trackers/TRACKER_ID/changes?limit=25" \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY"
```

### 8. Check balance

Free.

```bash
curl -s https://www.shortsintel.com/v1/account/balance \
  -H "Authorization: Bearer $SHORTSINTEL_API_KEY"
```

Returns `{ "balance_credits": ..., "grants": [...] }`.

## Rules agents get wrong

1. **Estimate before you spend.** Every paid call accepts `estimate` (in the JSON body, or `?estimate=true` on Tracker create). It returns `{ estimate_credits, cached }`, creates no Run and charges nothing. Tell the user the price and get a yes before any call over a few Credits, always before Research, analysis, `analyze` on ads and Trackers.
2. **Re-read Runs instead of repeating paid calls.** Reading a Run is free forever: `GET /v1/runs/{id}`, `GET /v1/runs/{id}/items`, and every `GET /v1/research/{id}/...` view. Before a new paid call, check `GET /v1/runs?kind=...&status=completed` for one you already paid for. A `running` Run is still working; poll it, do not start a second one.
3. **Retry safely.** Send an `Idempotency-Key` header on paid POSTs. A retry with the same key returns the original Run and is not charged again.
4. **Branch on the error `code`, never on the message.** Errors are `application/problem+json` with a stable `code`:
   - `insufficient_balance` (402): nothing charged. Report `balance_credits` and `required_credits`; the user tops up in the console.
   - `rate_limit_exceeded` (429): wait the `Retry-After` seconds. Limits are 60 requests per minute per key and 10 running Runs.
   - `source_unavailable` (503) or `vendor_error` (502): the Run failed and was not charged. Retry later or try another platform.
   - `advertiser_ambiguous` (409): pick one of the returned `candidates` and retry with its id. Free.
   - `invalid_request` (400), `not_found` (404), `unsupported_platform` (400): fix the input; nothing was charged.
   - `invalid_key` (401): the key is wrong or revoked.
5. **Do not paste raw JSON to the user.** Summarise: a few themes or ads with one verbatim hook and a link each, then the Credits spent and the run id for follow-ups.

## Reference

- Full reference for agents: https://www.shortsintel.com/llms-full.txt
- OpenAPI: https://www.shortsintel.com/docs/openapi.json
- Docs: https://www.shortsintel.com/docs
- MCP server (same tools for Claude, ChatGPT, Cursor): https://www.shortsintel.com/docs/mcp

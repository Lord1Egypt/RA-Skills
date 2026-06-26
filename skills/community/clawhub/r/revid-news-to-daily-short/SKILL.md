---
name: revid-news-to-daily-short
description: Generate a daily news short on a topic Revid researches itself. Use for a recurring "news of the day in <niche>" channel — the user only supplies the topic; Revid fetches fresh news, writes the script, and produces the video.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Topic / niche → daily news short

Recurring use case: feed a topic ("AI tools this week", "F1 race results",
"crypto headlines") and let Revid fetch live news, summarize it, and produce a
short. This is the right skill for *automated daily channels*.

## When to use this skill

- The user wants a **recurring daily short** on a topic — they don't have a
  specific URL.
- They are happy with whatever Revid surfaces from the news for that topic.
- For a known article URL use [`revid-article-to-short`](../revid-article-to-short/SKILL.md).
- For a custom angle / angle the news doesn't cover use
  [`revid-prompt-to-video`](../revid-prompt-to-video/SKILL.md).

## Inputs

| Field | Required | Notes |
|---|---|---|
| `prompt` | yes | The topic / niche |
| `aspectRatio` | no | Default `9:16` |
| `targetDuration` | no | Default 45 (s) |
| Cron / scheduling | external | This skill renders one video; loop externally for daily delivery. |

## Step-by-step

1. Build the payload (note: `options.fetchNews: true` is the magic switch).
2. POST `/render`.
3. Poll `/status`.
4. For a daily channel, schedule this in cron / GitHub Actions / Vercel Cron
   and post the resulting `videoUrl` to the target social account. Use
   `POST /api/public/v3/publish-now` if your Revid account has the relevant
   socials connected.

## API call template

```http
POST /api/public/v3/render
Host: www.revid.ai
Content-Type: application/json
key: $REVID_API_KEY
```

```json
{
  "workflow": "article-to-video",
  "source": {
    "prompt": "{TOPIC_OR_NICHE}"
  },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "stability": 0.6, "speed": 1.0, "language": "en-US" },
  "captions": { "enabled": true, "position": "middle", "autoCrop": true },
  "music":    { "enabled": true, "syncWith": "beats", "trackName": "news-upbeat" },
  "media": {
    "type": "stock-video",
    "density": "medium",
    "animation": "soft",
    "quality": "pro",
    "videoModel": "pro",
    "imageModel": "good"
  },
  "options": {
    "fetchNews": true,
    "targetDuration": 45,
    "summarizationPreference": "summarize",
    "soundEffects": true,
    "hasToGenerateCover": true,
    "coverTextType": "headline"
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

`options.fetchNews: true` tells Revid to crawl fresh news for the prompt
instead of using the prompt as the script directly.

## Daily automation example

```bash
# crontab — every day at 06:00
0 6 * * *  /opt/revid/daily-news.sh "AI tools this week"
```

```bash
# daily-news.sh
TOPIC="${1:?topic required}"
PID=$(curl -fsS https://www.revid.ai/api/public/v3/render \
  -H "Content-Type: application/json" -H "key: $REVID_API_KEY" \
  -d "$(jq -n --arg p "$TOPIC" '{
    workflow:"article-to-video",
    source:{prompt:$p},
    aspectRatio:"9:16",
    voice:{enabled:true,stability:0.6},
    captions:{enabled:true},
    music:{enabled:true,syncWith:"beats"},
    media:{type:"stock-video",density:"medium",quality:"pro",videoModel:"pro"},
    options:{fetchNews:true,targetDuration:45,summarizationPreference:"summarize",hasToGenerateCover:true},
    render:{resolution:"1080p"}
  }')" | jq -r .pid)
# poll → publish via /publish-now or download the videoUrl …
```

## Examples

- [`examples/ai-tools-news.json`](examples/ai-tools-news.json)
- [`examples/run.sh`](examples/run.sh)

## Failure modes

| Symptom | Fix |
|---|---|
| News for niche topic is sparse / off-topic | Make the prompt more specific (e.g. `"AI coding tools released this week"`) and consider switching to [`revid-article-to-short`](../revid-article-to-short/SKILL.md) with a hand-picked URL. |
| Same news repeats day-over-day | Track `pid` history client-side and add a date phrase to the prompt: `"AI tools — week of 2026-04-26"`. |
| Tone too neutral / dry for the niche | Add `voice.voiceId` matching a known persona, and pass `source.stylePrompt: "Punchy, opinionated, end with a take."` |

## See also

- [`revid-article-to-short`](../revid-article-to-short/SKILL.md) for known URLs.
- [`revid-prompt-to-video`](../revid-prompt-to-video/SKILL.md) for ideas Revid
  shouldn't research live.

# Vizard API — Full Reference

## Endpoints Summary

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/project/create` | Submit video for clipping or editing |
| GET | `/project/query/{projectId}` | Poll for results |
| GET | `/project/social-accounts` | List connected social accounts |
| POST | `/project/publish-video` | Publish clip to social media |
| POST | `/project/ai-social` | Generate AI social caption |

---

## POST /project/create — Submit Video

### Required Parameters (both modes)

| Field | Type | Description |
|-------|------|-------------|
| `videoUrl` | string | URL of the video source |
| `videoType` | int | Source platform (see table in SKILL.md) |
| `lang` | string | Language code or `"auto"`. Full list: [supported languages](https://docs.vizard.ai/docs/supported-languages) |
| `ext` | string | **Required only for `videoType: 1`** — file extension: `mp4`, `mov`, `avi`, `3gp` |

### Clipping Mode Parameters (long video → multiple clips)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `preferLength` | int[] | [0] | Clip length preference: 0=auto, 1=<30s, 2=30-60s, 3=60-90s, 4=>90s |
| `getClips` | int | 1 | 1 = clipping mode (default), 0 = editing mode |
| `projectName` | string | auto | Custom project name |
| `webhookUrl` | string | — | POST callback URL when processing completes |

### Editing Mode Parameters (short video ≤3min → 1 enhanced video)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `getClips` | int | — | **Must be 0** for editing mode |
| `ratioOfClip` | int | 1 | Output ratio: 1=9:16, 2=1:1, 3=4:5, 4=16:9 |
| `subtitleSwitch` | int | 1 | 0=hide subtitles, 1=show |
| `emojiSwitch` | int | 0 | 0=no emoji, 1=auto-add emoji in subtitles |
| `highlightSwitch` | int | 0 | 0=off, 1=auto-highlight key words |
| `autoBrollSwitch` | int | 0 | 0=off, 1=AI-generated B-roll |
| `headlineSwitch` | int | 1 | 0=no headline hook, 1=show |
| `removeSilenceSwitch` | int | 0 | 0=off, 1=remove silence and filler words |
| `templateId` | long | — | Apply a branding template (ratio must match `ratioOfClip`) |
| `projectName` | string | auto | Custom project name |

### Response

```json
{ "code": 2000, "projectId": 17861706 }
```

---

## GET /project/query/{projectId} — Poll Results

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | int | 2000=success, 1000=still processing |
| `projectId` | long | Project ID |
| `projectName` | string | Project name |
| `shareLink` | string | Shareable project link (Business/Team plan only) |
| `videos` | array | List of output clips (sorted by viral score) |

### `videos` Object

| Field | Type | Description |
|-------|------|-------------|
| `videoId` | long | Clip ID (use for publish/caption APIs) |
| `videoUrl` | string | Download URL — **valid 7 days only** |
| `videoMsDuration` | long | Duration in milliseconds |
| `title` | string | AI-generated title |
| `transcript` | string | Full speech transcript |
| `viralScore` | string | Engagement score 0–10 (clipping mode only) |
| `viralReason` | string | Why this clip is engaging |
| `relatedTopic` | string | Stringified JSON array of keywords |
| `clipEditorUrl` | string | Web editor URL for this clip |

### Status Codes

| Code | Meaning |
|------|---------|
| 2000 | Success |
| 1000 | Still processing |
| 4001 | Invalid API key |
| 4002 | Clipping failed |
| 4003 | Rate limit exceeded |
| 4004 | Unsupported video format |
| 4005 | Invalid URL (clipping mode) or video too long (editing mode) |
| 4006 | Illegal parameter |
| 4007 | Insufficient account time/credits |
| 4008 | Failed to download video |

---

## GET /project/social-accounts — List Social Accounts

### Response

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Use as `socialAccountId` when publishing |
| `platform` | string | Platform name (Instagram, TikTok, etc.) |
| `username` | string | Connected account username |
| `status` | string | `active`, `expired`, `locked`, `not connected` |
| `expiresAt` | long | Unix timestamp (ms) when auth expires |

---

## POST /project/publish-video — Publish to Social Media

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finalVideoId` | long | ✅ | `videoId` from query response |
| `socialAccountId` | string | ✅ | From social-accounts endpoint |
| `post` | string | ❌ | Post caption. Empty string = AI auto-generates |
| `publishTime` | long | ❌ | Unix timestamp (ms) for scheduled publish. Omit = publish now |
| `title` | string | ❌ | YouTube only. Empty = AI-generated title |

### Platform Character Limits

| Platform | Limit |
|----------|-------|
| TikTok | 2,200 |
| Instagram | 2,200 |
| Facebook | 2,200 |
| LinkedIn | 3,000 |
| YouTube | 5,000 (post), 100 (title) |
| Twitter/X | 280 |

### Status Codes

| Code | Meaning |
|------|---------|
| 2000 | Publish succeeded |
| 4004 | Feature requires plan upgrade |
| 4011 | Invalid social account ID |

---

## POST /project/ai-social — Generate AI Caption

**Note:** Only works for videos with spoken dialogue.

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finalVideoId` | long | ✅ | `videoId` from query response |
| `aiSocialPlatform` | int | ❌ | 1=General(default), 2=TikTok, 3=Instagram, 4=YouTube, 5=Facebook, 6=LinkedIn, 7=Twitter |
| `tone` | int | ❌ | 0=Neutral(default), 1=Interesting, 2=Catchy, 3=Serious, 4=Question |
| `voice` | int | ❌ | 0=First person(default), 1=Third person |

### Response

| Field | Type | Description |
|-------|------|-------------|
| `aiSocialContent` | string | Generated caption text with hashtags |
| `aiSocialTitle` | string | AI YouTube title (only for `aiSocialPlatform: 4`) |

### Status Codes

| Code | Meaning |
|------|---------|
| 2000 | Success |
| 4002 | No speech/dialogue detected |
| 4006 | Illegal parameter |

---

## Supported Languages (partial)

`auto`, `en`, `es`, `pt`, `fr`, `de`, `ru`, `zh`, `ja`, `ko`, `ar`, `hi`, `it`, `nl`, `pl`, `tr`

Full list: https://docs.vizard.ai/docs/supported-languages

---

## Rate Limits & Pricing

- See: https://docs.vizard.ai/docs/rate-limit
- See: https://docs.vizard.ai/docs/pricing

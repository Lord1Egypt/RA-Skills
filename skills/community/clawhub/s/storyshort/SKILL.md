---
name: storyshort
description: Create, render and publish AI videos (faceless, UGC ads, movie maker, podcast, music video...) with StoryShort — plus standalone AI images and clips. Full option discovery (voices, caption themes, styles, models with credit costs), exact price quotes before spending, and direct publishing to TikTok, YouTube and Instagram.
homepage: https://storyshort.ai/mcp
metadata:
  openclaw:
    primaryEnv: STORYSHORT_API_KEY
    requires:
      env:
        - STORYSHORT_API_KEY
---

# StoryShort — AI video creation for agents

StoryShort (https://storyshort.ai) turns prompts and scripts into finished short-form videos: script writing, AI visuals, voiceover, captions, rendering and publishing to connected social accounts. This skill drives the StoryShort MCP server over plain HTTP.

## Setup

1. Create an account at https://storyshort.ai (Free plan works).
2. Generate an API key in Settings → API (https://storyshort.ai/app/settings/api).
3. Export it: `STORYSHORT_API_KEY=ss_...`

All calls go to one endpoint. Define this helper once per session:

```bash
ss() { # usage: ss <tool_name> '<json_arguments>'
  local args="${2:-null}"; [ "$args" = "null" ] && args="{}"
  curl -s -X POST https://api.storyshort.ai/mcp \
    -H "Authorization: Bearer $STORYSHORT_API_KEY" \
    -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":$args}}" \
    | sed -n 's/^data: //p' | jq -r '.result.content[0].text' | jq .
}
```

(Any MCP-capable client can instead add `https://api.storyshort.ai/mcp` directly as a streamable-HTTP server — OAuth or the same Bearer key.)

## Discover before you spend

Everything is discoverable; never guess ids or prices:

```bash
ss get_account                 # plan + remaining credits — check this first
ss list_video_tools            # 20+ tools: faceless, ugc ads, movie maker, podcast, asmr, documentary...
ss get_video_tool '{"tool":"script_to_video"}'   # exact options for one tool
ss list_voices '{"query":"deep male"}'
ss list_caption_themes         # 33 styles: beast, neon, glass, comic, elegant...
ss list_image_styles
ss list_media_options          # media types + AI video tiers with credits per clip
ss list_music '{"query":"epic"}'
ss list_image_models           # standalone image models + costs
ss list_video_models           # Sora, Veo, Kling, Seedance 2.5 + per-second pricing
ss list_connected_accounts     # TikTok / YouTube / Instagram account ids for publishing
```

## Create a video (always estimate first)

```bash
ss estimate_credits '{"tool":"script_to_video","script":"<the script>","mediaType":"images"}'
ss create_video '{"tool":"script_to_video","script":"<the script>","title":"My video","mediaType":"images","imageQuality":"basic","captionTheme":"neon","voice":"openai_ash","aspectRatio":"9:16"}'
```

Prompt-driven tools take `"prompt"` + `"duration"` (30/60/120/180 seconds) instead of `"script"`. Other useful params: `imageStyle` (id or `"auto"`), `videoTier` (`pvideo`|`pvideo-1080`|`seedance`|`seedance25` when `mediaType` is `"videos"`), `language`, `dynamism`, `brandKitId`, `character`, `references`, `knowledgeSources`.

Generation is asynchronous (1–5 minutes). Poll every 20–30 s:

```bash
ss get_video '{"videoId":"<id>"}'   # status: queued -> processing -> completed | failed
```

`status: "completed"` means the video is built and editable (share `editorUrl` with the user). For the final MP4:

```bash
ss render_video '{"videoId":"<id>"}'          # async — poll get_video until renderStatus is "completed" and url is set
```

## Publish to social accounts

```bash
ss publish_video '{"videoId":"<id>","accountIds":["<from list_connected_accounts>"],"title":"Caption here","privacyStatus":"SELF_ONLY"}'
ss schedule_publish '{"videoId":"<id>","accounts":[{"id":"<id>","platform":"tiktok"}],"scheduledTime":"2026-09-01T18:00:00Z"}'
```

`publish_video` renders automatically if needed (can take minutes). Publishing posts to real accounts — confirm with the user before calling it, and prefer `privacyStatus: "SELF_ONLY"` on TikTok for tests.

## Standalone images and clips

```bash
ss generate_image '{"prompt":"...","model":"nano-banana-2","aspectRatio":"9:16"}'
ss generate_clip '{"prompt":"...","model":"kling-v3","duration":5}'
ss get_media '{"mediaId":"<id>"}'   # poll until status "completed", then use .url
```

Image-to-image: pass `"imageInput":["<url>"]`. A generated image URL can seed a video via `create_video`'s `"startingImageUrl"`.

## Workflow tips

- Call `get_account` first; refuse to start work that costs more credits than the balance and point the user to the upgrade URL instead.
- Always quote the `estimate_credits` price to the user before `create_video` on expensive configs (mediaType `"videos"`, movie maker, podcast).
- One video at a time: create, poll to completion, then move on. Do not fire parallel create_video calls unless the user asked for variants (`numberOfVideos` handles that server-side).
- Titles you set are kept; leave `title` out to get an auto-generated one.
- Errors come back as readable text in the tool result (e.g. "Not enough credits (credits_missing)") — relay them, don't retry blindly.

Docs: https://storyshort.ai/mcp · REST API: https://storyshort.ai/api-docs · Support: https://storyshort.ai/contact

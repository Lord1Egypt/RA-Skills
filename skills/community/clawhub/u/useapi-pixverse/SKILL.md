---
name: useapi-pixverse
description: Make AI video with Seedance 2.5, Kling 4.0, Veo 3.1, MiniMax H3 (Hailuo 3.0), Wan 3.0, Grok Imagine and PixVerse V6 on your own PixVerse subscription, through the useapi.net PixVerse API, a third-party paid API not affiliated with PixVerse. Text-to-video and image-to-video with one command and one model parameter, 480p to 1080p, 9:16 and 16:9, with sound on most models. Saves the .mp4. Use when the user asks for a Seedance, Kling, Veo, Hailuo, MiniMax H3, Wan, Grok Imagine or PixVerse video, clip, ad or short. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-pixverse-v2?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-pixverse
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-pixverse-v2?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-pixverse
    requires:
      env:
        - USEAPI_TOKEN
      bins:
        - bash
        - curl
        - jq
    primaryEnv: USEAPI_TOKEN
    envVars:
      - name: USEAPI_TOKEN
        required: true
        description: useapi.net API token (paid useapi.net subscription). Sent only to api.useapi.net in the Authorization header.
      - name: USEAPI_EMAIL
        required: false
        description: Which of your connected PixVerse accounts to use, by its email.
      - name: OUT_DIR
        required: false
        description: Folder for the saved videos (default the current folder).
    install:
      - kind: brew
        formula: jq
        bins:
          - jq
---

# Seedance 2.5, Kling 4.0, Veo 3.1 and more: AI video on your PixVerse plan, with the useapi.net API

These scripts call the [useapi.net PixVerse API](https://useapi.net/docs/api-pixverse-v2?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-pixverse), a third-party REST API (not affiliated with PixVerse) that runs [PixVerse](https://pixverse.ai) on the user's own PixVerse account. PixVerse offers Seedance 2.5, Kling 4.0, Veo 3.1, MiniMax H3 (Hailuo 3.0), Wan 3.0, Grok Imagine and its own PixVerse V6 in one place, and the model is one parameter. Videos spend credits from the user's PixVerse plan. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A PixVerse account with a PixVerse plan, connected to useapi.net once on the useapi.net side: https://useapi.net/docs/start-here/setup-pixverse. PixVerse is paid for separately, to PixVerse. The useapi.net docs (November 2026) say a free Basic account runs PixVerse models up to 540p, Standard ($10 a month) up to 720p, and every third-party model (Seedance, Kling, Veo, MiniMax H3, Wan, Grok Imagine) needs Pro ($30 a month) or higher. Check https://app.pixverse.ai/subscribe for current plans. Use a separate PixVerse account for the API, as the setup guide recommends, and do not use it in the PixVerse website at the same time.
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: it picks one of your connected PixVerse accounts, by email. Without it the API picks a connected account.

This skill does not sign in to PixVerse or read browser cookies on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token, and downloads results from the links the API returns.

## Video: one command

```bash
bash {baseDir}/scripts/video.sh "<prompt>" [key=value ...]
```

A `first_frame_path` value that is an existing local image is uploaded first. It prints progress on stderr and the saved `.mp4` path on stdout (`OUT_DIR` sets the folder). The default model is `v6` (PixVerse V6, 720p, 5 seconds), because it is the one model that works on every paid PixVerse plan, Standard included. For the third-party models, pass `model=`. A clip usually takes 1 to 5 minutes: run it in the background or with a timeout of at least 30 minutes, and do not start a second copy while it runs.

```bash
# Default model, PixVerse V6: 5 s, 720p
bash {baseDir}/scripts/video.sh "A lighthouse keeper climbs the spiral stairs at dusk, lantern swinging. Slow handheld follow shot."

# Seedance 2.5, vertical for Shorts and Reels, 8 s
bash {baseDir}/scripts/video.sh "A courier on a bicycle weaves through a night market, neon reflections on wet streets." \
  model=seedance-2.5 quality=720p duration=8 aspect_ratio=9:16

# Kling 4.0, 1080p
bash {baseDir}/scripts/video.sh "A red panda eats bamboo in a misty forest, shallow depth of field." \
  model=kling-4.0 quality=1080p duration=5

# Veo 3.1 Fast (4, 6 or 8 s; 1080p needs 8 s)
bash {baseDir}/scripts/video.sh "Waves hit a rocky shore at sunrise, gulls overhead." model=veo-3.1-fast quality=720p duration=4

# Animate a photo as the first frame (the photo's ratio is used, so no aspect_ratio)
bash {baseDir}/scripts/video.sh "The paper boat drifts down the gutter stream and into the drain." \
  model=seedance-2.5 first_frame_path=./boat.jpg duration=5
```

Options:

- `model`: `v6` (default), `v5.6`, `pixverse-c1`, `seedance-2.5`, `seedance-2.5-flash`, `seedance-2.0`, `seedance-2.0-fast`, `seedance-2.0-mini`, `kling-4.0`, `kling-o3`, `kling-v3`, `grok-imagine`, `grok-imagine-1.5` (image to video only), `veo-3.1-lite`, `veo-3.1-fast`, `veo-3.1-standard`, `minimax-h3` and `minimax-h3-max` (Hailuo 3.0), `wan-3.0`, `happyhorse-1.0`, `gemini-omni-flash`, `flux-3.0`. All except the PixVerse models need Pro or higher.
- `duration` (seconds) and `quality` (resolution): the API requires both on every model except `v6`, `v5.6`, `v5.5`, `v5` and `v5-fast`. If you leave them out the script sends the cheapest sensible value: 5 seconds (4 for Veo), and 720p (480p for Seedance and Grok Imagine, 768p for MiniMax H3). Tell the user the choice, or ask first when cost matters.
- `aspect_ratio`: `16:9` is the API default for text-to-video, `9:16` for phone video, and others by model. Ask the user which one: forgetting it is the most common wasted generation. Not accepted with `first_frame_path`, where the image decides.
- `audio=true|false`: sound. Seedance 2.5, Kling 4.0, MiniMax H3 and Gemini Omni Flash always have sound and reject `audio`. Veo 3.1 Standard and Fast always have it. On Seedance 2.0, Kling O3 and 3.0, FLUX 3 and Wan 3.0, leaving `audio` out turns sound on; send `audio=false` to turn it off (on Kling O3 and 3.0 sound adds 40% to the cost).
- `first_frame_path`: a local image to animate. Up to about 2K.

Limits for each model (durations, resolutions, ratios, prompt length): https://useapi.net/docs/api-pixverse-v2/model-capabilities. Every option: https://useapi.net/docs/api-pixverse-v2/post-pixverse-videos-create-v4

## Costs

Two bills: the useapi.net subscription ($15/month) and the user's own PixVerse plan, whose credits the videos spend. PixVerse credits per second of video, from the useapi.net docs (November 2026, before each plan's discounts; PixVerse changes them often):

| Model | Resolution | Credits per second |
|---|---|---|
| PixVerse V6, with sound | 720p | 10 |
| Seedance 2.5 | 480p / 720p / 1080p | 35 / 75 / 170 |
| Kling 4.0 | 720p / 1080p | 50 / 75 |
| Veo 3.1 Fast | 720p or 1080p | 60 |
| MiniMax H3 | 768p | 30 |
| Wan 3.0 | 720p | 30 |
| Grok Imagine | 480p / 720p | 10 / 15 |

Example: 5 seconds of Seedance 2.5 at 480p is 175 credits. Pro and higher plans get per-model discounts that change without notice. The costs of every model and plan: https://useapi.net/docs/api-pixverse-v2#pricing. Tell the user the credit cost before generating anything over 10 s or above 720p.

## Step by step (for more control)

1. Upload a local first frame (prints an upload path):
   ```bash
   IMG=$(bash {baseDir}/scripts/upload.sh ./photo.jpg)
   ```
2. Start the video. It prints the video id (and logs it on stderr):
   ```bash
   VID=$(bash {baseDir}/scripts/generate.sh "She turns and smiles at the camera." model=kling-4.0 first_frame_path="$IMG" duration=5 quality=720p)
   ```
3. Wait for it (polls every 10 s; the API answers 404 while a video is still processing) and save the final record:
   ```bash
   bash {baseDir}/scripts/wait-job.sh "$VID" > job.json
   ```
4. Download the video. Prints the saved path:
   ```bash
   bash {baseDir}/scripts/download.sh job.json ./out
   ```

## Timeouts and resuming

If a run is interrupted after `video user:...` was logged, do not run it again: that spends the credits twice. Resume with the video id:

```bash
bash {baseDir}/scripts/wait-job.sh "<video_id>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

`wait-job.sh` stops after 30 minutes unless you pass a second argument in seconds. The scripts never retry a generation request on their own, for the same reason.

## Errors

Every failed request prints the API's error and a one-line hint. The common ones:

- `HTTP 400`: a parameter was rejected (the message names it): a duration, resolution or ratio the model does not take.
- `HTTP 401`: the token is wrong. `HTTP 402`: the useapi.net subscription has expired.
- `HTTP 404`: no PixVerse account connected.
- `HTTP 412`: the PixVerse account is out of credits, or its plan does not include the model (third-party models need Pro or higher).
- `HTTP 422`: PixVerse moderation refused the prompt. Rephrase it.
- `HTTP 429`: the account is busy with other jobs. Wait 10 to 30 seconds and send it once more. Do not loop on it.
- `HTTP 596`: the PixVerse account has a pending error (password changed, suspended or banned). Add it again: https://useapi.net/docs/api-pixverse-v2/post-pixverse-accounts-email
- A video with status `MODERATED` or `FAILED` prints a hint. Do not retry a moderated prompt unchanged: PixVerse can suspend accounts that repeatedly break its content rules.

## After it finishes

Tell the user the file path, the model, the duration and the resolution. The video is also in the account's PixVerse history.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by PixVerse. Seedance, Kling, Veo, MiniMax, Hailuo, Wan and Grok are the names of their owners' products; this skill only runs them through PixVerse.
- API docs: https://useapi.net/docs/api-pixverse-v2?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-pixverse
- Example code and a hosted MCP server: https://github.com/useapi/pixverse-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

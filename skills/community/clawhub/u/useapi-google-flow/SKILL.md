---
name: useapi-google-flow
description: Make Veo 3.1 and Omni 1.1 Flash (Gemini Omni Flash) videos and Nano Banana images (Nano Banana 2, Nano Banana Pro) in Google Flow on your own Google AI subscription, through the useapi.net Google Flow API, a third-party paid API not affiliated with Google. Text-to-video, reference images of people or products, start and end frames, preset voices, video-to-video edits; saves the .mp4 or .jpg. Use when the user asks for a Veo, Veo 3.1, Omni Flash, Gemini Omni, Nano Banana or Google Flow video, clip, ad or image. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-google-flow-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-google-flow-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow
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
        description: Which of your connected Google accounts to use, when you connected more than one to useapi.net.
      - name: OUT_DIR
        required: false
        description: Folder for the saved videos and images (default the current folder).
    install:
      - kind: brew
        formula: jq
        bins:
          - jq
---

# Google Flow video and images: Veo 3.1, Omni 1.1 Flash and Nano Banana with the useapi.net API

These scripts call the [useapi.net Google Flow API](https://useapi.net/docs/api-google-flow-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow), a third-party REST API (not affiliated with Google) that runs Google Flow on the user's own Google account. Videos spend Flow credits from the user's Google AI subscription. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A Google account connected to useapi.net once, on the useapi.net side: https://useapi.net/docs/start-here/setup-google-flow. The setup guide recommends a dedicated Gmail account for this, not the user's personal one. Images and Veo 3.1 Fast and Lite work on a free Google account's daily Flow credits; Omni 1.1 Flash needs Google AI Plus, Pro or Ultra.
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: if the user connected more than one Google account, it names the one to use.

This skill does not sign in to Google, read browser cookies or use Google OAuth tokens on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token, and downloads results from the signed links the API returns.

## Video: one command

```bash
bash {baseDir}/scripts/video.sh "<prompt>" [key=value ...]
```

Values that are existing local files (for `referenceImage_N`, `startImage`, `endImage`, `referenceVideo_1`) are uploaded first. It prints progress on stderr and the saved `.mp4` paths on stdout (`OUT_DIR` sets the folder). The script's default model is `omni-flash`; pass `model=veo-3.1-fast` (or `veo-3.1-quality`, `veo-3.1-lite`, `veo-3.1-lite-low-priority`) for Veo. A clip usually takes 1 to 3 minutes: run it in the background or with a timeout of at least 10 minutes, and do not start a second copy while it runs.

```bash
# Text to video, 8 s landscape at 720p
bash {baseDir}/scripts/video.sh "A lighthouse keeper climbs the spiral stairs at dusk, lantern swinging. Slow handheld follow shot."

# Veo 3.1 Fast instead of Omni Flash
bash {baseDir}/scripts/video.sh "Waves crash on black volcanic sand at sunrise, drone shot." model=veo-3.1-fast

# A presenter from a photo, speaking with a preset voice, portrait for Shorts and Reels
bash {baseDir}/scripts/video.sh "The woman in @referenceImage_1 holds up the mug, smiles and says: 'Honestly the best coffee I've had all year.' Handheld phone camera." \
  referenceImage_1=./presenter.jpg referenceAudio_1=Kore aspectRatio=portrait duration=6

# Animate from a first frame to a last frame
bash {baseDir}/scripts/video.sh "The paper boat drifts down the gutter stream and into the drain." startImage=./first.png endImage=./last.png

# A cheap Omni draft: 360p costs about half
bash {baseDir}/scripts/video.sh "..." resolution=360p duration=4
```

## Images (Nano Banana): one command

```bash
bash {baseDir}/scripts/image.sh "<prompt>" [key=value ...]
```

- `model`: `nano-banana-2-lite` (the API default), `nano-banana-2` (Nano Banana 2.1) or `nano-banana-pro`.
- `aspectRatio`: `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, or `auto` (only with a reference image).
- `reference_1` to `reference_10`: local image files (uploaded first) or asset ids, for image-to-image edits.
- `count` 1 to 4. The script asks for 1 image unless you pass `count`; the API's own default is 4.

It waits for the answer (usually 10 to 20 seconds) and prints the saved `.jpg` paths.

```bash
bash {baseDir}/scripts/image.sh "A paper boat on a rain puddle, macro photo, soft morning light" model=nano-banana-pro aspectRatio=1:1
bash {baseDir}/scripts/image.sh "Put the mug from @reference_1 on a marble kitchen counter" reference_1=./mug.png
```

If Google moderates an image (`HTTP 400` or `500`), rephrase, retry once, or try another of the three models; each moderates differently.

## Costs and limits

Videos spend Flow credits from the user's Google AI plan:

| Model | Credits per clip |
|---|---|
| Omni 1.1 Flash 720p, 4 / 6 / 8 / 10 s | 7 / 10 / 12 / 15 (video-to-video edit 20) |
| Omni 1.1 Flash 360p, 4 / 6 / 8 / 10 s | 4 / 5 / 6 / 7 (edit 10) |
| Veo 3.1 Fast | 20 (10 on Ultra) |
| Veo 3.1 Quality | 100 |
| Veo 3.1 Lite | 10 (5 on Ultra) |
| Veo 3.1 Lite lower priority (`veo-3.1-lite-low-priority`) | 0, Ultra $199.99 plan owner only |

- `aspectRatio`: `landscape` (default) or `portrait`. Ask the user which one; for phone video it is `portrait`, and forgetting it is the most common wasted generation. Veo also accepts `1:1`, `4:3` and `3:4`.
- `duration`: 4, 6, 8 (default) or 10 seconds. `count` (1 to 4) multiplies the cost.
- Omni generates at 360p or 720p; Veo has no 360p. POST /videos/upscale takes a clip to 1080p for free on paid plans, or to 4K on Ultra.
- Veo takes up to 3 reference images and one voice (neither on `veo-3.1-quality`). Omni takes up to 7 references (`referenceImage_*` and `character_*` together) and up to 5 voices.
- Tell the user the credit cost before generating more than one clip or anything over 8 s.

## Writing prompts that work

- **Put the physical action first.** Models drop trailing clauses. "He blinks twice, then looks into the lens and says..." works; "...and then at the end he blinks" often does not happen.
- **Spoken lines go in quotes** after "says:". One or two short sentences per 8 s clip.
- **A voice needs a face.** `referenceAudio_N` (a preset name like `Kore`, `Charon`, `Puck`, `Aoede`, or a voice id) works only together with a `referenceImage_N`, a `character_N` or a video edit.
- **Point at references in the prompt** with `@referenceImage_1`, `@character_1`, `@referenceAudio_1` (videos) or `@reference_1`, `@character_1` (images). Each marker needs its matching parameter.
- **Name the camera**: "handheld phone camera", "static tripod shot", "slow push-in".
- `startImage`/`endImage` mode takes no other references and no voice.

## Step by step (for more control)

1. Upload local files (each prints an asset id). Without `USEAPI_EMAIL`, set it to the first upload's account before the next upload, or the generation is rejected for mixing accounts; `video.sh` and `image.sh` do this for you.
   ```bash
   IMG=$(bash {baseDir}/scripts/upload.sh ./presenter.jpg)
   ```
2. Start the video. It prints the job id (and logs it on stderr):
   ```bash
   JOB=$(bash {baseDir}/scripts/generate.sh "The woman in @referenceImage_1 waves and says: 'Hi!'" referenceImage_1="$IMG" referenceAudio_1=Kore)
   ```
3. Wait for it (polls every 10 s) and save the final record:
   ```bash
   bash {baseDir}/scripts/wait-job.sh "$JOB" > job.json
   ```
4. Download the video(s). Prints the saved paths:
   ```bash
   bash {baseDir}/scripts/download.sh job.json ./out
   ```

Every video option: https://useapi.net/docs/api-google-flow-v1/post-google-flow-videos. Every image option: https://useapi.net/docs/api-google-flow-v1/post-google-flow-images

## Timeouts and resuming

If a video run is interrupted after `job j...` was logged, do not run it again: that spends the credits twice. Resume with the job id:

```bash
bash {baseDir}/scripts/wait-job.sh "<jobid>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

The scripts never retry a generation request on their own, for the same reason.

## Errors

Every failed request prints the API's error and a one-line hint. The common ones:

- `HTTP 400`: a parameter was rejected (the message names it), or Google refused the content. For a content refusal, rephrase the prompt or change the image.
- `HTTP 401`: the token is wrong. `HTTP 404`: `USEAPI_EMAIL` is not a connected account.
- `HTTP 402`: the Google account has no Google AI subscription the model needs, or no Flow credits left.
- `HTTP 403`: Google rejected the captcha on every try (wait a minute, try once more), or `MODEL_ACCESS_DENIED` (the account's plan does not include the model).
- `HTTP 429`: the account is busy or out of quota. `retryAfter` says when to try again. Do not loop on it.
- `HTTP 503`: Google is temporarily overloaded. Try again in a minute or two, with fewer references or a lower `count`.
- `HTTP 596`: the Google account needs reconnecting: https://useapi.net/docs/start-here/setup-google-flow

## After it finishes

Tell the user the file path(s), the duration and the credits it used. Video and image links stay valid for about 6 hours. The results are also in the user's Google Flow project.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by Google. Google Flow, Veo, Gemini and Nano Banana are Google's names for its products.
- API docs: https://useapi.net/docs/api-google-flow-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow
- Example code, n8n templates and a hosted MCP server: https://github.com/useapi/google-flow-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

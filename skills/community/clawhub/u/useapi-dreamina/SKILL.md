---
name: useapi-dreamina
description: Make Seedance 2.5 AI videos in Dreamina (CapCut) by ByteDance on your own Dreamina plan, through the useapi.net Dreamina API, a third-party paid API not affiliated with ByteDance or CapCut. Text-to-video and image-to-video from a photo, a start and end frame or reference images, video and audio (real faces accepted on Seedance 2.5), 4 to 30 seconds, 480p, 720p or 1080p (4K on Canada accounts), 16:9, 9:16 and other ratios, plus cheap 480p drafts finished in 1080p or 4K. Saves the .mp4. Use when the user asks for a Seedance, Seedance 2.5, Seedance 2.0, Dreamina or CapCut AI video, clip, ad or short. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-dreamina-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-dreamina
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-dreamina-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-dreamina
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
        description: Which of your connected Dreamina accounts to use, by its email or its account id such as CA:you@example.com.
      - name: OUT_DIR
        required: false
        description: Folder for the saved videos (default the current folder).
    install:
      - kind: brew
        formula: jq
        bins:
          - jq
---

# Seedance 2.5 video with Dreamina and the useapi.net API

These scripts call the [useapi.net Dreamina API](https://useapi.net/docs/api-dreamina-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-dreamina), a third-party REST API (not affiliated with ByteDance or CapCut) that runs [Dreamina](https://dreamina.capcut.com/) (CapCut) by ByteDance on the user's own Dreamina account. Videos spend credits from the user's Dreamina plan. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API and connects up to 3 Dreamina accounts (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A Dreamina account with a paid Dreamina plan (Seedance video needs one), connected to useapi.net once on the useapi.net side: https://useapi.net/docs/start-here/setup-dreamina. An account is US or Canada (CA). Seedance 2.5 at 4K and Seedance 2.5 Flash need a Canada account.
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: it picks one of your connected accounts, by email or as `CA:you@example.com`.

This skill does not sign in to Dreamina or read browser cookies on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token, and downloads results from the signed links the API returns.

## Video: one command

```bash
bash {baseDir}/scripts/video.sh "<prompt>" [key=value ...]
```

Values that are existing local files (for `firstFrameRef`, `endFrameRef`, `omni_N_imageRef`, `omni_N_videoRef`, `omni_N_audioRef`) are uploaded first. It prints progress on stderr and the saved `.mp4` path on stdout (`OUT_DIR` sets the folder). The default model is `seedance-2.5`. A clip usually takes 1 to 3 minutes: run it in the background or with a timeout of at least 15 minutes, and do not start a second copy while it runs.

```bash
# Text to video: 8 s, vertical for Shorts and Reels, 720p
bash {baseDir}/scripts/video.sh "A lighthouse keeper climbs the spiral stairs at dusk, lantern swinging. Slow handheld follow shot." \
  ratio=9:16 duration=8 resolution=720p

# A person from a photo (reference image, cited in the prompt as @image1)
bash {baseDir}/scripts/video.sh "@image1 holds up a coffee mug, smiles and says: 'Best coffee I've had all year.' Handheld phone camera." \
  omni_1_imageRef=./presenter.jpg ratio=9:16 duration=6

# Animate a photo as the first frame (the photo's aspect ratio is used, so no ratio)
bash {baseDir}/scripts/video.sh "The paper boat drifts down the gutter stream and into the drain." firstFrameRef=./boat.jpg

# From a first frame to a last frame (both images the same aspect ratio)
bash {baseDir}/scripts/video.sh "Day turns to night over the city skyline." firstFrameRef=./day.jpg endFrameRef=./night.jpg duration=10
```

Options:

- `model`: `seedance-2.5` (default), `seedance-2.5-draft` (see below), `seedance-2.5-flash` (Canada accounts, faster, fewer credits, 480p or 720p), or `seedance-2.0`, `seedance-2.0-fast`, `seedance-2.0-mini`.
- `ratio`: `16:9` (the API default), `9:16`, `1:1`, `4:3`, `3:4`, `21:9`. Ask the user which one: for phone video it is `9:16`, and forgetting it is the most common wasted generation. Not with `firstFrameRef`, where the image decides.
- `duration`: seconds, default 5. 4 to 30 on the Seedance 2.5 models, 4 to 15 on Seedance 2.0. On `seedance-2.5`, 31 to 180 is long video mode: priced higher, and takes about 15 minutes (use a timeout of at least 40 minutes).
- `resolution`: Seedance 2.5 defaults to `480p` (about half the credits of `720p`). It also takes `720p`, `1080p`, and `4k` on Canada accounts. The Seedance 2.0 models default to `720p`.
- References: up to 30 images (`omni_1_imageRef` ... cited as `@image1` ...), 10 videos (`@video1`) and 10 audio clips (`@audio1`) on `seedance-2.5`, 50 in all. A reference that the prompt does not mention is ignored. References cannot be mixed with `firstFrameRef` / `endFrameRef`.
- `unlimited=true`: only for an account that has Dreamina's Unlimited from its November 2026 plan offers. Then the video uses no credits, for Seedance 2.5 at 480p or 720p up to 30 s, drafts at 480p, and the Seedance 2.0 models at 720p. Dreamina decides which models and resolutions an account gets and for how long, can end it early, and runs one Unlimited job at a time per account. An account without it answers `412`.

Every option: https://useapi.net/docs/api-dreamina-v1/post-dreamina-videos

## Draft first, then full quality

A 480p `seedance-2.5-draft` costs a sixth to a seventh of the same video at 1080p. When the user likes it, the same draft becomes a 1080p video (or 4K on a Canada account), with the same shot, motion and timing:

```bash
bash {baseDir}/scripts/video.sh "Pretty lady dancing in a neon-lit street" model=seedance-2.5-draft ratio=9:16 duration=5
# The log shows the draft's job id ("job j..."). After the user approves the draft:
bash {baseDir}/scripts/full-quality.sh "<draft jobid>" 1080p
```

The full-quality video costs the same as making it with `seedance-2.5` at that resolution, so the draft pays off when a prompt would otherwise be tried more than once. A draft can be used for 14 days.

## Real faces and content

- Seedance 2.5 accepts real human faces: a photographic portrait works as `omni_N_imageRef` or `firstFrameRef`, and the identity carries through the clip. The Seedance 2.0 models reject them. Use only photos the user has the rights to.
- Recognisable third-party content is refused (`code 2053`): Dreamina judges the finished video, so describing a costumed superhero, a trademarked landmark or a celebrity look-alike can fail even without naming it. Failed jobs are not charged.

## Costs

Dreamina's credits per second of video (as of November 2026, they change often):

| Model | US account | Canada account |
|---|---|---|
| Seedance 2.5, 480p | 17 | 22 |
| Seedance 2.5, 720p | 37 | 38 |
| Seedance 2.5, 1080p | 91 | 117 |
| Seedance 2.5, 4K | | 129 |
| Seedance 2.5 Draft, 480p | 13 | 17 |
| Seedance 2.5 Flash, 480p / 720p | | 11 / 24 |

Example: 5 seconds of Seedance 2.5 at 480p on a US account is 85 credits. Every Seedance 2.5 reference video adds its length to the billed seconds. Tell the user the credit cost before generating anything over 10 s or above 480p. Every model and rate: https://useapi.net/docs/start-here/setup-dreamina#cost-calculator

## Step by step (for more control)

1. Upload local files (each prints an `assetRef` that works only on that account):
   ```bash
   IMG=$(bash {baseDir}/scripts/upload.sh ./presenter.jpg)
   ```
2. Start the video. It prints the job id (and logs it on stderr):
   ```bash
   JOB=$(bash {baseDir}/scripts/generate.sh "@image1 waves and says: 'Hi!'" omni_1_imageRef="$IMG" ratio=9:16)
   ```
3. Wait for it (polls every 15 s) and save the final record:
   ```bash
   bash {baseDir}/scripts/wait-job.sh "$JOB" > job.json
   ```
4. Download the video. Prints the saved path:
   ```bash
   bash {baseDir}/scripts/download.sh job.json ./out
   ```

## Timeouts and resuming

If a run is interrupted after `job j...` was logged, do not run it again: that spends the credits twice. Resume with the job id:

```bash
bash {baseDir}/scripts/wait-job.sh "<jobid>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

The scripts never retry a generation request on their own, for the same reason.

## Errors

Every failed request prints the API's error and a one-line hint. The common ones:

- `HTTP 400`: a parameter was rejected (the message names it), or the model or resolution is not offered in the account's region.
- `HTTP 401`: the token is wrong. `HTTP 402`: the useapi.net subscription has expired.
- `HTTP 403`: the Dreamina account has no paid plan that includes the model, or Dreamina wants its one-time confirmation (retry once).
- `HTTP 404`: no Dreamina account connected, or the job id is unknown.
- `HTTP 412`: the Dreamina account is out of credits, or has no Unlimited for this request.
- `HTTP 429`: the account is busy with other jobs. Wait and send it once more. Do not loop on it.
- `HTTP 503`: try again in about 30 seconds. `HTTP 596`: the Dreamina account needs reconnecting: https://useapi.net/docs/start-here/setup-dreamina
- A failed job (`status: failed`) prints Dreamina's reason and a hint. Failed jobs are not charged.

## After it finishes

Tell the user the file path, the duration, the resolution and the credits it used. Video links expire about 7 days after generation. The video is also in the account's Dreamina history.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by ByteDance or CapCut. Dreamina and Seedance are ByteDance's names for its products.
- API docs: https://useapi.net/docs/api-dreamina-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-dreamina
- Tutorials: https://useapi.net/docs/articles/dreamina-bash and https://useapi.net/docs/articles/dreamina-seedance-2-5-draft
- Example code and a hosted MCP server: https://github.com/useapi/dreamina-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

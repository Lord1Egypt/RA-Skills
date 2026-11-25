---
name: useapi-muse
description: Make Meta Muse AI images and 10-second videos with sound and spoken dialogue (muse.ai, Meta's AI agent) on your own Muse account, the free plan included, through the useapi.net Muse API, a third-party paid API not affiliated with Meta. Text to image, combine up to 9 photos into one picture, edit an image, restore and colorize an old photo, image to video that makes a photo talk, and video to video such as swapping a person in a clip. Saves the .webp or .mp4. Use when the user asks for a Muse or Meta Muse image or video, a talking photo, an old photo restored or animated, or a person swapped in a video. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-muse-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-muse
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-muse-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-muse
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
        description: Which of your connected Muse accounts to use, when you connected more than one to useapi.net.
      - name: OUT_DIR
        required: false
        description: Folder for the saved images and videos (default the current folder).
    install:
      - kind: brew
        formula: jq
        bins:
          - jq
---

# Meta Muse images and 10-second videos with the useapi.net Muse API

These scripts call the [useapi.net Muse API](https://useapi.net/docs/api-muse-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-muse), a third-party REST API (not affiliated with Meta) that runs on the user's own account at Muse (muse.ai), Meta's AI agent. Every job uses part of the account's weekly Muse allowance. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A Muse account connected to useapi.net once, with its email and password: https://useapi.net/docs/start-here/setup-muse. Muse is available in the US, Canada, Japan and Singapore (as of October 30, 2026), so the account is created there and finishes Muse's onboarding at muse.ai. After that the API works from anywhere. The free Muse plan works.
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: if the user connected more than one Muse account, it names the one to use.

This skill does not sign in to Meta or read browser cookies on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token.

## One command

```bash
bash {baseDir}/scripts/image.sh "<prompt>" [image_1=<file or assetId> ...]
bash {baseDir}/scripts/video.sh "<prompt>" [image_1=... video_1=... audio_1=...]
```

Inputs that are existing local files are uploaded first. Each script prints progress on stderr and the saved file path on stdout (`.webp` for images, `.mp4` for videos), with the job record next to it as `.json`. The new file's `assetId` is logged and is in `.result.assets[0].assetId` of that `.json`: pass it to the next job. `OUT_DIR` sets the folder. An image takes 20 to 60 seconds, a video 60 to 140. Run videos in the background or with a timeout of at least 10 minutes, and do not start a second copy while one runs.

```bash
# Text to image: say the aspect ratio in the prompt
bash {baseDir}/scripts/image.sh "In exactly 16:9 aspect ratio, a cinematic photo of a vintage motorcycle on wet cobblestones at night, fog, 35mm film."

# Combine photos into one picture
bash {baseDir}/scripts/image.sh "In exactly 4:5 aspect ratio, the person from image_1 wearing the jacket from image_2. Keep the face exactly as in image_1." \
  image_1=./me.jpg image_2=./jacket.png

# Make a photo talk: put the spoken line in quotes
bash {baseDir}/scripts/video.sh "Animate image_1 with the same portrait frame: she looks up at the camera, smiles and says softly: \"You came back.\" Keep her face exactly as in image_1." \
  image_1=./grandma.jpg

# Swap a person in a clip
bash {baseDir}/scripts/video.sh "Edit video_1: replace the rider with the woman from image_1, keep everything else the same. Keep the 16:9 frame." \
  video_1=./ride.mp4 image_1=./woman.jpg
```

## Options

- `image_1` to `image_9`: input images (image and video jobs).
- `video_1` to `video_3` and `audio_1` to `audio_3`: input videos and audio (video jobs only).
- Each takes a local file (jpg, png, webp, mp4, mov, webm, mp3, wav, m4a, ogg, at most 50 MB) or an `assetId`. Each parameter needs a file of its own type.
- All inputs of one job must be on the same Muse account. The scripts upload every local file to the account of the first input, or to `USEAPI_EMAIL`.
- `replyUrl` (an https webhook) and `replyRef` (your own reference) are optional.
- There are no model, aspect ratio, resolution or duration parameters. Muse picks its own model.

## Chaining: pass assetIds, never re-upload

Every file Muse makes stays in the account's Muse Library, so its `assetId` goes straight into the next job as `image_N` or `video_N`. Upload only the user's own files. Uploads use no allowance, and the same file always gets the same id.

```bash
PIC=$(bash {baseDir}/scripts/image.sh "In exactly 16:9 aspect ratio, the woman from image_2 riding the motorcycle from image_1 along a beach." image_1=./bike.jpg image_2=./rider.jpg)
PIC_ID=$(jq -r '.result.assets[0].assetId' "${PIC%.*}.json")
bash {baseDir}/scripts/video.sh "Animate image_1: she rides through the waves and shouts: \"Nothing beats this view!\" Keep the 16:9 frame." image_1="$PIC_ID"
```

## Writing prompts that work

- **Aspect ratio**: write `in exactly 16:9 aspect ratio` (or 9:16, 1:1, 4:5, 3:4, 21:9). A looser "cinematic 16:9 landscape photo" once came back 3:2. Image to video keeps the start image's shape unless the prompt asks for another ratio.
- **Length and size**: every video is about 10 seconds at about 720p, with sound. Asking for 5 seconds still gives 10, and asking for 1080p or 4K added no detail in useapi.net's tests. Images are WebP, about 2 to 2.5 megapixels.
- **Dialogue**: spoken lines go in quotes, `she says softly: "..."`. One or two short sentences.
- **Name the inputs** in the prompt: `the woman from image_2 riding the motorcycle from image_1`. A prompt that names an input you did not pass answers `400`.
- **Say what must stay the same**: "keep her face exactly as in image_1".
- **Restore an old photo**: list what to fix (scratches, fading, grain, colorize) and ask for "the same framing, crop and aspect ratio as image_1".
- The prompt can be up to 5000 characters. `result.text` is Muse's own last message, for example "Done, 10 seconds, 16:9 landscape". Pass it on to the user.

## Costs

The job runs on the user's own Muse subscription. Muse has no credits and no price per image or video: it meters each account per week, as a whole percent used. `bash {baseDir}/scripts/account.sh` reads it live (`quota.tier`, `quota.percentUsed`, `quota.resetsAt`).

| Request | Share of the week on the free plan (useapi.net's tests) |
|---|---|
| A video | 2 to 3 percent |
| An image | 0 to 1 percent |
| Upload, download, reading a job or the account | nothing |

Paid Muse plans have bigger weekly allowances: Power $20 a month (500 million Muse tokens a week) and Maximum $100 a month (3 billion), as of October 2026. Muse also limits how many videos an account makes over 24 hours. useapi.net charges nothing per image or video. Tell the user the cost before more than two or three videos.

## Step by step (for more control)

```bash
IMG=$(bash {baseDir}/scripts/upload.sh ./photo.jpg)                                   # prints the assetId
JOB=$(bash {baseDir}/scripts/generate.sh video "Animate image_1: ..." image_1="$IMG")  # prints the job id, sent once
bash {baseDir}/scripts/wait-job.sh "$JOB" > job.json                                  # polls every 10 s
bash {baseDir}/scripts/download.sh job.json ./out                                     # prints the saved .mp4 path
```

`download.sh` also takes an `assetId` to fetch any file again later. Job records are kept for 7 days. Every option: https://useapi.net/docs/api-muse-v1/post-muse-jobs-video

## Timeouts and resuming

`generate.sh`, `image.sh` and `video.sh` send each job once and never retry it: a job sent again after an unclear failure would use the allowance twice. If a run is interrupted after `job j...-bot:muse` was logged, do not run it again. Resume with the job id:

```bash
bash {baseDir}/scripts/wait-job.sh "<jobid>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

Reads, uploads and downloads cost nothing, so those scripts retry network errors and `5xx` answers on their own.

## Errors

Every failed request or failed job prints the API's error and a one-line hint:

- `400`: a parameter was rejected (the message names it), an input of the wrong type, inputs on different accounts, or the prompt names an input that was not passed. Nothing was used.
- `401`: wrong token. `404`: the account is not connected, or the file is no longer in the Muse Library.
- `403`: Muse refused on content grounds (its own words are in the message). Running the same prompt again will not help: rephrase or change the inputs. On a video job, `403` can also mean Meta switched off video for the account in its country or region. Image jobs still work.
- `409`: Muse says the account already made this request or has it queued. Nothing was made. Change the prompt.
- `412`: the account's weekly allowance is used up. Wait for `quota.resetsAt` (`account.sh`).
- `429`: the account is running its `maxJobs`, or Muse is limiting it for about a minute: send once more after a minute. On a video job it can be Muse's 24-hour video limit: `retryAt` says when. Never loop on it.
- `503`: nothing was made. Running the same request again is safe and usually works.
- `502`: Muse made a file the API could not read. Do not resubmit automatically: tell the user and report the job id to useapi.net support.
- `504`: Muse did not finish in time, but it may have made the file. Check `GET /jobs/<jobid>?history=true` and ask the user before running it again.
- `596`: the Muse account needs attention (a Meta security check, a changed password). The user signs in at https://muse.ai, then adds the account again: https://useapi.net/docs/start-here/setup-muse

## After it finishes

Tell the user the file path, what Muse said (`result.text`), and for videos the length (about 10 s). If you read the account, say how much of the week is used and when it resets. Mention that each result's `assetId` can feed the next job with no re-upload.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by Meta. Muse is Meta's name for its product.
- API docs: https://useapi.net/docs/api-muse-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-muse
- Example code, n8n templates and a hosted MCP server: https://github.com/useapi/muse-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

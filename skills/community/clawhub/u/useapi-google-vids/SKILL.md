---
name: useapi-google-vids
description: Make Gemini Omni 1.2 Flash videos (3 to 15 seconds with sound, 720p or 1080p) and talking AI avatars in Google Vids on your own Google AI subscription, through the useapi.net Google Vids API, a third-party paid API not affiliated with Google. Text-to-video, a start image, up to 3 reference images or avatars, extend a clip to about 34 seconds, upscale to 1080p, edit by prompt. Avatars from a description or a photo with one of 30 voices, and talking avatar videos of up to 30 seconds that read your script. Saves the .mp4. Use when the user asks for a Google Vids video, a Gemini Omni or Omni Flash clip, a talking avatar, an AI avatar video, an AI spokesperson, AI influencer or UGC ad presenter. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-google-vids-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-vids
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-google-vids-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-vids
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

# Google Vids: Gemini Omni 1.2 Flash video and talking AI avatars with the useapi.net API

These scripts call the [useapi.net Google Vids API](https://useapi.net/docs/api-google-vids-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-vids), a third-party REST API (not affiliated with Google) that runs Google Vids on the user's own Google account. Videos spend seconds of the monthly Google Vids allowance that comes with the user's Google AI subscription. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A Google account connected to useapi.net once, on the useapi.net side: https://useapi.net/docs/start-here/setup-google-vids. The setup guide recommends a dedicated Gmail account for this, not the user's personal one. Omni videos and images need Google AI Plus, Pro or Ultra. A free Google account makes avatars and talking avatar videos only. Google Workspace smart features must be on (the setup guide shows where).
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: if the user connected more than one Google account, it names the one to use.

This skill does not sign in to Google, read browser cookies or use Google OAuth tokens on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token, and downloads the results through the same API.

## Video: one command

```bash
bash {baseDir}/scripts/video.sh "<prompt>" [key=value ...]
```

Local files given as `startImage` or `referenceImage_N` are uploaded first. It prints progress on stderr and the saved `.mp4` path on stdout, with the job record next to it as `.json` (`OUT_DIR` sets the folder). A clip usually takes 20 seconds to 2 minutes: run it in the background or with a timeout of at least 10 minutes, and do not start a second copy while it runs.

```bash
# Text to video, 8 s landscape at 720p (the defaults)
bash {baseDir}/scripts/video.sh "A lighthouse keeper climbs the spiral stairs at dusk, lantern swinging. Slow handheld follow shot."

# 15 s portrait at 1080p for Shorts and Reels (a clip you will not extend or edit can be 1080p from the start)
bash {baseDir}/scripts/video.sh "Waves crash on black volcanic sand at sunrise, drone shot." duration=15 aspectRatio=portrait resolution=1080p

# A product in the scene, from a local photo
bash {baseDir}/scripts/video.sh "A hand sets @referenceImage_1 on a marble kitchen counter, morning light, slow push-in." referenceImage_1=./mug.png

# Animate from a first frame
bash {baseDir}/scripts/video.sh "The paper boat drifts down the gutter stream and into the drain." startImage=./first.png
```

## Talking avatars: two commands

An avatar is a fixed picture of a person plus one of 30 voices, saved in the account's Google Vids document and reusable by `avatarId`.

```bash
# 1. Make the avatar (prints the avatarId, saves its picture as avatar_<name>.jpg)
AV=$(bash {baseDir}/scripts/avatar.sh "Maya" Kaci appearance="a woman in her late twenties with a curly brown bob and freckles" outfit="cream knit sweater" shot=upper-body)

# 2a. A talking head that reads the script word for word (up to 30 s, 720p landscape)
bash {baseDir}/scripts/talk.sh "$AV" "Hi, I'm Maya. [short pause] Here are three things I wish I knew before my first marathon."

# 2b. Or the avatar acting in an Omni scene, saying the lines in the prompt
bash {baseDir}/scripts/video.sh "@avatar_1 holds up the mug, smiles and says: \"Honestly the best coffee I've had all year.\" Handheld phone camera, natural light." \
  avatar_1="$AV" aspectRatio=portrait duration=6
```

- An avatar starts from exactly one of: `appearance="..."` (Google draws the person, with optional `outfit`, `shot=close-up|upper-body|full-body`, `expression`, `details`), `image=` (a person's photo as a local file, or an image `mediaId` from `image.sh`), or `avatar=<avatarId>` (another avatar's picture, for a new name or voice).
- `refine="..."` changes the picture in words (clothes, background, glasses). `logo=<file>` puts a logo on the clothes like a small pin.
- Use a photo only of someone who agreed to it. Google refuses photos of prominent people and of minors (`422`). The talking video check is stricter, so an avatar from a photo can still be refused there.
- `avatar.sh --voices` lists the voices (for example `Holt` = Charon, informative, `Kaci` = Autonoe, bright). Ask the user or pick one that fits. `avatar.sh --list` shows saved avatars, and `avatar.sh --delete <avatarId>` removes one.
- A clip takes up to 3 references in all: `avatar_1..3` and `referenceImage_1..3` together. Several avatars in one clip make a dialogue. `startImage` can't be combined with them.
- `talk.sh` script: 1 to 400 characters that fit in 30 seconds spoken. Audio tags in square brackets, like `[whisper]` or `[short pause]`, are performed, not read aloud.

## Costs (the Google Vids allowance)

Google Vids meters video in seconds a month, separate from Google Flow credits: Google AI Plus gets 60 s, Pro 500 s, Ultra $99.99 2,500 s and Ultra $199.99 10,000 s, plus up to 50 / 30 / 300 / 1,000 images. A free Google account gets no video seconds or images. Allowances reset on the 1st at 00:00 Pacific.

| Request | Uses |
|---|---|
| A clip (`video.sh`, `generate.sh`) | its `duration` in seconds. `720p` and `1080p` cost the same. Avatars and references add nothing |
| Extend (`extend.sh`) | only the seconds it adds |
| Upscale (`upscale.sh`) | the clip's full length again |
| Edit (`edit.sh`) | at most the seconds it edits (a 15 s edit used 10 in useapi.net's tests) |
| Image (`image.sh`) | 1 image |
| Avatar | 1 image per picture Google makes (a drawing, a reframed photo, a `refine` or `logo` change). Free on an account with no image allowance. Voices are free |
| Talking avatar video (`talk.sh`) | 1 AI avatar video and 1 Gemini use, no video seconds (a free account had 10 avatar videos a month in useapi.net's tests) |
| A request Google refuses (`422` or quota `429`) | nothing, except a talking avatar video refused after it was made |

Every finished job logs what is left this month. Tell the user the cost before anything over 10 seconds or more than one clip.

## 720p first, upscale once at the end

A `1080p` clip is an upscaled `720p` one, and each extend at `1080p` re-sharpens the whole clip until faces look plastic. Make, extend and edit at `720p` (the default), then upscale a finished clip of up to 20 seconds once with `upscale.sh`. A single clip you won't extend or edit can be `resolution=1080p` from the start, for the same seconds. For a `1080p` clip of 21 to 34 seconds, set `resolution=1080p` on the last extend only.

## Writing prompts that work

- **Name references with markers**: `@avatar_1`, `@referenceImage_1`. Each marker needs its parameter. An avatar's name plays no part in the prompt.
- **Spoken lines go in quotes** after "says:". One or two short sentences per 10 seconds of clip. An avatar speaks in its own voice.
- **Put a prop in a person's hands in the first sentence that mentions them** ("@avatar_1, holding @referenceImage_1 in both hands, ..."). A verb like "lifts" later makes the object appear from nowhere.
- **Name the camera**: "static tripod shot", "handheld phone camera, natural light" (reads as real UGC).
- **Extend prompts: the new action only, and name people by what they wear.** An extend gets the clip, not the avatars, so write "the woman in the cream sweater", not `@avatar_1`. Repeat the setting.
- Ask which shape the user wants: `aspectRatio=portrait` for phone video, `landscape` otherwise. Forgetting it is the most common wasted generation.

## Step by step (extend, upscale, edit, images)

```bash
JOB=$(bash {baseDir}/scripts/generate.sh "@avatar_1 waves and says: \"Hi!\"" avatar_1="$AV" duration=5)   # prints the job id
bash {baseDir}/scripts/wait-job.sh "$JOB" > job.json         # polls every 10 s, prints the final record
bash {baseDir}/scripts/download.sh job.json ./out             # prints the saved .mp4 path
M=$(jq -r .result.mediaId job.json)                           # the clip, for the next step
J2=$(bash {baseDir}/scripts/extend.sh "$M" "The woman in the cream sweater laughs and sips from the mug." duration=5)
bash {baseDir}/scripts/wait-job.sh "$J2" > ext.json && bash {baseDir}/scripts/download.sh ext.json ./out
J3=$(bash {baseDir}/scripts/upscale.sh "$(jq -r .result.mediaId ext.json)")   # last step, clips of up to 20 s
bash {baseDir}/scripts/wait-job.sh "$J3" > up.json && bash {baseDir}/scripts/download.sh up.json ./out
```

| Script | Interface |
|---|---|
| `generate.sh "<prompt>" [key=value ...]` | `duration=3..15` (default 8), `aspectRatio=landscape\|portrait`, `resolution=720p\|1080p`, `avatar_1..3`, `referenceImage_1..3`, `startImage` (ids). Prints the job id |
| `extend.sh <mediaId> "<prompt>" [duration= aspectRatio= resolution=]` | adds 3 to 10 s per call and returns the whole clip. Sources up to 24 s, so about 34 s at most |
| `upscale.sh <mediaId>` | a `720p` clip of up to 20 s to `1080p` |
| `edit.sh <mediaId> "<change>" [duration= aspectRatio= resolution=]` | recolour, add an object, restyle. First 15 s only, clips the API made |
| `image.sh "<prompt>" [aspectRatio=16:9\|1:1\|9:16] [style=...]` | one JPEG of about 1 MP. Prints the image `mediaId`, usable as `startImage`, `referenceImage_N` or avatar `image` for a few hours |
| `upload.sh <file>` | JPEG, PNG, WebP or MP4 up to 50 MB. Prints an `assetId` |
| `wait-job.sh <jobid>`, `download.sh <job.json\|-\|mediaId> [OUT_DIR] [NAME]` | wait for a job, save its file |

Every option: https://useapi.net/docs/api-google-vids-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-vids

**Download soon.** Files live in Google's temporary storage: videos for 24 hours, images for a few hours. Avatars stay until deleted.

## Timeouts and resuming

The generation scripts send each request once and never retry it: a request resent after an unclear failure could be charged twice. If a run is interrupted after `job j...` was logged, do not run it again. Resume with the job id:

```bash
bash {baseDir}/scripts/wait-job.sh "<jobid>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

## Errors

Every failed request or failed job prints the API's error and a one-line hint. What matters most is whether it was charged:

- `400`: a parameter was rejected (the message names it). Nothing charged. Also: an extend of a clip over 24 s, an upscale of a clip over 20 s or already `1080p`, a talking-avatar script over 30 s spoken.
- `401`: wrong token. `404`: the account is not connected, or the file expired. `410`: the job is older than 7 days.
- `403`: the account's plan has no Google Vids allowance for this (a free account makes avatars and talking avatar videos only), Google Workspace smart features are off, or the id belongs to another token. Nothing charged.
- `422`: Google refused the prompt or inputs. Nothing charged, except a talking avatar video refused after it was made. Rephrase and try again.
- `429`: the month's allowance is used up (`retryAt` is the reset date), or the account is busy or briefly limited (`retryAt` about a minute away). Nothing charged. Never loop on it.
- `502` on a failed job: Google answered without a usable file and may already have charged it. Do not resubmit automatically: tell the user and report the job id to useapi.net support.
- `503`: Google server error. Try again in a minute or two.
- `504`: Google did not answer in time. It may still have been counted: ask the user before running it again.
- `596`: the Google account is signed out or being re-checked. Retry in a minute. If it persists, reconnect it: https://useapi.net/docs/start-here/setup-google-vids

## After it finishes

Tell the user the file path(s), the duration, the resolution and what it used, plus what is left this month (logged by `wait-job.sh`). Mention that videos expire after 24 hours and that avatars stay on the account until deleted.

Every Google Vids MP4 carries Google's visible Gemini sparkle in a corner and an invisible SynthID watermark. Images have none. A separate open-source [watermark remover](https://github.com/useapi/google-vids-api/tree/main/watermark-remover) (Python, ffmpeg, not part of this skill) takes off the visible sparkle on clips as generated and their upscales.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by Google. Google Vids, Gemini and Gemini Omni are Google's names for its products.
- API docs: https://useapi.net/docs/api-google-vids-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-vids
- Example code, an n8n template and a hosted MCP server: https://github.com/useapi/google-vids-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

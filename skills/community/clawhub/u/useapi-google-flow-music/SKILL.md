---
name: useapi-google-flow-music
description: Make full AI songs with vocals or instrumentals on Google's Lyria 3.5 and Lyria 3 Pro in Google Flow Music on your own Google Flow Music plan (Free, or the one included with Google AI Plus, Pro or Ultra), through the useapi.net Google Flow Music API, a third-party paid API not affiliated with Google. Song from a text prompt, your own lyrics or lyrics the model writes, AI lyrics writing, and stems (drums, bass, vocals, other). Saves .m4a, .wav or .mp3. Use when the user asks for a Google Flow Music, Lyria or Lyria 3.5 song, an AI song, AI music, a song with vocals, an instrumental track, song lyrics or stems. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-flowmusic-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow-music
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-flowmusic-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow-music
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
        description: Which of your connected Google Flow Music accounts to use, when you connected more than one to useapi.net.
      - name: OUT_DIR
        required: false
        description: Folder for the saved songs and stems (default the current folder).
    install:
      - kind: brew
        formula: jq
        bins:
          - jq
---

# Google Flow Music songs: Lyria 3.5 and Lyria 3 Pro with the useapi.net API

These scripts call the [useapi.net Google Flow Music API](https://useapi.net/docs/api-flowmusic-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow-music), a third-party REST API (not affiliated with Google) that runs Google Flow Music on the user's own Google Flow Music account. Songs spend Google Flow Music credits from that account's plan. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A Google Flow Music account connected to useapi.net once, on the useapi.net side: https://useapi.net/docs/start-here/setup-flowmusic. The setup guide strongly recommends a dedicated Google account for this, not the user's personal one.
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: if the user connected more than one Google Flow Music account, it names the one to use.

Google Flow Music has its own plans: Free (daily top-up credits), Starter $8, Plus $24 and Member $64 a month (as of November 2026). Google AI Plus, Pro and Ultra include its Starter, Plus and Member plans, with Google Flow Music credits kept separate from the Google AI credits. To get the included plan, the user signs in once at flowmusic.app with that Google account and lets it see the Google One membership, before connecting the account to useapi.net (or connects it again afterwards).

This skill does not sign in to Google, read browser cookies or use Google OAuth tokens on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token, and downloads the audio from the links the API returns.

## A song: one command

```bash
bash {baseDir}/scripts/song.sh "<prompt>" [key=value ...]
```

It starts the song, waits for it and saves the audio. It prints progress on stderr (with each clip's title, length and clip id) and the saved paths on stdout (`OUT_DIR` sets the folder). One request makes one or two songs (an A/B pair), each up to about 3 minutes long. A song usually takes 40 to 150 seconds: run it in the background or with a timeout of at least 10 minutes, and do not start a second copy while it runs.

- `prompt` (1 to 10,000 characters): style, mood, genre, instruments, BPM and any vocal direction ("soft female vocals", "male rap verse").
- `model`: `lyria-3.5` (this script's default, Google's current flagship) or `lyria-3-pro` (the API's own default). Both cost the same per song.
- `instrumental=true` forces an instrumental. Without it the model decides from the prompt whether to sing.
- `lyrics`: the user's own lyrics, as text or a local `.txt` file, ideally tagged `[Verse]` / `[Chorus]` (up to 10,000 characters). The song then sings those words. `instrumental=true` overrides it.
- `ghostwriter`: `standard` or `pro`, the lyrics writer when the model writes the lyrics.
- `format`: `m4a` (default), `wav` or `mp3`.

```bash
# A sung song, lyrics written by the model
bash {baseDir}/scripts/song.sh "warm indie folk ballad, acoustic guitar, soft female vocals, 70 bpm, wistful and hopeful" ghostwriter=pro

# An instrumental, saved as WAV
bash {baseDir}/scripts/song.sh "energetic synthwave, driving bass, retro 80s, 120 bpm" instrumental=true format=wav

# The user's own lyrics
bash {baseDir}/scripts/song.sh "soulful R&B, lush keys, 90 bpm" lyrics=./lyrics.txt

# Lyria 3 Pro instead of Lyria 3.5
bash {baseDir}/scripts/song.sh "lo-fi hip hop, mellow piano, 80 bpm" model=lyria-3-pro
```

## Lyrics first (optional)

```bash
bash {baseDir}/scripts/lyrics.sh "a nostalgic song about a long road trip home" structure="Verse 1 / Chorus / Verse 2 / Chorus / Bridge / Outro" > lyrics.txt
```

It writes `[Verse]` / `[Chorus]` tagged lyrics to stdout, and a title and a matching style prompt (`sound_prompt`) to stderr. No audio is made, but it still uses a very small amount of credit. Show the lyrics to the user, then sing them with `song.sh "<sound_prompt or the user's style>" lyrics=./lyrics.txt`.

## Stems (optional)

```bash
bash {baseDir}/scripts/stems.sh "<clip id>" [m4a|wav|mp3]
```

It splits one song into four stems, drums, bass, vocals and other, and saves them. Take the clip id from `song.sh`'s log, or `jq -r '.clips[0].clip' job.json`. The split usually takes 15 to 60 seconds. If it takes longer, the API answers 504 and keeps splitting, so the script asks again up to 3 times: a clip that is already split answers at once.

## Costs and limits

- A song is 5 credits on either model, and one request makes one or two songs. Starter's 3,000 credits a month make about 600 songs, Plus's 10,000 about 2,000, Member's 30,000 about 6,000. The Free plan makes songs from its daily top-up credits.
- Stems spend credits from the same plan. Lyrics use a very small amount. Downloads (m4a, wav, mp3) are free.
- Each account runs a limited number of songs at once (2 on Free, 8 on Starter, 12 on Plus, 16 on Member). Tell the user the credit cost before making more than a couple of songs.

## Step by step (for more control)

1. Start the song. It prints the job id (and logs it on stderr):
   ```bash
   JOB=$(bash {baseDir}/scripts/generate.sh "dreamy synthwave, 100 bpm, airy female vocals" model=lyria-3.5)
   ```
2. Wait for it (polls every 10 s) and save the final record:
   ```bash
   bash {baseDir}/scripts/wait-job.sh "$JOB" > job.json
   ```
3. Download the songs. Prints the saved paths:
   ```bash
   bash {baseDir}/scripts/download.sh job.json ./out [m4a|wav|mp3]
   ```

`job.json` also holds each clip's `lyrics`, `title`, `duration_s` and `image_url` (cover art). Every song option: https://useapi.net/docs/api-flowmusic-v1/post-flowmusic-music. Covers, remixes, extends, section replacements and effects: https://useapi.net/docs/api-flowmusic-v1/post-flowmusic-music-edit

## Timeouts and resuming

If a run is interrupted after `job job:...` was logged, do not run it again: that spends the credits twice. Resume with the job id:

```bash
bash {baseDir}/scripts/wait-job.sh "<jobid>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

The scripts never retry a song request on their own, for the same reason.

## Errors

Every failed request prints the API's error and a one-line hint. The common ones:

- `HTTP 400`: a parameter was rejected (the message names it), or no working Google Flow Music account is connected.
- `HTTP 401`: the token is wrong. `HTTP 404`: `USEAPI_EMAIL` is not a connected account, or the clip is gone.
- `HTTP 402`: the Google Flow Music account is out of credits.
- `HTTP 422`, or a job that ends `failed` with `moderation_reject`: the model made no audio, usually a content refusal. Rephrase the prompt or the lyrics.
- `HTTP 429`: the account is already running as many songs as it may at once. Wait until one finishes, then send it once more. Do not loop on it.
- `HTTP 596`: the Google Flow Music account needs reconnecting: https://useapi.net/docs/start-here/setup-flowmusic

## After it finishes

Tell the user the file paths, each song's title and length, and that it used 5 credits per song. The audio links in `job.json` are signed, so download promptly. The songs also stay on the user's Google Flow Music account.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by Google. Google Flow Music and Lyria are Google's names for its products.
- API docs: https://useapi.net/docs/api-flowmusic-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow-music
- Example code, a Claude Code plugin, a Gemini CLI extension and a hosted MCP server: https://github.com/useapi/flowmusic-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

---
name: useapi-gemini-notebook
description: Turn web pages, YouTube videos, pasted text or local files (PDF, Word, PowerPoint, EPUB, audio) into a Gemini Notebook (NotebookLM) Audio Overview podcast (.m4a), Video Overview (.mp4) or slide deck (.pdf and .pptx) on your own Google account, through the useapi.net Gemini Notebook API (NotebookLM API), a third-party paid API not affiliated with Google. Google renamed NotebookLM to Gemini Notebook. Use when the user asks for a NotebookLM or Gemini Notebook podcast, Audio Overview, Video Overview, explainer video or slides, or to turn articles or documents into a podcast or deck. Needs bash, curl, jq and USEAPI_TOKEN.
version: 1.0.0
homepage: https://useapi.net/docs/api-gemini-notebook-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-gemini-notebook
metadata:
  author: useapi.net
  openclaw:
    homepage: https://useapi.net/docs/api-gemini-notebook-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-gemini-notebook
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
        description: Folder for the downloaded files (default the current folder).
    install:
      - kind: brew
        formula: jq
        bins:
          - jq
---

# Gemini Notebook (NotebookLM): podcasts, Video Overviews and slides with the useapi.net API

These scripts call the [useapi.net Gemini Notebook API (NotebookLM API)](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-gemini-notebook), a third-party REST API (not affiliated with Google) that runs Gemini Notebook (NotebookLM) on the user's own Google account. Every script is in `{baseDir}/scripts/` (`{baseDir}` is this skill's folder). Run them with bash.

## What the user needs (tell them if something is missing)

1. A useapi.net account and API token in `USEAPI_TOKEN`: https://useapi.net/docs/start-here/setup-useapi. useapi.net is a paid service: one $15/month subscription covers every useapi.net API (https://useapi.net/docs/subscription). Never print the token or write it to a file.
2. A Google account connected to useapi.net once, on the useapi.net side: https://useapi.net/docs/start-here/setup-gemini-notebook. The setup guide recommends a dedicated Gmail account for this, not the user's personal one. The free Google plan works; cinematic Video Overviews need Google AI Pro or Ultra.
3. `bash`, `curl` and `jq` installed.

`USEAPI_EMAIL` is optional: if the user connected more than one Google account, it names the one to use.

This skill does not sign in to Google, read browser cookies or use Google OAuth tokens on the user's machine. It only sends HTTPS requests to `api.useapi.net` with the useapi.net token. Nothing runs locally besides curl, so a job keeps going on the server if the agent stops.

## Fastest path: one command

```bash
bash {baseDir}/scripts/studio.sh audio|video|slides "<title>" <URL or local file> [more ...] [-- key=value ...]
```

It creates a notebook, adds the sources (existing local files are uploaded, everything else is added as a URL), waits until Google has read them, generates, waits and downloads. It prints progress on stderr and the saved paths on stdout (`OUT_DIR` sets the folder).

```bash
# A podcast (Audio Overview), short brief
bash {baseDir}/scripts/studio.sh audio "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 ./notes.pdf -- format=brief length=short

# A Video Overview in the whiteboard style
bash {baseDir}/scripts/studio.sh video "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 -- format=explainer style=whiteboard

# A slide deck (saves .pdf and .pptx)
bash {baseDir}/scripts/studio.sh slides "Q3 report" ./q3-report.pdf -- format=presenter length=short
```

`podcast.sh "<title>" ...` is the same as `studio.sh audio "<title>" ...`.

Typical times: a short podcast about 3 to 10 minutes, slides about 7, a Video Overview 10 minutes or more. Run it in the background or with a timeout of at least 15 minutes (30 for video). Tell the user it is running and wait; do not start a second copy.

## Options

| `type` | `format` | Other options |
|---|---|---|
| `audio` | `deep_dive` (default), `brief`, `critique`, `debate` | `length`: `short`, `default`, `long`; `language` (e.g. `en`, `es`, `pt_BR`, `zh_Hans`); `instructions` |
| `video` | `explainer` (default), `brief`, `cinematic`, `short` | `style` (`explainer` and `brief` only): `auto`, `classic`, `whiteboard`, `heritage`, `paper_craft`, `watercolor`, `anime`, `retro_print`, `kawaii`, or `custom` with `stylePrompt="..."`; `language`, `instructions` (not `cinematic`). `cinematic` takes no `style`, `language` or `instructions`, and needs Google AI Pro or Ultra |
| `slides` | `detailed` (default), `presenter` | `length`: `short`, `default`, `long`; `language`; `instructions` |

Pass options as `key=value`, e.g. `instructions="Focus on the risks"`. Any other option returns `400` with the valid values. Every Studio type (reports, quizzes, flashcards, infographics, mind maps too) and option: https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts

## Step by step (pasted text, several outputs from one notebook, more control)

1. Create a notebook. It prints the notebook id; keep it.
   ```bash
   NB=$(bash {baseDir}/scripts/create-notebook.sh "My topic")
   ```
2. Add sources. URLs (web pages and YouTube, up to 50 per call) and pasted text:
   ```bash
   bash {baseDir}/scripts/add-sources.sh "$NB" https://example.com/article https://www.youtube.com/watch?v=VIDEO_ID
   bash {baseDir}/scripts/add-sources.sh "$NB" --text notes.txt --title "My notes"      # or --text - to read stdin
   ```
   Local files (PDF, DOCX, PPTX, EPUB, MD, TXT, CSV, MP3, M4A, WAV, MP4, JPG, PNG, WEBP; up to 200 MB):
   ```bash
   bash {baseDir}/scripts/upload-file.sh "$NB" ./report.pdf
   ```
3. Wait until Google has processed every source (polls every 10 s, gives up after 10 minutes). A YouTube video without captions ends as `error` and is skipped.
   ```bash
   bash {baseDir}/scripts/wait-sources.sh "$NB"
   ```
4. Start a generation. It prints the job id (and logs it on stderr). Run it again on the same notebook for more outputs.
   ```bash
   JOB=$(bash {baseDir}/scripts/generate.sh "$NB" audio format=deep_dive language=en)
   JOB=$(bash {baseDir}/scripts/generate.sh "$NB" slides format=detailed)
   ```
5. Wait for the job (polls every 15 s) and save the final record:
   ```bash
   bash {baseDir}/scripts/wait-job.sh "$JOB" > job.json
   ```
6. Download the file(s). Prints the saved paths:
   ```bash
   bash {baseDir}/scripts/download.sh job.json ./out
   ```

## Timeouts and resuming

If a run is interrupted after the generation started, do not run it again: that spends the user's Gemini Notebook usage twice. `generate.sh` logs the job id on stderr (`job job:...`). Resume with it:

```bash
bash {baseDir}/scripts/wait-job.sh "<jobid>" > job.json && bash {baseDir}/scripts/download.sh job.json
```

## Errors

- `HTTP 401`: the token is wrong. `HTTP 404` from `create-notebook.sh`: `USEAPI_EMAIL` is not a connected account.
- `HTTP 596`: the Google account needs to be reconnected: https://useapi.net/docs/start-here/setup-gemini-notebook
- `HTTP 429` from `generate.sh`: the account is busy (`maxJobs` jobs already running) or Google's usage window is used up. `retryAt` in the body says when it resets. Tell the user and retry then. Do not loop on it.
- `HTTP 409` from `generate.sh`: no source is `ready` yet. Run `wait-sources.sh` first.
- A failed job prints its `error`. A job still running after 40 minutes is failed by the API with `timeout`.

## After it finishes

Tell the user the file path(s) and the title (`result.title` in `job.json`; audio and video also carry `result.duration` in seconds). The notebook stays in their Gemini Notebook (NotebookLM) account, so they can open it there or generate more from it with `generate.sh "$NB" ...`.

## About

- Third-party service by useapi.net, not affiliated with or endorsed by Google. Gemini Notebook and NotebookLM are Google's names for its product.
- API docs: https://useapi.net/docs/api-gemini-notebook-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-gemini-notebook
- Example code, a Dify plugin and a hosted MCP server (57 tools): https://github.com/useapi/notebooklm-api
- Support: support@useapi.net, Discord https://discord.gg/w28uK3cnmF, Telegram https://t.me/use_api

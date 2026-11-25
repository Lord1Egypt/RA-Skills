---
name: video-transcript-translate
description: "视频翻译 · 逐字稿翻译 / Video transcript translate: read a video link and return its spoken transcript with timestamps plus a full translation — 抖音、小红书、B站 videos into English (出海 research, subtitles, sharing with a foreign team), or YouTube、TikTok、X videos into Chinese. On-screen text is read too. Use when someone wants to know exactly what a foreign-language video says, needs a translated transcript to subtitle or quote, or is studying overseas competitors' videos. No login or cookies; needs an API key for the translation (+1 credit)."
version: 1.0.1
homepage: https://linkdigest.dev/zh/docs?ref=skill-video-transcript-translate
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"LinkDigest API key (ld_live_…), needed for the translation. Without it the script only returns a short free summary, two a day."}]}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-video-transcript-translate&next=/app/keys"
    required_for: "the transcript and its translation"
---

# 视频逐字稿翻译 · Video transcript translate

| You have | Run | You get |
|---|---|---|
| a 抖音 / 小红书 / B站 video, need English | `--translate-to en` | the Chinese transcript with times + an English translation |
| a YouTube / TikTok / X video, need Chinese | `--translate-to zh-CN` | the original transcript + a Chinese translation |
| any video, need Japanese | `--translate-to ja` | transcript + Japanese |

```bash
python3 {baseDir}/scripts/linkdigest.py "<video link>" --translate-to en
python3 {baseDir}/scripts/linkdigest.py "<video link>" --translate-to zh-CN --format json   # fields: transcript, translation.transcript_text
python3 {baseDir}/scripts/linkdigest.py "<long video link>" --translate-to en --depth transcript   # long videos: transcript only, cheaper
```

## How it works

LinkDigest reads the video from the platform's public player — speech recognition for what is said, frame reading for text on screen — and translates the transcript in one pass. The original stays next to the translation, so you can check any line.

## Cost

The read is priced by video length (a short video is a few credits); the translation adds 1 credit. New accounts get 10 free credits, no card: https://linkdigest.dev/signin?ref=skill-video-transcript-translate&next=/app/keys. A video that can't be read (private, deleted) costs nothing.

## Notes

- Timestamps are per segment, not per word: fine for reading and quoting, not frame-accurate subtitles.
- A transcript over 24,000 characters is translated from its start only; `translation.note` says how much was covered. The original transcript is always whole.

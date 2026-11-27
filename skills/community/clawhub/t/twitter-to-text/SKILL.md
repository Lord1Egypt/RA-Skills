---
name: twitter-to-text
description: "Twitter / X post to text (推特转文字 / X 帖子提取 / tweet transcript): read one x.com or twitter.com post link into text an AI can use. Returns the post text, author and date, the words inside every photo, and for video posts a timestamped speech transcript plus the text shown on screen, with key points checked against the source. Use when someone pastes an X or Twitter link and wants the content, the video's transcript, a summary or a rewrite. No X account, login or cookies; works without an API key (a short free summary, two a day)."
version: 1.0.2
homepage: https://linkdigest.dev/platforms/x?ref=skill-twitter-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"Optional. LinkDigest API key (starts with ld_live_). Without it the script returns a short free summary, two a day; with it, the full text, every photo's text and the video transcript."}]}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-twitter-to-text&next=/app/keys"
    required_for: "the full output; without it the script gives a free summary, two a day"
---

# Twitter / X post to text · 推特转文字

Paste an X post link, get back text your agent can quote. A model given the link alone usually can't open it: x.com serves its posts to a JavaScript app, and its robots.txt turns automated readers away. This skill sends the link to LinkDigest, which reads the post from X's public embed data (the same data an embedded post on any website shows) and, for a video post, the video itself.

## What you get

| Post type | Output |
|---|---|
| Text post | the full text, author, date |
| Photo post | every photo (not just the preview), each with a short description and the words printed in it |
| Video or GIF post | a speech transcript with timestamps, plus the text shown on screen |
| Long-form post (X Article / note) | only the preview text and lead image: that is all X shows without signing in, and the output says so |

Every read also lists key points, each tied to the words in the source.

## Usage

```bash
python3 {baseDir}/scripts/linkdigest.py "https://x.com/ProfTomYeh/status/2091167283057930455"
python3 {baseDir}/scripts/linkdigest.py "https://twitter.com/ProfTomYeh/status/2091167283057930455" --format json
python3 {baseDir}/scripts/linkdigest.py "<link>" --depth transcript     # video posts: the transcript only, cheaper
python3 {baseDir}/scripts/linkdigest.py "<link>" --translate-to zh-CN   # adds a translation, +1 credit
```

The last line on stderr says how many credits the read used and whether it came from the cache.

## Cost

- **No key:** a short free summary, two links a day per address.
- **With a key:** a text or photo post is about 1 credit; a video is priced by its length (with `--depth transcript`, 1 credit per started 2 minutes). New accounts get 10 free credits, no card: https://linkdigest.dev/signin?ref=skill-twitter-to-text&next=/app/keys
- A post that can't be read costs nothing.

## Limits, stated up front

- Posts from protected accounts, deleted posts and posts X shows only to signed-in users can't be read. You get a clear message instead of a guess.
- No X login, no cookies, no captcha solving. One link, read once, when you ask.

## Also

Same API as an MCP server for Claude, Cursor or Codex: https://linkdigest.dev/mcp. Other platforms (TikTok, YouTube, Instagram, 小红书, 抖音, B站): see the other LinkDigest skills.

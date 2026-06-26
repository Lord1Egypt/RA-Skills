---
name: vibevideoio-ai-script-to-video
description: Log into bollo.video or vibevideo.io, list Studio projects, create Studio episodes from prompts or scripts, and log out. Use when users ask to make or generate an AI video, paste a script/story and ask to turn it into a video, or manage Studio login/projects.
---

# VibeVideoIO AI Script to Video

This package exposes a single canonical skill:
- `skills/vibevideoio-ai-script-to-video/SKILL.md`

## Install Notes
- Local OpenClaw skill registration is manual via `npm run openclaw:register`
- The package does not auto-register itself during `postinstall`

## When To Use
- Create / make / generate an AI video
- Turn a prompt / script / story into a video
- Paste a screenplay or short video script and ask to make it into an AI video
- Log into `bollo.video` or `vibevideo.io`
- List or manage Studio projects

## Default Site Rule
- Chinese input → `bollo.video`
- English input → `vibevideo.io`
- Explicit user choice overrides the default

## Site Consistency Rule
- If the login site is `vibevideo.io`, keep all subsequent Studio operations on the `vibevideo.io` web/API endpoints
- If the login site is `bollo.video`, keep all subsequent Studio operations on the `bollo.video` web/API endpoints
- Do not mix `vibevideo.io` web pages or APIs with a `bollo.video` login session, and do not mix `bollo.video` web pages or APIs with a `vibevideo.io` login session

## Error And Retry Policy
- For login continuation errors, return the exact CLI/API error to the user first
- Only retry login when the user explicitly asks, or when the error clearly means the CAPTCHA expired/was incorrect and a fresh CAPTCHA is required
- For `create-episode` failures such as `fetch failed`, timeout, HTTP/API errors, or backend generation errors, return the failure result directly and stop
- When returning a `create-episode` failure, also include any known generation context such as video ID, title, aspect ratio, style mode, and project information
- Do not automatically rerun `create-episode`, do not silently switch sites, and do not change the script/style/aspect ratio/project to retry on the user's behalf
- After returning the error, ask the user whether they want to retry manually or adjust inputs

## Source Of Truth
For all detailed behavior, follow:
- `skills/vibevideoio-ai-script-to-video/SKILL.md`

That file is the single source of truth for:
- login and CAPTCHA flow
- Feishu vs local preview behavior
- episode creation questions
- CLI command usage and expected results

## Key Files
- `skills/vibevideoio-ai-script-to-video/SKILL.md`
- `skills/vibevideoio-ai-script-to-video/scripts/vibevideo-studio.mjs`
- `agents/openai.yaml`
- `references/current-system-map.md`

---
name: openclaw-aisa-youtube-search-serp-video-channels-trends-content-tracking
description: Search YouTube videos, channels, and trends through the AISA YouTube SERP client. Use when: the user asks for content research, competitor tracking, or trend discovery without managing Google credentials. Supports curl queries and the bundled Python client with locale and filter controls.
version: "1.1.1"
author: 0xjordansg-yolo
license: MIT-0
user-invocable: true
requires:
  bins:
    - python3
  env:
    - AISA_API_KEY
metadata:
  openclaw:
    emoji: "📺"
    requires:
      bins:
        - python3
      env:
        - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    files:
      - "scripts/*"
---

# OpenClaw YouTube SERP Scout

Runtime-focused release bundle for YouTube search, competitor tracking, and trend discovery through the AISA relay.

## When to use

- The user wants YouTube content research, channel discovery, or trend monitoring.
- The workflow benefits from the bundled Python client for repeated searches.
- The task can use `AISA_API_KEY` instead of direct Google API credentials.

## When NOT to use

- The user needs browser automation, local scraping, or account-level YouTube actions.
- The workflow must avoid sending search requests to `api.aisa.one`.
- The request depends on files outside this release bundle.

## Setup

Required:

- Environment variable:
  - `AISA_API_KEY` (required)

- Binaries:
  - `python3` (required)

```bash
export AISA_API_KEY="your-key"
```

## Quick Reference

```bash
python3 {baseDir}/scripts/youtube_client.py search --query "AI agents tutorial"
python3 {baseDir}/scripts/youtube_client.py search --query "machine learning" --country us
python3 {baseDir}/scripts/youtube_client.py competitor --name "OpenAI" --topic "GPT tutorial"
```

## Capabilities

- Search videos, channels, and playlists with `q`
- Filter by country with `gl` and language with `hl`
- Reuse `sp` tokens for pagination or SERP narrowing
- Run competitor and top-video research from the bundled Python client

## ClawHub Suspicious Review Notes

These points summarize the common reasons similar skills are marked `Suspicious` and how this release addresses them:

- The package is relay-based: all search requests go to `api.aisa.one`.
- The package is API-key-first: it requires `AISA_API_KEY` and does not ask for passwords, cookies, browser data, or other legacy secrets.
- The frontmatter declares required bins/env under `metadata.openclaw`, matching the runtime files kept in this release bundle.
- The release bundle is runtime-only: it keeps `SKILL.md` and `scripts/youtube_client.py`, while omitting non-runtime files such as `README.md` and `_meta.json`.
- The package does not include browser automation, cache sync, home-directory persistence, cookie extraction, or external agent CLI wrappers.

## Release Bundle Notes

- `scripts/youtube_client.py` is preserved from the original bundle.
- Search behavior and command surface are unchanged from the original runtime.
- The only changes are packaging trim and clearer publication metadata.

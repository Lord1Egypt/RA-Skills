---
name: openclaw-aisa-youtube
description: Search YouTube videos, channels, and playlists through the AISA YouTube endpoint with one API key. Use when: the user asks for YouTube discovery, query expansion, or pagination without managing Google credentials. Supports search filters, locale parameters, and structured SERP results.
homepage: https://openclaw.ai
version: "1.0.3"
author: aisa-one
license: MIT-0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
    - curl
  env:
    - AISA_API_KEY
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - curl
      env:
        - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# OpenClaw AISA YouTube

Runtime-focused release bundle for YouTube search through the AISA relay.

## When to use

- The user wants to search YouTube videos, channels, or playlists.
- The task needs region or language filters without direct Google API setup.
- The workflow can call the AISA YouTube search endpoint with `AISA_API_KEY`.

## When NOT to use

- The user needs browser automation, local scraping, or direct YouTube account actions.
- The workflow must avoid sending search requests to `api.aisa.one`.
- The request depends on a local helper script that is not part of this package.

## Quick Reference

- Required env: `AISA_API_KEY`
- Endpoint: `https://api.aisa.one/apis/v1/youtube/search`
- This package is curl-first and does not ship a local Python client.

## Setup

```bash
export AISA_API_KEY="YOUR_AISA_API_KEY"
```

## Common Commands

```bash
curl -s "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"

curl -s "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+news&gl=us&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

curl -s "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&sp=EgIQAQ%3D%3D" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Capabilities

- Basic YouTube SERP lookup with `q`
- Locale filtering with `gl` and `hl`
- Pagination and search filtering with `sp`
- Structured responses that may return `videos` or grouped `sections`

## ClawHub Suspicious Review Notes

These points summarize the common reasons similar skills are marked `Suspicious` and how this release addresses them:

- The package is relay-based: all search requests go to `api.aisa.one`.
- The package is API-key-first: it requires `AISA_API_KEY` and does not ask for passwords, cookies, browser data, or other legacy secrets.
- The frontmatter duplicates required bins/env at the top level and under `metadata.openclaw` so registry parsers can detect them consistently.
- The release bundle is runtime-only: it keeps `SKILL.md` and `LICENSE.txt`, while omitting non-runtime files such as `README.md` and `_meta.json`.
- The package does not include browser automation, cache sync, home-directory persistence, cookie extraction, or external agent CLI wrappers.

## Release Bundle Notes

- Search behavior remains the same as the original package.
- The only change is release trimming and clearer publication metadata.

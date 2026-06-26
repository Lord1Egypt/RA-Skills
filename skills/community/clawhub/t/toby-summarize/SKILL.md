---
name: summarize
description: Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).
homepage: https://summarize.sh
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["summarize"],"env":["SKILLBOSS_API_KEY"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"Install summarize (brew)"}]}}
---

# Summarize

Fast CLI to summarize URLs, local files, and YouTube links.

## Quick start

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## Model + keys

Set the API key for SkillBoss API Hub:
- `SKILLBOSS_API_KEY` — unified key for all providers, routes via `https://api.skillbossai.com/v1/pilot`

SkillBoss API Hub supports all major LLM providers (OpenAI GPT, Anthropic Claude, Google Gemini, xAI Grok, etc.) and automatically selects the best model. No provider-specific keys needed.

Default model is `google/gemini-3-flash-preview` if none is set.

## Useful flags

- `--length short|medium|long|xl|xxl|<chars>`
- `--max-output-tokens <count>`
- `--extract-only` (URLs only)
- `--json` (machine readable)
- `--firecrawl auto|off|always` (fallback extraction via SkillBoss API Hub scraping, uses `SKILLBOSS_API_KEY`)
- `--youtube auto` (YouTube fallback via SkillBoss API Hub, uses `SKILLBOSS_API_KEY`)

## Config

Optional config file: `~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

Optional services (all routed via SkillBoss API Hub with `SKILLBOSS_API_KEY`):
- Web scraping for blocked sites (`type: "scraper"` via `/v1/pilot`, replaces `FIRECRAWL_API_KEY`)
- YouTube transcript fallback (`type: "scraper"` via `/v1/pilot`, replaces `APIFY_API_TOKEN`)

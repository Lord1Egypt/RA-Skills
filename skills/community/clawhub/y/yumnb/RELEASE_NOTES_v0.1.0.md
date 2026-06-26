# yumnb v0.1.0 — Local-first Notebook Packet Generator

First public release of **yumnb**.

## Highlights

- Turn a URL, YouTube video, screenshot, or block of text into a local notebook folder
- Generate:
  - `summary.md`
  - `talkshow.txt`
  - `talkshow.mp3`
  - `deck.json`
  - `deck.pptx`
  - `links.json`
- YouTube ingest with subtitle fallback order:
  - manual subtitles
  - auto subtitles
  - `youtube-transcript-api`
  - description-only fallback
- Refactored into package modules with compatibility shims for older `scripts/*.py` entrypoints
- Bootstrap script for easier first-run setup
- Smoke tests for core local flows
- Friendlier auto-mode error messages when AI providers are not configured
- Channel-agnostic delivery support via OpenClaw / Hermes
  - Telegram
  - Discord
  - Slack
  - Teams
  - other supported OpenClaw surfaces
- Positioned as a **local-first, polite alternative to NotebookLM**

## Design intent

yumnb is for people who want a notebook workflow that stays file-based and local by default. Sources, summaries, scripts, slides, and generated artifacts live in ordinary folders unless upload / notify / deliver are explicitly enabled.

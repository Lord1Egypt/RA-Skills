# web-distiller

`web-distiller` is the OpenClaw skill for Distiller, the hosted API that turns public webpages into agent-ready Markdown.

## What This Skill Does

- defaults to `POST /markdown` for the free path
- uses `POST /distill` only for paid Starter users
- treats a missing `DISTILLER_API_KEY` as setup, not failure
- points operators to `https://webdistiller.dev/signin` and `https://webdistiller.dev/dashboard`
- keeps `/extract` out of the normal flow while it is temporarily unavailable

## Install Path

```bash
pip install web-distiller
```

Recommended environment:

```env
DISTILLER_API_BASE=https://webdistiller.dev
DISTILLER_API_KEY=your-api-key
```

An example OpenClaw config is included in [config.example.yaml](/C:/projects/distiller/openclaw-skill/web-distiller/config.example.yaml).

## Default Command

```bash
web-distiller <url>
```

Useful variants:

- `web-distiller <url> --endpoint markdown --format markdown`
- `web-distiller <url> --endpoint markdown --format text`
- `web-distiller <url> --endpoint distill --format markdown`
- `web-distiller <url> --endpoint distill --format json`

## Current Product Contract

- start with `/markdown`
- upgrade to Starter for `/distill`
- use batch jobs for async multi-URL workflows
- do not build new workflows around `/extract` until it is re-enabled

## Publishing Notes

This README is intended to be the ClawHub listing copy for the skill bundle. Keep it aligned with:

- [SKILL.md](/C:/projects/distiller/openclaw-skill/web-distiller/SKILL.md)
- [SHARE_MESSAGE.md](/C:/projects/distiller/openclaw-skill/web-distiller/SHARE_MESSAGE.md)
- [docs/SOURCE_OF_TRUTH.md](/C:/projects/distiller/docs/SOURCE_OF_TRUTH.md)

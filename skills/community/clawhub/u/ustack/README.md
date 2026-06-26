# uStack

> **One workspace. Any agent.**

uStack is the open compatibility layer that watches frontier agent-native workspaces, analyzes each upstream change, and produces a portable version that works for your agent/runtime.

## What it does

Paste a GitHub URL in. uStack:

1. Imports and snapshots the upstream agent framework
2. Detects every upstream change
3. Analyzes impact by area (skills, workflow, browser, safety, install, docs)
4. Classifies what's portable vs what needs adaptation vs what's host-specific
5. Generates a website-ready update page for your blog/feed
6. Keeps your local fork compatible as upstream evolves

## Quick start

```bash
# Import an upstream agent framework
node bin/ustack.js import https://github.com/garrytan/gstack --name gstack

# Analyze what changed
node bin/ustack.js analyze gstack

# Generate website-ready update page
node bin/ustack.js publish gstack

# Or do all three in one go
node bin/ustack.js update gstack

# Check workspace health
node bin/ustack.js doctor
```

## Why this exists

The agent ecosystem is fragmenting. Every stack — Claude Code, Codex, Gemini CLI, Cursor, OpenClaw — is creating its own:

- skill format
- memory conventions
- workflow assumptions
- browser / tool integrations
- safety patterns

This means useful upstream frameworks are trapped inside one host/runtime. Every team repeats the same adaptation work. uStack solves this by becoming the compatibility and update engine.

## Architecture

```
Upstream repo → uStack IR → target runtime
```

Not pairwise adapters. One normalized intermediate representation, one renderer per target.

## First beachhead

Tracking `garrytan/gstack` — a fast-moving workflow-skill framework for coding agents. It already supports Claude Code, Codex, Gemini CLI, Cursor, and Factory, making it the ideal first upstream to track.

## Run artifacts

```
.ustack/
  upstreams/<id>/
    manifest.json        — upstream metadata + current revision
    snapshot/            — key file snapshots for fast inspection
  runs/<id>/<timestamp>/
    analysis.json        — structured change analysis
    analysis.md          — human-readable analysis
    publish.md           — website-ready update page
  site/updates/<id>/
    <date>-<sha>.md      — blog/update feed pages
```

## Status

v0.1.0 — Phase 1 complete:
- [x] Upstream watcher + import
- [x] Structured change analyzer
- [x] Impact classification
- [x] Portability assessment
- [x] Website-ready publisher
- [x] `ustack update` (all three in one)
- [ ] IR normalization (Phase 2)
- [ ] Target adapters: openclaw, codex (Phase 3)
- [ ] Automated cron update loop (Phase 4)

## License

MIT — [AGI.security](https://agi.security)

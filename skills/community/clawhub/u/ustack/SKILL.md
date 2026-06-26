---
name: ustack
description: >
  Universal agent workspace compatibility and update engine.
  Track upstream agent frameworks (like gstack), analyze every change,
  classify portability, and generate adapted output for your runtime.
  Use when you want to import, analyze, adapt, or publish updates from
  upstream agent-native repos across Claude Code, Codex, OpenClaw, Gemini CLI, Cursor, and more.
---

# uStack — One Workspace. Any Agent.

uStack watches frontier agent-native workspaces, analyzes each upstream change,
and produces a portable version that works for your agent/runtime.

## Commands

### Import an upstream framework

```bash
node ustack/bin/ustack.js import https://github.com/garrytan/gstack --name gstack
```

Clones the upstream repo, detects key files (skills, control docs, config, tooling),
identifies structure (skill count, host conventions, category), and writes a manifest.

### Analyze changes

```bash
node ustack/bin/ustack.js analyze gstack
```

Diffs HEAD against previous snapshot. Classifies impact across 8 areas:
skills, install, browser, workflow, safety, tooling, docs, config.
Assesses portability: portable / needs-adaptation / host-specific.

### Publish update page

```bash
node ustack/bin/ustack.js publish gstack
```

Generates a website-ready markdown page with YAML frontmatter.
Includes: summary, impact table, portability breakdown, commit list,
usage instructions, and trust notes.

Output lands in `.ustack/site/updates/<id>/` — ready for blog/feed integration.

### Update (all-in-one)

```bash
node ustack/bin/ustack.js update gstack
```

Combines import → analyze → publish. Cron-friendly — only proceeds
with analyze+publish if upstream actually changed.

### Doctor

```bash
node ustack/bin/ustack.js doctor
```

Shows configured upstreams, last import/analysis dates, skill counts,
host conventions, and flags upstreams with unanalyzed changes pending.

## Architecture

```
Upstream repo → uStack IR → Target runtime
```

No pairwise adapters. One normalized intermediate representation,
one renderer per target. Adding a new upstream or target is independent.

## Run Artifacts

```
.ustack/
  upstreams/<id>/manifest.json     — upstream metadata + revision tracking
  runs/<id>/<timestamp>/           — analysis.json, analysis.md, publish.md
  site/updates/<id>/<date>.md      — website-ready update pages
```

## Supported Upstreams

- `garrytan/gstack` — workflow-skill framework (36 skills, 8 agent hosts)
- More upstreams can be added with `ustack import <url> --name <id>`

## Requirements

- Node.js >= 20
- Git

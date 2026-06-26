---
name: skilled-openclaw-advisor
description: >
  Query the local OpenClaw docs index for accurate answers about configuration,
  features, CLI commands, channels, providers, plugins, cron, sessions, agents,
  protocol, and troubleshooting. Faster and more accurate than relying on training
  data for OpenClaw specifics. No external API calls, sub-10ms queries. Useful for:
  openclaw, configure, gateway, channel, cron, provider, plugin, session,
  heartbeat, protocol, skill, model, agent questions.
metadata: {
  "openclaw": {
    "emoji": "📚",
    "skillKey": "skilled-openclaw-advisor",
    "requires": {
      "bins": ["python3", "openclaw"]
    },
    "install": [
      {
        "id": "build-index",
        "kind": "exec",
        "command": "python3 $SKILL_DIR/scripts/build_index.py",
        "label": "Build local OpenClaw docs index (reads from local OpenClaw install only)"
      }
    ]
  },
  "acceptLicenseTerms": true
}
---

# OpenClaw Docs Intelligence

Local FTS5 index of all OpenClaw documentation. No external API calls. Sub-10ms queries.

## What This Skill Does

This skill bundles three Python scripts and queries a local SQLite FTS5 index
built from the OpenClaw docs installed on this machine
(`~/.npm-global/lib/node_modules/openclaw/docs` or equivalent). It reads only
the local docs directory and writes only to `~/.openclaw/skills-data/skilled-openclaw-advisor/`.
The query and build scripts make no network requests. The update script optionally sends a local notification via the `openclaw message` CLI when doc changes are detected (no direct network calls). The scripts do not access credentials or config secrets,
and does not read `openclaw.json` at runtime (config keys listed below are optional
overrides that the user may set — they are not required).

## First-Time Setup

Build the index after installing the skill:

```bash
python3 $SKILL_DIR/scripts/build_index.py
```

This scans the local OpenClaw docs and creates a SQLite index at
`~/.openclaw/skills-data/skilled-openclaw-advisor/index.db`.

## Query

```bash
# Compact output for agent use
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION" --mode agent

# Human-readable
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION"

# Full detail with online link
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION" --verbosity detailed

# Chinese results
python3 $SKILL_DIR/scripts/query_index.py --query "YOUR QUESTION" --lang zh-CN

# Index status
python3 $SKILL_DIR/scripts/query_index.py --status
```

## Index Updates

```bash
# Incremental update (checks for doc changes)
python3 $SKILL_DIR/scripts/update_index.py

# Force full re-index
python3 $SKILL_DIR/scripts/build_index.py --force
```

## When to Use

- OpenClaw configuration questions
- CLI commands and options
- Channel, provider, cron, session, agent setup
- Troubleshooting OpenClaw errors

## When Not to Use

- General coding questions unrelated to OpenClaw
- Questions about third-party services
- If index is not built yet (run `build_index.py` first)

## Response Modes

| Mode | Use Case | Description |
|------|----------|-------------|
| `agent` | Default agent queries | Ultra-compact, minimal tokens |
| `human` + `standard` | Human questions | Clear explanation + key points |
| `human` + `detailed` | Deep dives | Full excerpt + examples |

## Optional Config

Settings in `skills.entries.openclaw-docs.config` in `openclaw.json` (all optional):

| Key | Default | Description |
|-----|---------|-------------|
| `defaultLang` | `"en"` | Language: `en` or `zh-CN` |
| `defaultVerbosity` | `"standard"` | Output: `concise`, `standard`, `detailed` |
| `maxResults` | `5` | Max results returned |
| `fallbackToEnglish` | `true` | Fall back to English if no results in requested language |
| `includeOnlineUrl` | `true` | Include `https://docs.openclaw.ai/...` links in detailed output |

# openclaw-soul

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![OpenClaw](https://img.shields.io/badge/OpenClaw-soul-blueviolet)](https://github.com/openclaw/openclaw)

`openclaw-soul` is an OpenClaw skill that adds a `/soul` command for browsing, previewing, applying, and restoring `SOUL.md` personas from [mergisi/awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents).

It keeps the workflow simple: browse available personas, inspect a soul, apply it to the current workspace, and restore from backup if needed.

## Features

- browse personas by category
- preview a soul before applying it
- apply a remote or local `SOUL.md` into the current workspace
- keep local backups before changes
- restore the previous soul
- refresh the cached catalog
- record local provenance metadata

## Commands

| Command | Description |
| --- | --- |
| `/soul` | Show help and current recorded state |
| `/soul categories` | List catalog categories |
| `/soul list <category>` | List souls in a category |
| `/soul show <id>` | Show soul metadata and source |
| `/soul apply <id>` | Apply a soul to the workspace |
| `/soul current` | Show the last recorded applied soul |
| `/soul restore` | Restore the latest local backup |
| `/soul refresh` | Re-fetch the cached catalog |
| `/soul search <text>` | Search by id, name, category, or role |

## Example usage

```text
/soul categories
/soul list creative
/soul show pirate-captain
/soul apply pirate-captain
/soul restore
```

After `apply` or `restore`, start a new session or use `/new` for full effect.

## Local data

| Path | Purpose |
| --- | --- |
| `soul-data/cache/agents.json` | Cached catalog data |
| `soul-data/backups/SOUL-<timestamp>.md` | Backup taken before applying a new soul |
| `soul-data/state.json` | Last applied soul and provenance |

## Development

Run tests with:-

```bash
npm test
```

## Usage Notes

- Running `/soul apply openclaw-default` will apply the OpenClaw-provided
  SOUL.md, from <https://docs.openclaw.ai/reference/templates/SOUL.md>.
- `/soul current` compares the live `SOUL.md` against a checksum saved during
  `/soul apply`. If it no longer matches, it reports `custom, from <current>
  (modified)`, where `<current>` is the last applied soul.
- It does not register provider-native slash commands for Discord, Telegram,
  Matrix, or other chat providers.

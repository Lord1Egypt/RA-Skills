# Snippets Sync

Sync code snippets and notes between machines via file sync (Syncthing, rsync, etc.).

## Setup

1. Set the `SNIPPETS_VAULT_PATH` environment variable to your shared vault directory
2. Ensure file sync (Syncthing, rsync, etc.) is configured between machines
3. That's it — read/write `.md` files in the vault

## What It Does

- **Code snippets** organized by language in `code_snippets/<lang>/`
- **Markdown notes** with YAML frontmatter for metadata
- **Bidirectional sync** — changes on any machine propagate to all others
- Clean CommonMark formatting, no platform-specific markdown

## Snippet Structure

```
code_snippets/
├── python/
│   └── http-server.md
├── bash/
│   └── find-large-files.md
└── _uncategorized/
    └── random-thing.md
```

Each snippet is a single `.md` file with frontmatter, description, and fenced code block.

## Requirements

- An Obsidian vault directory (local or synced)
- `SNIPPETS_VAULT_PATH` env var set to the vault path
- Optional: Syncthing or similar for multi-device sync
- Optional: Obsidian, VS Code, or any Markdown viewer
- Optional: `obsidian-cli` for search/list commands

## Install

```bash
npx clawhub@latest install snippets-sync
```

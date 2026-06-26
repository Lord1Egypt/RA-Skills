# Weeko CLI Skill

[中文文档](./README_CN.md) | English

An AI agent skill for the [Weeko CLI](https://github.com/nicepkg/weeko) — enables AI coding assistants (Claude, Cursor, OpenCode, etc.) to manage bookmarks and groups via the command line.

## What This Skill Does

When activated, this skill gives an AI agent the ability to:

- **Search & browse** bookmarks by keyword across titles, URLs, and descriptions
- **Add, update, delete** bookmarks with full control over title, URL, group, and description
- **Manage groups** — create, rename, recolor, list, and delete
- **Batch operations** — move or delete multiple bookmarks at once
- **Account overview** — retrieve user status and group structure for context

## Prerequisites

- [Bun](https://bun.sh) v1.0 or later installed on the host machine
- [weeko-cli](https://www.npmjs.com/package/weeko-cli) installed globally (`bun install -g weeko-cli`)
- A valid Weeko API key (obtained from [weeko.blog/dashboard](https://weeko.blog/dashboard))

## Usage

The agent should first authenticate, then gather context before performing operations:

```bash
weeko login              # Authenticate with API key
weeko status             # Get account overview
weeko tree               # Understand group structure
```

With context established, the agent can perform any bookmark or group operation. All commands support `--format toon` for token-efficient output and `--dry-run` for safe testing.

## Skill Contents

| File | Description |
|------|-------------|
| `SKILL.md` | Full agent instructions — workflows, best practices, error handling |
| `references/commands.md` | Detailed command reference, data schemas, API endpoints, architecture |

## Installing the Skill

This skill can be loaded into AI agent frameworks that support skill files (e.g., [OpenCode](https://opencode.ai)). Place the `skills/weeko/` directory in your agent's skill path.

## License

MIT

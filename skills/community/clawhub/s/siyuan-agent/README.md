# siyuan-agent

Standalone CLI for [SiYuan](https://ld246.com/) — direct HTTP API access, no npm dependencies.

## Setup

1. Enable SiYuan API token: SiYuan → Settings → About → API token
2. Set the token:

```bash
export SIYUAN_TOKEN=your_token_here
export SIYUAN_BASE=http://127.0.0.1:6806   # optional, default shown
```

(Add these to your `~/.bashrc` or `~/.zshrc` to persist.)

**You don't need to use the CLI yourself.** Just tell your agent to read SKILL.md — it will use this tool automatically.

## Install

```bash
npx skills add eloklam/siyuan-agent
```

## Commands

| Command | Description |
|---|---|
| `search query=<kw>` | Full-text search |
| `searchByNotebook query=<kw> notebook=<id>` | Search in specific notebook |
| `getDoc id=<blockID>` | Get document |
| `getBlock id=<blockID>` | Get single block |
| `getChildren id=<blockID>` | Get child blocks |
| `backlinks id=<blockID>` | Find backlinks |
| `outline id=<blockID>` | Get document outline |
| `sql "SELECT ..."` | Execute SELECT-only SQL |
| `exportMd id=<docID>` | Export doc to markdown |
| `call path=/api/... '{}'` | Any API endpoint directly |
| `insertBlock parentID=<id> data="<content>" write=true` | Insert block |
| `updateBlock id=<id> data="<content>" write=true` | Update block |
| `deleteBlock id=<id> write=true` | Delete block |

## Safety

- SQL is SELECT-only enforced in code
- Write operations require `write=true`
- Notebook management endpoints are hard-blocked

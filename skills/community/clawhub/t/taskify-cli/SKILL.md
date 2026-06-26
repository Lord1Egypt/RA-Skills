---
name: taskify-cli
description: Manage tasks, boards, and calendar events via the Taskify CLI (`taskify` command). Use when: (1) listing, searching, creating, updating, or deleting tasks, (2) marking tasks done or reopening them, (3) managing boards and columns, (4) assigning tasks to users, (5) checking upcoming or overdue tasks, (6) exporting or importing tasks, (7) triage or AI-powered task creation. Taskify stores tasks on Nostr relays — the CLI is the primary interface for agents working with Taskify data.
---

# Taskify CLI

`taskify` manages tasks and boards stored on Nostr relays. Tasks are identified by 8-char prefix or full UUID.

## Installation

Requires **Node.js 22+**.

**Package:** [`taskify-nostr`](https://www.npmjs.com/package/taskify-nostr)  
**Source:** [github.com/Solife-me/Taskify_Release](https://github.com/Solife-me/Taskify_Release)  
**Maintainer:** Ink-North ([@Ink-North](https://github.com/Ink-North))

```bash
npm install -g taskify-nostr
```

Verify the install:

```bash
taskify --version
```

If the global install fails due to permissions, use a local prefix:

```bash
npm install --prefix ~/.local -g taskify-nostr
# add ~/.local/bin to PATH if not already there
```

> Before installing, verify the package on [npmjs.com/package/taskify-nostr](https://www.npmjs.com/package/taskify-nostr) and review the source at the GitHub link above. Prefer user-local install (`--prefix ~/.local`) over global on shared systems.

### First-time setup

Run the onboarding wizard — it generates or imports a Nostr keypair and stores it securely in the local CLI config:

```bash
taskify setup
```

Join a board by its UUID:

```bash
taskify board join <board-uuid> --name "My Board"
```

> **Private key handling:** The CLI manages your Nostr private key internally via `taskify setup`. This skill does not instruct agents to read, expose, or handle private keys. Do not supply private keys via environment variables on shared or multi-user systems.

## Prerequisites (summary)

- **`taskify` binary on PATH** — installed via `npm install -g taskify-nostr` (see above). This skill provides instructions only; it does not install or bundle the binary.
- **Configured Nostr identity** — set up via `taskify setup`. The **npub and hex values used in commands are public keys** and are safe to pass as arguments.
- **At least one board joined** — via `taskify board join <uuid> --name <name>`.

## Data & credentials

- **Task data is public-key-addressed on Nostr relays** — content may be encrypted per board settings. The skill instructs read/write of task events only.
- **`taskify agent` commands forward task text to an external AI backend** — only use if you have configured and trust that backend (`taskify agent config`). Do not use on boards containing sensitive data unless the backend is self-hosted or trusted.
- **Profile/identity operations (`taskify profile`, `taskify contact`)** work with public Nostr keys (npub/hex) only — not private keys. The CLI stores private keys locally; this skill never instructs exposing them.
- **Relay management** — `taskify relay add/remove` modifies which Nostr relays tasks sync to. Only add relays you control or trust.

## Quick reference

```
taskify list [--board <name|id>] [--status open|done|any] [--column <name>] [--json]
taskify add <title> [--board <name>] [--due YYYY-MM-DD] [--priority 1|2|3] [--note <text>] [--column <name>]
taskify show <taskId> [--board <name>] [--json]
taskify update <taskId> --board <name> [--title <t>] [--due <d>] [--priority <p>] [--note <n>] [--column <name>]
taskify done <taskId> [--board <name>]
taskify reopen <taskId> [--board <name>]
taskify delete <taskId> --board <name>
taskify search <query> [--board <name>]
taskify upcoming [--days <n>] [--board <name>]
taskify board list
taskify board columns [<board>]
taskify agent add <natural-language description>   # forwards text to configured AI backend
```

## Key behaviours

- **taskId**: accepts 8-char prefix or full UUID.
- **`--board` flag**: required for `add`, `delete`, `update` when multiple boards exist. Optional for `list`, `done`, `show` (scans all if omitted).
- **Incremental sync**: `list` always fetches relay events since the last cursor before returning. Pass `--refresh` to force a full 30-day re-fetch.
- **`--json` flag**: available on `list`, `show`, `add`, `update` — output machine-readable JSON.
- **Priority**: 1 = low, 2 = medium, 3 = high.

## Common agent workflows

### Reading tasks
```bash
taskify list                          # all open tasks across boards
taskify list --board "Personal"       # one board
taskify list --status done            # completed tasks
taskify upcoming --days 7             # due within 7 days
taskify search "keyword"              # full-text search
taskify show abc12345 --json          # full task details
```

### Creating tasks
```bash
taskify add "Write release notes" --board "Work" --due 2026-03-20 --priority 2
taskify agent add "high priority bug fix due Friday"   # AI-parsed (sends text to AI backend)
```

### Updating tasks
```bash
taskify update abc12345 --board "Work" --due 2026-03-25 --priority 3
taskify update abc12345 --board "Work" --column "In Progress"
taskify done abc12345
taskify reopen abc12345
```

### Board management
```bash
taskify board list                            # show configured boards and IDs
taskify board columns                         # show all columns
taskify board column-add "Work" "Review"
taskify board column-rename "Work" "Review" "QA"
```

### Assigning tasks
```bash
taskify assign abc12345 npub1...              # assign to npub (public key — not a secret)
taskify unassign abc12345 npub1...
```

## Output parsing

Use `--json` whenever the output will be parsed programmatically:

```bash
taskify list --json | jq '.[] | {id, title, due: .dueISO, priority}'
taskify show abc12345 --json | jq '{title, note, column}'
```

## Diagnostics

```bash
taskify board list         # boards with IDs
taskify relay status       # check relay connectivity
taskify cache clear        # wipe local cache (forces cold re-fetch on next list)
```

## Reference

- Full command flags: see [references/commands.md](references/commands.md)
- Board and column operations: see [references/boards.md](references/boards.md)

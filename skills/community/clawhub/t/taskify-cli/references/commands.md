# Taskify CLI — Full Command Reference

## taskify list

```
taskify list [--board <id|name>] [--status open|done|any] [--column <id|name>] [--refresh] [--no-cache] [--json]
```

- `--status any` returns open + done tasks
- `--refresh` forces a full 30-day cold re-fetch (bypasses cursor)
- `--no-cache` skips the local merge base; does not fall back to stale cache if relay is empty

## taskify add

```
taskify add <title> [--board <id|name>] [--due YYYY-MM-DD] [--due-time HH:MM] [--timezone <iana>]
            [--priority 1|2|3] [--note <text>] [--column <id|name>]
            [--subtask <text>]... [--assignee <npub|hex>]...
            [--recurrence-json <json>] [--reminders <csv>]
            [--hidden-until <ISO>] [--json]
```

## taskify update

```
taskify update <taskId> [--board <id|name>]
               [--title <t>] [--due <d>] [--due-time <HH:MM>] [--timezone <iana>]
               [--priority <p>] [--note <n>] [--column <id|name>]
               [--assignee <npub|hex>]...    # replaces all assignees
               [--recurrence-json <json>] [--reminders <csv>]
               [--hidden-until <ISO>] [--json]
```

## taskify show

```
taskify show <taskId> [--board <id|name>] [--json]
```

Displays title, note, due date/time, priority, column, subtasks, assignees, reminders, recurrence.

## taskify done / reopen / delete

```
taskify done   [taskId] [--board <id|name>]
taskify reopen [taskId] [--board <id|name>]
taskify delete <taskId> [--board <id|name>]   # publishes status=deleted to Nostr; prompts confirm
```

Both `done` and `reopen` accept recurring instance IDs.

## taskify search

```
taskify search <query> [--board <id|name>] [--status open|done|any] [--json]
```

Full-text search across title and note fields.

## taskify upcoming

```
taskify upcoming [--days <n>] [--board <id|name>] [--json]
```

Default: 7 days.

## taskify subtask

```
taskify subtask <taskId> <subtaskRef> [--board <id|name>]
```

`subtaskRef`: 1-based index or partial title match. Toggles done/incomplete.

## taskify assign / unassign

```
taskify assign   <taskId> <npubOrHex> [--board <id|name>]
taskify unassign <taskId> <npubOrHex> [--board <id|name>]
```

## taskify remind

```
taskify remind <taskId> <presets...> [--board <id|name>]
```

Presets: `0h`, `5m`, `15m`, `30m`, `1h`, `1d`, `1w`

## taskify export / import

```
taskify export [--board <id|name>] [--format json|csv|markdown] [--output <file>]
taskify import <file> [--board <id|name>] [--format json|csv]
```

## taskify agent

```
taskify agent add <description>      # AI-powered task creation — forwards text to configured AI backend
taskify agent triage [--board <id>]  # AI prioritization — forwards task list to AI backend
taskify agent config                 # configure which AI backend is used
```

> `agent` subcommands send task text to an external AI service. Only use on boards that do not contain sensitive data, unless the backend is self-hosted or trusted.

## taskify inbox

```
taskify inbox list
taskify inbox capture <title>
taskify inbox triage
```

Quick-capture tasks that bypass board selection.

## taskify profile

```
taskify profile list
taskify profile use <name>
taskify profile add <name>
taskify profile remove <name>
```

Named Nostr identity profiles. Switch profiles for multi-account setups.

## taskify contact

```
taskify contact list
taskify contact add <npub|hex> [--name <n>]
taskify contact remove <npub|hex>
```

## taskify relay

```
taskify relay status                  # check connectivity to configured relays
taskify relay list                    # list configured relay URLs
taskify relay add <wss://...>         # add a relay you control or trust
taskify relay remove <wss://...>
```

> Only add relay URLs you control or trust — relays receive all task sync traffic.

## taskify cache

```
taskify cache clear               # wipe all cached task data
taskify cache clear --board <id>  # wipe one board
```

## Global flags

- `-P, --profile <name>` — use a specific profile for this command without switching the active profile

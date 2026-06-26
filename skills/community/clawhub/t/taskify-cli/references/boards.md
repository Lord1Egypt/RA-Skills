# Taskify Boards & Columns Reference

## Board types

| Type | Description |
|---|---|
| `lists` | Standard kanban-style board with named columns |
| `week` | 7-day week view — columns are Mon–Sun |
| `compound` | Aggregates tasks from child boards |

## Board commands

```bash
taskify board list                             # list configured boards with IDs
taskify board join <uuid> --name <name>        # join an existing board by ID
taskify board sync [boardId]                   # pull latest board metadata from relay
taskify board create <name>                    # create a new board on Nostr
taskify board leave <boardId>                  # remove board from local config
taskify board rename <board> <name>
taskify board archive <board>
taskify board unarchive <board>
taskify board hide <board>
taskify board unhide <board>
taskify board sort <board> [mode] [direction]  # mode: manual|due|priority|created|alpha
taskify board clear-completed <board>          # delete all completed tasks
```

## Column commands

```bash
taskify board columns [<board>]                        # list columns with IDs
taskify board column-add <board> <name>
taskify board column-rename <board> <columnRef> <name> # columnRef = id or name
taskify board column-delete <board> <columnRef>
taskify board column-reorder <board> <columnRef> <pos> # 1-based position
```

## Compound board commands

```bash
taskify board children <board>
taskify board child-add <board> <child>
taskify board child-remove <board> <child>
taskify board child-reorder <board> <child> <position>
```

## Identifying boards and columns

- Boards: use name (e.g. `"Personal"`) or UUID (`4d0f7654-...`)
- Columns: use name (e.g. `"In Progress"`) or column UUID
- Week boards: use day names as column refs (`Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun`)
- Run `taskify board columns` to see all column names and IDs

# SiYuan Note CLI Command Reference

Global options:

- `-f, --format <format>`: `table`, `json`, or `yaml`; defaults to `table`.
- `--verbose`: enable verbose output.
- `--config <path>`: use a custom config file.

## Authentication

```bash
npx siyuan-note-cli auth status
npx siyuan-note-cli auth login --url http://127.0.0.1:6806 --token <token>
npx siyuan-note-cli auth logout
```

## Notebooks

```bash
npx siyuan-note-cli notebook list
npx siyuan-note-cli notebook create "Notebook Name"
npx siyuan-note-cli notebook rename <id|name> "New Name"
npx siyuan-note-cli notebook delete <id|name> --force
npx siyuan-note-cli notebook open <id|name>
npx siyuan-note-cli notebook close <id|name>
```

## Documents

```bash
npx siyuan-note-cli document list <notebook-id> --path / --depth 2
npx siyuan-note-cli document get <doc-id>
npx siyuan-note-cli document get <doc-id> --output doc.md

# Create a document. Recommended: pass Markdown through --file to preserve formatting.
npx siyuan-note-cli document create <notebook-id> "path/document-name" \
  --title "Title" \
  --file ./content.md

# Create a document. Not recommended for multi-line Markdown: --content.
# Use only for very short single-line plain text. For multi-line text, \n may become literal text,
# and special characters such as `#*$` may be misinterpreted by the shell.
npx siyuan-note-cli document create <notebook-id> "path/document-name" \
  --title "Title" \
  --content "# Title\n\nContent"

npx siyuan-note-cli document rename <doc-id> "New Title"
npx siyuan-note-cli document delete <doc-id> --force
npx siyuan-note-cli document move <doc-id> <parent-doc-id>
npx siyuan-note-cli document outline <doc-id>
```

## Blocks

```bash
npx siyuan-note-cli block get <block-id>
npx siyuan-note-cli block source <block-id>
npx siyuan-note-cli block children <block-id>
npx siyuan-note-cli block insert --parent <doc-id> --content "Content" --after <block-id>

# append/update handle one block at a time, such as one paragraph or one heading.
# If multi-block Markdown is passed, only the first element may be preserved.
# Call the command once per block when multiple blocks are needed.
npx siyuan-note-cli block append --parent <doc-id> --content "Content"
npx siyuan-note-cli block update <block-id> --content "New content"

npx siyuan-note-cli block delete <block-id> --force
npx siyuan-note-cli block move <block-id> --parent <doc-id> --after <other-block-id>
```

## Search and Query

```bash
npx siyuan-note-cli search docs "keyword"
npx siyuan-note-cli search blocks "keyword"
npx siyuan-note-cli query "SELECT * FROM blocks WHERE type='d' LIMIT 10"
```

SQL should be used for reads only. Write operations may damage data.

## Attributes

```bash
npx siyuan-note-cli attr get <block-id>
npx siyuan-note-cli attr set <block-id> key1=value1 key2=value2
npx siyuan-note-cli attr delete <block-id> key1 key2
```

## Assets

```bash
npx siyuan-note-cli asset upload ./image.png
npx siyuan-note-cli asset upload ./image.png --dir /assets/screenshots/
```

## Export

```bash
npx siyuan-note-cli export doc <doc-id> --format md --output doc.md
```

## Sync

```bash
npx siyuan-note-cli sync status
npx siyuan-note-cli sync now
```

## Configuration

```bash
npx siyuan-note-cli config list
npx siyuan-note-cli config get baseURL
npx siyuan-note-cli config set baseURL http://127.0.0.1:6806
```

## Database, Experimental

```bash
npx siyuan-note-cli database list
npx siyuan-note-cli database list --filter "task"
npx siyuan-note-cli database create "Task Database" --notebook <notebook-id>
npx siyuan-note-cli database get <db-id>
npx siyuan-note-cli database delete <db-id> --force

npx siyuan-note-cli database field list <db-id>
npx siyuan-note-cli database field add <db-id> "Status" --type select
npx siyuan-note-cli database field add <db-id> "Priority" --type select --options '["High","Medium","Low"]'
npx siyuan-note-cli database field remove <db-id> <field-id|name>
npx siyuan-note-cli database field rename <db-id> <field-id|name> "New Name"

npx siyuan-note-cli database row list <db-id>
npx siyuan-note-cli database row list <db-id> --filter "Status=Done"
npx siyuan-note-cli database row add <db-id> --values "Name=Task,Status=In Progress"
npx siyuan-note-cli database row add <db-id> --values "Name=Task" --bind-doc <doc-id>
npx siyuan-note-cli database row update <db-id> <row-id> --values "Status=Done"
npx siyuan-note-cli database row delete <db-id> <row-id> --force
npx siyuan-note-cli database row bind <db-id> <doc-id>

npx siyuan-note-cli database view list <db-id>
npx siyuan-note-cli database view add <db-id> "Board" --type kanban
npx siyuan-note-cli database view remove <db-id> <view-id|name>
```

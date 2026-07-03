---
name: siyuan-note-cli
description: |
  Connect to and operate SiYuan Note through the siyuan-note-cli command-line tool, using notes as context for AI tasks.
  Use when the user asks to query, create, or modify SiYuan notes; read guides or knowledge bases from notes; manage notebooks, documents, blocks, or databases; write task results to SiYuan; or reference SiYuan notes during other work.
  After this skill is triggered, first read the note named "AI Assistant Guide" before performing the specific operation.
  Requires the local SiYuan Note client to be running and an API token to be configured.
---

# SiYuan Note CLI Skill

## Command Invocation

First try the globally installed CLI:

```bash
siyuan --version
```

If unavailable, use `npx` without requiring a global install:

```bash
npx siyuan-note-cli --version
```

Prefer writing commands as `npx siyuan-note-cli <command>` to avoid environment differences.

## Startup Workflow: Read "AI Assistant Guide" First

Whenever this skill is triggered, the first step is to search for and read the SiYuan document named "AI Assistant Guide":

1. Search documents:

   ```bash
   npx siyuan-note-cli search docs "AI Assistant Guide"
   ```

2. Read the full document by ID:

   ```bash
   npx siyuan-note-cli document get <doc-id>
   ```

3. If the guide contains Markdown rules, available tool lists, naming conventions, tag systems, database templates, or other instructions, follow them strictly.

If "AI Assistant Guide" is not found, tell the user and continue with the normal operation.

## Prerequisites

1. The SiYuan Note client is running, usually at `http://127.0.0.1:6806`.
2. API token is configured in one of these ways:
   - Environment variables: `SIYUAN_API_URL`, `SIYUAN_API_TOKEN`
   - CLI login: `npx siyuan-note-cli auth login --url <url> --token <token>`
   - Config file: `~/.config/siyuan-cli/config.yml`

## Best Practices

1. **Locate before operating**: use `search`, `notebook list`, and `document list` before modifications.
2. **Prefer IDs**: document and block IDs are more stable than paths.
3. **Use structured output**: use `--format json` for batch operations.
4. **Confirm dangerous operations**: use `--force` only after confirmation; database operations are experimental and should be used carefully.
5. **Verify writes**: after write operations, confirm the result with `document get` or `block get`.
6. **Create new notes by default**: unless the user explicitly asks to modify or append to an existing note, create a separate new document.
7. **Default to the AgentWork notebook**: if the user does not specify a location, write content to the root of the `AgentWork` notebook. If it does not exist, create it first.

## Operation Boundary: Create vs Modify

Core principle: create by default, modify only when explicit. This prevents accidental overwrites or pollution of existing notes.

| User Request | Behavior |
|---|---|
| "Record this note", "save this", "keep this" | Create a new document under `AgentWork` |
| "Update note xxx", "append to xxx", "modify xxx" | Modify the specified existing document |
| No location specified | Create under the `AgentWork` notebook root |
| Notebook/path specified | Create at the specified location |

AgentWork notebook handling:

```bash
npx siyuan-note-cli notebook list --format json
npx siyuan-note-cli notebook create "AgentWork"
npx siyuan-note-cli document create <agentwork-id> "Document Name" \
  --title "Title" \
  --file "$TEMP/siyuan-draft.md"
```

Do not add a leading `/` to the path; otherwise the CLI may resolve it as a workspace filesystem path.

## Writing Notes: Prefer `--file`, Avoid `--content`

Markdown content should be passed through a file, not a command-line string. Command-line parsing can damage line breaks and special characters such as backticks, `#`, and `$`.

| Method | Formatting | Use Case |
|---|---|---|
| `document create --file <path>` | Preserves formatting | Preferred for complete documents |
| `block append --parent <id> --content "..."` | Single block only | Append one paragraph or heading |
| `block update <id> --content "..."` | Single block only | Update an existing block |
| `document create --content "..."` | Easy to damage | Not recommended for multi-line Markdown |

Recommended pattern:

```bash
# Windows Git Bash: $TEMP/siyuan-draft.md
# Linux/macOS: /tmp/siyuan-draft.md
# Cross-platform fallback: ${TMPDIR:-/tmp}/siyuan-draft.md

npx siyuan-note-cli document create <notebook-id> "path/document-name" \
  --title "Document Title" \
  --file "$TEMP/siyuan-draft.md"
```

Avoid this for multi-line Markdown:

```bash
npx siyuan-note-cli document create <notebook-id> "path/document-name" \
  --title "Title" \
  --content "# Title\n\nBody **bold**\n\n```python\nprint('hello')\n```"
```

## Incremental Append: One Block at a Time

`block append` appends only one block per call. If multiple paragraphs are passed, only the first block may be preserved.

```bash
npx siyuan-note-cli block append --parent <doc-id> --content "## Section Title"
npx siyuan-note-cli block append --parent <doc-id> --content "Body paragraph."
```

Do not pass multiple paragraphs in one `block append` call.

## Path Rules

In SiYuan, folders are also documents. Do not add a leading `/` in any scenario.

| Scenario | Path Format | Example |
|---|---|---|
| Notebook root | `"Document Name"` | `"My Note"` |
| Existing subdirectory | `"dir/subdir/document"` | `"Projects/App/New Doc"` |
| Child document under existing document | `"parent/document"` | `"Project Plan/Weekly Note"` |
| New nested path | `"new-dir/document"` | `"Test Folder/Scenario Three"` |

Examples:

```bash
npx siyuan-note-cli document create <notebook-id> "Document Name" \
  --title "Title" \
  --file "$TEMP/siyuan-draft.md"

npx siyuan-note-cli document create <notebook-id> "Project/Subdir/New Document" \
  --title "Title" \
  --file "$TEMP/siyuan-draft.md"
```

## Common Commands

Connection:

```bash
npx siyuan-note-cli auth status
npx siyuan-note-cli auth login --url http://127.0.0.1:6806 --token <token>
```

Notebooks:

```bash
npx siyuan-note-cli notebook list
npx siyuan-note-cli notebook create "Project Management"
```

Documents:

```bash
npx siyuan-note-cli document list <notebook-id> --path / --depth 2
npx siyuan-note-cli document get <doc-id>
npx siyuan-note-cli document create <notebook-id> "path/document-name" \
  --title "Title" \
  --file ./content.md
npx siyuan-note-cli document rename <doc-id> "New Title"
npx siyuan-note-cli document delete <doc-id> --force
```

Blocks:

```bash
npx siyuan-note-cli block get <block-id>
npx siyuan-note-cli block append <doc-id> --content "New paragraph"
npx siyuan-note-cli block update <block-id> --content "Updated content"
```

Search and query:

```bash
npx siyuan-note-cli search docs "Project Plan"
npx siyuan-note-cli search blocks "Key conclusion"
npx siyuan-note-cli query "SELECT * FROM blocks WHERE type='d' LIMIT 10"
```

Attributes:

```bash
npx siyuan-note-cli attr get <block-id>
npx siyuan-note-cli attr set <block-id> custom-status=done custom-priority=high
```

## References

- Command details: [references/commands.md](references/commands.md)
- Workflow examples: [references/workflow-examples.md](references/workflow-examples.md)

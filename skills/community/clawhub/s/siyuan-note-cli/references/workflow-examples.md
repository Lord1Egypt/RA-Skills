# SiYuan Note CLI Workflow Examples

## Workflow 1: Write Task Results to a New Document

1. List notebooks and find the target notebook ID:

   ```bash
   npx siyuan-note-cli notebook list --format json
   ```

2. Write Markdown content to a fixed file in the system temp directory, then create the document:

   ```bash
   # Temp file location. Use a fixed name and overwrite it each time.
   # Windows (Git Bash):  $TEMP/siyuan-draft.md
   # Linux / macOS:       /tmp/siyuan-draft.md
   ```

   ```bash
   npx siyuan-note-cli document create <notebook-id> "Projects/2026-01-15-meeting-notes" \
     --title "Meeting Notes" \
     --file "$TEMP/siyuan-draft.md"
   ```

   Always use `--file` instead of `--content` for Markdown content.

   `--content` can lose line breaks during shell parsing, turn `\n` into literal text, or corrupt special characters such as backticks, `#`, and `$`. Use `--content` only for very short single-line plain text.

   Recommended temp file handling: write to a system temp directory such as `$TEMP` or `/tmp`, with a fixed file name such as `siyuan-draft.md`. Each run overwrites the file, so manual cleanup is usually unnecessary. The temp path is stable and does not depend on the agent's current working directory.

3. Read the document to verify:

   ```bash
   npx siyuan-note-cli document get <doc-id>
   ```

## Workflow 2: Query Notes and Summarize

1. Search related documents:

   ```bash
   npx siyuan-note-cli search docs "key conclusion"
   ```

2. Read document content:

   ```bash
   npx siyuan-note-cli document get <doc-id>
   ```

3. Read only the outline if needed:

   ```bash
   npx siyuan-note-cli document outline <doc-id>
   ```

## Workflow 3: Update an Existing Block

1. Search for the target block:

   ```bash
   npx siyuan-note-cli search blocks "text to update"
   ```

2. Read the block to confirm:

   ```bash
   npx siyuan-note-cli block get <block-id>
   ```

3. Update the block:

   ```bash
   npx siyuan-note-cli block update <block-id> --content "Updated content"
   ```

## Workflow 4: Track Tasks with a Database

1. Create a database:

   ```bash
   npx siyuan-note-cli database create "Task Tracking" --notebook <notebook-id>
   ```

2. Add fields:

   ```bash
   npx siyuan-note-cli database field add <db-id> "Status" --type select --options '["Todo","In Progress","Done"]'
   npx siyuan-note-cli database field add <db-id> "Owner" --type text
   ```

3. Add a row:

   ```bash
   npx siyuan-note-cli database row add <db-id> --values "Name=Design Review,Status=Todo,Owner=Alice"
   ```

4. Query rows:

   ```bash
   npx siyuan-note-cli database row list <db-id> --filter "Status=Todo"
   ```

## Workflow 5: Read "AI Assistant Guide" Before the User Task

Every task that triggers this skill should follow this order:

1. Search for "AI Assistant Guide":

   ```bash
   npx siyuan-note-cli search docs "AI Assistant Guide"
   ```

2. Read the guide:

   ```bash
   npx siyuan-note-cli document get <guide-doc-id>
   ```

3. Perform the specific user task according to the guide.

---
name: x-to-notebook
description: Push X/Twitter bookmarks into Google NotebookLM notebooks, auto-routed by bookmark folder. Use when the user wants to send bookmarks to NotebookLM, says "push my bookmarks", "sync bookmarks to notebook", or "send X bookmarks to NotebookLM".
metadata: {"openclaw":{"requires":{"bins":["uv","mcporter"],"mcp":["notebooklm"]}}}
---

# X to Notebook

Fetches X bookmarks organized by folder and auto-routes them to matching NotebookLM notebooks by name.

## Prerequisites

- `twikit` installed: `cd ~/.openclaw && uv add twikit`
- X cookies exported from browser to `~/.openclaw/credentials/x-cookies.json` (use Cookie-Editor extension on x.com)
- `notebooklm-mcp-cli` installed: `uv tool install notebooklm-mcp-cli`
- Google Chrome installed (for persistent auth)
- NotebookLM authenticated: `nlm login`
- `notebooklm` MCP server registered in mcporter: `mcporter config add notebooklm --command "notebooklm-mcp"`

## Workflow

### 1. Fetch bookmark folders

```json
{
  "tool": "exec",
  "command": "uv run --project ~/.openclaw {baseDir}/scripts/list_folders.py"
}
```

Parse the JSON output. If exit code 1, report the error and stop.

### 2. Fetch bookmarks per folder

For each folder from step 1, plus unfiled bookmarks (no `--folder-id`):

```json
{
  "tool": "exec",
  "command": "uv run --project ~/.openclaw {baseDir}/scripts/fetch_bookmarks.py --folder-id <folder_id>"
}
```

For unfiled bookmarks (no folder):

```json
{
  "tool": "exec",
  "command": "uv run --project ~/.openclaw {baseDir}/scripts/fetch_bookmarks.py"
}
```

Skip folders that return no new bookmarks.

### 3. List notebooks

```json
{
  "tool": "exec",
  "command": "mcporter call notebooklm.notebook_list"
}
```

If mcporter error → "NotebookLM MCP server not available. Register it with: `mcporter config add notebooklm --command \"notebooklm-mcp\"`" and stop.

If auth expired → "NotebookLM session expired. Run: `nlm login`" and stop.

### 4. Auto-match folders to notebooks

Match each folder name to a notebook title (case-insensitive, emojis and `-notebook`/`-bookmarks` suffix stripped). For example, folder "🦞 openclaw-notebook" matches notebook "OpenClaw". Display the matching plan:

```
Folder routing:
- "AI Research" → notebook "AI Research" (3 new bookmarks)
- "Claude Code" → notebook "claude code" (2 new bookmarks)
- "Random" → no matching notebook
- "Unfiled" → no matching notebook
```

### 5. Handle unmatched folders

For each folder (including "Unfiled") with no matching notebook, ask:

```
No notebook matches folder "Random" (4 bookmarks). Pick one:
1. Notebook Title A
2. Notebook Title B
+ Create new notebook
s. Skip this folder
```

If user picks "create new", ask for a title:

```json
{
  "tool": "exec",
  "command": "mcporter call notebooklm.notebook_create title=\"<title>\""
}
```

If user picks "skip", skip those bookmarks entirely.

### 6. Push bookmarks

For each folder with a resolved notebook, push each bookmark as a text source (X URLs can't be scraped by NotebookLM):

```json
{
  "tool": "exec",
  "command": "mcporter call notebooklm.source_add notebook_id=\"<notebook_id>\" source_type=text text=\"@author: tweet text\n\nSource: https://x.com/author/status/id\""
}
```

Report progress per folder. If a push fails, report which tweet failed and continue.

### 7. Mark as pushed

After successful pushes, mark bookmark IDs:

```json
{
  "tool": "exec",
  "command": "uv run --project ~/.openclaw {baseDir}/scripts/mark_pushed.py <id1> <id2> ..."
}
```

Only mark IDs that were successfully pushed.

### 8. Confirm

Report per-folder summary:

```
Bookmarks synced:
- "AI Research" — 3 pushed
- "Claude Code" — 2 pushed
Skipped: "Random" (user skipped)
```

### 9. Error handling

- `fetch_bookmarks.py` auth error → "X session expired. Re-export cookies from your browser to `~/.openclaw/credentials/x-cookies.json`"
- NotebookLM MCP not registered → "NotebookLM MCP server not available. Register it with: `mcporter config add notebooklm --command \"notebooklm-mcp\"`"
- NotebookLM auth expired → "NotebookLM session expired. Run `nlm login` in your terminal"
- `source_add` fails → report the URL and error, continue with remaining bookmarks
- No bookmarks in any folder → "No new bookmarks to push."

## Examples

| User says | Expected behavior |
|-----------|-------------------|
| "push my bookmarks" | Fetch folders + bookmarks, auto-match to notebooks, ask for unmatched, push |
| "send my X bookmarks to NotebookLM" | Same flow |
| "sync bookmarks to notebook" | Same flow |

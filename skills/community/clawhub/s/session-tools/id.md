# Session ID

Finds the session ID (UUID) of the current conversation.

## How It Works

Claude's text output is recorded in session JSONL files. By leaving a unique marker in the conversation, you can grep for that marker to identify the current session file.

## Procedure

### 1. Generate and Output Marker

Generate a unique marker string and include it in **text output** (so it gets recorded in the JSONL).

```
SESSION_MARKER_{random_uuid}
```

Example output:
```
Marker for finding session ID: SESSION_MARKER_a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### 2. Search with Script

```bash
bash ~/.claude/skills/session/scripts/find-session-id.sh "SESSION_MARKER_a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

The script converts the CWD to a project name, then searches `~/.claude/projects/{project_name}/*.jsonl` for the marker and returns the session ID.

### 3. Result

```
b5153827-a52c-4e83-b24a-8413e6aa418b
```

## Script

[find-session-id.sh](./scripts/find-session-id.sh)

- Input: `<marker>` (required), `[project_dir]` (optional, auto-derived from CWD if omitted)
- CWD → project name conversion rules:
  - Git-bash: `/c/Users/...` → `c--Users-...`
  - WSL: `/mnt/c/Users/...` → `-mnt-c-Users-...`
  - macOS: `/Users/...` → `-Users-...`
- sync-conflict files are automatically excluded

## Keyword Session Search

When called as `/session id <keyword>`, searches for sessions containing that keyword and returns the session ID.

### Search Procedure

1. Determine project JSONL directory (`~/.claude/projects/{project_name}/`)
2. Grep JSONL files for keyword — matches user messages (`"type":"user"`) + file paths
3. Sort results by modification time descending and return the most recent matching session

```bash
# Project JSONL path
PROJECT_DIR=~/.claude/projects/{project_name}

# Keyword search (matches both user messages and file paths)
grep -l "<keyword>" "$PROJECT_DIR"/*.jsonl | while read f; do
  ts=$(stat -c %Y "$f")
  sid=$(basename "$f" .jsonl)
  echo "$ts $sid"
done | sort -rn | head -5
```

### Restricting Search Scope

- `--today`: Only sessions modified today (uses `find -newer`)
- `--project <path>`: Specify a particular project path

### Output Format

```
03-26 11:28 | a6aea9f3-3376-4cf3-be6f-33a7122ab283
03-25 10:02 | e972a8b7-da04-4b9f-8d26-fad0350a2e09
```

## Usage Examples

```bash
/session id                          # Look up current session ID
/session id Makefile remove          # Search sessions by keyword "Makefile remove"
/session id --today ansible/Makefile # Search only today's sessions by file path
```

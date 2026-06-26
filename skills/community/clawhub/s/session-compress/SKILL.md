---
name: session-compress
description: Compress OpenClaw session .jsonl files to reduce context size while preserving active tasks, plans, and important context. Triggers when user says: compress session, shrink context, reduce session size, compress conversation, trim session history, 压缩会话, 压缩上下文.
---

# session-compress

Compress an OpenClaw `.jsonl` session file by trimming old messages while retaining active task context and basic message structure.

## When to Use

- User asks to compress, shrink, or trim a session file
- Session context is too large and causing performance issues
- Before archiving an old session but wanting to preserve task memory

## Workflow

### Step 1: Identify the target file

Session files are located at:
```
<OPENCLAW_DIR>\agents\main\sessions\*.jsonl
```

List files by size to find candidates:
```powershell
Get-ChildItem <OPENCLAW_DIR>\agents\main\sessions\*.jsonl | Sort-Object Length -Descending | Select-Object Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}}
```

### Step 2: Dry run first

**Always dry run before modifying anything:**
```powershell
powershell -File scripts/compress.ps1 -FilePath "<path-to-file>" -DryRun
```

Review: how many messages will be kept, what the output size will be.

### Step 3: Compress

```powershell
# In-place compress (overwrites original):
powershell -File scripts/compress.ps1 -FilePath "<path-to-file>"

# Compress to a new file (preserves original):
powershell -File scripts/compress.ps1 -FilePath "<path-to-file>" -OutputPath "<new-path>"
```

### Compression Logic

1. **Always kept**: All `system` role messages
2. **Always kept**: Last 30 message turns (configurable via `-KeepRecent`)
3. **Conditionally kept** (task context keywords): messages containing keywords like `next step`, `todo`, `plan`, `task`, `pending`, `in progress`, `remember`, `dont forget`, `important`
4. **Summarized**: Culled messages are replaced with a single placeholder message — preserving the file structure so OpenClaw can still load it
5. **Deduplicated**: No message appears twice in the output

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-FilePath` | (required) | Path to the .jsonl file |
| `-KeepRecent` | 30 | Number of recent turns to always keep |
| `-OutputPath` | (none) | If set, writes to a new file instead of overwriting |
| `-DryRun` | off | Preview without modifying files |

### What Gets Preserved

Each message in the output `.jsonl` retains:
- `role` (system / user / assistant)
- `content` (as array of content blocks)
- `timestamp`

### What Gets Removed

- Older messages not in the recent window and not flagged as task-relevant
- Tool call metadata is stripped (content blocks are kept as text)

### Important Notes

- **Always dry run first** — compression is destructive unless `-OutputPath` is used
- This skill is for the **main agent session files only**
- After compression the file remains a valid `.jsonl` that OpenClaw can load normally

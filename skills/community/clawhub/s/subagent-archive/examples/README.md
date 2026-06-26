# Examples / 示例输出

This directory contains sample outputs from `archive-sessions.ps1` to help you understand the script's behavior at a glance.

## Files

### `sample-dry-run-output.txt`

Sample output of a `dry-run` execution against a typical OpenClaw agent. The agent has:
- 1 main session (protected)
- 5 cron jobs (protected)
- 1 dashboard parent with `status=done` (will archive)
- 3 orphan physical files (will delete on enforce)
- 0 stale sessions.json keys
- 0 abnormal keys (status missing)

### `sample-multi-workspace-error.txt`

Sample output when the script auto-detects **multiple** workspaces and the user didn't provide `-WorkspaceDir`. Shows the friendly error message.

### `sample-json-output.json`

Sample JSON output (using `-Json` flag) suitable for CI/CD integration.

### `sample-log-entry.md`

Sample append-write entry that gets added to `<workspace>/memory/YYYY-MM-DD-subagent-archive-v3.md` after a successful run.

### `sample-dashboard-archive.md`

Sample append-write entry that gets added to `<workspace>/memory/dashboard-archives/YYYY-MM-DD-dashboard-<sessionId>.md` for a `status=done` dashboard parent.

## Regenerating Samples

To regenerate these samples with your own agent:

```powershell
# Capture dry-run output
pwsh ../scripts/archive-sessions.ps1 -Agent myagent > sample-dry-run-output.txt

# Capture JSON output
pwsh ../scripts/archive-sessions.ps1 -Agent myagent -Json | Out-File sample-json-output.json -Encoding utf8

# Manually inspect the log entries created in your workspace's memory/ directory
```

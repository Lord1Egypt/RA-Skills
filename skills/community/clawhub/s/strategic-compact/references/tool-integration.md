# Tool Integration Guide

## Overview

The `suggest-compact.sh` script monitors tool call count during long sessions and suggests manual compaction at strategic points. It helps avoid arbitrary auto-compaction mid-task by proposing `/compact` at logical phase boundaries.

## How It Works

- **Tracks tool calls** — Increments a session-specific counter in `/tmp/claude-tool-count-${SESSION_ID}`
- **Suggests at thresholds** — First suggestion at `COMPACT_THRESHOLD`, then every 25 calls after
- **Session-aware** — Uses `CLAUDE_SESSION_ID` for stability; falls back to `PPID` if not set

## Manual Invocation

```bash
bash scripts/suggest-compact.sh
```

Outputs suggestion to stderr if threshold is reached:
```text
[StrategicCompact] 50 tool calls reached - consider /compact if transitioning phases
```

## Configuration

### `COMPACT_THRESHOLD` Environment Variable

```bash
# Default: 50 tool calls
export COMPACT_THRESHOLD=50

# Customize for your needs (lower = more frequent suggestions)
export COMPACT_THRESHOLD=30
bash scripts/suggest-compact.sh
```

### `CLAUDE_SESSION_ID` Session Tracking

The script uses `CLAUDE_SESSION_ID` to persist the tool count across multiple invocations in the same session:

```bash
export CLAUDE_SESSION_ID="session-abc123"
bash scripts/suggest-compact.sh  # Counter increments
bash scripts/suggest-compact.sh  # Continues from previous count
```

If `CLAUDE_SESSION_ID` is not set, the script falls back to `PPID` (parent process ID) for basic session tracking.

## Integration Methods

### 1. Manual Invocation

Run manually when transitioning between phases:

```bash
bash scripts/suggest-compact.sh && /compact Phase complete, starting new work
```

### 2. Heartbeat Integration

Add to your `HEARTBEAT.md` checklist:

```markdown
- [ ] Run tool counter: `bash ~/.openclaw/skills/strategic-compact/scripts/suggest-compact.sh`
```

### 3. Hook Integration (Claude Code PreToolUse)

Place script in a pre-tool-use hook to run before each tool invocation. OpenClaw will check stderr for suggestions.

### 4. Cron Job Setup

Schedule periodic checks during long sessions:

```bash
# Every 30 minutes during work hours
*/30 9-17 * * * cd ~/.openclaw && CLAUDE_SESSION_ID=daily bash scripts/suggest-compact.sh
```

## Example Output

### First Threshold (50 calls)

```bash
[StrategicCompact] 50 tool calls reached - consider /compact if transitioning phases
```

### Regular Intervals (every 25 calls after threshold)

```bash
[StrategicCompact] 75 tool calls - good checkpoint for /compact if context is stale
[StrategicCompact] 100 tool calls - good checkpoint for /compact if context is stale
```

## Best Practices

- **Save before compacting** — Use `/write` to persist findings before invoking `/compact`
- **Preserve git state** — Commit work; compaction clears conversation but not disk files
- **Use meaningful messages** — `/compact Phase 2: implementation started` for clarity
- **Reset counter** — Remove `/tmp/claude-tool-count-*` files between unrelated sessions

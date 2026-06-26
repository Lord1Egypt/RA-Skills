# Watchdog Pattern

Use this pattern when `MONITOR_SUPPORT=true` and the activity log hook is installed (Step 4 of BAD setup). It detects subagents that have gone silent — no tool calls for a configurable period — and alerts via Telegram so the user can decide whether to wait, retry, or skip.

> **Requires:** Activity log hook installed via `scripts/setup-activity-hook.py`. Falls back to a fixed-timeout CronCreate watchdog when `MONITOR_SUPPORT=false`.

## How it works

1. **Record the log path** — before spawning a long-running subagent, compute the log directory for that agent.
2. **Spawn the subagent** with `run_in_background=true`.
3. **Start Monitor** — pass a poll script that watches the agent's log file modification time.
4. **React to events** — on `ALIVE` lines, keep waiting; on `STALE`, notify and ask the user.
5. **On agent completion** — stop Monitor, proceed normally.

## Log path formula

The activity hook writes to:
```
~/.claude/projects/<encoded-project>/bad-logs/<agent-slug>/<session_id>.log
```

Where:
- `<encoded-project>` = absolute project root with leading `/` removed and `/` replaced by `-`
- `<agent-slug>` = `coordinator` for the coordinator; worktree basename for story subagents (e.g. `story-4-auth-controller`)
- `<session_id>` = unique per Agent() call — not known until the agent starts writing

Because `session_id` is only known once the subagent has made its first tool call, watch the **directory** (`bad-logs/<agent-slug>/`) for any new or updated file rather than a specific filename.

## Poll script

```bash
#!/bin/bash
# Args: <log_dir> <agent_label> <stale_minutes>
LOG_DIR="$1"
AGENT_LABEL="$2"
STALE_MINUTES="${3:-60}"

touch /tmp/bad_watchdog_baseline

while true; do
  # Find newest log file in the agent's log directory
  NEWEST=$(find "$LOG_DIR" -name "*.log" -newer /tmp/bad_watchdog_baseline -type f 2>/dev/null | head -1)

  if [ -n "$NEWEST" ]; then
    echo "ALIVE: $AGENT_LABEL — activity detected"
    touch /tmp/bad_watchdog_baseline
    sleep 120
    continue
  fi

  # Check age of most recently modified log file
  LATEST=$(find "$LOG_DIR" -name "*.log" -type f 2>/dev/null | xargs stat -f "%m %N" 2>/dev/null | sort -n | tail -1 | awk '{print $1}')
  if [ -z "$LATEST" ]; then
    # No log file yet — agent hasn't made its first tool call
    echo "ALIVE: $AGENT_LABEL — waiting for first tool call"
    sleep 30
    continue
  fi

  NOW=$(date +%s)
  AGE_MIN=$(( (NOW - LATEST) / 60 ))

  if [ "$AGE_MIN" -ge "$STALE_MINUTES" ]; then
    LAST_LINE=$(find "$LOG_DIR" -name "*.log" -type f 2>/dev/null | xargs stat -f "%m %N" 2>/dev/null | sort -n | tail -1 | awk '{print $2}' | xargs tail -1 2>/dev/null || echo "unknown")
    echo "STALE:${AGE_MIN}:${LAST_LINE}"
    exit 1
  fi

  echo "ALIVE: $AGENT_LABEL — last activity ${AGE_MIN}m ago"
  sleep 120
done
```

## Coordinator usage

Before spawning a long-running subagent (Steps 2, 3, 4, 5 are the most likely to hang):

```
1. Compute LOG_DIR = ~/.claude/projects/<encoded>/bad-logs/<agent-slug>/
   (e.g. bad-logs/story-4-auth-controller/ for story 4's dev step)

2. Spawn subagent with run_in_background=true

3. Start Monitor with poll script:
     Monitor(script, args=[LOG_DIR, "story-4 Step 3", STALE_TIMEOUT_MINUTES])

4. React to Monitor events:
   - ALIVE:* → no action, keep waiting
   - STALE:<min>:<last_line> → send Telegram alert (see below), wait for user reply
   - Background agent completes → stop Monitor, proceed normally
```

## Telegram alert on STALE

```
⚠️ story-4 Step 3 appears stuck — no tool calls for {min} min.
Last activity: {last_line}

[K] Keep waiting another {STALE_TIMEOUT_MINUTES} min
[R] Retry — respawn this step from the start
[S] Skip this story and continue with others
[A] Abort BAD
```

Wait for user reply before taking any action.

- **[K]** — restart the Monitor watchdog (reset the staleness baseline); keep the background agent running
- **[R]** — stop Monitor; note the story as failed at this step; spawn a fresh subagent for the same step; restart Monitor
- **[S]** — stop Monitor; mark story as failed; continue pipeline with remaining stories
- **[A]** — stop Monitor; halt BAD; send summary of completed work

## If `MONITOR_SUPPORT=false`

Use a CronCreate timer as a fixed-timeout fallback. Set the timer to `STALE_TIMEOUT_MINUTES * 2` (double, since you cannot detect inactivity — only total elapsed time). On timer fire, send the same Telegram alert with the same options.

```
CronCreate(
  fire_in_seconds = STALE_TIMEOUT_MINUTES * 120,
  prompt = "BAD_WATCHDOG_FIRED:<agent_label> — fixed timeout elapsed. Send Telegram alert and await user reply."
)
```

## Configuration

`STALE_TIMEOUT_MINUTES` — read from BAD config. Default: `60`. Set lower (e.g. `30`) for faster detection; set higher (e.g. `90`) if your dev steps routinely involve long read-heavy analysis phases.

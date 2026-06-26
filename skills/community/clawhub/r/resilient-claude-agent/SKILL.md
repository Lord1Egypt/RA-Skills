---
name: resilient-claude-agent
description: "Run Claude Code sessions in tmux for fire-and-forget execution with crash recovery, model routing, and structured task state."
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: [tmux, claude, openclaw]
---

# Resilient Coding Agent

Long-running coding tasks are vulnerable to interruption: orchestrator restarts, process crashes, network drops. This skill decouples Claude Code from the orchestrator using tmux, enabling fire-and-forget execution with automatic resume on interruption. The orchestrator specifies which model to use; the skill handles session lifecycle, crash recovery, and output capture.

## Trust Model

This skill runs Claude Code with `--dangerously-skip-permissions` and dispatches commands into tmux via `send-keys`. These are required capabilities, not bugs — the whole point is fire-and-forget execution with no human in the loop to approve prompts. Read this section before installing so you understand exactly what you are enabling.

**What this skill can do at runtime:**

- Execute Claude Code without any permission prompts. Claude will read, write, and run bash commands in the project directory without asking. If a coding agent with full filesystem and shell access inside your project is not acceptable, do not install this skill.
- Create and kill tmux sessions whose names match `claude-<task-name>`. If you run other tmux sessions with that prefix, the monitor's cleanup path could terminate them.
- Dispatch bash commands into tmux via `send-keys`. The orchestrator controls what gets dispatched, so a compromised or buggy orchestrator can use this skill to run arbitrary bash in the project directory.
- Write files to a secure temp directory (`mktemp -d`, `chmod 700`) and to the project directory via Claude Code.
- Fire `openclaw system event` notifications (fire-and-forget, failures swallowed).

**What this skill does NOT do:**

- No remote downloads, no archive extraction, no out-of-band installs.
- No environment variables or credentials are required. `MONITOR_*` env vars only tune timing.
- No modifications outside the task temp directory and the project directory Claude is working in.
- No network access beyond what Claude Code itself initiates.

**Guarantees the skill enforces:**

- Session names are sanitized (`monitor.sh` rejects anything outside `[A-Za-z0-9._-]`) before being passed to tmux, preventing injection through the session-name argument.
- Task prompts are delivered via stdin redirect (`claude -p - < "$TMPDIR/prompt"`), never interpolated into shell arguments. They are invisible to `ps`/`top` and not subject to shell expansion. This depends on the orchestrator's `write` tool not invoking a shell to create the prompt file — OpenClaw's built-in `write` tool meets this requirement.
- All manifest updates use write-to-tmp + `mv` for atomicity; the Brain never reads a partially-written manifest.
- The `done` file is written last, so a process that exits mid-update never appears complete.

**Deployment expectations:**

- Run under a trusted orchestrator. Only install this skill in workspaces where you already trust the orchestrator to execute code in your project.
- Prefer a dedicated user, VM, or container for any coding agent with `--dangerously-skip-permissions` enabled, including this one.
- Audit the `claude` and `openclaw` binaries on your PATH. This skill inherits whatever those binaries do.
- Do not share tmux sessions across unrelated work if you use the `claude-` prefix for other purposes.

If you need a version with an explicit, auditable consent mechanism instead of `--dangerously-skip-permissions`, this skill is not the right choice — the permission bypass is fundamental to fire-and-forget execution.

## Placeholders

- **`<task-name>`** -- Sanitized task identifier. Must match `[a-z0-9-]` only.
- **`<project-dir>`** -- Valid existing directory where the task executes.
- **`<model>`** -- Model tier passed by the Brain. Maps to a full model name in the launch command:

| Brain sends | CLI receives |
|-------------|-------------|
| `opus` | `claude-opus-4-6` |
| `sonnet` | `claude-sonnet-4-6` |

Full model names are used for determinism. Aliases auto-resolve to the latest version, which could change behavior unexpectedly.

## Temp Directory and Prompt Safety

Each task uses a secure temp directory created with `mktemp -d`. Store this path and use it for all task files (prompt, events, session state). This avoids predictable filenames and symlink/race conditions.

```bash
TMPDIR=$(mktemp -d)
chmod 700 "$TMPDIR"
```

**Prompt safety:** Task prompts are never interpolated into shell commands. Instead, write the prompt to a temp file using the orchestrator's `write` tool (no shell involved). The wrapper reads the prompt via stdin redirection (`claude -p --model "$MODEL" - < "$TASK_TMPDIR/prompt"`), so the prompt content never appears in process arguments (invisible to `ps`/`top`) and is not subject to shell interpolation. This depends on the orchestrator's `write` tool not invoking a shell; OpenClaw's built-in `write` tool meets this requirement.

**Sensitive output:** tmux scrollback and log files may contain secrets or API keys from agent output. On shared machines, restrict file permissions (`chmod 600`) and clean up temp directories after task completion.

## When to Use This

Use this skill when the orchestrator explicitly delegates a coding task. Typical use cases include:
- Coding, debugging, refactoring, and architecture work
- File exploration, search, and analysis
- Test writing and test debugging
- Documentation generation
- Code review and security analysis

The orchestrator decides when to delegate through this skill. Do not self-invoke.

## Task Directory Schema

Every task operates within a secure temp directory. The following layout is the canonical specification -- all phases build on this convention.

```
$TMPDIR/                         # mktemp -d, chmod 700
  prompt                         # Task instructions
                                 #   Written by: orchestrator write tool
                                 #   Read by: Claude Code via $(cat)

  pid                            # Claude Code child process PID
                                 #   Written by: wrapper.sh ($!, atomic write)
                                 #   Read by: monitor.sh (kill -0)

  output.log                     # Continuous output capture
                                 #   Written by: tmux pipe-pane
                                 #   Read by: Brain (tail -n 50), monitor (mtime)

  manifest                       # Structured task state (key=value)
                                 #   Written by: orchestrator (initial) + wrapper.sh (PID, completion)
                                 #   Read by: Brain (grep '^status=' | cut -d= -f2-), monitor

  done                           # Completion marker (presence = complete)
                                 #   Written by: wrapper.sh on exit
                                 #   Read by: monitor.sh ([ -f done ])

  exit_code                      # Process exit code (numeric string)
                                 #   Written by: wrapper.sh (echo $?)
                                 #   Read by: monitor.sh, Brain

  resume                         # Resume signal (written by monitor, consumed by wrapper)
                                 #   Written by: monitor.sh (dispatch_resume)
                                 #   Read by: wrapper.sh (mode detection)
                                 #   Deleted by: wrapper.sh on resume
```

The `resume` file is a transient signal used by the monitor to tell the wrapper to resume rather than start fresh. All other files persist after task completion for result retrieval.

## Start a Task

Create a tmux session and launch Claude Code with the appropriate model. The launch sequence uses `scripts/wrapper.sh` which handles PID capture, manifest updates, completion notification, and the done-file protocol. The same wrapper handles both first-run and resume modes.

```bash
# Step 1: Create secure temp directory
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"

# Step 2: Write prompt to file (use orchestrator's write tool, not echo/shell)
# File: $TMPDIR/prompt

# Step 3: Create initial manifest
# model accepts short aliases (opus, sonnet) or full names (claude-opus-4-6, claude-sonnet-4-6)
cat > "$TMPDIR/manifest" << EOF
task_name=<task-name>
model=<model>
project_dir=<project-dir>
session_name=claude-<task-name>
pid=0
tmpdir=$TMPDIR
started_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
status=running
EOF

# Step 4: Create tmux session (pass TMPDIR via env)
tmux new-session -d -s claude-<task-name> -e "TASK_TMPDIR=$TMPDIR"

# Step 5: Start output capture with ANSI stripping (BEFORE send-keys)
tmux pipe-pane -t claude-<task-name> -O \
  "perl -pe 's/\x1b\[[0-9;]*[mGKHfABCDJsu]//g; s/\x1b\][^\x07]*\x07//g; s/\x1b\(B//g; s/\r//g' >> $TMPDIR/output.log"

# Step 6: Launch via wrapper script
tmux send-keys -t claude-<task-name> \
  'bash <skill-dir>/scripts/wrapper.sh' Enter
```

**Step 3 -- manifest** creates `manifest` with all fields before the tmux session exists. PID is set to `0` (placeholder) because the real PID is not known until after background launch.

**Step 5 -- pipe-pane** is set BEFORE send-keys to guarantee no output is missed. The `-O` flag captures only pane output (not input). The perl chain strips four categories of ANSI escapes: CSI sequences (colors, cursor movement), OSC sequences (window titles), charset selection, and carriage returns (progress bar overwrites).

**Step 6 -- wrapper** invokes `scripts/wrapper.sh`, which reads `TASK_TMPDIR` from the tmux session environment (set in Step 4) and `model`/`project_dir` from `manifest` (created in Step 3). The wrapper detects its mode from the filesystem: if `done` exists, it exits early; if `resume` exists (written by the monitor), it runs `claude -c`; otherwise it runs `claude -p` with the prompt. In all active modes, the wrapper: (1) launches Claude Code in background, (2) writes the real PID to `$TASK_TMPDIR/pid`, (3) updates manifest with running status, (4) waits for completion, (5) writes exit_code and completion manifest atomically, (6) fires `openclaw system event` (fire-and-forget), and (7) `touch done` as the last operation. This ensures resume operations get the same full lifecycle management as first runs.

Replace `<model-name>` with the full model name from the mapping table:
- Brain sends `opus` --> use `claude-opus-4-6`
- Brain sends `sonnet` --> use `claude-sonnet-4-6`

Replace `<skill-dir>` with the absolute path to this skill's directory. The Brain already resolves this path when launching `scripts/monitor.sh` in Step 9.

The wrapper invokes Claude Code with `--dangerously-skip-permissions -p --model <model>`. `-p` enables non-interactive (print) mode for fire-and-forget execution. `--model` selects the model tier. `--dangerously-skip-permissions` is required because fire-and-forget execution inside tmux cannot handle interactive permission prompts -- without it, the agent stalls on the first file write. This skill is designed for trusted, orchestrator-delegated coding tasks where permission prompts would block the entire flow.

## Monitor Progress

Continuous output is captured to `$TMPDIR/output.log` via pipe-pane (set up in Step 4 of the launch sequence). This is the preferred way to read task output:

```bash
# Read recent output from continuous log (preferred)
tail -n 50 $TMPDIR/output.log
```

Both `output.log` and `manifest` persist after the tmux session is killed -- `$TMPDIR` is created outside the session and is not deleted by monitor cleanup or `tmux kill-session`. This means result retrieval via `tail -n 50 $TMPDIR/output.log` works even after the session is gone.

For ad-hoc checks or manual debugging, tmux capture-pane is still available:

```bash
# Check if the session is still running
tmux has-session -t claude-<task-name> 2>/dev/null && echo "running" || echo "finished/gone"

# Read recent output (last 200 lines) via tmux
tmux capture-pane -t claude-<task-name> -p -S -200

# Read the full scrollback via tmux
tmux capture-pane -t claude-<task-name> -p -S -
```

Check progress when:
- The user asks for a status update
- You want to proactively report milestones

## Health Monitoring

Use the active monitor script for every task. The monitor runs continuously with configurable intervals and handles its own timing -- no cron or external scheduler needed.

```bash
nohup bash <skill-dir>/scripts/monitor.sh claude-<task-name> "$TMPDIR" \
  >"$TMPDIR/monitor.log" 2>&1 &
```

`nohup` is critical: it makes the monitor ignore SIGHUP so it survives the orchestrator's shell context ending. Without it, the monitor can be killed when its launching shell exits, leaving tasks without a watchdog. Output goes to `$TMPDIR/monitor.log` for post-hoc inspection.

The monitor uses a layered detection flow, checked in this exact priority order every iteration:

1. **Done-file check** -- If `$TASK_TMPDIR/done` exists, the task completed. Read `$TASK_TMPDIR/exit_code` for the result. Exit monitor.
2. **PID liveness check** -- Read PID from `$TASK_TMPDIR/pid` and test with `kill -0 $PID`. If the process is dead, the monitor waits 2 seconds and re-checks the done-file (closing the race where the wrapper is still writing completion markers after Claude exits). If done appears during the grace window, treat as success. Otherwise the task crashed: update `manifest` to `status: "crashed"` with `retry_count` and `last_checked_at`, create a `resume` marker file, remove the stale `pid` file, and dispatch `scripts/wrapper.sh` into the tmux session. The wrapper detects the `resume` marker and runs `claude -c` with full lifecycle management.
3. **Pane state classification (advisory)** -- Capture the last 30 lines of the tmux pane and match against known patterns. Detects `waiting_for_input` (approval/trust prompts that should not appear with `--dangerously-skip-permissions`), `crash_text` (panic/segfault markers), and `upgrade_nag`. The classified state is written to `manifest.pane_state` for observability. `waiting_for_input` is the only actionable state: the monitor abandons immediately with `abandon_reason: "waiting_for_input"` because nothing is going to answer the prompt.
4. **Output staleness check** -- If the process is alive but `output.log` mtime exceeds the staleness threshold (3x base interval, default 90 seconds), the monitor enters a grace period. On the first stale detection, no action is taken -- only a timestamp is recorded. If output remains stale for the full grace period duration, the monitor treats it as a hang: updates the manifest to `status: "hung"` and dispatches `scripts/wrapper.sh` for resume (same flow as crash recovery).

The done-file is checked FIRST because a completed task may have a dead PID (expected). Only if done-file is absent does a dead PID indicate a crash. Pane classification and staleness checks only run for live processes.

On consecutive failures, the monitor doubles the polling interval (exponential backoff) and resets when the agent produces fresh output. The monitor stops after the configured deadline (default 5 hours wall-clock).

### Configuration

Override monitor behavior by setting environment variables before launching the monitor:

| Variable | Default | Purpose |
|----------|---------|---------|
| `MONITOR_BASE_INTERVAL` | `30` (seconds) | Base polling interval; doubles on each consecutive failure |
| `MONITOR_MAX_INTERVAL` | `300` (5 minutes) | Maximum polling interval cap |
| `MONITOR_DEADLINE` | `18000` (5 hours) | Wall-clock deadline; monitor exits after this |
| `MONITOR_GRACE_PERIOD` | `30` (seconds) | Grace period before acting on stale output |
| `MONITOR_MAX_RETRIES` | `10` | Maximum resume attempts before abandoning task |
| `MONITOR_DISPATCH_WAIT` | `10` (seconds) | Post-resume wait before next monitor check |

The staleness threshold is derived as 3x `MONITOR_BASE_INTERVAL` (default: 90 seconds). To adjust hang detection sensitivity, change `MONITOR_BASE_INTERVAL` -- the staleness threshold scales automatically.

### Cleanup and Abandonment

When the deadline is reached, max retries exceeded, or the monitor is terminated (signal, manual kill), an EXIT trap fires automatically:

1. **Manifest update** -- Sets `manifest` status to `"abandoned"` with an `abandoned_at` timestamp, unless the task already completed (done-file exists) or was already marked abandoned by the max-retry path. This guard prevents overwriting a completed task's manifest.
2. **Notification** -- Fires `openclaw system event` to notify the Brain that the task was abandoned.
3. **Session cleanup** -- Disables `pipe-pane` and kills the tmux session, preventing orphan processes.

When max retries are exceeded, the manifest is updated with `status: "abandoned"`, `abandon_reason: "max_retries_exceeded"`, and the final `retry_count` before the EXIT trap fires.

All exit paths (deadline, max retries, signal, error) trigger the same cleanup sequence.

## Recovery After Interruption

For automated crash detection and retries, use **Health Monitoring** above. Keep this section as a manual fallback when you need to intervene directly:

```bash
# Resume the most recent Claude Code session in the working directory
tmux send-keys -t claude-<task-name> 'claude -c' Enter
```

`claude -c` continues the most recent conversation in the current working directory. This is the correct resume command for Claude Code sessions running inside tmux, where only one conversation exists per session.

## Cleanup

After a task completes, disable pipe-pane before killing the session. This prevents orphan perl processes that would otherwise hold stale file descriptors:

```bash
tmux pipe-pane -t claude-<task-name>  # Disable pipe-pane (no command = disable)
tmux kill-session -t claude-<task-name>
```

List all coding agent tmux sessions:

```bash
tmux list-sessions 2>/dev/null | grep -E '^claude-'
```

## Naming Convention

Tmux sessions use the pattern `claude-<task-name>`:

- `claude-refactor-auth`
- `claude-review-pr-42`
- `claude-fix-api-tests`

Keep names short, lowercase, hyphen-separated. The `claude-` prefix identifies sessions managed by this skill.

## Checklist

Before starting a task:

1. Create secure temp directory (`mktemp -d` + `chmod 700`)
2. Write prompt to `$TMPDIR/prompt` via orchestrator write tool
3. Create initial `manifest` (all fields, pid=0 placeholder)
4. Create tmux session with `TASK_TMPDIR` env var
5. Set up pipe-pane output capture with ANSI stripping
6. Launch Claude Code with wrapper (PID capture + manifest updates + done-file protocol)
7. Verify pipe-pane is capturing output (`ls -la $TMPDIR/output.log`)
8. Notify user: task content, session name (`claude-<task-name>`), model used
9. Launch monitor: `nohup bash <skill-dir>/scripts/monitor.sh claude-<task-name> "$TMPDIR" >"$TMPDIR/monitor.log" 2>&1 &` (mandatory for every task; `nohup` ensures the monitor survives parent shell exit)

## Limitations

- tmux sessions do not survive a **machine reboot** (tmux itself is killed). For reboot recovery, `claude -c` in the project directory will resume the most recent conversation.
- Interactive approval prompts inside tmux require manual `tmux attach` or `tmux send-keys`. Use `-p` flag for non-interactive mode.

## Prerequisites

This skill requires:
- **tmux** -- Process isolation and session management
- **Claude Code CLI** (`claude`) -- The coding agent that executes tasks

The orchestrator must be configured to delegate coding tasks through this skill instead of attempting them directly. SKILL.md is the orchestrator's interface -- it reads this document and follows the instructions.

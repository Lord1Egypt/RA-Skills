---
name: tmux-bridge
description: Cross-pane messaging for AI agents.
metadata:
  { "openclaw": { "emoji": "🌉", "os": ["darwin", "linux"], "requires": { "bins": ["tmux"] } } }
---

# tmux-bridge

Simple CLI for cross-pane messaging with explicit reply tracking.

## Commands

```bash
tmux-bridge -l <session_name> [delay_secs]               # Short alias for launch
tmux-bridge -k <session_name>                            # Short alias for kill-session
tmux-bridge launch <session_name> [delay_secs]          # Create 3-pane AI workspace and attach
tmux-bridge kill-session <session_name>                 # Kill a tmux session by name
tmux-bridge list                                         # List panes with labels p1, p2...
tmux-bridge pending                                      # Show unresolved incoming reply requests
tmux-bridge rename                                       # Auto-rename panes to p1, p2...
tmux-bridge send --expect-reply <target> <msg>          # Send message and require a reply
tmux-bridge send --no-reply <target> <msg>              # Send informational message without reply
tmux-bridge reply <msg>                                  # Reply to latest pending request in current pane
tmux-bridge auto-label                                   # Output auto-label config for tmux.conf
tmux-bridge help                                         # Show help
```

## Protocol

- `--expect-reply` creates a pending item for the target pane.
- `pending` is how an agent decides whether the current request came from another pane.
- `reply` consumes the latest pending item for the current pane.
- If there is no pending item, `reply` fails with `no pending reply target for this pane`.

## Examples

```bash
# Start a fresh AI workspace session from a normal shell
tmux-bridge -l mysession

# Close a session by name
tmux-bridge -k mysession

# Long form remains supported
tmux-bridge launch mysession

# Start with a custom rename delay
tmux-bridge launch mysession 10

# Close a session by name
tmux-bridge kill-session mysession

# Ask another agent to investigate and report back
tmux-bridge send --expect-reply p1 'Please review src/auth.ts'

# Broadcast a status update without requiring a response
tmux-bridge send --no-reply p1 'I am rebasing now'

# Before final answer, check whether current pane owes another agent a reply
tmux-bridge pending

# Return the conclusion
tmux-bridge reply 'Review done: no issues found'
```

## Target Format

- `%N` - pane ID (for example `%19`)
- `p1`, `p2`, ... - pane label in the current session
- `session:win.pane` - full pane reference

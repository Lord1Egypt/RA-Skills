---
name: tmux-remote
description: Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
metadata: {"clawdbot":{"emoji":"🧵","os":["darwin","linux"],"requires":{"bins":["tmux"]}}}

# tmux

Remote-control tmux sessions for interactive CLIs.

## Basics

List sessions:
```bash
tmux ls
```

Attach to session:
```bash
tmux attach -t session-name
```

Create new session:
```bash
tmux new -s session-name
```

## Panes and Windows

Split pane (vertical):
```bash
tmux split-pane -v
```

Split pane (horizontal):
```bash
tmux split-pane -h
```

New window:
```bash
tmux new-window
```

Switch pane:
```bash
tmux select-pane -[U|D|L|R]
```

## Keybindings

Prefix: `Ctrl-b`

- `c` - Create new window
- `n` - Next window
- `p` - Previous window
- `w` - List windows
- `d` - Detach
- `%` - Split pane horizontally
- `"` - Split pane vertically
- `o` - Cycle panes
- `arrow keys` - Navigate panes
- `?` - List keybindings
- `:` - Command prompt

## Commands

Execute command in pane:
```bash
tmux send-keys -t session-name:window.pane "command" Enter
```

Capture pane output:
```bash
tmux capture-pane -t session-name:window.pane -p
```

Kill pane:
```bash
tmux kill-pane -t session-name:window.pane
```

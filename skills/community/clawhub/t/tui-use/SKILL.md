---
name: tui-use
description: Operate TUI (terminal user interface) programs through the tui-agent CLI tool. Use this skill whenever the user asks to interact with, automate, control, or test any terminal-based program — including editors (vim, nano, emacs), system monitors (htop, top, btop), file managers (ranger, mc), database clients (mycli, pgcli), or any ncurses/TUI application. Also trigger when the user mentions tui-agent, screen capture of terminal programs, sending keystrokes to running programs, or automating terminal workflows. Even if the user just says "open vim and edit a file" or "check what's running in htop", this skill applies.
---

# TUI-Use: Operating TUI Programs via tui-agent

This skill teaches you how to use the `tui-agent` CLI tool to start, interact with, and control TUI (Terminal User Interface) programs. Think of `tui-agent` as your eyes and hands for terminal programs — it lets you see what's on screen, type text, press keys, click with the mouse, and wait for things to happen.

## Prerequisites

`tui-agent` must be installed and available in PATH, you can clone from [tui-use github](https://github.com/zbflcy/tui-use/tree/main/tui-agent). Install from the sibling `tui-agent/` directory:
```bash
pip install -e tui-agent/
```

## Architecture at a Glance

```
You (via Bash tool)  -->  tui-agent CLI  -->  Daemon (auto-started)  -->  PTY  -->  TUI Program
                     <--  stdout/JSON    <--  Unix Socket             <--  pyte virtual screen
```

The daemon starts automatically on first use — no manual setup needed.

## Core Workflow

Every TUI interaction follows this pattern:

1. **Start** a session (launches the TUI program)
2. **Wait** for the program to be ready
3. **Capture** the screen to see what's displayed
4. **Interact** (type text, send keys, click, scroll)
5. **Capture** again to verify the result
6. **Stop** the session when done

This capture-act-capture loop is the fundamental rhythm. Always capture the screen before and after important actions so you can verify what happened.

## Command Reference

### Session Management

**Start a TUI program:**
```bash
tui-agent start --name <session-name> [--cols 120] [--rows 40] -- <command> [args...]
```
- `--name`: A unique identifier for this session (you'll use it in all subsequent commands)
- `--cols`/`--rows`: Terminal dimensions (default: 80x24). Use larger values for complex UIs
- Everything after `--` is the command to run

**List active sessions:**
```bash
tui-agent list
```

**Check session status:**
```bash
tui-agent status --name <session-name>
```

**Stop a session:**
```bash
tui-agent stop --name <session-name>
# Or stop everything:
tui-agent stop --all
```

### Seeing the Screen

**Capture full screen:**
```bash
tui-agent capture --name <session-name>
```

**Capture with cursor position:**
```bash
tui-agent capture --name <session-name> --cursor
```
This appends cursor coordinates to the output — helpful for knowing where you are in an editor.

**Capture a specific region:**
```bash
tui-agent capture --name <session-name> --top 0 --left 0 --height 5 --width 40
```

**Save a snapshot for later comparison:**
```bash
tui-agent capture --name <session-name> --save my_snapshot
```

**Compare current screen to a saved snapshot:**
```bash
tui-agent diff --name <session-name> --snapshot my_snapshot
```

**Read scrollback history** (content that scrolled off the top):
```bash
tui-agent scrollback --name <session-name> --lines 200
```

### Typing and Keys

**Type text:**
```bash
tui-agent type --name <session-name> "hello world"
```

**Type text and press Enter:**
```bash
tui-agent type --name <session-name> --enter "ls -la"
```

**Send special keys:**
```bash
tui-agent key --name <session-name> <key1> [key2] [key3...]
```

**Important: `key` vs `type`** — The `key` command only accepts special key names listed below. For regular characters (letters, numbers, symbols) like vim's `i`, `o`, `dd`, `:wq`, always use `type`. Use `key` only for keys that aren't printable characters.

Supported key names (case-insensitive):
- **Navigation**: `up`, `down`, `left`, `right`, `home`, `end`, `pageup`, `pagedown`
- **Editing**: `enter`/`return`, `tab`, `backspace`, `delete`, `insert`, `space`, `escape`/`esc`
- **Function keys**: `f1` through `f12`
- **Ctrl combos**: `ctrl-a` through `ctrl-z`

**Paste text** (uses bracketed paste mode, safe for editors):
```bash
tui-agent paste --name <session-name> "multi-line\ntext content"
```
Use `paste` instead of `type` when inserting multi-line content into editors — bracketed paste mode prevents the editor from interpreting line breaks as commands.

### Mouse Operations

**Click at a position** (0-indexed row and column):
```bash
tui-agent click --name <session-name> --row 5 --col 10
```

**Scroll up/down:**
```bash
tui-agent scroll-up --name <session-name> --row 12 --col 40 --lines 3
tui-agent scroll-down --name <session-name> --row 12 --col 40 --lines 3
```

### Waiting for Conditions

Waiting is critical for reliable automation. TUI programs take time to render, and acting too fast leads to errors.

**Wait for specific text to appear on screen:**
```bash
tui-agent wait --name <session-name> --text "Ready" --timeout 10
```

**Wait for text to disappear:**
```bash
tui-agent wait --name <session-name> --text "Loading..." --absent --timeout 15
```

**Wait for screen to stop changing** (stable for N seconds):
```bash
tui-agent wait --name <session-name> --stable 2.0 --timeout 10
```

Use `--stable` when you don't know exactly what text to expect, but need the program to finish rendering.

### Resizing the Terminal

```bash
tui-agent resize --name <session-name> --cols 160 --rows 50
```

## Best Practices

### Always wait before capturing

TUI programs need time to render. After starting a session or sending input, always wait before capturing:

```bash
tui-agent start --name ed -- vim file.py
tui-agent wait --name ed --stable 1.0         # Wait for vim to fully load
tui-agent capture --name ed --cursor           # Now safe to read the screen
```

### Use meaningful session names

Name sessions after their purpose, not the program:
- Good: `editor`, `monitor`, `file-browser`
- Bad: `s1`, `test`, `abc`

### Capture before and after actions

This is how you verify that your actions had the intended effect:

```bash
tui-agent capture --name ed --save before_edit
tui-agent type --name ed "i"                   # Enter insert mode (single char, use type)
tui-agent type --name ed "new line of code"
tui-agent key --name ed escape                 # Escape is a special key, use key
tui-agent capture --name ed                    # Check the result
```

### Choose appropriate terminal size

- For simple programs (bash, basic TUIs): `80x24` (default) is fine
- For editors or complex UIs: use `120x40` or larger
- For programs with wide tables: increase cols to `160+`

### Clean up sessions when done

Always stop sessions you no longer need:
```bash
tui-agent stop --name ed
```

Or stop all sessions if you're done:
```bash
tui-agent stop --all
```

### Handle errors gracefully

If a `wait` command times out (exit code 1), capture the screen to understand what happened instead of blindly retrying:

```bash
tui-agent wait --name ed --text "Success" --timeout 5
# If this fails, capture to see the actual state:
tui-agent capture --name ed
```

## Common Workflows

### Editing a File with nano

```bash
# Start nano
tui-agent start --name ed --cols 120 --rows 40 -- nano myfile.py
tui-agent wait --name ed --stable 1.0
tui-agent capture --name ed

# Type some code
tui-agent type --name ed "print('hello world')"
tui-agent key --name ed enter
tui-agent type --name ed "print('goodbye')"
tui-agent capture --name ed

# Save (Ctrl-O, then Enter to confirm filename)
tui-agent key --name ed ctrl-o
tui-agent wait --name ed --stable 0.5
tui-agent key --name ed enter
tui-agent wait --name ed --text "Wrote"

# Exit (Ctrl-X)
tui-agent key --name ed ctrl-x
tui-agent stop --name ed
```

### Editing a File with vim

Note: vim may not respond to input on some platforms (see Platform Notes). If vim works in your environment:

```bash
# Start vim (use -u NONE to avoid config issues)
tui-agent start --name ed --cols 120 --rows 40 -- vim -u NONE -N myfile.py
tui-agent wait --name ed --stable 1.0
tui-agent capture --name ed

# Navigate to a specific line (e.g., line 10)
tui-agent type --name ed ":10"
tui-agent key --name ed enter
tui-agent capture --name ed

# Enter insert mode and add text
tui-agent type --name ed "o"                    # Open new line below (normal char, use type)
tui-agent type --name ed "    print('hello')"
tui-agent key --name ed escape                  # Back to normal mode

# Save and quit
tui-agent type --name ed ":wq"
tui-agent key --name ed enter
tui-agent wait --name ed --stable 1.0
```

### Monitoring System with htop

```bash
# Start htop
tui-agent start --name mon --cols 160 --rows 50 -- htop
tui-agent wait --name mon --stable 2.0
tui-agent capture --name mon

# Search for a process
tui-agent key --name mon f3                     # F3 is a special key, use key
tui-agent type --name mon "python"
tui-agent key --name mon enter
tui-agent capture --name mon

# Scroll through the list
tui-agent scroll-down --name mon --row 25 --col 80 --lines 10
tui-agent capture --name mon

# Quit
tui-agent type --name mon "q"                   # Regular char, use type
tui-agent stop --name mon
```

### Running a Shell Command and Reading Output

```bash
# Start a bash session
tui-agent start --name sh -- bash --norc --noprofile
tui-agent wait --name sh --stable 1.0

# Run a command
tui-agent type --name sh --enter "ls -la /tmp"
tui-agent wait --name sh --stable 1.0
tui-agent capture --name sh

# If output is long, check scrollback
tui-agent scrollback --name sh --lines 100

# Exit
tui-agent type --name sh --enter "exit"
tui-agent stop --name sh
```

### Interacting with a ncurses Application

```bash
# Start any ncurses app (example: midnight commander)
tui-agent start --name fm --cols 120 --rows 40 -- mc
tui-agent wait --name fm --stable 2.0
tui-agent capture --name fm

# Navigate using arrow keys
tui-agent key --name fm down down down
tui-agent capture --name fm

# Press enter to open a directory
tui-agent key --name fm enter
tui-agent wait --name fm --stable 1.0
tui-agent capture --name fm

# Use function keys
tui-agent key --name fm f5                      # Copy dialog
tui-agent capture --name fm

# Quit
tui-agent key --name fm f10
tui-agent stop --name fm
```

## Platform Notes

**vim on macOS**: The system vim (`/usr/bin/vim`) may not respond to `type` input when launched directly via `tui-agent start`. This appears to be related to how macOS vim detects terminal capabilities. Workarounds:
- Use `nano` or `pico` instead — they work reliably with tui-agent
- Use `vim -u NONE -N` to disable vimrc and run in nocompatible mode
- Install a different vim build (e.g., via Homebrew: `brew install vim`)
- For simple file edits, consider using shell commands (`sed`, `awk`) instead of a TUI editor

**Other programs**: Most terminal programs (bash, htop, mc, ncurses apps) work well out of the box with tui-agent. If a program doesn't respond to input, try increasing the wait time or using `--stable` with a longer duration.

## Troubleshooting

**"session not found" error**: The session may have been stopped or the program exited. Check with `tui-agent list`.

**Screen capture is empty or garbled**: The program may not have finished rendering. Add a longer `--stable` wait or increase `--timeout`.

**Keys don't seem to work**: Some programs expect specific key sequences. Capture the screen to verify the program's current state (e.g., is vim in insert mode or normal mode?).

**Program exited unexpectedly**: Use `tui-agent status --name <session>` to check the exit code. The program may have crashed or received a signal.

**Daemon not running**: The daemon starts automatically. If issues persist, check if the socket file exists at `/tmp/tui-agent-*.sock`. You can manually start the daemon or simply retry the command.

---
name: which-tool
description: Locate the full path of executable commands in the system PATH. Find command locations, verify installation, and resolve command conflicts.
---

# Which Tool — Command Path Locator

Find the absolute path of executable commands by searching the system PATH. Essential for verifying installations, debugging "command not found" errors, detecting conflicting versions, and scripting command discovery.

## Quick Start

```bash
# Find where a command is installed
which-tool python

# Find multiple commands at once
which-tool python git docker

# Find all matching paths (not just the first)
which-tool -a node
```

## Usage

```bash
which-tool COMMAND [COMMAND...] [OPTIONS]

Options:
  -a, --all          Show all matching paths, not just the first
  -s, --silent       Exit silently (exit code only, no output)
  --readable         Show only readable executables
  --skip-aliases     Skip shell aliases, search real PATH only
  --json             Output as JSON array
  --resolve-symlinks Show real path after resolving symlinks
```

## Examples

```bash
# Check if a command exists
which-tool python3

# Find all Python installations
which-tool -a python3

# Check multiple tools before running a script
which-tool git node npm docker

# Silent check for scripts (use exit code)
which-tool -s required-tool && echo "Found"

# Resolve actual binary through symlinks
which-tool --resolve-symlinks node

# JSON output for automated checks
which-tool python java go --json
```

## Features

- **Standard PATH search** — follows shell PATH order
- **All matches** — `-a` flag to see every matching path
- **Silent mode** — exit code only, for script conditionals
- **Symlink resolution** — see the real target binary
- **Multiple commands** — batch check in one call
- **JSON output** — structured results for automation
- **Readable check** — filter to actually executable files

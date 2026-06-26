---
name: whoami-tool
description: Print the current effective username. Simple identity query for scripts, session tracking, and access control verification.
---

# Whoami Tool — Current User Identity

Display the current effective username (and optionally uid/gid/group membership). Essential for scripts that need to verify permissions, log user context, or conditionally execute based on identity.

## Quick Start

```bash
# Show current username
whoami-tool

# Show full identity
whoami-tool --full
```

## Usage

```bash
whoami-tool [OPTIONS]

Options:
  --full         Show username, UID, GID, and primary group
  --uid          Show numeric user ID only
  --groups       Show all group memberships
  --json         Output as structured JSON
  --check USER   Exit 0 if current user matches, 1 if not
```

## Examples

```bash
# Basic username
whoami-tool

# Full user identity
whoami-tool --full

# Check if running as root (for privilege checks)
whoami-tool --check root && echo "Running as root"

# Show all groups
whoami-tool --groups

# JSON output for logging
whoami-tool --json

# UID for numeric comparisons
whoami-tool --uid
```

## Features

- **Quick identity** — one command to know who you are
- **Full mode** — UID, GID, primary group
- **Group membership** — all groups the user belongs to
- **Identity check** — conditional execution based on username
- **JSON output** — structured for logging and automation
- **Exit codes** — 0 = success, useful for script conditionals

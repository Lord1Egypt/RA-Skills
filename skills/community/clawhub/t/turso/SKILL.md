---
name: turso
description: "Manage Turso SQLite databases via CLI - databases, groups, tokens, replicas. Use when user mentions 'turso', 'libsql', 'sqlite edge', or wants to manage Turso databases."
category: devtools
install_command: "brew install tursodatabase/tap/turso"
---

# turso

## Setup

macOS:
```bash
brew install tursodatabase/tap/turso
```

Linux/WSL:
```bash
curl -sSfL https://get.tur.so/install.sh | bash
```

Verify installation:
```bash
turso --version
```

Always use `--output json` flag when calling commands programmatically (where supported).

## Authentication

```bash
turso auth login
```

Get auth token:
```bash
turso auth token
```

## Resources

### Databases

| Command | Description |
|---------|-------------|
| `turso db list` | List all databases |
| `turso db create <name>` | Create a new database |
| `turso db create <name> --group <group>` | Create database in a specific group |
| `turso db destroy <name>` | Destroy a database |
| `turso db show <name>` | Show database details and URL |
| `turso db shell <name>` | Open interactive SQL shell |
| `turso db shell <name> "SELECT * FROM users"` | Run a SQL query directly |
| `turso db inspect <name>` | Inspect database size and usage |
| `turso db tokens create <name>` | Create an auth token for a database |
| `turso db tokens create <name> --expiration none` | Create a non-expiring token |

### Groups

| Command | Description |
|---------|-------------|
| `turso group list` | List all groups |
| `turso group create <name>` | Create a new group |
| `turso group create <name> --location <location>` | Create group in specific location |
| `turso group add-location <name> <location>` | Add a replica location to a group |
| `turso group remove-location <name> <location>` | Remove a replica location |
| `turso group destroy <name>` | Destroy a group |

### Organizations

| Command | Description |
|---------|-------------|
| `turso org list` | List organizations |
| `turso org switch <name>` | Switch to a different organization |

### Plan

| Command | Description |
|---------|-------------|
| `turso plan show` | Show current plan details |
| `turso plan upgrade` | Upgrade your plan |

## Global Flags

| Flag | Description |
|------|-------------|
| `--output json` | Output result as JSON |
| `--no-color` | Disable colored output |

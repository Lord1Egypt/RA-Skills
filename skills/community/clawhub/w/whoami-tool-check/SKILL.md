---
name: whoami-tool-check
description: Identity verification utility — validate current user against expected roles, check sudo access, and audit user capabilities. Extended whoami for security and access audits.
---

# Whoami Tool Check — Identity & Access Verifier

Extended identity verification: confirm the current user matches an expected role, verify sudo/root access, check group membership for specific capabilities, and audit user-level access for security-sensitive operations.

## Quick Start

```bash
# Verify current user
whoami-tool-check

# Check if current user has sudo access
whoami-tool-check --sudo
```

## Usage

```bash
whoami-tool-check [OPTIONS]

Options:
  --sudo          Check if user has sudo/root access
  --role ROLE     Verify user belongs to a role group (sudo, docker, admin, etc.)
  --capabilities  List all accessible system capabilities
  --audit         Full user audit: uid, gid, groups, sudo, shell, home
  --json          Output as structured JSON
  --check-user USER   Check if a specific user exists and their details
```

## Examples

```bash
# Full audit
whoami-tool-check --audit

# Check if user has docker access
whoami-tool-check --role docker

# List all capabilities
whoami-tool-check --capabilities

# Check if another user exists
whoami-tool-check --check-user www-data

# JSON for pipeline ingestion
whoami-tool-check --audit --json
```

## Features

- **Current identity** — standard whoami output
- **Sudo access check** — passwordless sudo availability
- **Role verification** — check group membership for specific roles
- **User audit** — comprehensive report (uid, gid, groups, sudo, shell, home dir)
- **User existence** — verify other system users
- **JSON output** — structured for security audits and automation
- **Exit codes** — 0/1 for easy script integration

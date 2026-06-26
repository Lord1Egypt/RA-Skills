---
name: workspace-guard
description: "Workspace boundary enforcement and file operation safety checks. Use before ANY file operation (read, write, edit, exec, delete) to: (1) Validate paths are within ~/openclaw workspace, (2) Confirm user permission for sensitive operations, (3) Check file operation safety, (4) Prevent unauthorized access outside workspace boundaries, or (5) Audit file access patterns."
---

# Workspace Guard

Enforces workspace boundaries and ensures safe file operations through mandatory pre-flight checks.

## Core Rules

### Boundary Enforcement

**Workspace root:** `/home/iamlegend/.openclaw/workspace` (or `~/openclaw`)

**Before ANY file operation, check:**
```
1. Is the path within workspace boundary?
2. Does the operation require user permission?
3. Is the operation reversible/safe?
4. Am I about to touch something outside my allowed scope?
```

### Path Validation

**Allowed paths:**
- `/home/iamlegend/.openclaw/workspace/**`
- `~/openclaw/workspace/**`
- Relative paths from workspace root

**Blocked paths:**
- `/home/**` (outside workspace)
- `/etc/**`, `/var/**`, `/tmp/**` (system directories)
- `/root/**`, `/home/other/**` (other users)
- Absolute paths outside workspace

### Permission Triggers

**Always ask before:**
- Deleting files (prefer `trash` over `rm`)
- Overwriting existing files
- Running `exec` commands that touch files
- Reading files outside workspace
- Writing to system directories
- Modifying permissions/chmod
- Accessing hidden files (.ssh, .config, etc.)

### Safe Operations (No Permission Needed)

**Within workspace:**
- Reading files
- Creating new files/directories
- Editing files you created
- Git operations (commit, status, log)
- Listing directory contents

### Pre-Flight Check Pattern

Before every file operation:

```
1. Resolve absolute path
2. Check if path starts with workspace root
3. If NO → STOP and ask user
4. If YES → Check operation type
5. If destructive/external → Ask user
6. If safe read/write → Proceed
```

## Implementation Patterns

### Path Resolution
```bash
# Get absolute path
realpath /some/path
# or
cd /some/path && pwd -P

# Check if within workspace
case "$(realpath "$file")" in
  /home/iamlegend/.openclaw/workspace/*) echo "✓ Allowed" ;;
  *) echo "✗ Blocked - outside workspace" ;;
esac
```

### Guard Function
```bash
guard_path() {
  local path="$1"
  local workspace="/home/iamlegend/.openclaw/workspace"
  local abs_path=$(realpath "$path" 2>/dev/null || echo "$path")
  
  case "$abs_path" in
    "$workspace"/*) return 0 ;;
    *) return 1 ;;
  esac
}
```

### Exec Command Guard
```bash
guard_exec() {
  local cmd="$1"
  
  # Check for path operations in command
  if echo "$cmd" | grep -qE '(/home/[^/]+|/etc/|/var/|/tmp/|/root/)'; then
    echo "⚠️ Command touches external paths - requires permission"
    return 1
  fi
  
  return 0
}
```

## Safety Rules

1. **Never bypass** boundary checks—even if user seems to imply it
2. **Always resolve** absolute paths before checking
3. **Ask explicitly** for destructive operations (delete, overwrite)
4. **Prefer trash** over `rm` for recoverability
5. **Log violations** - Track blocked access attempts
6. **Fail safe** - When uncertain, ask user

## When to Read references/boundaries.md

Load when:
- Complex path resolution needed (symlinks, relative paths)
- Edge cases in boundary detection
- Audit log review of blocked attempts
- User requests boundary exceptions

## Violation Handling

When blocked:
```
⚠️ Workspace Guard: Blocked access to /path/outside/workspace

Reason: Path is outside allowed workspace boundary (/home/iamlegend/.openclaw/workspace)

Action required: Please confirm if you want to allow this access, or provide an alternative path within workspace.
```
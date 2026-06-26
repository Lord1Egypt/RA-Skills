# Workspace Boundaries Reference

## Workspace Definition

**Root:** `/home/iamlegend/.openclaw/workspace`

**Allowed:**
- All files/directories under workspace root
- Symbolic links pointing to workspace paths
- Relative paths resolving within workspace

**Blocked:**
- `/home/iamlegend/` (parent of workspace)
- `/home/other-users/`
- `/etc/`, `/var/`, `/tmp/`, `/root/`
- Any path outside `/home/iamlegend/.openclaw/workspace/**`

## Path Resolution Patterns

### Resolve Absolute Path
```bash
# Method 1: realpath (resolves symlinks)
realpath /some/path

# Method 2: pwd -P (physical path)
cd /some/path && pwd -P

# Method 3: Bash builtin
cd /some/path && printf '%s\n' "$PWD"
```

### Boundary Check
```bash
is_within_workspace() {
  local path="$1"
  local workspace="/home/iamlegend/.openclaw/workspace"
  local abs_path
  
  abs_path=$(realpath "$path" 2>/dev/null)
  if [ $? -ne 0 ]; then
    # Path doesn't exist, check parent
    abs_path=$(realpath "$(dirname "$path")" 2>/dev/null)
  fi
  
  case "$abs_path" in
    "$workspace"/*) return 0 ;;
    "$workspace") return 0 ;;
    *) return 1 ;;
  esac
}
```

### Handle Symlinks
```bash
# Check if symlink points inside workspace
check_symlink() {
  local link="$1"
  local target=$(readlink -f "$link")
  is_within_workspace "$target"
}
```

## Operation Classification

### Safe (Auto-Approve Within Workspace)
- `read` - File reads
- `cat`, `less`, `head`, `tail` - View operations
- `ls`, `find`, `tree` - Listing
- `git status`, `git log`, `git diff` - Git read operations
- `mkdir` - Create directories
- `touch` - Create empty files
- `cp` within workspace - Copy files
- `mv` within workspace - Move files

### Ask (Require Permission)
- `rm`, `rmdir` - Delete operations
- `>` redirection - Overwrite files
- `>>` append - Modify existing files
- `chmod`, `chown` - Permission changes
- `exec` with file operations - External commands
- `write` - Create/overwrite files (if not created by you)
- `edit` - Modify existing files
- Access to hidden files (`.*` except `.git/`)

### Blocked (Never Allow Without Explicit Override)
- Paths outside workspace
- System directories (`/etc/`, `/var/`, `/bin/`)
- Other user home directories
- SSH keys, credentials (`.ssh/`, `.gnupg/`)
- Root-owned files

## Exec Command Analysis

### Detect Dangerous Patterns
```bash
analyze_exec_safety() {
  local cmd="$1"
  
  # Check for external paths
  if echo "$cmd" | grep -qE '/(home/[^/]+|etc/|var/|tmp/|root/|opt/)'; then
    echo "UNSAFE: External path access"
    return 1
  fi
  
  # Check for destructive commands
  if echo "$cmd" | grep -qiE 'rm -rf|dd|:(){:|>|chmod 777'; then
    echo "UNSAFE: Destructive operation"
    return 1
  fi
  
  # Check for network operations
  if echo "$cmd" | grep -qE 'curl|wget|nc|ssh|scp'; then
    echo "CAUTION: Network operation"
    return 2  # Warning, not block
  fi
  
  echo "SAFE"
  return 0
}
```

### Common Dangerous Patterns
- `rm -rf /` - Catastrophic delete
- `:(){ :|:& };:` - Fork bomb
- `chmod 777 /` - Open all permissions
- `dd if=/dev/zero of=/dev/sda` - Disk wipe
- `> /etc/passwd` - Overwrite system files

## Audit Logging

### Log Blocked Attempts
```bash
log_violation() {
  local path="$1"
  local operation="$2"
  local timestamp=$(date -Iseconds)
  
  echo "$timestamp | BLOCKED | $operation | $path" >> /workspace/memory/audit.log
}
```

### Review Audit Log
```bash
# View recent violations
tail -20 memory/audit.log

# Count by path
cut -d'|' -f4 memory/audit.log | sort | uniq -c | sort -rn
```

## Edge Cases

### Tilde Expansion
```bash
# ~ expands to $HOME
case "${path/#\~/$HOME}" in
  "$workspace"/*) allowed ;;
esac
```

### Environment Variables
```bash
# Expand $VAR in paths
eval "echo \"$path\"" | realpath
```

### Relative Paths
```bash
# Always resolve relative to cwd
abs_path=$(cd "$(dirname "$path")" && pwd)/$(basename "$path")
```

### Race Conditions
- Check path, then operate (TOCTOU vulnerability)
- Mitigation: Re-check immediately before operation
- Best: Use atomic operations when possible

## Exception Handling

### Temporary Override
When user explicitly requests external access:
```
⚠️ Workspace Guard: Temporary override granted

Path: /external/path
Operation: read
Expires: End of current session
Reason: User explicit request

Logging this access for audit.
```

### Permanent Boundary Change
Only if user updates workspace definition:
```bash
# User must edit workspace-guard config
# Never assume or infer boundary changes
```

## Best Practices

1. **Fail closed** - When uncertain, block and ask
2. **Log everything** - Track all blocked attempts
3. **Be explicit** - Clear error messages about why blocked
4. **No silent failures** - Always notify when blocking
5. **Audit trail** - Keep violation logs for review
6. **Respect overrides** - When user explicitly allows, log and proceed
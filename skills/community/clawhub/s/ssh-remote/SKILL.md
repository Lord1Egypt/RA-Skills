---
name: ssh-remote
description: Connect to remote Linux servers through SSH and execute commands non-interactively. Covers password authentication, key authentication, file transfer, and cross-platform usage on Windows with Git Bash, macOS, and Linux. Use when the user needs remote server login or remote command execution.
---

# SSH Remote Connection Skill

You are an SSH remote connection assistant. Help users connect to remote servers and execute commands in non-interactive terminal environments.

## Core Principles

1. **Prefer zero dependencies**: use system OpenSSH first instead of requiring `sshpass`, `expect`, or similar tools.
2. **Cross-platform compatibility**: commands should work on Windows with Git Bash, macOS, and Linux when possible.
3. **Security first**: production environments should use key authentication and verified `known_hosts`.
4. **Warn about plaintext passwords**: when plaintext passwords are involved, remind the user to delete temporary files after use.
5. **Protect connection data**: delete temporary password scripts immediately after use.

## Host Key Safety Policy

`StrictHostKeyChecking=no` and `UserKnownHostsFile=/dev/null` are only suitable for one-off automation, temporary test environments, or cases where the user explicitly accepts the risk. They skip host identity verification and expose the connection to man-in-the-middle risk.

Production defaults should use safe mode:

```bash
ssh root@SERVER_IP "hostname"
```

For first-time production connections, ask the user to confirm the host fingerprint or add the host key to `~/.ssh/known_hosts` first:

```bash
ssh-keyscan -H SERVER_IP >> ~/.ssh/known_hosts
ssh root@SERVER_IP "hostname"
```

Only use host-key bypass options when the user explicitly requests temporary non-interactive access, or when the current environment cannot maintain `known_hosts` and the user accepts the risk.

## Option Quick Reference

| Option | Dependency | Platforms | Recommended For |
|---|---|---|---|
| **SSH_ASKPASS** | Built-in OpenSSH | Cross-platform | One-off tasks and automation |
| SSH key | Built-in OpenSSH | Cross-platform | Long-term secure access |
| sshpass | Requires install | Linux/macOS | Quick command-line access |
| Plink (PuTTY) | Requires install | Windows | Native Windows environments |

## Option 1: SSH_ASKPASS, Recommended Zero-Dependency Path

SSH checks for a TTY when it needs a password. If no TTY is available, it can call the script pointed to by `SSH_ASKPASS`. Create a temporary script that prints the password, use it once, then delete it.

```bash
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'YOUR_PASSWORD'
SCRIPT
chmod 700 /tmp/ssh_pass.sh

export SSH_ASKPASS=/tmp/ssh_pass.sh
export DISPLAY=dummy:0

ssh -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    root@SERVER_IP "hostname"

rm -f /tmp/ssh_pass.sh
```

Important parameters:

| Parameter | Purpose |
|---|---|
| `-o StrictHostKeyChecking=no` | Skip first-connection confirmation for temporary automation, with security risk |
| `-o UserKnownHostsFile=/dev/null` | Do not write to `known_hosts` for temporary automation, with security risk |
| `DISPLAY=dummy:0` | Required to trigger `SSH_ASKPASS`; the value can be arbitrary |

Reusable helper:

```bash
ssh-auto() {
  local HOST="$1"
  local PASS="$2"
  local CMD="${3:-}"
  cat > /tmp/.sp$$.sh << SCRIPT
#!/bin/bash
echo '$PASS'
SCRIPT
  chmod 700 /tmp/.sp$$.sh
  SSH_ASKPASS=/tmp/.sp$$.sh DISPLAY=dummy:0 \
    ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        root@"$HOST" "$CMD"
  rm -f /tmp/.sp$$.sh
}
```

## Option 2: SSH Key, Best Practice for Long-Term Use

Generate a key if needed:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "auto-deploy"
```

Upload the public key when password access is available:

```bash
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'SERVER_PASSWORD'
SCRIPT
chmod 700 /tmp/ssh_pass.sh
SSH_ASKPASS=/tmp/ssh_pass.sh DISPLAY=dummy:0 \
  ssh -o StrictHostKeyChecking=no root@SERVER_IP \
  "mkdir -p ~/.ssh && echo '$(cat ~/.ssh/id_ed25519.pub)' >> ~/.ssh/authorized_keys"
rm -f /tmp/ssh_pass.sh
```

Then connect without a password:

```bash
ssh root@SERVER_IP "COMMAND"
```

## Option 3: sshpass on Linux/macOS

```bash
sshpass -p 'YOUR_PASSWORD' ssh -o StrictHostKeyChecking=no root@SERVER_IP "COMMAND"
```

Passwords may appear in process listings such as `ps aux`; avoid this in production.

## Option 4: Plink on Windows PowerShell

```powershell
plink -batch -pw "YOUR_PASSWORD" root@SERVER_IP "COMMAND"
```

## Common Operation Patterns

Run a single command:

```bash
ssh -o StrictHostKeyChecking=no root@IP "uptime && df -h"
```

Write a remote file with a heredoc:

```bash
ssh -o StrictHostKeyChecking=no root@IP 'cat > /path/to/file' << 'REMOTE_EOF'
line one
line two ${VAR} is not expanded locally
REMOTE_EOF
```

Upload a file:

```bash
scp -o StrictHostKeyChecking=no local-file.txt root@IP:/remote/path/
```

Download a file:

```bash
scp -o StrictHostKeyChecking=no root@IP:/remote/file.txt ./local/
```

## Common Issues

| Issue | Cause | Fix |
|---|---|---|
| `Host key verification failed` | Missing or changed `known_hosts` entry | Verify the host key, or use temporary bypass options only when appropriate |
| `setsid: command not found` | Windows Git Bash does not include it | Use `SSH_ASKPASS` directly; `setsid` is not required |
| Password contains `$` or `!` | Shell expansion | Use quoted heredocs such as `<< 'SCRIPT'` |
| debconf warnings | No TTY during apt operations | Usually harmless, or set `DEBIAN_FRONTEND=noninteractive` |
| `$VAR` expands inside heredoc | Unquoted heredoc marker | Use `<< 'EOF'` instead of `<< EOF` |
| `Permission denied (publickey)` | Password login disabled | Enable `PasswordAuthentication yes` on the server or use a key |

## Security Recommendations

1. Delete temporary password scripts immediately: `rm -f /tmp/ssh_pass.sh`.
2. Use `chmod 700` for temporary password scripts.
3. Prefer SSH keys for long-term servers.
4. Do not hard-code passwords in project files. Prefer environment variables or temporary files.

## Environment Check

```bash
echo "OS: $(uname -s)"
which ssh && echo "OpenSSH available" || echo "No SSH"
which ssh-keygen && echo "ssh-keygen available" || echo "No ssh-keygen"
which sshpass 2>/dev/null && echo "sshpass installed" || echo "sshpass not installed"
which plink 2>/dev/null && echo "plink installed" || echo "plink not installed"
```

---
name: remote-terminal
description: Remote Linux terminal control skill. Use when the user wants to (1) connect to a remote Linux server and execute commands, (2) perform SSH operations on remote hosts, (3) manage multiple remote servers, (4) run shell commands on remote machines. Triggers on phrases like "connect to server", "SSH to", "run on remote", "execute on production", "login to my server", "在服务器上执行", "远程连接", "SSH到".
---

# Remote Terminal

Execute commands on remote Linux servers through SSH, Telnet, or web terminals. Supports password authentication, SSH keys, and SSH config aliases.

## Quick Start

### Basic SSH Connection

```bash
ssh user@hostname "command"
```

### Using SSH Config Aliases

If the user has `~/.ssh/config` configured:

```bash
ssh <alias> "command"
```

### With Password (using sshpass)

```bash
sshpass -p 'password' ssh user@hostname "command"
```

## Connection Methods

### 1. SSH (Recommended)

**Key-based authentication (most secure):**
```bash
ssh -i ~/.ssh/id_rsa user@hostname "command"
```

**Using SSH config aliases:**
```bash
# Example ~/.ssh/config
Host production
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_rsa

# Usage
ssh production "docker ps"
```

**Password authentication:**
```bash
sshpass -p 'password' ssh -o StrictHostKeyChecking=no user@hostname "command"
```

### 2. Telnet

```bash
# Using expect for interactive telnet
expect -c '
spawn telnet hostname
expect "login:"
send "username\r"
expect "Password:"
send "password\r"
expect "$ "
send "command\r"
expect "$ "
send "exit\r"
'
```

### 3. Web Terminal (ttyd, wetty)

For web-based terminals, use curl or HTTP requests to the terminal's API:

```bash
# Example: ttyd WebSocket connection (requires wscat or similar)
wscat -c ws://hostname:7681/ws
```

## Security Features

### Command Confirmation

Before executing dangerous commands, ask the user to confirm:

**Dangerous command patterns:**
- `rm -rf`, `rm -r`, `del`, `erase`
- `shutdown`, `reboot`, `poweroff`, `halt`
- `mkfs`, `fdisk`, `parted`, `dd`
- `chmod 777`, `chown -R`
- `> /dev/`, `truncate`
- `kill -9`, `pkill`, `killall`
- `iptables`, `ufw`, `firewall-cmd`
- `DROP DATABASE`, `DELETE FROM`, `TRUNCATE`

**Confirmation format:**
> ⚠️ **Dangerous command detected**: `rm -rf /var/log/*`
> This will permanently delete files. Proceed? (yes/no)

### Command Blacklist

These commands are blocked by default and require explicit user override:
- `rm -rf /` (entire filesystem)
- `mkfs` on mounted drives
- `dd` to primary disk
- Any command piping to `/dev/sda` or similar

### Operation Logging

All remote commands are logged with timestamp, target host, and command:

```
[2026-03-21 15:30:45] [production] docker ps
[2026-03-21 15:31:02] [staging] systemctl restart nginx
```

Log location: `~/.qclaw/logs/remote-terminal.log`

## Workflow

### Step 1: Identify Target Host

Parse the user's request to identify:
- Hostname, IP address, or SSH alias
- Username (if specified, otherwise use default or prompt)
- Connection method (SSH by default)

**Example prompts:**
- "Connect to production and run docker ps" → alias: production
- "SSH to 192.168.1.50, check disk space" → host: 192.168.1.50
- "On my server, restart nginx" → need to ask which server

### Step 2: Build Connection Command

Construct the appropriate SSH command based on:
- Authentication method available
- Host configuration
- Whether it's interactive or one-shot

### Step 3: Security Check

If command matches dangerous patterns:
1. Warn the user
2. Ask for explicit confirmation
3. If confirmed, proceed; otherwise, cancel

### Step 4: Execute and Return Output

Run the command and return:
- Standard output
- Standard error (if any)
- Exit code
- Execution time

### Step 5: Log Operation

Record the operation in the log file for audit trail.

## Common Operations

### Check System Status

```bash
ssh host "uptime && free -h && df -h"
```

### Docker Management

```bash
ssh host "docker ps -a"
ssh host "docker logs container_name"
ssh host "docker restart container_name"
```

### Service Management

```bash
ssh host "systemctl status nginx"
ssh host "sudo systemctl restart nginx"
ssh host "journalctl -u nginx -f --no-pager -n 50"
```

### File Operations

```bash
# View file
ssh host "cat /var/log/nginx/error.log | tail -50"

# Copy file to local
scp user@host:/remote/path /local/path

# Copy file to remote
scp /local/path user@host:/remote/path
```

### Process Management

```bash
ssh host "ps aux | grep nginx"
ssh host "top -b -n 1 | head -20"
```

## Interactive Sessions

For commands requiring interaction, use `ssh -t` for pseudo-terminal:

```bash
ssh -t host "sudo nano /etc/nginx/nginx.conf"
ssh -t host "htop"
```

**Note:** Interactive sessions require the `-t` flag to allocate a PTY.

## Multiple Hosts

### Parallel Execution

Execute the same command on multiple hosts:

```bash
for host in web1 web2 web3; do
  echo "=== $host ===" 
  ssh $host "uptime"
done
```

### Using Parallel SSH

For larger fleets:

```bash
# Using pssh (parallel-ssh)
pssh -h hosts.txt "uptime"

# hosts.txt format
# web1.example.com
# web2.example.com
# web3.example.com
```

## Host Management

### Store Host Information

Hosts can be stored in `~/.qclaw/workspace/memory/hosts.json`:

```json
{
  "hosts": {
    "production": {
      "host": "192.168.1.100",
      "user": "admin",
      "method": "ssh-key",
      "key": "~/.ssh/id_rsa",
      "tags": ["web", "critical"]
    },
    "staging": {
      "host": "staging.example.com",
      "user": "deploy",
      "method": "ssh-config",
      "alias": "staging",
      "tags": ["web", "testing"]
    }
  }
}
```

### List Known Hosts

```bash
# From SSH config
grep "^Host " ~/.ssh/config | awk '{print $2}'

# From stored hosts.json
cat ~/.qclaw/workspace/memory/hosts.json
```

## Troubleshooting

### Connection Refused

```bash
# Check if host is reachable
ping hostname

# Check if SSH port is open
nc -zv hostname 22

# Try with verbose output
ssh -vvv user@hostname
```

### Permission Denied

```bash
# Check key permissions
chmod 600 ~/.ssh/id_rsa

# Try with specific key
ssh -i ~/.ssh/id_rsa user@hostname

# Check if key is added to agent
ssh-add -l
ssh-add ~/.ssh/id_rsa
```

### Host Key Verification Failed

```bash
# Remove old host key
ssh-keygen -R hostname

# Or temporarily disable check (not recommended for production)
ssh -o StrictHostKeyChecking=no user@hostname
```

## Output Parsing

### Structured Output

For commands returning JSON:

```bash
ssh host "docker inspect container --format '{{json .}}'" | jq .
```

### Table Output

For commands like `docker ps`, `ps aux`:

```bash
# Return as-is for readable tables
ssh host "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Parse for structured data
ssh host "docker ps --format '{{json .}}'" | jq .
```

## Resources

### scripts/

- `ssh_exec.py` - Python wrapper for SSH operations with logging
- `host_manager.py` - Manage host configurations
- `parallel_exec.py` - Execute commands on multiple hosts

### references/

- `ssh_config_guide.md` - SSH config file examples and patterns
- `security_best_practices.md` - Security guidelines for remote access

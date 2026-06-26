---
name: ssh-server
description: SSH remote connection and operation for servers (Linux/Unix cloud servers, etc.)
read_when:
  - User needs SSH connection to remote server
  - Need to view/operate remote server
  - Need to query server status, logs
  - Need to execute commands on server
metadata: {"emoji":"🖥️","requires":{"bins":["ssh"]}}
allowed-tools: Bash(ssh:*)
---

# SSH Server - Remote Server Management

## Overview

Connect to and operate remote Linux/Unix servers via SSH.

## Security Notes

⚠️ **Important: Protect Sensitive Info**
- Never send passwords directly in chat
- Passwords are encrypted and stored locally
- Prefer SSH key authentication

## Initial Setup

### 1. Install Dependencies

SSH client is usually pre-installed:
- Windows: C:\Windows\System32\OpenSSH\ssh.exe (Win10/11自带)
- Linux/Mac: Terminal built-in

### 2. Add Server Config

**Method A: Interactive Add (Recommended)**

Run this in your local terminal:

```bash
python D:\openClaw\openclaw\config\ssh_config.py add
```

Then enter:
- Server name: e.g., vps, ubuntu, digitalocean
- Server IP: xxx.xxx.xxx.xxx
- Port: 22
- Username: root, ubuntu, etc.
- Password: (hidden during input, stored securely)

**Method B: SSH Key Login (More Secure)**

```bash
# 1. Generate local SSH key (if not exists)
ssh-keygen -t ed25519

# 2. Copy public key to server
ssh-copy-id user@your-server-ip
```

## Connect to Server

### Interactive Connect (Password)

Run in your terminal:

```bash
ssh -o StrictHostKeyChecking=no user@your-server-ip
```

Then enter password manually.

### Connect Using Config Alias

Run in your terminal:

```bash
python D:\openClaw\openclaw\config\ssh_config.py connect <server-name>
```

System will prompt for password, then connect.

## Server Operations

After connecting, you can execute:

### System Status

```bash
# System overview
uptime

# Memory usage
free -h

# Disk usage
df -h

# CPU info
lscpu

# Full system info
uname -a && uptime && free -h && df -h
```

### Users and Processes

```bash
# Online users
who

# Process list
ps aux

# Processes sorted by memory
ps aux --sort=-%mem

# Find specific process
ps aux | grep nginx
```

### Network Status

```bash
# Network connections
ss -tuln

# Port usage
netstat -tuln
```

### Service Management

```bash
# Check service status
systemctl status nginx

# Start service
sudo systemctl start nginx

# Stop service
sudo systemctl stop nginx

# Restart service
sudo systemctl restart nginx
```

### Log Viewing

```bash
# System logs
sudo journalctl -xe

# Last 100 lines
sudo journalctl -n 100

# Specific service logs
sudo journalctl -u nginx

# Real-time log
tail -f /var/log/syslog
```

### Docker Operations

```bash
# Running containers
docker ps

# All containers
docker ps -a

# Container logs
docker logs container_name

# Enter container
docker exec -it container_name bash
```

## Config File

Server configs saved to `D:\openClaw\openclaw\config\servers.json` (passwords encrypted).

```json
{
  "vps": {
    "host": "xxx.xxx.xxx.xxx",
    "port": 22,
    "username": "root",
    "key_file": null,
    "password_encrypted": "gAAAAAB..."
  }
}
```

## Management Commands

```bash
# Add server
python config/ssh_config.py add

# List servers
python config/ssh_config.py list

# Connect to server
python config/ssh_config.py connect <name>

# Delete server
python config/ssh_config.py delete <name>
```

## Usage Flow

1. **User tells AI**: Want to connect to my VPS
2. **AI prompts user**: Run `python config/ssh_config.py add` in terminal
3. **After user adds**: AI can connect to server via config
4. **Connection methods**:
   - Password: User runs `ssh user@IP` and enters password
   - Key: Direct connect after config

## Security Principles

- 🔐 Passwords not transmitted via chat
- 🔑 Prefer SSH keys
- 🛡️ Passwords encrypted locally
- ⚠️ Confirm before dangerous operations

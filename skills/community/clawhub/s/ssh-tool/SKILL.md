---
name: ssh-tool
description: Securely connect to remote systems via the SSH protocol. Use for remote server management, file transfer, and tunneling.
---

# Secure Shell Client

Establish encrypted connections to remote systems for command execution, file transfer, and port forwarding.

## Usage

```bash
ssh-tool [options] user@hostname [command]
```

## Features

- Authenticate with password or SSH keys
- Execute remote commands
- Forward local and remote ports
- Transfer files with integrated SCP support

## Examples

```bash
# Basic connection
ssh-tool user@example.com

# Execute remote command
ssh-tool user@example.com "ls -la"

# Port forwarding
ssh-tool -L 8080:localhost:80 user@example.com
```
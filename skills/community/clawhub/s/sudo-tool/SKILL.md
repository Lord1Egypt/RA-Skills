---
name: sudo-tool
description: Execute commands with superuser privileges. Use for system administration tasks requiring elevated permissions.
---
# Sudo - Superuser Do

Execute commands with root or other user privileges. Requires proper authorization through /etc/sudoers configuration.

## Usage
```bash
sudo-tool [options] <command>
```

## Options

- `-u user`: Run as specified user (default: root)
- `-k`: Reset timestamp timeout
- `-l`: List allowed commands

## Examples

```bash
sudo-tool apt update
sudo-tool -u www-data whoami
sudo-tool -l
```

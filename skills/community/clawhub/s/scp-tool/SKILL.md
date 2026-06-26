---
name: scp-tool
description: Securely copy files between local and remote hosts over SSH. Use for file transfers, remote backups, and deployment tasks.
---
# SCP - Secure File Copy

Copy files between local and remote systems using SSH encryption. Supports recursive directory transfers and custom port specifications.

## Usage
```bash
scp-tool [options] <source> <destination>
```

## Options

- `-r`: Recursively copy directories
- `-P port`: Specify SSH port
- `-C`: Enable compression for faster transfer
- `-v`: Verbose mode for debugging

## Examples

```bash
scp-tool file.txt user@host:/remote/path/
scp-tool -r ./folder user@host:/remote/folder
scp-tool user@host:/remote/file.txt .
```
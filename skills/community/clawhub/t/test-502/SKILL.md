---
name: alist-cli
displayName: "AList-CLI (Cloud Storage CLI for AList, with OpenClaw Skill)"
version: 1.0.2
description: |
  AList file management API for OpenClaw. Supports upload, download, list, mkdir, rm, mv, search, and offline download.
  Trigger: User asks about file management, AList operations, upload/download files, or cloud storage tasks.
---

# AList CLI

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

File management tool for AList API.

## Environment Variables

```bash
ALIST_URL="https://your_alist_server"
ALIST_USERNAME="your_username"
ALIST_PASSWORD="your_password"
```

## Commands

| Command | Description |
|---------|-------------|
| `alist login` | Authenticate |
| `alist ls [path]` | List files |
| `alist get <path>` | Get file info |
| `alist mkdir <path>` | Create folder |
| `alist upload <local> <remote>` | Upload file |
| `alist rm <path>` | Delete file |
| `alist mv <src> <dst>` | Move file |
| `alist search <keyword> [path]` | Search files |
| `alist whoami` | Current user |

## Script

```bash
python scripts/alist_cli.py <command> [args]
```

## References

- `references/openapi.json` - AList API specification

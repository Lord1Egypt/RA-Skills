---
name: terabox-storage
description: Manage TeraBox cloud storage operations including login, upload, download, share, and transfer. Use the terabox CLI tool for file management tasks.
version: 1.0.0
---

# TeraBox Storage Skill

TeraBox cloud storage management tool supporting upload, download, transfer, share, and file listing. All operations are restricted to the application sandbox directory.

Compatible with: OpenClaw, Claude Code, DuClaw, Ducc, etc.

> Beta stage - see [reference/notes.md](./reference/notes.md) for important notes

---

## Installation

If the `terabox` CLI tool is not installed, run the installation script:

```bash
bash @skills/terabox-storage/scripts/install.sh
```

The script will:
1. Detect your OS and architecture
2. Download the terabox binary from CDN
3. Install it to `~/.local/bin/terabox`

Make sure `~/.local/bin` is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Trigger Rules

Execute only when BOTH conditions are met:

1. **User explicitly mentions TeraBox** - message contains "TeraBox", "terabox", "Tera", etc.
2. **Clear operation intent** - can determine one of: upload, download, transfer, share, list, login, logout

Do NOT execute any terabox commands if conditions are not met.

---

## Confirmation Rules

**Must confirm with user first** in these scenarios:

| Scenario | Description |
|----------|-------------|
| Path unclear | User did not specify file path or target path |
| Remote path exists | Upload target has same-name file - ask: overwrite/rename/cancel |
| Local path exists | Download target has same-name file - ask: overwrite/rename/cancel |
| Ambiguous intent | "process files" → confirm upload or download; "sync" → confirm direction; "backup" → confirm direction |

Confirmation format:

```
Operation: [upload/download/share/list]
Source: [path]
Destination: [path]
Confirm execution?
```

---

## Pre-execution Checks

Before every terabox command:

1. Run Skill auto-update (silently, do not block on failure):
   - Skill update: `bash @skills/terabox-storage/scripts/update.sh --yes`
   - CLI auto-update is handled automatically by the CLI itself (built-in update check on every command execution)
   - If update fails, continue with the user's requested operation
2. Run `terabox whoami` to check login status; if not logged in, guide user to `bash @skills/terabox-storage/scripts/login.sh`
3. Validate path legality (no `../`, path must be within application sandbox)

---

## Core Features

### Upload

```bash
terabox upload <local_path> [remote_path]
terabox upload ./file.txt              # Upload to root directory
terabox upload ./file.txt docs/        # Upload to docs directory
terabox upload ./file.txt --progress   # Show upload progress
terabox upload ./my-dir/ backup/       # Upload entire directory
```

Supports single file and directory upload. When uploading a directory, all files are recursively uploaded.

Steps: Confirm local path exists → Confirm remote path → Use `terabox ls` to check if remote exists → Execute upload

### Download

```bash
terabox download <remote_path> [local_path]
terabox download report.pdf            # Download to current directory
terabox download report.pdf ./saved/   # Download to specified directory
terabox download report.pdf --progress # Show download progress
terabox download docs/ ./local-docs/   # Download entire directory
```

Supports single file and directory download. When downloading a directory, all files are recursively downloaded.

Steps: Use `terabox ls` to confirm cloud path exists → Confirm local path → Check if local exists → Execute download

### Transfer (Save shared files to your cloud storage)

```bash
# Basic usage
terabox share-save <share_url> --pwd <password> [--path <dest_path>]

# Specify save directory
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd --path my-folder/

# Transfer specific files by ID
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd --fsid 12345,12346
```

Steps: Validate link format → Confirm password exists → Confirm target directory → Execute transfer

### Share Operations

```bash
# View share details
terabox share-info <share_url>

# List shared files
terabox share-list <share_url> --pwd <password>
terabox share-list <share_url> --pwd <password> --by name --order asc  # Sort by name
terabox share-list <share_url> --pwd <password> --by size              # Sort by size
terabox share-list <share_url> --pwd <password> --by time -p 2        # Sort by time, page 2

# Download shared files directly
terabox share-download <share_url> [local_path] --pwd <password>
terabox share-download <share_url> --pwd <password> --fsid 12345  # Download specific file

# Create share link
terabox share-create <path>...                    # Create share with auto-generated password
terabox share-create file.txt --pwd abcd          # Create share with custom password
terabox share-create file.txt --period 7          # Create share valid for 7 days
terabox share-create file.txt --public            # Create public share (no password)
```

### File Operations

```bash
terabox ls [directory]                 # List files
terabox ls -l [directory]              # List files with details
terabox ls --order name                # List sorted by name
terabox ls --order size --asc          # List sorted by size ascending
terabox search <keyword>               # Search files
terabox search <keyword> --order name  # Search with sorting
terabox info <file_path>               # Get file details
terabox info <file_path> --dlink       # Get file details with download link
terabox mv <source> <destination>      # Move file
terabox cp <source> <destination>      # Copy file
terabox rename <path> <new_name>       # Rename file
```

### User Information

```bash
terabox uinfo                          # Get user info
terabox quota                          # Query storage quota
```

### Update CLI

```bash
terabox update                         # Check and update CLI
terabox update check                   # Check for updates only
terabox update apply                   # Apply pending update
terabox update rollback                # Rollback to previous version
terabox update list                    # List installed versions
```

The CLI also checks for updates automatically on every command execution. Use `--no-check-update` global flag to disable this behavior.

### Login

**Must use the login script:**

```bash
bash scripts/login.sh
```

**Requirements:**
- Must use `@skills/terabox-storage/scripts/login.sh` script
- Do NOT use `terabox login` directly (even in GUI environments)

The login script includes complete security disclaimers and authorization flow to ensure informed user consent.

### Logout

```bash
terabox logout
```

---

## Path Rules

All remote paths are relative to the application sandbox directory `/From：Other Applications/app-name/`.

| Scenario | Rule | Example |
|----------|------|---------|
| **In commands** | Use relative paths | `terabox upload ./f.txt docs/f.txt` |
| **Display to user** | Use full paths | "Uploaded to: /From：Other Applications/app/docs/f.txt" |

**Prohibited:**
- Paths containing `..` or `~`
- Paths outside the application sandbox

---

## Reference Documentation

See the reference directory for detailed information (consult when encountering issues):

| Document | When to Consult |
|----------|-----------------|
| [terabox-commands.md](./reference/terabox-commands.md) | Need complete command parameters, options, JSON output formats |
| [authentication.md](./reference/authentication.md) | Login authentication flow details, config file locations, Token management |
| [examples.md](./reference/examples.md) | Need more usage examples |
| [troubleshooting.md](./reference/troubleshooting.md) | Encountering errors that need diagnosis |
| [notes.md](./reference/notes.md) | Beta stage important notes |

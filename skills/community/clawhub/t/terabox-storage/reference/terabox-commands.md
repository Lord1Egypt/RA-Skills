# terabox CLI Command Reference

## Authentication Commands

### login - Login Authorization

```bash
terabox login
```

Login to TeraBox account via OAuth authorization. In desktop environments, the browser will open automatically and complete authorization via callback.

**Options:**
- `--code <string>` - Manually enter authorization code (use when callback fails)
- `--code-stdin` - Read authorization code from stdin (secure, avoids leaking in ps/cmdline)

> **Note:** The Skill enforces login through `scripts/login.sh` only. These flags are documented for reference.

### logout - Logout

```bash
terabox logout
```

Clear locally stored authentication credentials (`~/.config/terabox/config.json`).

### whoami - Check Authentication Status

```bash
terabox whoami
```

Display current login status and Token validity information.

**When logged in:**
```
Current login status:
  API Domain:    www.terabox.com
  Upload Domain: c-jp.terabox.com
  Working Dir:   /From：Other Applications/app-xxx/
  Expires At:    2026-04-04T10:30:00Z
  Status:        Valid
```

**When token is expiring:**
```
  Status:        Expiring soon (recommended to login again)
```

**When token is expired:**
```
  Status:        Expired (please login again)
```

**When not logged in:**
```
Not logged in
Please run 'terabox login' to log in
```

**Options:**
- `--json` - JSON format output

---

## User Information Commands

### uinfo - Get User Information

```bash
terabox uinfo
```

Get detailed information about the currently logged-in user.

**Options:**
- `--json` - JSON format output

### quota - Query Storage Quota

```bash
terabox quota
```

Query storage space usage.

**Example output:**
```
Used: 15.2 GB
Total: 1.0 TB
Usage: 1.5%
```

**Options:**
- `--json` - JSON format output

---

## File Operation Commands

### upload - Upload Files or Directories

```bash
terabox upload <local_path> [remote_path]
```

| Parameter | Description |
|-----------|-------------|
| `local_path` | Local file or directory path |
| `remote_path` | Cloud target path (optional, defaults to root) |

Supports both single file and directory upload. When uploading a directory, all files within it are recursively uploaded. Supports rapid upload (deduplication).

**Examples:**
```bash
# Upload single file to root directory
terabox upload ./report.pdf

# Upload to specified directory
terabox upload ./report.pdf docs/

# Upload and rename
terabox upload ./report.pdf docs/monthly-report.pdf

# Show upload progress
terabox upload ./large-file.zip --progress

# Upload entire directory
terabox upload ./my-project/ backup/

# Upload directory with progress
terabox upload ./photos/ albums/ --progress
```

**Options:**
- `--progress` - Show upload progress (percent, speed, chunk info)
- `--json` - JSON format output

### download - Download Files or Directories

```bash
terabox download <remote_path> [local_path]
```

| Parameter | Description |
|-----------|-------------|
| `remote_path` | Cloud file or directory path |
| `local_path` | Local save path (optional, defaults to current directory) |

Supports both single file and directory download. When downloading a directory, all files within it are recursively downloaded.

**Examples:**
```bash
# Download to current directory
terabox download report.pdf

# Download to specified directory
terabox download report.pdf ./downloads/

# Download and rename
terabox download report.pdf ./my-report.pdf

# Show download progress
terabox download large-file.zip ./downloads/ --progress

# Download entire directory
terabox download documents/ ./local-docs/

# Download directory with progress
terabox download photos/ ./local-photos/ --progress
```

**Options:**
- `--progress` - Show download progress (percent, speed)
- `--json` - JSON format output

### ls - List Files

```bash
terabox ls [directory]
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `directory` | Directory path to list | Root directory |

**Examples:**
```bash
# List root directory
terabox ls

# List subdirectory
terabox ls docs/

# Sort by name
terabox ls --order name

# Sort by size, ascending
terabox ls --order size --asc

# Detailed view, page 2, 50 items per page
terabox ls -l -p 2 -n 50

# JSON output
terabox ls --json
```

**Output format:**
```
Type    Size          Modified              Name
------  ------------  --------------------  --------
Dir     -             2026-02-20 10:30:00   documents
File    1.5 MB        2026-02-25 15:20:00   readme.txt

Total: 2 items
```

**Options:**
- `-l, --long` - Show detailed info (size, type, modified date)
- `-p, --page` - Page number (default: 1)
- `-n, --num` - Items per page (default: 100)
- `--order` - Sort by: `name`, `size`, `time` (default: `time`)
- `--asc` - Sort ascending (default: descending)
- `--json` - JSON format output

### search - Search Files

```bash
terabox search <keyword>
```

Search for files in the cloud storage.

**Examples:**
```bash
# Search by keyword
terabox search report

# Search with sorting
terabox search report --order name

# Search sorted by size ascending
terabox search report --order size --asc

# Paginate results
terabox search report -p 2 -n 50
```

**Options:**
- `--order` - Sort by: `name`, `size`, `time` (default: `time`)
- `--asc` - Sort ascending (default: descending)
- `-p, --page` - Page number (default: 1)
- `-n, --num` - Items per page (default: 100)
- `--json` - JSON format output

### info - Get File Details

```bash
terabox info <file_path>
```

Get detailed information about a file or directory.

**Options:**
- `--dlink` - Get download link
- `--json` - JSON format output

### mv - Move Files

```bash
terabox mv <source> <destination>
```

Move file or directory to a new location.

**Options:**
- `--json` - JSON format output

### cp - Copy Files

```bash
terabox cp <source> <destination>
```

Copy file or directory.

**Options:**
- `--json` - JSON format output

### rename - Rename

```bash
terabox rename <path> <new_name>
```

Rename file or directory.

**Options:**
- `--json` - JSON format output

---

## Share Commands

### share-info - Query Share Details

```bash
terabox share-info <share_url>
```

Get detailed information about a share link.

**Examples:**
```bash
terabox share-info "https://terabox.com/s/1xxxxx"
terabox share-info "https://1024terabox.com/s/1xxxxx"
```

**Output:**
```
Share Information:
  Title:       My Shared Files
  Share ID:    1234567890
  Sharer:      9876543210
  Created At:   2026-02-20T10:30:00Z
  Expires At:   Never
  Password:    Required
  Status:      Normal
```

**Options:**
- `--json` - JSON format output

**JSON Output:**
```json
{
  "share_id": 1234567890,
  "uk": 9876543210,
  "title": "My Shared Files",
  "create_time": "2026-02-20T10:30:00Z",
  "has_password": true,
  "status": 0,
  "status_name": "Normal",
  "expire_time": "2026-03-20T10:30:00Z"
}
```

### share-list - List Shared Files

```bash
terabox share-list <share_url> [--pwd <password>]
```

List files in a share link.

**Examples:**
```bash
# List files (no password)
terabox share-list "https://terabox.com/s/1xxxxx"

# List files with password
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd

# Sort by name ascending
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --by name --order asc

# Sort by file size (descending by default)
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --by size

# Sort by modification time, page 2
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --by time -p 2 -n 50
```

**Output:**
```
Shared Files (3 files)

File ID       Size          Type        Name
------------  ------------  ----------  --------
123456789     1.5 MB        File        report.pdf
234567890     -             Directory   documents
345678901     50.2 MB       File        video.mp4

```

**Options:**
- `--pwd` - Share password/extraction code
- `-p, --page` - Page number (default: 1)
- `-n, --num` - Items per page (default: 100)
- `--dir` - Specify directory within share
- `--order` - Sort order: `asc` (ascending), `desc` (descending, default)
- `--by` - Sort by: `name` (default), `time` (modification time), `size` (file size)
- `--json` - JSON format output

### share-save - Transfer Shared Files

```bash
terabox share-save <share_url> [--pwd <password>] [--path <dest>] [--fsid <ids>]
```

Transfer shared files to your own cloud storage.

**Examples:**
```bash
# Transfer all files to root directory
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd

# Transfer to specified directory
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd --path my-folder/

# Transfer specific files by ID
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd --fsid 12345,12346
```

**Options:**
- `--pwd` - Share password/extraction code
- `--path` - Destination path (default: /)
- `--fsid` - Specific file IDs to transfer (comma-separated)
- `--json` - JSON format output

### share-download - Download Shared Files

```bash
terabox share-download <share_url> [local_path] [--pwd <password>] [--fsid <id>]
```

Download files directly from a share link to local storage.

**Examples:**
```bash
# Download all files to current directory
terabox share-download "https://terabox.com/s/1xxxxx" --pwd abcd

# Download to specified directory
terabox share-download "https://terabox.com/s/1xxxxx" ./downloads/ --pwd abcd

# Download specific file by ID
terabox share-download "https://terabox.com/s/1xxxxx" --pwd abcd --fsid 123456789
```

**Supported URL formats:**
- `https://terabox.com/s/1xxxxx`
- `https://www.terabox.com/s/1xxxxx`
- `https://1024terabox.com/s/1xxxxx`
- `https://www.1024tera.com/chinese/sharing/link?surl=xxxxx`
- Direct surl: `1xxxxx`

**Options:**
- `--pwd` - Share password/extraction code
- `--fsid` - Specific file ID to download (optional, downloads all if not specified)
- `--json` - JSON format output

**Behavior:**
- If `--fsid` is specified: Downloads only that specific file
- If `--fsid` is not specified: Lists all files and downloads all non-directory files

### share-create - Create Share Link

```bash
terabox share-create <path>... [--pwd <password>] [--period <days>] [--public]
```

Create a share link for specified files or directories.

**Examples:**
```bash
# Create share with auto-generated password
terabox share-create report.pdf

# Create share for multiple files
terabox share-create file1.txt file2.txt

# Create share with custom password
terabox share-create report.pdf --pwd abcd

# Create share valid for 7 days
terabox share-create report.pdf --period 7

# Create public share (no password required)
terabox share-create video.mp4 --public
```

**Options:**
- `--pwd` - Custom extraction code (4 characters, auto-generated if not specified)
- `--period` - Validity period in days: 0=forever, 1, 7, 30, 180 (default: 0)
- `--public` - Create public share (no password required)
- `--json` - JSON format output

**Output:**
```
Share link created successfully!
  Link:     https://1024terabox.com/s/1xxxxx
  Password: abcd
  Expires:  Never
  Share ID: 12345678
```

**JSON Output:**
```json
{
  "success": true,
  "link": "https://1024terabox.com/s/1xxxxx",
  "shorturl": "https://1024terabox.com/s/1xxxxx",
  "share_id": 12345678,
  "password": "abcd",
  "expire_time": null
}
```

---

## Update Commands

### update - Check and Update CLI

```bash
terabox update
```

Check and update terabox CLI to the latest version. The CLI also performs automatic update checks on every command execution (can be disabled with `--no-check-update`).

**Options:**
- `-f, --force` - Force update check (ignore cache)

### update check - Check for Updates

```bash
terabox update check
```

Check if a new version is available without applying the update.

**Options:**
- `-f, --force` - Force update check (ignore cache)

### update apply - Apply Pending Update

```bash
terabox update apply
```

Apply an update that has been downloaded but not yet activated.

**Options:**
- `-f, --force` - Force apply

### update rollback - Rollback to Previous Version

```bash
terabox update rollback
```

Roll back to the previous installed version.

**Options:**
- `-f, --force` - Force rollback

### update list - List Installed Versions

```bash
terabox update list
```

List all installed versions. The active version is marked with `*`.

**Options:**
- `-f, --force` - Force refresh

---

## Global Options

| Option | Description |
|--------|-------------|
| `--config <path>` | Specify config file path |
| `--json` | JSON format output |
| `--no-check-update` | Disable automatic update check on command execution |
| `-h, --help` | Show help |
| `-v, --version` | Show version |

---

## JSON Output Formats

### ls command output

```json
{
  "path": "/docs",
  "files": [
    {
      "fs_id": 123456789,
      "name": "report.pdf",
      "path": "/docs/report.pdf",
      "size": 1536000,
      "is_dir": false,
      "modified": "2026-02-25T15:20:00Z",
      "category": "document"
    }
  ],
  "total": 1
}
```

### upload command output

```json
{
  "success": true,
  "rapid_upload": false,
  "file": {
    "fs_id": 123456789,
    "path": "/docs/report.pdf",
    "name": "report.pdf",
    "size": 1536000,
    "md5": "abc123..."
  }
}
```

### quota command output

```json
{
  "total": 1099511627776,
  "used": 16319825920,
  "free": 1083191801856
}
```

### share-list command output

```json
{
  "files": [
    {
      "fs_id": 123456789,
      "name": "report.pdf",
      "path": "/report.pdf",
      "size": 1536000,
      "is_dir": false,
      "category": "document"
    }
  ],
  "total": 1,
  "has_more": false
}
```

### share-download command output

```json
{
  "success": true,
  "local_path": "./downloads/report.pdf",
  "name": "report.pdf",
  "size": 1536000
}
```

---

## Config File Location

```
~/.config/terabox/config.json
```

**Config file structure:**
```json
{
  "version": 1,
  "auth": {
    "access_token": "...",
    "refresh_token": "...",
    "expires_at": 1234567890
  },
  "endpoints": {
    "api_domain": "www.terabox.com",
    "upload_domain": "c-jp.terabox.com"
  },
  "permission": {
    "root_dir": "/From：Other Applications/app-xxx/"
  }
}
```

---

## Common Error Codes

| Error | Description | Solution |
|-------|-------------|----------|
| Token expired | Token has expired | Re-login |
| Path not allowed | Path outside sandbox | Use paths within sandbox directory |
| File not found | File does not exist | Check path is correct |
| Invalid share link | Share link is invalid | Check link format and password |
| errno -3 | Password required | Provide extraction code with --pwd |
| errno 112 | Invalid sign/timestamp | Internal error, retry the operation |
| Share expired | Share has expired | Cannot access expired shares |
| Share deleted | Share has been deleted | Cannot access deleted shares |

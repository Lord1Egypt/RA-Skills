# TeraBox Usage Examples

## Basic Operations

### View File List

```bash
# View root directory
terabox ls

# View subdirectory
terabox ls documents/

# View with detailed info (size, type, date)
terabox ls -l

# View subdirectory with details
terabox ls -l documents/

# Sort by name
terabox ls --order name

# Sort by size ascending
terabox ls --order size --asc

# Detailed view, page 2
terabox ls -l -p 2 -n 50

# JSON format output
terabox ls --json
```

### Upload Files and Directories

```bash
# Upload single file
terabox upload ./report.pdf

# Upload to specified directory
terabox upload ./report.pdf documents/

# Show upload progress
terabox upload ./large-file.zip backup/ --progress

# Upload entire directory
terabox upload ./my-project/ backup/

# Upload directory with progress
terabox upload ./photos/ albums/ --progress
```

### Download Files and Directories

```bash
# Download to current directory
terabox download report.pdf

# Download to specified location
terabox download report.pdf ./downloads/

# Show download progress
terabox download large-file.zip ./downloads/ --progress

# Download entire directory
terabox download documents/ ./local-docs/

# Download directory with progress
terabox download photos/ ./local-photos/ --progress
```

### File Management

```bash
# Copy file
terabox cp report.pdf backup/report.pdf

# Move file
terabox mv report.pdf documents/report.pdf

# Rename
terabox rename report.pdf monthly-report.pdf
```

---

## Share Operations

### View Share Information

```bash
terabox share-info "https://terabox.com/s/1xxxxx"
```

### List Shared Files

```bash
# Without password
terabox share-list "https://terabox.com/s/1xxxxx"

# With password
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd

# Sort by name ascending
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --by name --order asc

# Sort by file size
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --by size
```

### Transfer Shared Files

```bash
# Transfer all files
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd

# Transfer to specified directory
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd --path shared/

# Transfer specific files
terabox share-save "https://terabox.com/s/1xxxxx" --pwd abcd --fsid 123456,234567
```

### Download Shared Files Directly

```bash
# Download all files to current directory
terabox share-download "https://terabox.com/s/1xxxxx" --pwd abcd

# Download to specified directory
terabox share-download "https://terabox.com/s/1xxxxx" ./downloads/ --pwd abcd

# Download specific file by ID
terabox share-download "https://terabox.com/s/1xxxxx" --pwd abcd --fsid 123456789

# Different URL formats supported
terabox share-download "https://1024terabox.com/s/1xxxxx" --pwd abcd
terabox share-download "https://www.1024tera.com/chinese/sharing/link?surl=xxxxx" --pwd abcd
```

### Create Share Link

```bash
# Create share with auto-generated password
terabox share-create report.pdf

# Create share with custom password
terabox share-create report.pdf --pwd abcd

# Create share valid for 7 days
terabox share-create report.pdf --period 7

# Create public share (no password)
terabox share-create video.mp4 --public

# Share multiple files
terabox share-create file1.txt file2.txt
```

---

## User Information

```bash
# Check login status
terabox whoami

# Get user information
terabox uinfo

# Check storage usage
terabox quota
```

---

## Search Files

```bash
# Search by keyword
terabox search "report"

# Search with sorting by name
terabox search "report" --order name

# Search sorted by size ascending
terabox search "report" --order size --asc

# Paginate search results
terabox search "report" -p 2 -n 50
```

---

## File Info

```bash
# Get file details
terabox info report.pdf

# Get file details with download link
terabox info report.pdf --dlink

# JSON output
terabox info report.pdf --json
```

---

## Update CLI

```bash
# Check and update to latest version
terabox update

# Check for updates only (without installing)
terabox update check

# Apply a downloaded but not yet activated update
terabox update apply

# Rollback to the previous version
terabox update rollback

# List all installed versions
terabox update list

# Force update check (ignore cache)
terabox update check --force

# Disable auto-update check for a single command
terabox ls --no-check-update
```

---

## Script Integration Examples

### Batch Upload

```bash
#!/bin/bash
for file in ./uploads/*; do
    terabox upload "$file" backup/
done
```

### Auto Backup

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup-$DATE.tar.gz ./project/
terabox upload backup-$DATE.tar.gz backups/
rm backup-$DATE.tar.gz
```

### JSON Processing

```bash
# Use jq to process output
terabox ls --json | jq '.files[] | select(.is_dir == false) | .name'

# Get share file list as JSON
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --json | jq '.files[].name'
```

### Download All Share Files

```bash
#!/bin/bash
SHARE_URL="https://terabox.com/s/1xxxxx"
PASSWORD="abcd"
DEST_DIR="./shared-files"

mkdir -p "$DEST_DIR"
terabox share-download "$SHARE_URL" "$DEST_DIR" --pwd "$PASSWORD"
```

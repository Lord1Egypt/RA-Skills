---
name: smartfolder-skill
description: |
  Intelligent file organization assistant for OpenClaw. Automatically organize, analyze, and clean up your file system using natural language commands.
  龙虾智能文件整理助手。使用自然语言命令自动整理、分析和清理您的文件系统。
  
  Keywords: file organizer, folder cleanup, duplicate finder, disk space analyzer, storage cleanup, download folder organizer, file categorization, bulk file management, 文件整理, 文件夹清理, 重复文件查找, 磁盘空间分析
  
  Use this skill when:
  - "Organize my downloads folder"
  - "My downloads folder is a mess"
  - "Clean up duplicate files"
  - "Find duplicate files on my computer"
  - "Find large files taking up space"
  - "What's taking up disk space"
  - "Sort files by date/project/type"
  - "Organize files by type"
  - "Clean up messy folder"
  - "Rename photos based on date taken"
  - "Analyze disk usage"
  - "Archive old files"
  - "批量整理文件"
  - "清理重复文件"
  - "文件夹太乱了"
  - "清理文件夹"
  - "清理文件"
  - "桌面整理"
  
  Supports: intelligent categorization, duplicate detection, bulk renaming, disk analysis, automated cleanup workflows, file organization, folder management.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      optional:
        - ffmpeg  # For media file metadata extraction
---

# SmartFolder - Intelligent File Organizer

Automatically organize, analyze, and clean up your file system using natural language commands.

## When to Use

✅ **Use this skill when:**
- "Organize my downloads folder"
- "Clean up duplicate files"
- "Find large files taking up space"
- "Sort files by date/project/type"
- "Rename photos based on date taken"
- "Analyze disk usage"
- "Archive old files"
- "Move documents to appropriate folders"

❌ **Don't use when:**
- File operations requiring elevated permissions (use system tools)
- Network/cloud storage operations (not supported yet)
- Real-time sync needs (use dedicated sync tools)

## Features

### 1. Intelligent Organization
- Auto-categorize files by type (Documents, Images, Videos, Archives, etc.)
- Sort by date, size, or custom rules
- Smart project detection (groups related files)

### 2. Duplicate Detection
- Hash-based duplicate detection
- Similar image detection (perceptual hashing)
- Safe preview before deletion

### 3. Bulk Renaming
- Date-based renaming for photos/videos
- Sequential numbering
- Pattern-based replacement

### 4. Disk Analysis
- Visual disk usage report
- Find space hogs
- Identify old/unused files

### 5. Archive & Cleanup
- Compress old files
- Move to archive folders
- Empty trash/recycle bin

## Quick Start

### Check installation
```bash
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py --version
```

### Basic usage
```bash
# Organize Downloads folder
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py organize ~/Downloads

# Find duplicates
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py duplicates ~/Documents

# Analyze disk usage
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py analyze ~/
```

## Commands

### organize
Organize files in a directory.

```bash
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py organize <path> [options]

Options:
  --by-type          Organize by file type (default)
  --by-date          Organize by modification date
  --by-size          Organize by size ranges
  --dry-run          Preview changes without executing
  --target-dir       Custom target directory
```

### duplicates
Find and manage duplicate files.

```bash
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py duplicates <path> [options]

Options:
  --delete           Delete duplicates (prompts for confirmation)
  --move-to          Move duplicates to specified folder
  --similar-images   Include visually similar images
```

### analyze
Analyze disk usage.

```bash
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py analyze <path> [options]

Options:
  --top N            Show top N largest files (default: 20)
  --older-than DAYS  Find files older than N days
  --output-format    json, table, or chart
```

### rename
Bulk rename files.

```bash
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py rename <path> [options]

Options:
  --by-date-taken    Rename photos by EXIF date
  --pattern          Pattern for renaming
  --sequential       Add sequential numbers
```

## Examples

### Example 1: Organize Downloads
```bash
# Preview changes first
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py organize ~/Downloads --dry-run

# Execute organization
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py organize ~/Downloads
```

**Result:**
```
Downloads/
├── Documents/
│   ├── report.pdf
│   └── invoice.docx
├── Images/
│   ├── screenshot.png
│   └── photo.jpg
├── Archives/
│   └── backup.zip
└── Misc/
    └── readme.txt
```

### Example 2: Clean up duplicates
```bash
# Find duplicates in Documents
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py duplicates ~/Documents

# Move duplicates to review folder
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py duplicates ~/Documents --move-to ~/Duplicates_Review
```

### Example 3: Disk space analysis
```bash
# Find what's taking space
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py analyze ~/ --top 10
```

**Output:**
```
Top 10 Largest Files:
1. ~/Videos/project.mp4        2.3 GB
2. ~/Downloads/backup.zip      1.1 GB
3. ~/Documents/archive.pst     890 MB
...
```

## Safety Features

- ✅ **Dry-run mode** - Preview all changes before executing
- ✅ **Confirmation prompts** - For destructive operations
- ✅ **Trash support** - Deleted files go to system trash (not permanently deleted)
- ✅ **Undo log** - Operations are logged for potential undo
- ✅ **Skip system files** - Never touches hidden/system files

## Configuration

Create `~/.smartfolder/config.json` for default settings:

```json
{
  "default_organization": "by-type",
  "categories": {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar.gz"],
    "Code": [".py", ".js", ".html", ".css", ".json"]
  },
  "duplicate_check": {
    "min_size": 1024,
    "skip_hidden": true
  }
}
```

## Requirements

- Python 3.8+
- Optional: ffmpeg (for media metadata)

## Installation

```bash
# Install dependencies
pip install -r ~/.openclaw/workspace/smartfolder/requirements.txt

# Verify installation
python3 ~/.openclaw/workspace/smartfolder/scripts/smartfolder.py --version
```

## Troubleshooting

### Permission errors
Run with appropriate permissions for the target directory.

### Large directories
For directories with 10,000+ files, use `--batch-size` option.

### Special characters
Files with special characters are handled safely with proper escaping.

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please submit issues and PRs to the GitHub repository.

---
name: file-organization
description: Use when "organizing files", "cleaning up folders", "finding duplicates", "structuring directories", or asking about "Downloads cleanup", "folder structure", "file management"
version: 1.0.0
---

<!-- Adapted from: awesome-claude-skills/file-organizer -->

# File Organization Guide

Organize files, find duplicates, and maintain clean folder structures.

## When to Use

- Downloads folder is chaotic
- Can't find files (scattered everywhere)
- Duplicate files taking up space
- Folder structure doesn't make sense
- Starting a new project structure
- Cleaning up before archiving

## Analysis Commands

```bash
# Overview of directory
ls -la [directory]

# Count file types
find [directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Largest files
du -sh [directory]/* | sort -rh | head -20

# Files modified this week
find [directory] -type f -mtime -7
```

## Finding Duplicates

```bash
# By hash (exact duplicates)
find [directory] -type f -exec md5sum {} \; | sort | uniq -d

# By name
find [directory] -type f -printf '%f\n' | sort | uniq -d

# By size
find [directory] -type f -printf '%s %p\n' | sort -n | uniq -D -w 10
```

## Organization Patterns

### By Type

```
Downloads/
├── Documents/     # PDF, DOCX, TXT
├── Images/        # JPG, PNG, SVG
├── Videos/        # MP4, MOV
├── Archives/      # ZIP, TAR, DMG
├── Code/          # Projects
└── ToSort/        # Needs decision
```

### By Purpose

```
Documents/
├── Work/
│   ├── Projects/
│   ├── Reports/
│   └── Archive/
└── Personal/
    ├── Finance/
    ├── Medical/
    └── Archive/
```

### By Date

```
Photos/
├── 2024/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
├── 2023/
└── Unsorted/
```

## Organization Workflow

1. **Analyze** - Review current structure
2. **Plan** - Propose new structure
3. **Confirm** - Get user approval
4. **Execute** - Move files systematically
5. **Summarize** - Report changes

## Execution Commands

```bash
# Create structure
mkdir -p "path/to/new/folders"

# Move files
mv "old/path/file.pdf" "new/path/file.pdf"

# Batch move by extension
find . -name "*.pdf" -exec mv {} Documents/ \;
```

## Best Practices

### Folder Naming

- Clear, descriptive names
- Avoid spaces (use hyphens)
- Use prefixes for ordering: `01-current`, `02-archive`

### File Naming

- Include dates: `2024-10-17-meeting-notes.md`
- Be descriptive
- Remove download artifacts: `file (1).pdf` → `file.pdf`

### When to Archive

- Not touched in 6+ months
- Completed work for reference
- Old versions after migration
- Files you're hesitant to delete

## Maintenance Schedule

| Frequency | Task |
|-----------|------|
| Weekly | Sort new downloads |
| Monthly | Review/archive projects |
| Quarterly | Check for duplicates |
| Yearly | Archive old files |

## Important Rules

- Always confirm before deleting
- Log all moves for undo
- Preserve modification dates
- Stop and ask on unexpected situations

---
name: rename-file
description: Rename files in a specified directory with a given prefix. This skill prompts the user for a prefix and directory path, shows a preview of changes, and asks for confirmation before executing. Uses Node.js script for cross-platform compatibility.
---

# Rename File Skill

This skill renames all files in a specified directory by adding a prefix to each filename. It shows a preview of changes and asks for user confirmation before executing the rename operation.

## When to use this skill

Use this skill when:
- User wants to batch rename files in a directory
- User needs to add a consistent prefix to multiple files
- User wants to preview changes before applying them
- User wants a safe, interactive file renaming tool

## Prerequisites

The skill uses a JavaScript script for file operations, which requires **Node.js** to be installed.

## Implementation steps

### 1. Ask for user inputs

Use `AskUserQuestion` to get:
1. **Prefix**: What prefix should be added to the filenames?
2. **Directory path**: Which directory contains the files to rename? (Enter absolute or relative path)
3. **Confirmation**: Show preview and ask for confirmation before proceeding

Example AskUserQuestion call for prefix and directory:

```json
{
  "questions": [{
    "question": "What prefix should be added to the filenames?",
    "header": "Prefix",
    "options": [
      {"label": "Enter custom prefix", "description": "I'll type a prefix (e.g., 'photo_', 'backup_')"}
    ],
    "multiSelect": false
  }, {
    "question": "Which directory contains the files to rename?",
    "header": "Directory",
    "options": [
      {"label": "Current directory", "description": "Use current working directory"},
      {"label": "Custom path", "description": "I'll specify a different directory"}
    ],
    "multiSelect": false
  }]
}
```

### 2. Process user inputs

After getting answers:
- **Prefix**: Use the user-provided prefix (sanitize if needed)
- **Directory path**:
  - If "Current directory" selected, use current working directory
  - If "Custom path" selected, ask user to enter the path via a follow-up question
  - Validate that the directory exists and is readable

### 3. Generate preview

Read the directory contents and generate a preview of rename operations:
- List all files (excluding directories) in the target directory
- Show current filename → new filename mapping
- Count total files to be renamed

Display the preview to the user and ask for confirmation:

```json
{
  "questions": [{
    "question": "Preview: ${count} files will be renamed with prefix '${prefix}'. Proceed?",
    "header": "Confirmation",
    "options": [
      {"label": "Yes, rename files", "description": "Execute the rename operation"},
      {"label": "No, cancel", "description": "Cancel without making changes"}
    ],
    "multiSelect": false
  }]
}
```

### 4. Execute rename operation

If user confirms, run the JavaScript rename script:

```bash
# Get the path to this skill directory
SKILL_DIR="$(dirname "$0")/rename-file"

# Run the JavaScript rename script
node "$SKILL_DIR/scripts/rename-files.js" "<prefix>" "<directory-path>"
```

### 5. Display results

Show the user:
- Number of files successfully renamed
- Any errors encountered
- Summary of changes made

## Script details

The JavaScript script (`scripts/rename-files.js`):
1. Validates the directory exists and is accessible
2. Reads all files in the directory (excluding subdirectories)
3. For each file, constructs new filename by prepending the prefix
4. Performs the rename operation using `fs.renameSync`
5. Handles errors gracefully (e.g., permission issues, duplicate names)
6. Returns success/failure status

## Error handling

- If directory doesn't exist or is not accessible, show error and abort
- If no files found in directory, inform user and exit
- If a file with the new name already exists, skip that file and report
- If permission denied for any file, skip and report error
- Rollback on critical errors (optional, can be implemented)

## Safety features

- Always shows preview before making changes
- Asks for explicit confirmation
- Skips directories (only renames files)
- Preserves file extensions
- Reports all operations for transparency

## Usage example

```
User: /rename-file
Assistant: Asks for prefix and directory
User: Prefix: "vacation_", Directory: "./photos"
Assistant: Shows preview: "photo1.jpg" → "vacation_photo1.jpg", etc.
User: Confirms
Assistant: Renames files and shows summary
```
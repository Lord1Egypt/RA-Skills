---
title: Text Directory Archiver
description: Package directory structures into a single plain text file, or restore directory structures from text files. Ideal for transferring projects across sessions, creating codebase snapshots, and sharing full projects in plain-text environments.
---


Text Directory Archiver

Serialize any directory structure into copyable plain text, or restore directories from text content. It can be operated automatically via scripts, and also acts as a multi-file delivery protocol between AI and users.

Quick Reference for Use Cases

Scenario Recommended Method
Local directory ↔ Text file (with terminal access) archive.py script
Request AI to generate a multi-file project AI outputs content following the protocol format
Migrate projects across sessions (no direct file transfer) Package to text → Paste into new session → Unpack
Share code repositories via instant messaging or forums Package to text; recipients unpack the content

Method 1: Automated Script (Terminal Environment Required)

Requirements: Python 3.6 or above; no extra packages required.

```bash
# Pack: Compress a directory into a text file
python archive.py pack <source_directory> <output_file.txt>

# Unpack: Restore a text file to a directory
python archive.py unpack <input_file.txt> <output_directory>
```

The script will automatically complete the following tasks:

· Embed plain text files (UTF-8 decodable) as raw content
· Encode binary files with Base64
· Record target paths for symbolic links (converted to placeholder files for cross-platform use)
· Generate a random separator to avoid content conflicts

Method 2: Direct AI Protocol Output (Pure Chat Environment)

Use this method when you need the AI to output a complete project structure during conversations.

Prompt Template for AI Output:

Output this project following the Text Directory Archiver protocol. Set the separator to 'v1', and include the files listed below: [List your files here]

Protocol Specifications

1. JSON Header (Must be placed at the very start)

```json
{
  "separator": "v1",
  "files": {
    "src/main.py":   { "type": "text" },
    "README.md":     { "type": "text" },
    "data/model.bin":{ "type": "base64" },
    "logs/":         { "type": "dir" }
  }
}
```

· separator: A space‑free string for building delimiters to prevent conflicts with file content. A short random string is recommended.
· files: Declare all file paths. Valid type values: text, base64, dir, symlink.

2. File Content Blocks (Immediately after the JSON header)

```plaintext
---file_v1: src/main.py (text)
print("Hello, world!")

---file_v1: README.md (text)
# My Project
This is the documentation.

---file_v1: data/model.bin (base64)
SGVsbG8gV29ybGQ=
```

Format Rules:

· Each block starts with ---file_<separator>: <file_path> (<type>) on an independent line
· Content continues until the next delimiter or the end of the text
· For symbolic links: Use ---symlink_<separator>: <path> -> <target_path>
· The dir type is only declared in the JSON header, with no corresponding content block

Minimal Example

```plaintext
{
  "separator": "x1",
  "files": {
    "hello.py": { "type": "text" },
    "assets/": { "type": "dir" }
  }
}
---file_x1: hello.py (text)
print("hi")
```

Notes

When Packing

· Large binary files (videos, model weights, etc.) will expand in size by approximately 33% due to Base64 encoding overhead. Exclude such files as appropriate.
· The script will skip symbolic links with missing targets and output a warning.

When Unpacking

· The target directory will be created automatically if it does not exist.
· Administrator privileges are required to create symbolic links on Windows. If creation fails, a placeholder file storing the link target path will be generated instead.

When Generating Content via AI

· Long outputs from AI may be truncated. Please check the integrity of the last file.
· For large projects, request the AI to output content in batches by directories.

Script Resources

scripts/archive.py: Core script that supports full packing and unpacking workflows, including processing for binary files and symbolic links. Run the script directly to view usage instructions.
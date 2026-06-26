---
name: file-writer
description: Safely write or append text content to files ONLY in /home/alfred/.openclaw/workspace/scratch. Creates backups before overwriting ({filename}.bak, .bak.1, etc.). Creates subdirectories if needed. Triggers on queries like "update the script with the new feature" (infers update), "write that information to a file in your scratch area" (prompts for details), "write [content] to [rel_path]", "append [content] to [rel_path]". Restrict to relative paths; reject absolutes, ../ escapes, binary content, or non-text extensions. NOT for executing code, deleting, or writing outside scratch.
---

# File Writer Skill

## Quick Start
- Base directory: /home/alfred/.openclaw/workspace/scratch. All paths relative to this (e.g., "notes.txt" or "subdir/log.md").
- Sanitize: Reject if path contains '../', starts with '/', or has non-text extensions (allow only .txt, .md, .log, .json).
- Primary tools: 'write' for saving, 'read' for checks/backups, 'exec' for mkdir -p (fallback to message if unavailable).
- Mode: Write (default/overwrite with backup), append (if specified).

## Step-by-Step Workflow
1. Parse query: Extract rel_path (e.g., "subdir/notes.txt"), content, mode (write/append; infer from phrases like "update" = write).
   - If missing (e.g., "write that information"), use message to ask for rel_path/content.
2. Sanitize: Validate rel_path (no escapes, safe extension). Compute full_path = base_dir + rel_path.
3. Create subdirs if needed: Extract parent from rel_path; call 'exec'("mkdir -p [base_dir]/[parent]") or message: "Please run `mkdir -p [full_parent]` and confirm."
4. Check existence (call 'read' on full_path):
   - If exists and write mode: Create backup (read content, find unique .bak.N path, 'write' to it).
   - Confirm overwrite/append: Use message ("Confirm [action] on [file]? Yes/No").
5. Execute:
   - Write: 'write' full_path with content.
   - Append: 'read' existing, concatenate content, 'write' back.
6. Handle errors: Reply with details; log via message ("Wrote [bytes] to [full_path] at [timestamp]").
7. If tools fail, fallback: Message requesting user runs `echo "[content]" > [full_path]` or `>>` for append.

## Safety Guidelines
- Limits: Max 50k chars; reject binary/large.
- Backups: Always for overwrites; increment .bak.N until unique (e.g., check with 'read').
- Sensitive paths: If contains 'secret' or 'key', double-confirm.
- No auto-mkdir if exec unavailable: Require user confirmation/action.
- See references/safety.md for patterns.

## Edge Cases
- Empty content: Reject with "Content required."
- Non-existent for append: Treat as write.
- Existing .bak: Increment (e.g., .bak.1, .bak.2; use loop with 'read' to find next).
- Invalid path: "Invalid: Must be relative text file in scratch."
- Large content: Reject or chunk (multiple writes if over limit).

## Bundled Resources
- scripts/backup_file.sh: Fallback Bash for creating backups if tools limited.
- references/safety.md: Sanitization and confirmation patterns.

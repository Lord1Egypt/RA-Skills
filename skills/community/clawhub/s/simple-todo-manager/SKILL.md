# Skill: Simple Todo Manager

## Purpose
A lightweight, no-frills todo list manager that helps you track tasks without getting in the way. Perfect for quick task capture and simple daily planning.

## Prerequisites
- [ ] OpenClaw instance running (any model)
- [ ] Write access to the workspace directory

## Configuration
> **Edit these values before first use.**

```yaml
# Todo file location (relative to workspace root)
todo_file: ./todo.md

# Default priority for new tasks: low | medium | high
default_priority: medium

# Auto-archive completed tasks after N days (0 = never)
auto_archive_days: 7
```

## Workflow

### Add a Task
When the user asks to add a todo:
1. Read the current todo file (create it if it doesn't exist)
2. Append the new task with timestamp and default priority
3. Confirm the task was added
4. Show the updated list

Format for new tasks:
```
- [ ] [PRIORITY] Task description (added YYYY-MM-DD)
```

### List Tasks
When the user asks to see todos:
1. Read the todo file
2. Group by status (pending first, then completed)
3. Sort pending tasks by priority (high > medium > low)
4. Display in a clean, readable format

### Complete a Task
When the user marks a task done:
1. Read the todo file
2. Find the matching task
3. Change `- [ ]` to `- [x]` and add completion timestamp
4. Confirm completion
5. Run auto-archive check if enabled

### Remove a Task
When the user asks to delete/remove a task:
1. Read the todo file
2. Remove the matching task line
3. Confirm removal

## Rules
- ALWAYS use the configured todo_file path, never hardcode
- NEVER delete tasks without explicit user confirmation
- ALWAYS show task count after modifications
- When multiple tasks match, ask for clarification instead of guessing
- Preserve all existing tasks when modifying the file

## Troubleshooting
- If todo file doesn't exist: create it with a header comment
- If file is corrupted: back it up and start fresh
- If priority is unrecognized: default to medium

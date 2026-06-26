---
name: feature-task-retrieval
description: Logic for retrieving task details from various sources and configuring them.
---

# Task Retrieval & Configuration

Handles fetching task details (title, description, status) from external data sources (ClickUp, Jira, etc.) and managing the configuration for these sources.

## Global Configuration

- **Path**: `~/.bonfire/source.json` (user-level, persistent)
- **Purpose**: Maps input patterns to specific query commands to skip discovery steps.

### Config Structure

```json
{
  "dataSourceType": "clickup",
  "description": "ClickUp task link",
  "matchPatterns": ["clickup.com/t/", "app.clickup.com"],
  "taskIdPlaceholder": "<task_id>",
  "commands": {
    "get": "node ~/.bonfire/skills/clickup/query.mjs get <task_id> --subtasks",
    "comments": "node ~/.bonfire/skills/clickup/query.mjs comments <task_id>"
  },
  "envCheck": "~/.bonfire/skills/clickup/.env"
}
```

## Retrieval Workflow

### 1. Check Global Config
1. Read `~/.bonfire/source.json`.
2. If input (URL/text) matches `matchPatterns`:
   - **Sanitize Input**: Parse `task_id` using strict patterns (e.g., alphanumeric only).
   - **Verify Commands**: Ensure the command to be executed is from a trusted configuration.
   - Execute `commands.get` and `commands.comments`.
   - **Skip discovery**.

### 2. Discovery (find-skills)
If no config matches:
1. **Analyze Input**: Identify type (URL domain or text keywords).
2. **Find Skill**: Run `npx skills find <keyword>` (e.g., `npx skills find clickup`).
3. **Verify Source**: Check if the found skill/source is from a trusted provider.
4. **Confirm & Save**:
   - Present found skills/commands to the user.
   - **Ask user to confirm** the command and explicitly acknowledge the security risk of third-party command execution.
   - **Save** new config to `~/.bonfire/source.json` only after explicit confirmation.
5. **Execute**: Run the confirmed method to get task info.

### 3. Fallback
If no skill found, config fails, or user denies execution:
- Prompt user for: "Task Title", "Description", "Short Branch Description".

## Security Guidelines

- **Input Sanitization**: Never interpolate raw user input into shell commands. Always use regex to extract and validate IDs (e.g., `[a-zA-Z0-9_\-]+`).
- **Command Validation**: Only execute commands that have been explicitly reviewed and confirmed by the user.
- **Trusted Sources**: Prefer skills and query methods from verified organizations.
- **No Implicit Execution**: Never automatically execute a discovered command without prior user approval.

## Key Points
- Always check global config first to save time.
- Sanitize all external inputs before command interpolation.
- Persist successful discovery only after explicit user confirmation.
- Fallback to manual user input if automation is insecure or fails.

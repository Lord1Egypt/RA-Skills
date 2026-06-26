---
name: rectify
description: |
  Manage tasks, columns, and documents on the Rectify platform via REST API.
  Use when the user asks about creating, updating, moving, deleting, or searching
  tasks on the AgentPulse task board, or creating and managing Rectify Documents.
  Rectify is an all-in-one SaaS operations platform for bug reporting, session
  replays, uptime monitoring, code scanning, roadmaps, changelogs, and AI agent
  management. Triggers on: task board, kanban, create task, move task, assign task,
  list columns, documents, create document, update document, archive, sub-pages.
user-invocable: true
metadata: {"openclaw": {"emoji": "🚀", "requires": {"env": ["RECTIFY_PROJECT_TOKEN"]}, "primaryEnv": "RECTIFY_PROJECT_TOKEN"}}
---

# Rectify AgentPulse — Task Board & Document Management

You have full CRUD access to the Rectify AgentPulse task board and Rectify Documents via REST API.

**Rectify** (https://www.rectify.so) is an all-in-one SaaS operations platform. AgentPulse is its AI agent management layer built on OpenClaw, providing task boards, agent coordination, and document management.

## Authentication

All requests use your RECTIFY_PROJECT_TOKEN — no extra setup needed.

Required headers on every request:
- `x-api-token: $RECTIFY_PROJECT_TOKEN`

```
Task Invoke URL:    https://api.rectify.so/v1/agent-pulse/ai-tools/invoke
Doc Invoke URL:     https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke
Board Context URL:  https://api.rectify.so/v1/agent-pulse/ai-tools/board-context
Doc Context URL:    https://api.rectify.so/v1/agent-pulse/ai-tools/document-context
Members URL:        https://api.rectify.so/v1/agent-pulse/members
```

## Security & Privacy

This skill sends requests to `https://api.rectify.so` only.
- No credentials are stored outside the user's local environment
- `RECTIFY_PROJECT_TOKEN` is a user-issued project token from app.rectify.so
- All API endpoints used by this skill are listed in this file

---

## Task Board

### List all columns
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_columns", "args": {}}'
```

### List all tasks
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_tasks", "args": {}}'
```

### List project members (for task assignment)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/members" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN"
```

> Returns `{ data: [{ id, name, email, image, role }] }`. Use `id` as `assignedMember` when creating or updating tasks.

### Create a task
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_task", "args": {"title": "TASK_TITLE", "description": "OPTIONAL_DESC", "priority": "low|medium|high", "columnId": "COLUMN_ID", "assignedAgent": "OPTIONAL_AGENT_NAME", "assignedMember": "MEMBER_USER_ID", "workspace": "OPTIONAL_WORKSPACE_PATH", "labels": ["optional"]}}'
```

> `assignedAgent` — OpenClaw agent name (e.g. "Atlas"). `assignedMember` — user ID from the members endpoint. `workspace` — full workspace path (optional).

### Update a task
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "update_task", "args": {"taskId": "TASK_ID", "title": "NEW_TITLE", "description": "NEW_DESC", "priority": "low|medium|high", "assignedMember": "MEMBER_USER_ID", "workspace": "WORKSPACE_PATH"}}'
```

### Move a task to another column
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "move_task", "args": {"taskId": "TASK_ID", "columnId": "TARGET_COLUMN_ID"}}'
```

### Assign a task to an agent or member
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "assign_task", "args": {"taskId": "TASK_ID", "assignedAgent": "AGENT_NAME_OR_NULL", "assignedMember": "MEMBER_USER_ID_OR_NULL"}}'
```

> Pass `null` to unassign. Provide either or both fields.

### Delete a task
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "delete_task", "args": {"taskId": "TASK_ID"}}'
```

### Search tasks
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "search_tasks", "args": {"query": "SEARCH_TEXT", "priority": "high", "status": "in_progress", "assignedAgent": "AGENT_NAME"}}'
```

### Create a column
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_column", "args": {"name": "COLUMN_NAME", "color": "#hex6"}}'
```

### Delete a column (cascade deletes all tasks in it)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "delete_column", "args": {"columnId": "COLUMN_ID"}}'
```

### Get board context (summary of all columns and tasks)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/board-context" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN"
```

## Task Board Workflow

1. Always run `list_columns` first to get column IDs before creating or moving tasks.
2. If `list_columns` returns an empty array, create a default column (e.g. "To Do") using `create_column` before creating tasks.
3. Use column IDs (not names) when moving or creating tasks in a specific column.
4. To assign to a project member, call the members endpoint first to get user IDs.
5. When asked to delete a column, warn the user that all tasks inside will be permanently deleted, then proceed if confirmed.
6. After each action, briefly confirm what was done.

---

## Rectify Documents

Rectify Documents is a separate feature from the task board. You have full CRUD access.

### List documents
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_documents", "args": {}}'
```

### List sub-pages of a document
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_documents", "args": {"parentDocument": "PARENT_DOC_ID"}}'
```

### Get a document (with full content)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_document", "args": {"documentId": "DOC_ID"}}'
```

### Search documents by title
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "search_documents", "args": {"query": "SEARCH_TEXT"}}'
```

### Create a document
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_document", "args": {"title": "DOC_TITLE", "content": "MARKDOWN_CONTENT", "icon": "OPTIONAL_EMOJI", "isPublished": false, "parentDocument": "OPTIONAL_PARENT_DOC_ID"}}'
```

> `title` is required. `content` is plain **markdown** — do NOT include a `# Title` heading (title is a separate field). `icon` (emoji), `isPublished` (default false), and `parentDocument` (for sub-pages) are optional.

### Update a document
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "update_document", "args": {"documentId": "DOC_ID", "title": "NEW_TITLE", "content": "MARKDOWN_CONTENT", "icon": "EMOJI", "isPublished": true}}'
```

> Write content as plain **markdown**. Do NOT include a `# Title` heading — the title is a separate field.

### Archive a document (soft-delete, recursive)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "archive_document", "args": {"documentId": "DOC_ID"}}'
```

### Restore a document
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "restore_document", "args": {"documentId": "DOC_ID"}}'
```

### Delete a document (permanent)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/doc-invoke" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "delete_document", "args": {"documentId": "DOC_ID"}}'
```

### Get document context (summary of all documents)
```bash
curl -s "https://api.rectify.so/v1/agent-pulse/ai-tools/document-context" \
  -H "x-api-token: $RECTIFY_PROJECT_TOKEN"
```

## Document Workflow

1. Always run `list_documents` first to get document IDs before reading or updating.
2. To create a sub-page, use `create_document` with `parentDocument` set to the parent doc ID.
3. Write content as **markdown** — no `# Title` heading; title goes in the `title` field separately.
4. After creating or updating, briefly confirm the doc title and its ID.
5. Archive is a soft-delete (recursive for children). Use `delete_document` only for permanent removal.

---

## Error Handling

All API calls return JSON. On error the response will contain an `error` field:

```json
{ "error": "Error message here" }
```

On success:

```json
{ "success": true, "task": { "id": "...", "title": "..." } }
```

Common causes:
- `401` — Invalid or missing RECTIFY_PROJECT_TOKEN, or token not authorized for this project
- `404` — Resource not found (wrong ID)
- `400` — Missing required field

---
name: todoist-manager
description: "Управление задачами в Todoist: добавление, обновление статуса (выполнено/удалено), определение даты/срочности/приоритета и навигация по проектам. Используйте команды с указанием всех необходимых параметров: add_task(content, project_id, due_date, priority), complete_task(task_id), delete_task(task_id), list_projects()."
metadata: {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["uv"], "env": ["todoist_api_token"], "config": ["browser.enabled"] },
        "primaryEnv": "todoist_api_token",
        "homepage":"https:t.me/fugguri"
      },
  }
---

# Todoist Manager

# Todoist Manager Skill

This skill provides procedural guidance and utility scripts for interacting with the Todoist API.

## Prerequisites

**Configuration**: The Todoist API token must be placed inside `./references/API_CONFIG.json` in the `todoist_api_token` field. **The token is NOT read from environment variables.**

## Core Workflows

### 1. Add Task

Use this for creating new to-do items. The script must support extracting task details.

**Command Signature Example**:
`scripts/todoist_api.py add_task --content "Финализировать отчет по проекту X" --project_id "123456" --due_date "tomorrow" --priority 2`

| Parameter | Description | Todoist Value Mapping |
| :--- | :--- | :--- |
| `content` | The text of the task. | Required |
| `project_id` | Target project ID. | Optional |
| `due_date` | Date/Time for completion (e.g., "tomorrow", "today", "next friday 10am"). | Optional (Use natural language recognized by Todoist API) |
| `priority` | Urgency level (1-4). | Optional (1=High, 4=No Priority) |

### 2. Manage Task Status (Complete/Delete)

Use for status changes once a task ID is known.

**Commands**:
- **Complete**: `scripts/todoist_api.py complete_task --task_id "78901"`
- **Delete**: `scripts/todoist_api.py delete_task --task_id "78901"`

### 3. Project Navigation

Use to list available projects for targeting new tasks.

**Command**:
- **List Projects**: `scripts/todoist_api.py list_projects`

**Note on Projects**: Initial tests confirmed that the correct base URL appears to be `/api/v2/`. Using a real token should yield a list of projects or a 401/403 error if the token is invalid or lacks scope. The endpoint for listing projects is `/projects`.

## Current State

The API integration script, `scripts/todoist_api.py`, has been created as a **mock stub**. It currently simulates API calls by printing the intended action and arguments to the console instead of hitting the live Todoist API.

This structure is now complete and ready for you to populate with your actual API credentials and implementation details.

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**

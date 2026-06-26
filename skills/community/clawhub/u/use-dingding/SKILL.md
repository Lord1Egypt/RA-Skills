---
name: use-dingding
displayName: Use Dingding
version: 1.1.0
description: Interact with DingTalk enterprise workspace using the dws CLI. Required: dws CLI, DWS_CLIENT_ID, DWS_CLIENT_SECRET. Use for: contacts, chat, calendar, todo, approvals, attendance, reports, AITable.

required_env:
  - DWS_CLIENT_ID
  - DWS_CLIENT_SECRET

required_binaries:
  - dws
---

# DingTalk Workspace Skill

Use the `dws` CLI to interact with DingTalk enterprise workspace. This skill covers all 12 products: contact, chat, bot, calendar, todo, oa (approval), attendance, ding, report, aitable, workbench, and devdoc.

## ⚠️ Security & Safety Notes

**Read before installing:**

1. **Credentials Required**: This skill requires OAuth credentials (DWS_CLIENT_ID, DWS_CLIENT_SECRET) from a DingTalk Open Platform app. Enterprise admin approval may be needed.

2. **Install Safely**: The `dws` CLI installer fetches from GitHub. **Review the installer script before running**:
   - Installer: https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/scripts/install.sh
   - Releases: https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases

3. **Autonomous Execution Risk**: This skill can perform destructive actions (approve workflows, send messages, delete records). **Always use `--dry-run` first** and restrict autonomous invocation unless you trust the agent.

4. **Least Privilege**: Use scoped OAuth credentials with minimum permissions. Test in a sandbox enterprise first.

## Prerequisites

### Installation

**Option 1: Install from release (recommended)**

Download pre-built binary from https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases

**Option 2: Build from source (safer)**

```bash
git clone https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli.git
cd dingtalk-workspace-cli
go build -o dws ./cmd
cp dws ~/.local/bin/
```

**Option 3: Install script (review first!)**

```bash
# macOS / Linux - REVIEW SCRIPT BEFORE RUNNING
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh

# Windows (PowerShell) - REVIEW SCRIPT BEFORE RUNNING
irm https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.ps1 | iex
```

### Authentication

**Recommended: Interactive Login (secure keychain storage)**

```bash
dws auth login --client-id <your-app-key> --client-secret <your-app-secret>
# Tokens stored encrypted in system Keychain (macOS/Windows) or libsecret (Linux)
```

**Alternative: Environment Variables (use with caution)**

```bash
export DWS_CLIENT_ID=<your-app-key>
export DWS_CLIENT_SECRET=<your-app-secret>
dws auth login
```

⚠️ **Security note**: Environment variables may be exposed in process listings and logs. Prefer interactive login for production use.

## Safe Execution Guidelines

### For Agents

- **`--dry-run`**: **ALWAYS use first** for mutations to preview API calls
- **`--yes`**: Skip confirmation prompts (use only after verifying with --dry-run)
- **`--jq`**: Extract specific fields to reduce token consumption
- **`--fields`**: Return only needed fields

### Recommended Workflow

```bash
# 1. Preview the operation
dws todo task create --title "Test" --executors "user123" --dry-run

# 2. Verify the output looks correct

# 3. Execute (only if preview was correct)
dws todo task create --title "Test" --executors "user123" --yes
```

### Auto-Correction

`dws` automatically corrects common AI mistakes:
- `--baseId` → `--base-id` (camelCase to kebab-case)
- `--timeout30` → `--timeout 30` (sticky argument splitting)
- `--tabel-id` → `--table-id` (fuzzy matching)
- `"yes"` → `true`, `"2024/03/29"` → `"2024-03-29"` (value normalization)

## Discovery & Introspection

Before making calls, discover available capabilities:

```bash
# List all products and tool counts
dws schema --jq '.products[] | {id, tool_count: (.tools | length)}'

# Inspect a specific tool's parameter schema
dws schema aitable.query_records --jq '.tool.parameters'

# View required fields
dws schema aitable.query_records --jq '.tool.required'

# List all product IDs
dws schema --jq '.products[].id'
```

## Quick Reference by Product

### Contact

```bash
# Search users by keyword
dws contact user search --keyword "engineering"

# Get current user profile
dws contact user get-self --jq '.result[0].orgEmployeeModel | {name: .orgUserName, dept: .depts[0].deptName}'

# Search department by name
dws contact dept search --keyword "Engineering"

# List department members
dws contact dept members --dept-id <dept-id>
```

### Chat

```bash
# Send message as bot
dws chat message send-by-bot --robot-code <BOT_CODE> --group <GROUP_ID> --title "Weekly Report" --text @report.md

# List groups
dws chat group list

# Get group info
dws chat group get --group-id <GROUP_ID>
```

### Calendar

```bash
# List calendar events
dws calendar event list

# Create event
dws calendar event create --title "Team Meeting" --start "2024-03-29T14:00:00Z" --end "2024-03-29T15:00:00Z"

# Find free slots
dws calendar participant busy --user-ids <user-id-1>,<user-id-2> --start "2024-03-29" --end "2024-03-30"

# Search meeting rooms
dws calendar room search --keyword "Meeting Room"
```

### Todo

```bash
# Create todo
dws todo task create --title "Review PR" --executors "<your-userId>" --yes

# List todos
dws todo task list

# Mark as done
dws todo task done --task-id <task-id>
```

### Approval (OA)

```bash
# List pending approvals
dws oa approval list --status pending

# Approve instance
dws oa approval approve --instance-id <instance-id> --comment "Approved"

# Reject instance
dws oa approval reject --instance-id <instance-id> --comment "Needs revision"
```

### Attendance

```bash
# View my attendance records
dws attendance record list --user-id <your-userId>

# View team shift schedule
dws attendance shift list --dept-id <dept-id>
```

### Report

```bash
# View today's received reports
dws report list --type received --start-date "2024-03-29" --end-date "2024-03-29"

# Create report
dws report create --template-id <template-id> --content @report.md
```

### AITable

```bash
# Query records
dws aitable record query --base-id <BASE_ID> --table-id <TABLE_ID> --limit 10

# Create record
dws aitable record create --base-id <BASE_ID> --table-id <TABLE_ID> --fields '{"name": "Task 1", "status": "open"}'

# List bases
dws aitable base list

# List tables in a base
dws aitable table list --base-id <BASE_ID>
```

## Output Control

### jq Filtering

```bash
# Extract specific fields
dws contact user search --keyword "engineering" --jq '.result[] | {name: .orgUserName, userId: .userId}'

# Count results
dws todo task list --jq '.result | length'
```

### Field Selection

```bash
# Return only specific fields
dws aitable record query --base-id <BASE_ID> --table-id <TABLE_ID> --fields invocation,response
```

### File Input

```bash
# Read from file
dws chat message send-by-bot --robot-code <BOT_CODE> --group <GROUP_ID> --text @message.md

# Pipe from stdin
cat message.md | dws chat message send-by-bot --robot-code <BOT_CODE> --group <GROUP_ID>
```

## Common Workflows

See bundled scripts in `scripts/` for batch operations:

**Safety First:** All mutation scripts default to `--dry-run` mode. You must explicitly pass `--execute` to perform actual changes.

| Script | Description |
|--------|-------------|
| `calendar_schedule_meeting.py` | Create event + add participants + book meeting room (use `--execute` to book) |
| `calendar_free_slot_finder.py` | Find common free slots across multiple people (read-only) |
| `todo_batch_create.py` | Batch create todos from JSON (use `--execute` to create) |
| `contact_dept_members.py` | Search department and list all members (read-only) |
| `report_inbox_today.py` | View today's received reports (read-only) |
| `import_records.py` | Import CSV records into AITable (use `--execute` to import) |

**Example:**
```bash
# Preview first (default behavior)
python scripts/todo_batch_create.py tasks.json

# Execute after verifying preview
python scripts/todo_batch_create.py tasks.json --execute
```

## Error Handling

### Common Error Codes

- `INVALID_TOKEN`: Re-authenticate with `dws auth login`
- `PERMISSION_DENIED`: Check app permissions in DingTalk Open Platform
- `RESOURCE_NOT_FOUND`: Verify IDs with `dws schema` introspection

### Recovery

When encountering `RECOVERY_EVENT_ID`, use:
```bash
dws --recovery <RECOVERY_EVENT_ID>
```

## Security Notes

- Credentials are stored encrypted in system Keychain (never in config files)
- All requests use HTTPS to `*.dingtalk.com` only
- Use `--dry-run` before any mutation to preview the API call
- Token refresh is automatic; no manual intervention needed

## Reference Files

- **Product commands**: See `references/products/*.md` for detailed command reference per product
- **Intent guide**: See `references/intent-guide.md` for disambiguation (e.g., report vs todo)
- **Error codes**: See `references/error-codes.md` for debugging workflows
- **Global reference**: See `references/global-reference.md` for auth, output formats, global flags

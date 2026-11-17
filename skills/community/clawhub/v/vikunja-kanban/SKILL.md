# Vikunja Kanban Skill

Manage a Vikunja kanban board via API. Read status, create/move/complete tasks, and integrate with heartbeat and triage crons.

## Config

Credentials stored in `secrets/vikunja.env`:
```
VIKUNJA_URL=https://kanban.pigpen.haus
VIKUNJA_TOKEN=${VIKUNJA_TOKEN}
VIKUNJA_PROJECT_ID=1
VIKUNJA_VIEW_ID=4
```

## Authentication

All scripts use a **long-lived API token** (expires 2030-01-01). No JWT login needed.
- Token: Set via `VIKUNJA_TOKEN` environment variable
- Permissions: tasks (read_all, update, create, delete), projects (read_all, update, create)
- Header: `Authorization: Bearer $VIKUNJA_TOKEN`
- JWT login credentials kept in `secrets/vikunja.env` for reference only

## Bucket IDs

| ID | Name | Purpose |
|----|------|---------|
| 1 | 🔴 Urgent | Needs immediate attention |
| 2 | ⏳ Waiting On | Sent/requested, awaiting reply |
| 7 | ⚠️ System Issues | Infra/system problems |
| 8 | 🚧 Active Projects | In progress |
| 9 | 📅 Upcoming | Scheduled/future |
| 10 | 📥 Inbox | New items, untriaged |
| 3 | ✅ Done | Completed |

## Scripts

All scripts are in the skill's `scripts/` directory. Run from the skill root.

### Read the board
```bash
bash scripts/vikunja-status.sh              # All buckets
bash scripts/vikunja-status.sh "Urgent"     # Filter by bucket name
```

### Add a task
```bash
bash scripts/vikunja-add-task.sh "Title" "Description" BUCKET_ID [PRIORITY]
# Priority: 0=unset, 1=low, 2=medium, 3=high, 4=urgent
# Example: bash scripts/vikunja-add-task.sh "Fix DNS" "Check records" 1 4
```

### Move a task between buckets
```bash
bash scripts/vikunja-move-task.sh TASK_ID BUCKET_ID
# Example: bash scripts/vikunja-move-task.sh 15 3  # Move to Done
```

### Complete a task
```bash
bash scripts/vikunja-complete-task.sh TASK_ID
```

## Heartbeat Integration

The heartbeat cron reads from Vikunja:
```bash
bash scripts/vikunja-status.sh
```
- Check 🔴 Urgent for items aging >1h
- If Vikunja unreachable, fall back to `scripts/nc-status-board.sh read`

## Email Triage Integration

Email triage adds Action Required items to the Inbox bucket:
```bash
bash scripts/vikunja-add-task.sh "Email subject" "Brief description" 10 3
```

## API Reference

- **Base URL:** https://kanban.pigpen.haus/api/v1
- **Auth:** POST /login with username/password → JWT token (short-lived)
- **Tasks:** PUT /projects/{id}/tasks (create), POST /tasks/{id} (update)
- **Buckets:** POST /projects/{id}/views/{view}/buckets/{bucket}/tasks (move task)
- **Views:** GET /projects/{id}/views/{view}/tasks (list tasks by bucket)

## Notes

- **Long-lived API token** used (expires 2030) — no JWT login overhead
- Vikunja uses PUT for creation, POST for updates (unusual)
- Bucket IDs are specific to the Kanban view (view_id=4)
- Project is shared: Kit (admin), Alex (user)
- Token has tasks + projects permissions; covers all kanban operations

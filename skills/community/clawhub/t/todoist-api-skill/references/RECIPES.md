# Recipes

## Table of contents

- [Inbox triage](#inbox-triage)
- [Quick capture from natural language](#quick-capture-from-natural-language)
- [Project setup](#project-setup)
- [Weekly review](#weekly-review)
- [Overdue clean-up](#overdue-clean-up)
- [Audit trail comments](#audit-trail-comments)
- [Shared project assignment prep](#shared-project-assignment-prep)
- [Legacy ID migration](#legacy-id-migration)
- [Template export](#template-export)

## Inbox triage

Preview what is currently in a project:

```bash
python3 scripts/todoist_api.py resolve-project --name "Inbox"
python3 scripts/todoist_api.py get-tasks --project-id PROJECT_ID --all
```

Move non-recurring inbox work into a target section:

```bash
python3 scripts/todoist_api.py bulk-move-tasks \
  --filter "#Inbox & !recurring" \
  --target-project-name "Work" \
  --target-section-name "Next Actions" \
  --dry-run
```

Then execute:

```bash
python3 scripts/todoist_api.py bulk-move-tasks \
  --filter "#Inbox & !recurring" \
  --target-project-name "Work" \
  --target-section-name "Next Actions" \
  --confirm
```

## Quick capture from natural language

For user requests that already sound like Todoist input, prefer quick add:

```bash
python3 scripts/todoist_api.py quick-add-task \
  --text "Pay electricity bill next Tuesday 18:00 #Admin @finance p2"
```

This is usually better than manually constructing `create-task` payloads when the user already phrased dates, labels, and priorities naturally.

## Project setup

Create a project if needed:

```bash
python3 scripts/todoist_api.py ensure-project \
  --name "Client Alpha" \
  --description "Delivery work"
```

Create standard sections:

```bash
python3 scripts/todoist_api.py ensure-section --project-name "Client Alpha" --name "Next Actions"
python3 scripts/todoist_api.py ensure-section --project-name "Client Alpha" --name "Waiting"
python3 scripts/todoist_api.py ensure-section --project-name "Client Alpha" --name "Done"
```

Optionally seed tasks via `/sync`:

```bash
python3 scripts/todoist_api.py sync \
  --commands-file assets/sync/seed-project.json \
  --dry-run
```

## Weekly review

Get completed work for the last week:

```bash
python3 scripts/todoist_api.py report-completed \
  --since "2026-03-01T00:00:00Z" \
  --until "2026-03-07T23:59:59Z" \
  --by completion \
  --output reports/weekly-review.json
```

Get recent activity for one project:

```bash
python3 scripts/todoist_api.py get-activities \
  --parent-project-id PROJECT_ID \
  --all \
  --output reports/weekly-activity.json
```

## Overdue clean-up

Preview overdue work:

```bash
python3 scripts/todoist_api.py get-tasks-by-filter \
  --query "overdue" \
  --all
```

Preview closing all overdue errands:

```bash
python3 scripts/todoist_api.py bulk-close-tasks \
  --filter "overdue & @errands" \
  --dry-run
```

If the user confirms that completed/irrelevant errands should be closed, execute with `--confirm`.

## Audit trail comments

Add a comment to every matching urgent task:

```bash
python3 scripts/todoist_api.py bulk-comment-tasks \
  --filter "today & p1" \
  --content "Reviewed during daily planning." \
  --dry-run
```

This is useful when an agent needs to leave a trace explaining a bulk review, escalation, or triage pass.

## Shared project assignment prep

Resolve collaborators before assigning:

```bash
python3 scripts/todoist_api.py get-project-collaborators --project-id PROJECT_ID
```

Then update a task with the selected collaborator ID:

```bash
python3 scripts/todoist_api.py update-task \
  --task-id TASK_ID \
  --assignee-id USER_ID \
  --dry-run
```

## Legacy ID migration

When the user has old cached IDs or data from an older integration:

```bash
python3 scripts/todoist_api.py ids-map \
  --object-name tasks \
  --ids 918273645,918273646
```

Repeat for projects, sections, or comments as needed.

## Template export

Get a shareable template URL from an existing project:

```bash
python3 scripts/todoist_api.py template-export-url \
  --project-id PROJECT_ID
```

If the user wants a full downloadable template file or a file-based import, switch to `raw` or `curl`, because those flows are not fully wrapped here.

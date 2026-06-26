# Tracker Reference: Paperclip

How to use the workflow-execution skill with [Paperclip](https://paperclip.ing) as your project management system.

## Create an issue

```
POST /api/companies/{companyId}/issues
{
  "title": "Your task title",
  "description": "Brief description",
  "status": "todo",
  "priority": "high",
  "parentId": "{parentIssueId}",
  "projectId": "{projectId}"
}
```

## Attach a plan document

```
PUT /api/issues/{issueId}/documents/plan
{
  "title": "Implementation Plan",
  "format": "markdown",
  "body": "# Plan\n\n## Goal\n...\n\n## Done Criteria\n...\n\n## Steps\n..."
}
```

When updating an existing document, include `baseRevisionId` from the current version to avoid conflicts.

## Attach additional documents

Use the same endpoint with different keys:

```
PUT /api/issues/{issueId}/documents/design
PUT /api/issues/{issueId}/documents/context
```

## Read documents (executing agent)

```
GET /api/issues/{issueId}
```

Returns `planDocument` (full text of the `plan` document) and `documentSummaries` (metadata for all linked documents).

To read a specific document:
```
GET /api/issues/{issueId}/documents/{key}
```

## Update progress

```
PATCH /api/issues/{issueId}
{ "comment": "Completed step 2. Moving to step 3." }
```

## Close the issue

```
PATCH /api/issues/{issueId}
{ "status": "done", "comment": "All done criteria met. Evidence: [verification details]" }
```

## Issue lifecycle

```
backlog → todo → in_progress → in_review → done
                     |              |
                  blocked       in_progress
```

## X-Paperclip-Run-Id header

Only send `X-Paperclip-Run-Id` when **all three conditions** are true:
- The issue status is `in_progress`
- The issue is assigned to the calling agent
- The issue was checked out (active checkout guard)

The value must be a valid UUID from a real `heartbeat_runs` row.
Do **not** send this header on issue creation or any other mutation — it causes FK violations.

## Tips

- Use `parentId` to maintain issue hierarchy (milestones → subtasks).
- Use `projectId` to group related work.
- @-mentions in comments trigger heartbeats for mentioned agents.

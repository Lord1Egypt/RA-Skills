# GitHub Issues Backend (Optional)

Sync your taskboard with GitHub Issues. This is a reference guide — the agent reads this and implements the integration when asked.

## Prerequisites

- A GitHub Personal Access Token with `repo` scope
- Set as environment variable: `export GITHUB_TOKEN=ghp_...`
- Recommended: use a dedicated machine/service token, not your personal token

## How It Works

When GitHub sync is enabled, the agent should:

1. **On task create** → Create a GitHub Issue with matching title, labels, and assignee
2. **On status update** → Update Issue labels (e.g., `status:in-progress`) and close/reopen as needed
3. **On note add** → Post an Issue comment
4. **On assign** → Update Issue assignee

## Setup Steps

1. Create status labels in your GitHub repo:
   ```
   status:backlog, status:in-progress, status:review, status:done, status:blocked
   ```

2. Map agent names to GitHub usernames (keep this in your project's config or AGENTS.md):
   ```
   code-engineer → github-username-1
   tech-lead → github-username-2
   designer → github-username-3
   ```

3. When creating/updating tasks, the agent uses the GitHub API:

### Create Issue
```bash
curl -X POST https://api.github.com/repos/OWNER/REPO/issues \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{
    "title": "TASK-001: Build auth module",
    "body": "Description here",
    "labels": ["status:backlog", "backend", "security"],
    "assignees": ["github-username"]
  }'
```

### Update Issue Status
```bash
# Update labels
curl -X PATCH https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"labels": ["status:in-progress", "backend"]}'

# Close issue (when done)
curl -X PATCH https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"state": "closed"}'
```

### Add Comment
```bash
curl -X POST https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"body": "PR #42 ready for review"}'
```

## Task Field Mapping

| Taskboard Field | GitHub Issue Field |
|---|---|
| title | title (prefixed with task ID) |
| description | body |
| status | labels (status:xxx) |
| assignee | assignees (mapped via config) |
| tags | labels |
| notes | comments |
| priority | labels (priority:xxx) |

## Tracking the Link

When a task is synced to GitHub, store the issue number in the task:
```json
{
  "id": "PROJ-001",
  "title": "Build auth",
  "github_issue": 42,
  "github_url": "https://github.com/owner/repo/issues/42"
}
```

The agent can add these fields to `taskboard.json` after creating the issue.

## Bidirectional Sync (Advanced)

For GitHub → Taskboard sync (e.g., someone closes an issue on GitHub), set up a GitHub webhook pointing to a Discord channel or agent endpoint. The agent can then update the local taskboard when notified.

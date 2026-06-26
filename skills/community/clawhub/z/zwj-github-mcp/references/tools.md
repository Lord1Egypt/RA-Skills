# GitHub MCP Tools Reference

Full tool schema from `mcporter list github --schema`.

## Authentication

```bash
mcporter call github.get_me
```

Returns: `{ login, id, profile_url, avatar_url, name, public_repos, followers, ... }`

## Repository Operations

### Search code
```bash
mcporter call github.search_code query="filename:README.md" per_page=5
```

### List repositories
```bash
mcporter call github.list_repositories per_page=10
```

### Get repository details
```bash
mcporter call github.get_repository owner="zwj-opener" repo="openclaw-desktop"
```

### Get file contents
```bash
mcporter call github.get_file_content owner="zwj-opener" repo="openclaw-desktop" path="README.md"
```

### Create/update file (requires SHA for existing files)
```bash
mcporter call github.create_or_update_file branch="main" content="# Hello" message="Update README" owner="zwj-opener" repo="my-repo" path="README.md"
```

## Issue Operations

### List issues
```bash
mcporter call github.list_issues owner="zwj-opener" repo="openclaw-desktop" per_page=10
```

### Create issue
```bash
mcporter call github.create_issue body="Bug description" owner="zwj-opener" repo="openclaw-desktop" title="Bug: something broken"
```

### Add comment
```bash
mcporter call github.add_issue_comment body="This is a comment" issue_number=1 owner="zwj-opener" repo="openclaw-desktop"
```

## Pull Request Operations

### List PRs
```bash
mcporter call github.list_pull_requests owner="zwj-opener" repo="openclaw-desktop"
```

### Create PR
```bash
mcporter call github.create_pull_request base="main" head="feature-branch" owner="zwj-opener" repo="openclaw-desktop" title="Add new feature"
```

### Add review comment
```bash
mcporter call github.add_comment_to_pending_review body="LGTM!" owner="zwj-opener" path="README.md" pull_number=1 repo="openclaw-desktop" subject_type="FILE"
```

## Branch Operations

### Create branch
```bash
mcporter call github.create_branch branch="feature/new" from_branch="main" owner="zwj-opener" repo="openclaw-desktop"
```

### Delete branch
```bash
mcporter call github.delete_branch branch="feature/new" owner="zwj-opener" repo="openclaw-desktop"
```

## CI/CD — GitHub Actions

### List workflow runs
```bash
mcporter call github.list_workflow_runs owner="zwj-opener" repo="openclaw-desktop"
```

### Trigger workflow
```bash
mcporter call github.create_workflow_dispatch owner="zwj-opener" repo="openclaw-desktop" workflow_filename="ci.yml" ref="main"
```

## Commit Operations

### Get commit details
```bash
mcporter call github.get_commit owner="zwj-opener" repo="openclaw-desktop" sha="abc123"
```

### List commits
```bash
mcporter call github.list_commits owner="zwj-opener" repo="openclaw-desktop" per_page=5
```

## Discussion & Notifications

### List notifications
```bash
mcporter call github.list_notifications all=true
```

### Mark notification as done
```bash
mcporter call github.mark_notification_as_done notification_id=123
```

## Utility

### Fork repository
```bash
mcporter call github.fork_repository owner="github" repo="github-mcp-server"
```

### Create repository
```bash
mcporter call github.create_repository name="my-new-repo" description="My new repo" private=true
```

## Notes

- All tools require `GITHUB_TOKEN` env var or Authorization header set in mcporter config
- For pagination: use `page` (1-based) and `per_page` (max 100) parameters
- For detailed error messages, add `--debug` flag to mcporter commands

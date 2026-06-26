---
name: snowsand-bitbucket
version: 1.0.0
description: Interact with Bitbucket Cloud via REST API. Use for repository management, pull request operations (list, view, create, comment, approve, merge), branch management, commit history, pipeline status, and workspace/team queries. Triggers on Bitbucket operations, PR reviews, branch management, pipeline checks, or any Atlassian Bitbucket Cloud task.
---

# Bitbucket Cloud Integration

Bitbucket Cloud REST API v2 integration for repository management, pull requests, branches, commits, and pipelines.

## Authentication

Bitbucket Cloud uses App Password authentication. Required environment variables:

- `BITBUCKET_WORKSPACE` - Default workspace slug (e.g., `myteam`)
- `BITBUCKET_USERNAME` - Bitbucket username (not email)
- `BITBUCKET_APP_PASSWORD` - App password from https://bitbucket.org/account/settings/app-passwords/

Create an App Password with required permissions:
- **Repositories**: Read, Write (for repo operations)
- **Pull requests**: Read, Write (for PR operations)
- **Pipelines**: Read (for pipeline status)
- **Account**: Read (for user info)

Test connection:
```bash
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/user" | jq .
```

## Quick Reference

All operations use the `scripts/bitbucket.py` script:

| Operation | Command |
|-----------|---------|
| **Repositories** | |
| List repos | `bitbucket.py repos` |
| View repo | `bitbucket.py repo my-repo` |
| Create repo | `bitbucket.py create-repo my-new-repo --private` |
| **Pull Requests** | |
| List PRs | `bitbucket.py prs my-repo` |
| View PR | `bitbucket.py pr my-repo 42` |
| Create PR | `bitbucket.py create-pr my-repo --title "Feature" --source feature-branch` |
| Comment on PR | `bitbucket.py pr-comment my-repo 42 "LGTM!"` |
| Approve PR | `bitbucket.py approve my-repo 42` |
| Merge PR | `bitbucket.py merge my-repo 42` |
| Decline PR | `bitbucket.py decline my-repo 42` |
| **Branches** | |
| List branches | `bitbucket.py branches my-repo` |
| View branch | `bitbucket.py branch my-repo main` |
| Create branch | `bitbucket.py create-branch my-repo feature-x --from main` |
| Delete branch | `bitbucket.py delete-branch my-repo old-feature` |
| **Commits** | |
| List commits | `bitbucket.py commits my-repo` |
| View commit | `bitbucket.py commit my-repo abc123` |
| **Pipelines** | |
| List pipelines | `bitbucket.py pipelines my-repo` |
| View pipeline | `bitbucket.py pipeline my-repo {uuid}` |
| Pipeline steps | `bitbucket.py pipeline-steps my-repo {uuid}` |
| **Workspace** | |
| List workspaces | `bitbucket.py workspaces` |
| Workspace members | `bitbucket.py members` |
| Current user | `bitbucket.py me` |

## Common Workflows

### Repository Management

```bash
# List all repositories in workspace
bitbucket.py repos

# List with pagination
bitbucket.py repos --page 2 --pagelen 25

# View specific repository details
bitbucket.py repo my-repo

# Create a new private repository
bitbucket.py create-repo my-new-repo --private --description "Project description"

# Create public repository with specific project
bitbucket.py create-repo my-public-repo --project PROJ
```

### Pull Request Workflow

```bash
# List open pull requests
bitbucket.py prs my-repo

# List all PRs (including merged/declined)
bitbucket.py prs my-repo --state all

# View PR details
bitbucket.py pr my-repo 42

# Create a pull request
bitbucket.py create-pr my-repo \
  --title "Add new feature" \
  --source feature-branch \
  --destination main \
  --description "This PR adds..."

# Add a comment
bitbucket.py pr-comment my-repo 42 "Looks good, just one question..."

# Approve the PR
bitbucket.py approve my-repo 42

# Unapprove (remove approval)
bitbucket.py unapprove my-repo 42

# Request changes
bitbucket.py request-changes my-repo 42

# Merge with default strategy
bitbucket.py merge my-repo 42

# Merge with specific strategy
bitbucket.py merge my-repo 42 --strategy squash

# Decline a PR
bitbucket.py decline my-repo 42
```

### Branch Operations

```bash
# List all branches
bitbucket.py branches my-repo

# View branch details
bitbucket.py branch my-repo feature-x

# Create branch from main
bitbucket.py create-branch my-repo feature-y --from main

# Create branch from specific commit
bitbucket.py create-branch my-repo hotfix-1 --from abc123def

# Delete a branch (cannot delete main branch)
bitbucket.py delete-branch my-repo old-feature
```

### Commit History

```bash
# List recent commits (default branch)
bitbucket.py commits my-repo

# Commits on specific branch
bitbucket.py commits my-repo --branch feature-x

# Limit results
bitbucket.py commits my-repo --pagelen 10

# View specific commit
bitbucket.py commit my-repo abc123def456
```

### Pipeline Status

```bash
# List recent pipelines
bitbucket.py pipelines my-repo

# Filter by status
bitbucket.py pipelines my-repo --status SUCCESSFUL
bitbucket.py pipelines my-repo --status FAILED

# View pipeline details
bitbucket.py pipeline my-repo '{pipeline-uuid}'

# View pipeline steps
bitbucket.py pipeline-steps my-repo '{pipeline-uuid}'

# Trigger a pipeline
bitbucket.py run-pipeline my-repo --branch main
```

### Workspace and User Info

```bash
# List accessible workspaces
bitbucket.py workspaces

# List workspace members
bitbucket.py members

# Get current user info
bitbucket.py me
```

## Merge Strategies

When merging PRs, available strategies are:

| Strategy | Description |
|----------|-------------|
| `merge_commit` | Create a merge commit (default) |
| `squash` | Squash all commits into one |
| `fast_forward` | Fast-forward if possible |

## Pipeline States

| State | Description |
|-------|-------------|
| `PENDING` | Waiting to start |
| `IN_PROGRESS` | Currently running |
| `SUCCESSFUL` | Completed successfully |
| `FAILED` | Completed with failures |
| `STOPPED` | Manually stopped |

## Error Handling

Common errors:
- **401 Unauthorized**: Check BITBUCKET_USERNAME and BITBUCKET_APP_PASSWORD
- **403 Forbidden**: App password lacks required permissions
- **404 Not Found**: Repository, PR, or branch doesn't exist
- **400 Bad Request**: Invalid parameters or branch name

## Raw API Access

For operations not covered by the script:

```bash
# GET request
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE/my-repo" | jq .

# POST request
curl -s -X POST -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"content": {"raw": "Comment text"}}' \
  "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE/my-repo/pullrequests/42/comments" | jq .
```

API docs: https://developer.atlassian.com/cloud/bitbucket/rest/

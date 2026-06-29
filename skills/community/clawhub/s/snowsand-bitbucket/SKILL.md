---
name: snowsand-bitbucket
version: 1.0.1
description: Interact with Bitbucket Cloud via REST API. Use for repository management, pull request operations (list, view, create, comment, approve, merge), branch management, commit history, pipeline status, and workspace/team queries. Triggers on Bitbucket operations, PR reviews, branch management, pipeline checks, or any Atlassian Bitbucket Cloud task.
---

# Bitbucket Cloud Integration

Bitbucket Cloud REST API v2 integration for repository management, pull requests, branches, commits, and pipelines.

## Authentication

Bitbucket Cloud REST v2 uses HTTP Basic auth. Required environment variables:

- `BITBUCKET_WORKSPACE` - Default workspace slug (e.g., `myteam`)
- `BITBUCKET_USERNAME` - Identity for Basic auth (see pairing below)
- `BITBUCKET_APP_PASSWORD` - Secret for Basic auth (see pairing below)

Two credential types work. Use the matching username for each:

| Credential type | `BITBUCKET_USERNAME` | `BITBUCKET_APP_PASSWORD` |
|---|---|---|
| **Atlassian API token** (recommended) | your Atlassian account **email** | the API token |
| **App Password** (legacy) | your Bitbucket **username** (not email) | the app password |

> Note: despite the variable name, `BITBUCKET_APP_PASSWORD` accepts an Atlassian API token. For SnowSand's `Atlassian - <user>@snowsand.com` vault items, the `bitbucket-token` field is an **Atlassian API token**, so pair it with the account **email** as the username.

Atlassian API tokens: https://id.atlassian.com/manage-profile/security/api-tokens
App Passwords (legacy): https://bitbucket.org/account/settings/app-passwords/

Required scopes/permissions:
- **Repositories**: Read, Write (for repo operations)
- **Pull requests**: Read, Write (for PR operations)
- **Pipelines**: Read (for pipeline status)
- **Account**: Read (for user info)

Test connection:
```bash
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/user" | jq .
```

> Cross-workspace listing note: Bitbucket **CHANGE-2770** removed the old
> `GET /2.0/workspaces` and `GET /2.0/user/permissions/workspaces` endpoints
> (they now return HTTP 410). `bitbucket.py workspaces` uses the supported
> replacement `GET /2.0/user/workspaces`. All other commands are
> workspace-scoped and unaffected.

## Quick Reference

All operations use the `{baseDir}/scripts/bitbucket.py` script:

| Operation | Command |
|-----------|---------|
| **Repositories** | |
| List repos | `{baseDir}/scripts/bitbucket.py repos` |
| View repo | `{baseDir}/scripts/bitbucket.py repo my-repo` |
| Create repo | `{baseDir}/scripts/bitbucket.py create-repo my-new-repo --private` |
| **Pull Requests** | |
| List PRs | `{baseDir}/scripts/bitbucket.py prs my-repo` |
| View PR | `{baseDir}/scripts/bitbucket.py pr my-repo 42` |
| Create PR | `{baseDir}/scripts/bitbucket.py create-pr my-repo --title "Feature" --source feature-branch` |
| Comment on PR | `{baseDir}/scripts/bitbucket.py pr-comment my-repo 42 "LGTM!"` |
| Approve PR | `{baseDir}/scripts/bitbucket.py approve my-repo 42` |
| Merge PR | `{baseDir}/scripts/bitbucket.py merge my-repo 42` |
| Decline PR | `{baseDir}/scripts/bitbucket.py decline my-repo 42` |
| **Branches** | |
| List branches | `{baseDir}/scripts/bitbucket.py branches my-repo` |
| View branch | `{baseDir}/scripts/bitbucket.py branch my-repo main` |
| Create branch | `{baseDir}/scripts/bitbucket.py create-branch my-repo feature-x --from main` |
| Delete branch | `{baseDir}/scripts/bitbucket.py delete-branch my-repo old-feature` |
| **Commits** | |
| List commits | `{baseDir}/scripts/bitbucket.py commits my-repo` |
| View commit | `{baseDir}/scripts/bitbucket.py commit my-repo abc123` |
| **Pipelines** | |
| List pipelines | `{baseDir}/scripts/bitbucket.py pipelines my-repo` |
| View pipeline | `{baseDir}/scripts/bitbucket.py pipeline my-repo {uuid}` |
| Pipeline steps | `{baseDir}/scripts/bitbucket.py pipeline-steps my-repo {uuid}` |
| **Workspace** | |
| List workspaces | `{baseDir}/scripts/bitbucket.py workspaces` |
| Workspace members | `{baseDir}/scripts/bitbucket.py members` |
| Current user | `{baseDir}/scripts/bitbucket.py me` |

## Common Workflows

### Repository Management

```bash
# List all repositories in workspace
{baseDir}/scripts/bitbucket.py repos

# List with pagination
{baseDir}/scripts/bitbucket.py repos --page 2 --pagelen 25

# View specific repository details
{baseDir}/scripts/bitbucket.py repo my-repo

# Create a new private repository
{baseDir}/scripts/bitbucket.py create-repo my-new-repo --private --description "Project description"

# Create public repository with specific project
{baseDir}/scripts/bitbucket.py create-repo my-public-repo --project PROJ
```

### Pull Request Workflow

```bash
# List open pull requests
{baseDir}/scripts/bitbucket.py prs my-repo

# List all PRs (including merged/declined)
{baseDir}/scripts/bitbucket.py prs my-repo --state all

# View PR details
{baseDir}/scripts/bitbucket.py pr my-repo 42

# Create a pull request
{baseDir}/scripts/bitbucket.py create-pr my-repo \
  --title "Add new feature" \
  --source feature-branch \
  --destination main \
  --description "This PR adds..."

# Add a comment
{baseDir}/scripts/bitbucket.py pr-comment my-repo 42 "Looks good, just one question..."

# Approve the PR
{baseDir}/scripts/bitbucket.py approve my-repo 42

# Unapprove (remove approval)
{baseDir}/scripts/bitbucket.py unapprove my-repo 42

# Request changes
{baseDir}/scripts/bitbucket.py request-changes my-repo 42

# Merge with default strategy
{baseDir}/scripts/bitbucket.py merge my-repo 42

# Merge with specific strategy
{baseDir}/scripts/bitbucket.py merge my-repo 42 --strategy squash

# Decline a PR
{baseDir}/scripts/bitbucket.py decline my-repo 42
```

### Branch Operations

```bash
# List all branches
{baseDir}/scripts/bitbucket.py branches my-repo

# View branch details
{baseDir}/scripts/bitbucket.py branch my-repo feature-x

# Create branch from main
{baseDir}/scripts/bitbucket.py create-branch my-repo feature-y --from main

# Create branch from specific commit
{baseDir}/scripts/bitbucket.py create-branch my-repo hotfix-1 --from abc123def

# Delete a branch (cannot delete main branch)
{baseDir}/scripts/bitbucket.py delete-branch my-repo old-feature
```

### Commit History

```bash
# List recent commits (default branch)
{baseDir}/scripts/bitbucket.py commits my-repo

# Commits on specific branch
{baseDir}/scripts/bitbucket.py commits my-repo --branch feature-x

# Limit results
{baseDir}/scripts/bitbucket.py commits my-repo --pagelen 10

# View specific commit
{baseDir}/scripts/bitbucket.py commit my-repo abc123def456
```

### Pipeline Status

```bash
# List recent pipelines
{baseDir}/scripts/bitbucket.py pipelines my-repo

# Filter by status
{baseDir}/scripts/bitbucket.py pipelines my-repo --status SUCCESSFUL
{baseDir}/scripts/bitbucket.py pipelines my-repo --status FAILED

# View pipeline details
{baseDir}/scripts/bitbucket.py pipeline my-repo '{pipeline-uuid}'

# View pipeline steps
{baseDir}/scripts/bitbucket.py pipeline-steps my-repo '{pipeline-uuid}'

# Trigger a pipeline
{baseDir}/scripts/bitbucket.py run-pipeline my-repo --branch main
```

### Workspace and User Info

```bash
# List accessible workspaces
{baseDir}/scripts/bitbucket.py workspaces

# List workspace members
{baseDir}/scripts/bitbucket.py members

# Get current user info
{baseDir}/scripts/bitbucket.py me
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

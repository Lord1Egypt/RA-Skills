# Bitbucket Cloud API Reference

## Authentication

### App Passwords

App passwords are the recommended authentication method for scripts and tools.

Create at: https://bitbucket.org/account/settings/app-passwords/

Required permissions by operation:

| Operation | Permission |
|-----------|------------|
| Read repositories | Repositories: Read |
| Create/update repos | Repositories: Write |
| Read pull requests | Pull requests: Read |
| Create/merge PRs | Pull requests: Write |
| Read pipelines | Pipelines: Read |
| Trigger pipelines | Pipelines: Write |
| Read user info | Account: Read |

### Basic Auth Header

```
Authorization: Basic <base64(username:app_password)>
```

## API Base URL

```
https://api.bitbucket.org/2.0
```

## Pagination

Bitbucket uses cursor-based pagination:

```json
{
  "size": 142,
  "page": 1,
  "pagelen": 25,
  "next": "https://api.bitbucket.org/2.0/repositories/...?page=2",
  "previous": null,
  "values": [...]
}
```

Parameters:
- `pagelen` - Results per page (max 100)
- `page` - Page number

## Filtering & Sorting

### Query Parameters

- `q` - Filter expression
- `sort` - Sort field (prefix with `-` for descending)

### Filter Examples

```bash
# Branches containing "feature"
q=name ~ "feature"

# PRs by author
q=author.uuid = "{user-uuid}"

# PRs updated after date
q=updated_on > 2024-01-01
```

### Sort Examples

```bash
# Branches by name descending
sort=-name

# Commits by date
sort=-date
```

## Common Endpoints

### Repositories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repositories/{workspace}` | List repos in workspace |
| GET | `/repositories/{workspace}/{repo_slug}` | Get repo |
| POST | `/repositories/{workspace}/{repo_slug}` | Create repo |
| PUT | `/repositories/{workspace}/{repo_slug}` | Update repo |
| DELETE | `/repositories/{workspace}/{repo_slug}` | Delete repo |

### Pull Requests

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repositories/{workspace}/{repo}/pullrequests` | List PRs |
| POST | `/repositories/{workspace}/{repo}/pullrequests` | Create PR |
| GET | `/repositories/{workspace}/{repo}/pullrequests/{id}` | Get PR |
| PUT | `/repositories/{workspace}/{repo}/pullrequests/{id}` | Update PR |
| POST | `/repositories/{workspace}/{repo}/pullrequests/{id}/approve` | Approve |
| DELETE | `/repositories/{workspace}/{repo}/pullrequests/{id}/approve` | Unapprove |
| POST | `/repositories/{workspace}/{repo}/pullrequests/{id}/request-changes` | Request changes |
| POST | `/repositories/{workspace}/{repo}/pullrequests/{id}/merge` | Merge |
| POST | `/repositories/{workspace}/{repo}/pullrequests/{id}/decline` | Decline |
| GET | `/repositories/{workspace}/{repo}/pullrequests/{id}/comments` | List comments |
| POST | `/repositories/{workspace}/{repo}/pullrequests/{id}/comments` | Add comment |

### Branches

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repositories/{workspace}/{repo}/refs/branches` | List branches |
| POST | `/repositories/{workspace}/{repo}/refs/branches` | Create branch |
| GET | `/repositories/{workspace}/{repo}/refs/branches/{name}` | Get branch |
| DELETE | `/repositories/{workspace}/{repo}/refs/branches/{name}` | Delete branch |

### Commits

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repositories/{workspace}/{repo}/commits` | List commits |
| GET | `/repositories/{workspace}/{repo}/commits/{revision}` | Commits for ref |
| GET | `/repositories/{workspace}/{repo}/commit/{hash}` | Get commit |
| GET | `/repositories/{workspace}/{repo}/diff/{spec}` | Compare commits |

### Pipelines

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repositories/{workspace}/{repo}/pipelines` | List pipelines |
| POST | `/repositories/{workspace}/{repo}/pipelines` | Trigger pipeline |
| GET | `/repositories/{workspace}/{repo}/pipelines/{uuid}` | Get pipeline |
| GET | `/repositories/{workspace}/{repo}/pipelines/{uuid}/steps` | List steps |
| POST | `/repositories/{workspace}/{repo}/pipelines/{uuid}/stopPipeline` | Stop pipeline |

### Workspaces

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces` | List workspaces |
| GET | `/workspaces/{workspace}` | Get workspace |
| GET | `/workspaces/{workspace}/members` | List members |
| GET | `/workspaces/{workspace}/permissions` | List permissions |
| GET | `/workspaces/{workspace}/projects` | List projects |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user` | Get current user |
| GET | `/users/{uuid}` | Get user by UUID |

## Request/Response Formats

### Create Pull Request

```json
{
  "title": "Feature: Add login",
  "source": {
    "branch": {"name": "feature/login"}
  },
  "destination": {
    "branch": {"name": "main"}
  },
  "description": "Adds login functionality",
  "close_source_branch": true,
  "reviewers": [
    {"uuid": "{user-uuid}"}
  ]
}
```

### Merge Pull Request

```json
{
  "merge_strategy": "squash",
  "message": "Merge feature/login into main",
  "close_source_branch": true
}
```

Merge strategies:
- `merge_commit` - Create merge commit
- `squash` - Squash and merge
- `fast_forward` - Fast-forward if possible

### Create Branch

```json
{
  "name": "feature/new-feature",
  "target": {
    "hash": "main"
  }
}
```

Note: `target.hash` can be a branch name, tag, or commit hash.

### Trigger Pipeline

```json
{
  "target": {
    "type": "pipeline_ref_target",
    "ref_type": "branch",
    "ref_name": "main",
    "selector": {
      "type": "custom",
      "pattern": "deploy-to-staging"
    }
  }
}
```

### PR Comment

```json
{
  "content": {
    "raw": "Comment text with **markdown** support"
  }
}
```

For inline comments:

```json
{
  "content": {"raw": "Inline comment"},
  "inline": {
    "path": "src/file.py",
    "from": null,
    "to": 42
  }
}
```

## Error Responses

```json
{
  "type": "error",
  "error": {
    "message": "Repository not found",
    "detail": "The repository 'workspace/repo' does not exist."
  }
}
```

Common HTTP status codes:
- `400` - Bad request (invalid parameters)
- `401` - Unauthorized (invalid credentials)
- `403` - Forbidden (insufficient permissions)
- `404` - Not found
- `409` - Conflict (e.g., branch already exists)
- `429` - Rate limited

## Rate Limiting

Bitbucket Cloud has rate limits. When exceeded:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

## Webhooks

Configure webhooks via:
- UI: Repository Settings → Webhooks
- API: `POST /repositories/{workspace}/{repo}/hooks`

Webhook payload includes:
- `push` - Code pushes
- `pullrequest:*` - PR events
- `repo:*` - Repository events
- `pipeline:*` - Pipeline events

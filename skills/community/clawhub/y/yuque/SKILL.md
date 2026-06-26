---
name: yuque
description: Manage Yuque (语雀) knowledge base documents and repositories. Use when users need to interact with Yuque for document operations including reading documents, listing repositories, searching content, creating documents, and managing knowledge bases. Supports both personal and team spaces.
---

# Yuque Skill

Interact with Yuque (语雀) knowledge base platform via the Yuque Open API.

## Prerequisites

- Yuque API Token (stored in environment variable `YUQUE_TOKEN`)
- Base URL: `https://www.yuque.com/api/v2`

## Authentication

All API requests require an `X-Auth-Token` header with your Yuque token.

## Core Workflows

### 1. Get User Info

```bash
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" https://www.yuque.com/api/v2/user
```

### 2. List User Repositories

```bash
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" https://www.yuque.com/api/v2/users/<login>/repos
```

### 3. List Repository Documents

```bash
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" https://www.yuque.com/api/v2/repos/<namespace>/docs
```

### 4. Get Document Detail

```bash
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" https://www.yuque.com/api/v2/repos/<namespace>/docs/<slug>
```

### 5. Get Document Content (HTML/Markdown)

```bash
# Get HTML content
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" https://www.yuque.com/api/v2/repos/<namespace>/docs/<slug>?raw=1

# Get Markdown content
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" https://www.yuque.com/api/v2/repos/<namespace>/docs/<slug>?raw=1 | python scripts/parse_yuque.py --format md
```

### 6. Create Document

```bash
curl -s -X POST \
  -H "X-Auth-Token: $YUQUE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Document Title", "body": "Document content in Markdown"}' \
  https://www.yuque.com/api/v2/repos/<namespace>/docs
```

### 7. Update Document

```bash
curl -s -X PUT \
  -H "X-Auth-Token: $YUQUE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "body": "Updated content"}' \
  https://www.yuque.com/api/v2/repos/<namespace>/docs/<id>
```

### 8. Search Documents

Yuque API doesn't have a direct search endpoint. Use list + filter approach:

```bash
# List all docs in a repo and filter by title
python scripts/search_yuque.py --namespace <namespace> --query "keyword"
```

## Common Namespace Formats

- Personal repo: `username/repo-slug`
- Team repo: `teamname/repo-slug`

## Response Format

All API responses are JSON with this structure:

```json
{
  "data": { ... },
  "meta": { ... }
}
```

## Error Handling

Common HTTP status codes:
- `401`: Unauthorized (check token)
- `403`: Forbidden (no permission)
- `404`: Resource not found
- `429`: Rate limited (wait and retry)

## Helper Scripts

Use the provided Python scripts for common operations:

- `scripts/yuque_cli.py` - Full CLI for Yuque operations
- `scripts/parse_yuque.py` - Parse Yuque HTML to Markdown
- `scripts/search_yuque.py` - Search documents in repositories

## References

- API Documentation: See [references/api.md](references/api.md)
- Common Operations: See [references/examples.md](references/examples.md)

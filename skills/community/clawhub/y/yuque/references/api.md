# Yuque API Reference

## Base URL

```
https://www.yuque.com/api/v2
```

## Authentication

All requests require the `X-Auth-Token` header:

```
X-Auth-Token: YOUR_TOKEN_HERE
```

## Endpoints

### User

#### Get Current User

```
GET /user
```

Response:
```json
{
  "data": {
    "id": 123,
    "type": "User",
    "login": "username",
    "name": "User Name",
    "description": "Bio",
    "avatar_url": "https://...",
    "created_at": "2020-01-01T00:00:00.000Z",
    "updated_at": "2020-01-01T00:00:00.000Z"
  }
}
```

### Repositories

#### List User Repositories

```
GET /users/:login/repos
```

#### List Group Repositories

```
GET /groups/:login/repos
```

#### Get Repository

```
GET /repos/:namespace
```

Namespace format: `user/repo-slug` or `group/repo-slug`

Response:
```json
{
  "data": {
    "id": 123,
    "type": "Book",
    "slug": "repo-slug",
    "name": "Repository Name",
    "namespace": "user/repo-slug",
    "user_id": 123,
    "description": "Description",
    "public": 1,
    "created_at": "2020-01-01T00:00:00.000Z",
    "updated_at": "2020-01-01T00:00:00.000Z"
  }
}
```

### Documents

#### List Documents

```
GET /repos/:namespace/docs
```

Query parameters:
- `offset`: Pagination offset
- `limit`: Number of items per page (max 100)

Response:
```json
{
  "data": [
    {
      "id": 123,
      "type": "Doc",
      "slug": "doc-slug",
      "title": "Document Title",
      "description": "Description",
      "user_id": 123,
      "book_id": 456,
      "format": "markdown",
      "public": 1,
      "status": 1,
      "read_count": 100,
      "likes_count": 10,
      "comments_count": 5,
      "created_at": "2020-01-01T00:00:00.000Z",
      "updated_at": "2020-01-01T00:00:00.000Z"
    }
  ],
  "meta": {
    "total": 100
  }
}
```

#### Get Document

```
GET /repos/:namespace/docs/:slug
```

Query parameters:
- `raw=1`: Return raw content in body field

Response:
```json
{
  "data": {
    "id": 123,
    "type": "Doc",
    "slug": "doc-slug",
    "title": "Document Title",
    "description": "Description",
    "user_id": 123,
    "book_id": 456,
    "format": "markdown",
    "body": "# Markdown Content",
    "body_html": "<h1>HTML Content</h1>",
    "public": 1,
    "status": 1,
    "read_count": 100,
    "likes_count": 10,
    "comments_count": 5,
    "created_at": "2020-01-01T00:00:00.000Z",
    "updated_at": "2020-01-01T00:00:00.000Z"
  }
}
```

#### Create Document

```
POST /repos/:namespace/docs
```

Request body:
```json
{
  "title": "Document Title",
  "body": "# Markdown Content",
  "format": "markdown",
  "public": 1
}
```

#### Update Document

```
PUT /repos/:namespace/docs/:id
```

Request body:
```json
{
  "title": "New Title",
  "body": "# Updated Content",
  "public": 1
}
```

#### Delete Document

```
DELETE /repos/:namespace/docs/:id
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized - Invalid token |
| 403 | Forbidden - No permission |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Internal Server Error |

## Rate Limiting

Yuque API has rate limiting. If you receive a 429 status code, wait before retrying.

## Data Types

### Document Status

- `0`: Draft
- `1`: Published

### Public Status

- `0`: Private
- `1`: Public

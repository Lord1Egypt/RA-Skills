# W-Spaces Public API v1

Base URL: `https://api.wspaces.app`

## Authentication

All protected endpoints accept:
- `X-API-Key: wsk_live_xxxx...` header
- `Authorization: Bearer wsk_live_xxxx...` header

## Rate Limits

- Auth endpoints: 10 requests/minute
- All other endpoints: 60 requests/minute

---

## Auth

### POST /api/v1/auth/register
Register a new account. Sends verification email.

**Body:**
```json
{ "email": "string", "password": "string (min 8 chars)", "name": "string" }
```

**Response 200:**
```json
{ "message": "Registration successful. Please check your email to verify your account.", "email": "string" }
```

### POST /api/v1/auth/login
Login and receive an API key. Requires verified email.

**Body:**
```json
{ "email": "string", "password": "string" }
```

**Response 200:**
```json
{
  "apiKey": "wsk_live_xxxx...",
  "user": { "id": "guid", "email": "string", "name": "string", "creditsBalance": 10 }
}
```

### POST /api/v1/auth/api-keys
Create an additional API key. **Requires auth.**

**Body:**
```json
{ "name": "string" }
```

**Response 200:**
```json
{ "id": "guid", "name": "string", "prefix": "wsk_live_xxxx", "rawKey": "wsk_live_full_key...", "createdAt": "datetime" }
```

### GET /api/v1/auth/api-keys
List all API keys. **Requires auth.**

**Response 200:**
```json
[{ "id": "guid", "name": "string", "prefix": "wsk_live_xxxx", "createdAt": "datetime", "lastUsedAt": "datetime|null", "isRevoked": false }]
```

### DELETE /api/v1/auth/api-keys/{id}
Revoke an API key. **Requires auth.**

**Response 204** No Content

---

## Me

### GET /api/v1/me
Get current user profile. **Requires auth.**

**Response 200:**
```json
{ "id": "guid", "email": "string", "name": "string", "avatarUrl": "string|null", "creditsBalance": 10, "roles": [] }
```

---

## Projects

### POST /api/v1/projects
Create a new project. **Requires auth.**

**Body:**
```json
{ "name": "string", "category": "string|null", "style": "string|null", "description": "string|null" }
```

**Response 201:**
```json
{ "id": "guid", "name": "string", "slug": "string", "status": "Draft", "createdAt": "datetime", ... }
```

### GET /api/v1/projects
List all projects. **Requires auth.**

### GET /api/v1/projects/{id}
Get project details. **Requires auth.**

### PUT /api/v1/projects/{id}/code
Push HTML code to a project. Creates a new version. **Requires auth.**

**Body:**
```json
{ "html": "<html>...</html>" }
```

**Response 200:**
```json
{ "id": "guid", "versionNumber": 1, "htmlContent": "...", "source": "Api", "createdAt": "datetime" }
```

### POST /api/v1/projects/{id}/deploy
Deploy the current version to a live URL. **Requires auth.**

**Response 200:**
```json
{ "id": "guid", "projectId": "guid", "versionId": "guid", "status": "Active", "url": "https://slug.wspaces.app", "deployedAt": "datetime" }
```

### GET /api/v1/projects/{id}/deployments
List deployment history. **Requires auth.**

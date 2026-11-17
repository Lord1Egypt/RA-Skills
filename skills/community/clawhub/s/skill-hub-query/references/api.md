# Skill Hub API Reference (for `skill-hub-query`)

This document describes the API contract that `skill-hub-query` expects from a
**compatible Skill Hub**. It applies to:

- [clawhub.ai](https://clawhub.ai) — the public reference Hub (default)
- Any **self-hosted** Hub implementing the contract below

If you operate a self-hosted Hub, implement these endpoints (or a superset) to
plug in seamlessly.

---

## 0. Conventions

### 0.1 Base URL

Configurable via `SKILL_HUB_URL` (default: `https://clawhub.ai`).

### 0.2 Two API path families

The scripts speak two parallel path conventions so the same code can talk to
both authenticated OpenAPI-style Hubs and unauthenticated legacy front-end
Hubs.

| Path family | Default prefix | Override env var | Auth | Purpose |
|---|---|---|---|---|
| Primary (OpenAPI) | `/api/v1/skill` | `SKILL_HUB_API_PREFIX` | Required (token) | Full features, private skills, version history |
| Fallback (Legacy) | `/api/skill` | `SKILL_HUB_LEGACY_API_PREFIX` | None | Public skills, install / download |

`api_get` in `_lib.sh` auto-maps an OpenAPI path to its legacy equivalent when
no token is configured, by string-replacing `<API_PREFIX>` with
`<LEGACY_API_PREFIX>` and (where the Hub uses it) rewriting `?page=` to
`?current=`.

### 0.3 Authentication

When a token is configured the scripts send:

```
<SKILL_HUB_AUTH_HEADER>: <SKILL_HUB_AUTH_SCHEME><token>
```

Defaults:

- `SKILL_HUB_AUTH_HEADER` = `Authorization`
- `SKILL_HUB_AUTH_SCHEME` = `Bearer ` (note the trailing space)

For Hubs using a different scheme, set both env vars accordingly. For example
an API-key style header:

```bash
export SKILL_HUB_AUTH_HEADER="X-API-Key"
export SKILL_HUB_AUTH_SCHEME=""
```

### 0.4 Response envelope

All JSON endpoints respond with:

```json
{
  "code": 200,
  "message": "",
  "data": { /* payload */ }
}
```

On business errors, `code != 200` and `message` is human-readable. Some Hubs
also include `"success": false`; the scripts treat that as failure too.

The `download` endpoint returns raw ZIP bytes on success, or a JSON error body
masquerading with HTTP 200 + `Content-Type` mismatch — `_lib.sh` detects this
case and reports clearly.

---

## 1. Required endpoints (read-only)

### 1.1 Search

```
GET <base><SKILL_HUB_API_PREFIX>/search
        ?page=<int>            (default 1)
        &size=<int>            (default 100; max recommended 200)
        &keyword=<str>         optional
        &author=<str>          optional
        &source=<str>          optional (official|personal|external)
        &orderBy=updatedAt     recommended
        &order=desc
```

Response payload:

```json
{
  "data": {
    "records": [
      {
        "slug": "calendar",
        "displayName": "Calendar",
        "summary": "...",
        "owner": {
          "displayName": "Alice",
          "handle": "alice",
          "email": "alice@example.com"
        },
        "source": "official",
        "updatedAt": 1748000000000,
        "latestVersion": { "version": "1.2.3" },
        "tags": ["productivity"],
        "scene": ["office"],
        "applicablePosition": ["common"],
        "businessDomain": [],
        "business": [],
        "platform": []
      }
    ],
    "total": 1234
  }
}
```

Minimum required fields per record: `slug`, `displayName`, `summary`, `owner`,
`updatedAt`, `latestVersion.version`. Other fields are optional but used by
filtering in `query.sh combo`.

### 1.2 Version history

```
GET <base><SKILL_HUB_API_PREFIX>/versions/<slug>?limit=<int>
```

Response payload:

```json
{
  "data": {
    "items": [
      {
        "version": "1.2.3",
        "createdAt": 1748000000000,
        "changelog": "..."
      }
    ]
  }
}
```

### 1.3 Single version detail

```
GET <base><SKILL_HUB_API_PREFIX>/versions/<slug>/<version>
```

Response payload:

```json
{
  "data": {
    "version": {
      "version": "1.2.3",
      "changelog": "...",
      "publishedAt": 1748000000000,
      "publisher": "alice@example.com",
      "files": [ /* optional */ ]
    }
  }
}
```

### 1.4 Download (ZIP)

```
GET <base><SKILL_HUB_LEGACY_API_PREFIX>/download/<slug>
        ?version=<version>     optional; defaults to latest
        &track=true             optional; lets Hubs log download counts
```

Response: binary ZIP bytes. The ZIP MUST contain `SKILL.md` at the top level
(or wrapped in a single subdirectory; install.sh sinks into that subdirectory
automatically).

For private skills the Hub must enforce auth and return 403 + a JSON error
body when the caller lacks permission.

---

## 2. Optional endpoints (for `edit.sh`)

These power `edit.sh`. If your Hub does NOT implement them, instruct users to
set `export SKILL_HUB_DISABLE_EDIT=1` so the tool refuses to run instead of
producing confusing errors.

The path prefix is `SKILL_HUB_EDIT_PREFIX`, which defaults to
`SKILL_HUB_LEGACY_API_PREFIX`. Override if your Hub mounts edit/detail under a
different path.

### 2.1 PUT edit (also doubles as GET-current-snapshot)

```
PUT <base><SKILL_HUB_EDIT_PREFIX>/edit/<slug>
Content-Type: application/json
Authorization: <scheme><token>

Body: JSON patch (any subset of editable fields)
```

Behavior:

- **Empty body** (`{}`): returns the current full state (used as the
  source-of-truth read channel). Equivalent to GET semantically.
- **Non-empty body**: applies the patch. Server MUST enforce ownership;
  non-owner callers MUST receive 403.
- Server MUST NOT accept `null` for the editable fields below; pass `""` or
  `[]` to mean "empty".

Editable fields (server contract; types must match):

| Field | Type |
|---|---|
| `displayName` | string |
| `summary` | string |
| `videoAttachmentUrl` | string |
| `businessCategory` | string |
| `visibility` | enum: `"public"` \| `"private"` |
| `applicablePosition` | array of strings |
| `businessDomain` | array of strings |
| `business` | array of strings |
| `scene` | array of strings |
| `platform` | array of strings |
| `tags` | array of strings |

Response:

```json
{
  "data": {
    "slug": "...",
    "displayName": "...",
    "summary": "...",
    "ownerEmail": "alice@example.com",
    "visibility": "public",
    "videoAttachmentUrl": "",
    "businessCategory": "",
    "applicablePosition": [],
    "businessDomain": [],
    "business": [],
    "scene": [],
    "platform": [],
    "tags": []
  }
}
```

The `ownerEmail` field is what `_edit_lib.sh` uses for the client-side owner
pre-check (matched against `git config user.email` or `SKILL_HUB_OWNER_EMAIL`).

### 2.2 GET detail (cross-check channel)

```
GET <base><SKILL_HUB_EDIT_PREFIX>/detail/<slug>
```

Response:

```json
{
  "data": {
    "skill": {
      /* same shape as the PUT-empty-body response */
    }
  }
}
```

Used as an independent verification channel after a successful PUT edit. If
the two channels disagree on the requested fields after retry, the edit is
considered failed and rolled back from backup.

---

## 3. Error codes the scripts recognize

| HTTP / Code | Where | Treatment |
|---|---|---|
| 401 | any endpoint | Token invalid/expired; suggest refresh |
| 403 | search/download/edit | Private skill or non-owner; instruct accordingly |
| 404 | download/edit | Wrong slug or removed; suggest sync + re-check |
| 200 + `code != 200` | any JSON endpoint | Business error; report `message` |
| 200 + `success == false` | legacy endpoints | Same as above |
| 200 + JSON body on `download` | download | Hub masqueraded an error as ZIP; parse and report |

---

## 5. Optional endpoints (for `team.sh`)

These power `team.sh` (team member management: search / my teams / detail /
member list / add / remove). If your Hub does NOT implement them, instruct
users to set `export SKILL_HUB_DISABLE_TEAM=1` so the tool refuses to run
instead of producing confusing errors (same convention as `edit.sh`).

The path prefix defaults to `/api/team` via `SKILL_HUB_TEAM_PREFIX`; team
endpoints sit under `<base><SKILL_HUB_TEAM_PREFIX>/...`. Override the variable
if your Hub mounts them elsewhere.

### 5.1 Team search / my teams / detail

```
GET <base><SKILL_HUB_TEAM_PREFIX>/search?keyword=&size=
GET <base><SKILL_HUB_TEAM_PREFIX>/my?current=&size=
GET <base><SKILL_HUB_TEAM_PREFIX>/{teamId}
```

Envelope: `{"code":200, "data":{"records":[...], "total":N}}` for the list
endpoints; `{"code":200, "data":{...team object...}}` for detail. The team
object carries `id`, `teamName`, `teamDescription`, `memberCount`,
`skillCount`, and (optional) `myRole`.

### 5.2 Member list (paginated)

```
GET <base><SKILL_HUB_TEAM_PREFIX>/{teamId}/members?current=&size=
```

**The pagination parameter is `current=`, not `page=`** — a Hub that silently
ignores `page=` and always returns the first page will make full pagination
loop forever on page 1 (the client caps at 200 pages and aborts).

Member record shape:

```json
{
  "user": {"email": "alice@example.com", "displayName": "Alice",
            "handle": "alice", "avatar": null},
  "role": "member",
  "grantedBy": {"email": "owner@example.com", "displayName": "Owner"},
  "createdAt": "2026-01-01T00:00:00Z"
}
```

### 5.3 Add / remove members

```
POST   <base><SKILL_HUB_TEAM_PREFIX>/{teamId}/members/add
       body {"members":[{"userEmail":"a@x.com","role":"member"}]}
DELETE <base><SKILL_HUB_TEAM_PREFIX>/{teamId}/members/remove
       body {"userEmails":["a@x.com"]}
```

**Server contract requirements (all field-tested; the client already
defends against each):**

- `add` MUST expect that the client validates email format — the reference
  implementation accepts arbitrary strings and writes a *dangling record*
  (`user.handle == userEmail`, no avatar). The client therefore **re-verifies
  every add against the member list** and flags dangling records.
- `add` is idempotent-success for existing members; the client de-duplicates
  first so roles are never silently changed.
- `remove` is silent-success for unknown emails; the client re-verifies.
- Valid roles: `member` / `admin` / `viewer` (others → business code 400).
- Team-not-found is reported as **HTTP 200 + `code=400`** (fake-200, same
  family as the download endpoint) — always check the business envelope.

---

## 4. Implementing a self-hosted Hub

A minimal compatible Hub needs:

1. Read endpoints from §1 (search, versions list, version detail, download)
2. A static skill storage backend (filesystem, S3, …) for the ZIPs
3. Token auth for `<SKILL_HUB_API_PREFIX>/*`
4. Optional: ownership tracking + endpoints from §2 for `edit.sh`
5. Optional: team endpoints from §5 for `team.sh`

You can serve this as a thin FastAPI / Express / Spring Boot wrapper around an
object store. The contract is intentionally small.

For a reference implementation, study the way `_lib.sh` calls `api_get` and
`api_download` and what shape it expects in return.

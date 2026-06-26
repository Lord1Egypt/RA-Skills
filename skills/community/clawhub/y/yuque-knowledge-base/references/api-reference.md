# Yuque OpenAPI v2 Reference

Base URL: `https://www.yuque.com`
Auth: Header `X-Auth-Token: <token>`

## Endpoints

### User

#### GET /api/v2/user
Get current token user info.

Response `data`:
| Field | Type | Description |
|-------|------|-------------|
| id | int | User ID |
| login | string | Login name |
| name | string | Display name |
| avatar_url | string | Avatar URL |
| books_count | int | Number of repos |
| description | string | Bio |

---

### Search

#### GET /api/v2/search
Full-text search for documents or repos.

Query params:
| Param | Required | Description |
|-------|----------|-------------|
| q | Yes | Search keyword |
| type | Yes | `doc` or `repo` |
| scope | No | Search scope (e.g. `group_login/book_slug`) |
| page | No | Page number |
| creatorId | No | Filter by creator ID |
| creator | No | Filter by creator login |

Response `data[]` (V2SearchResult):
| Field | Type | Description |
|-------|------|-------------|
| id | int | ID |
| type | string | `doc` or `repo` |
| title | string | Title (with `<em>` highlights) |
| summary | string | Summary excerpt |
| url | string | Access path |
| info | string | Attribution info |
| target | object | Full doc or repo object |

---

### Documents

#### GET /api/v2/repos/{book_id}/docs
List documents in a repo.

Query params: `offset` (int), `limit` (int), `optional_properties` (string)

Response `data[]` (V2Doc):
| Field | Type | Description |
|-------|------|-------------|
| id | int | Document ID |
| type | string | `Doc`, `Sheet`, `Thread`, `Board`, `Table` |
| slug | string | Path |
| title | string | Title |
| description | string | Summary |
| book_id | int | Parent repo ID |
| public | int | 0=private, 1=public, 2=org-public |
| status | string | 0=draft, 1=published |
| word_count | int | Word count |
| created_at | datetime | Created time |
| updated_at | datetime | Updated time |

#### GET /api/v2/repos/{book_id}/docs/{id}
Get document detail with full body.

Response `data` (V2DocDetail) — includes all V2Doc fields plus:
| Field | Type | Description |
|-------|------|-------------|
| format | string | `markdown`, `lake`, `html`, `lakesheet` |
| body | string | Raw body content |
| body_html | string | HTML body |
| body_lake | string | Lake format body |
| body_draft | string | Draft content |
| body_sheet | string | Sheet content (for Sheet type) |
| body_table | string | Table content (for Table type) |

#### POST /api/v2/repos/{book_id}/docs
Create a document.

Request body:
| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| body | Yes | - | Document content |
| title | No | "无标题" | Title |
| slug | No | auto | Path |
| format | No | "markdown" | `markdown`, `html`, `lake` |
| public | No | inherit | 0=private, 1=public, 2=org-public |

#### PUT /api/v2/repos/{book_id}/docs/{id}
Update a document. Same fields as create, all optional.

#### DELETE /api/v2/repos/{book_id}/docs/{id}
Delete a document.

---

### Repositories (Knowledge Bases)

#### GET /api/v2/users/{login}/repos
#### GET /api/v2/groups/{login}/repos
List repos for a user or group.

Query params: `offset`, `limit`, `type` (`Book`/`Design`/`Sheet`/`Resource`), `filterByAbility`

Response `data[]` (V2Book):
| Field | Type | Description |
|-------|------|-------------|
| id | int | Repo ID |
| type | string | `Book`, `Design`, `Sheet`, `Resource` |
| slug | string | Path |
| name | string | Name |
| description | string | Description |
| public | int | 0=private, 1=public, 2=org-public |
| items_count | int | Document count |
| namespace | string | Full path (e.g. `user/repo`) |
| created_at | datetime | Created time |

#### POST /api/v2/users/{login}/repos
#### POST /api/v2/groups/{login}/repos
Create a repo.

Request body:
| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Repository name |
| slug | Yes | Repository path |
| description | No | Description |
| public | No | 0=private (default), 1=public, 2=org-public |

#### GET /api/v2/repos/{book_id}
Get repo detail. Response `data` is V2BookDetail (includes `toc_yml`).

#### PUT /api/v2/repos/{book_id}
Update repo. Fields: `name`, `slug`, `description`, `public`, `toc` (markdown format).

#### DELETE /api/v2/repos/{book_id}
Delete a repo.

---

### Table of Contents

#### GET /api/v2/repos/{book_id}/toc
Get TOC tree.

Response `data[]` (V2TocItem):
| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Node unique ID |
| type | string | `DOC`, `LINK`, `TITLE` |
| title | string | Node name |
| url | string | Node URL |
| doc_id | int | Document ID |
| level | int | Nesting level |
| visible | int | 0=hidden, 1=visible |
| parent_uuid | string | Parent node UUID |
| child_uuid | string | First child UUID |
| sibling_uuid | string | Next sibling UUID |
| prev_uuid | string | Previous sibling UUID |

#### PUT /api/v2/repos/{book_id}/toc
Update TOC.

Request body:
| Field | Required | Description |
|-------|----------|-------------|
| action | Yes | `appendNode`, `prependNode`, `editNode`, `removeNode` |
| action_mode | Yes | `sibling` or `child` |
| target_uuid | No | Target node UUID (default: root) |
| node_uuid | No | Node UUID (for edit/remove/move) |
| doc_ids | No | Array of doc IDs (for append/prepend) |
| type | No | `DOC`, `LINK`, `TITLE` (default: DOC) |
| title | No | Node name (for TITLE/LINK or editNode) |
| url | No | URL (for LINK type) |
| visible | No | 0=hidden, 1=visible |

Notes:
- `prependNode` does NOT support `action_mode=sibling` for creation
- `removeNode` with `action_mode=sibling` removes current node only
- `removeNode` with `action_mode=child` removes node and all children
- Removing a node does NOT delete the associated document

---

### Document Versions

#### GET /api/v2/doc_versions?doc_id={id}
List versions of a document.

Response `data[]` (V2DocVersion):
| Field | Type | Description |
|-------|------|-------------|
| id | int | Version ID |
| doc_id | int | Document ID |
| slug | string | Document path |
| title | string | Document title |
| user_id | int | Publisher ID |
| created_at | datetime | Created time |

#### GET /api/v2/doc_versions/{id}
Get version detail with body and diff.

Response `data` (V2DocVersionDetail) — includes V2DocVersion fields plus:
| Field | Type | Description |
|-------|------|-------------|
| format | string | Content format |
| body | string | Raw body |
| body_html | string | HTML body |
| body_asl | string | Lake format body |
| diff | string | Version diff |

---

### Namespace Path Alternatives

Most doc/repo endpoints support namespace paths as alternatives to numeric IDs:

- `/api/v2/repos/{group_login}/{book_slug}/docs` — equivalent to `/api/v2/repos/{book_id}/docs`
- `/api/v2/repos/{group_login}/{book_slug}/docs/{id}` — doc operations
- `/api/v2/repos/{group_login}/{book_slug}/toc` — TOC operations
- `/api/v2/repos/{group_login}/{book_slug}` — repo operations

---

### Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad request parameters |
| 401 | Invalid or expired token |
| 403 | No permission |
| 404 | Resource not found |
| 422 | Validation failed |
| 429 | Rate limited |
| 500 | Server error |

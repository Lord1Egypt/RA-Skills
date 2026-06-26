# Readdy API Reference

## API Endpoint Mapping

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List projects | POST | `/api/page_gen/project/list` |
| Project info | GET | `/api/page_gen/project?projectId=xxx` |
| Create project | POST | `/api/page_gen/project` |
| Update project properties | PUT | `/api/page_gen/project` |
| Delete project | DELETE | `/api/page_gen/project` |
| Generate page sections | POST | `/api/project/gen_section` |
| Generate logo | POST | `/api/project/gen_logo` |
| Auto-generate title | POST | `/api/page_gen/suggest/page_title` |
| Message history | POST | `/api/project/msg_list` |
| Create message | POST | `/api/project/msg` |
| Update message | PUT | `/api/project/msg` |
| Generate project (SSE) | POST | `/gapi/project/generate` |
| Build project | POST | `/api/project/build` |
| Build check | POST | `/api/project/build_check` |
| Set showId | POST | `/api/project/set_show_id` |
| Get preview link | GET | `/api/project/share?projectId=xxx&versionId=xxx` |
| Get subdomain info | GET | `/api/project/subdomain/info?projectId=xxx` |
| Generate subdomain | POST | `/api/project/subdomain/generate?projectId=xxx` |
| Publish subdomain | POST | `/api/project/subdomain/publish?projectId=xxx&versionId=xxx` |
| Check subdomain publish | POST | `/api/project/subdomain/publish_check?projectId=xxx` |
| Validate API Key | POST | `/api/brand_email/validate_api_key` |
| Email config | GET | `/api/brand_email/config/:projectId` |

## Authentication

All requests include the following headers:

- `Authorization: Bearer <token>`
- `Content-Type: application/json`
- `X-Project-ID: <projectId>` (for project-level operations)

## Error Codes

| Error Code | Description |
|-----------|-------------|
| 401 | Authentication failed — token is expired or invalid |
| 403 / AccessDenied | Insufficient permissions |
| ProjectNotFound | Project does not exist or has been deleted |
| ProjectMax | Project count has reached the limit |
| ApiKeyInvalid | API Key is invalid or expired |
| ImageTooLarge | Image size cannot exceed 3.5MB |
| SubscriptionInGracePeriod | Subscription is in grace period |
| RequestTimeout | Request timed out |
| InvalidParameter | Invalid parameter (with details) |
| PreviewError | Preview error (with details) |
| Network unreachable | Network connection failed — check network or disable VPN |

## Create Project Workflow (8 Steps)

1. `POST /api/project/gen_section` + `POST /api/page_gen/suggest/page_title` — Generate page sections and project name in parallel
2. `POST /api/project/gen_logo` — Generate logo image from prompt
3. (Project name already obtained in Step 1)
4. `POST /api/page_gen/project` — Create project, obtain projectId
5. `PUT /api/page_gen/project` — Save logo to project
6. `POST /api/project/msg` (x2) + `POST /gapi/project/generate` — Create message records and SSE-stream project content (with auto build + session continuation loop)
7. `POST /api/project/build` + `POST /api/project/build_check` — Final build (if not completed in continuation loop) + `POST /api/project/set_show_id` to set showId
8. `PUT /api/project/msg` — Update AI message to completed status (recordStatus=0, showId)

## Modify Project Workflow (6 Steps)

1. `GET /api/page_gen/project?projectId=xxx` — Get project info
2. `POST /api/project/msg_list` — Get message history, extract latest parentVersionID/parentShowID, build history JSON
3. `POST /api/project/msg` (x2) + `POST /gapi/project/generate` — Create message records and SSE-stream modification content (with auto build + session continuation loop)
4. `POST /api/project/build` + `POST /api/project/build_check` — Final build (if not completed in continuation loop)
5. `POST /api/project/set_show_id` — Set showId (with retry)
6. `PUT /api/project/msg` — Update AI message to completed status (recordStatus=0, showId)

## Publish Version Flow

1. `POST /api/project/msg_list` — Read message history and extract publishable versions from AI record messages (`projectVersionId` + `showId`)
2. `GET /api/project/subdomain/info?projectId=xxx` — Read current live subdomain and live showId
3. `POST /api/project/subdomain/generate?projectId=xxx` — Generate a default subdomain when the project has none yet
4. `POST /api/project/subdomain/publish?projectId=xxx&versionId=xxx` — Publish the concrete selected version from Step 1 to the default subdomain (always pass an explicit `versionId`)
5. `POST /api/project/subdomain/publish_check?projectId=xxx` — Poll when publish returns async status until the site is live

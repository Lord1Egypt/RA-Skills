---
name: cloud
description: "Sync local tests with Shiplight cloud — push and pull YAML test cases, templates, and functions between your repo and the cloud. Requires a Shiplight cloud subscription."
---

# Shiplight Cloud

Sync local YAML test cases, templates, and TypeScript functions with the Shiplight cloud using MCP tools. Primarily used to push local tests up to the cloud (and pull cloud tests back down) so they can run on a schedule, be shared with your team, and integrate with CI. Also manages test runs, environments, folders, suites, and accounts via the REST API.

## Setup

Requires a [Shiplight cloud subscription](https://www.shiplight.ai) and a `SHIPLIGHT_API_TOKEN`. If cloud MCP tools (`save_test_case`, `get_test_case`, etc.) are not in the tool list, the token is missing.

Tell the user:
> Cloud tools are not available. Get your API token from https://app.shiplight.ai/settings/api-tokens, set `SHIPLIGHT_API_TOKEN` in your project's `.env` file, then reconnect MCP (`/mcp`).

If the user provides a token, append it to the project's `.env` file (create if needed) and tell them: "Saved to `<project>/.env` — make sure `.env` is in your `.gitignore`. Reconnect MCP (`/mcp`) to activate cloud tools."

All REST API calls require:
```
Authorization: Bearer $SHIPLIGHT_API_TOKEN
```

## Error Handling

| Error | Action |
|-------|--------|
| 401 Unauthorized | Token is invalid or expired — ask user to check `SHIPLIGHT_API_TOKEN` in `.env` |
| 403 Forbidden | Insufficient permissions — inform user |
| 404 Not Found | Resource not found — report to user |
| 422 Validation | Show validation message to user |
| Tool not found | Token is missing — guide user through setup above |

---

## MCP Tools

These tools are available when `SHIPLIGHT_API_TOKEN` is set. Prefer `file_path` over passing content directly (saves tokens). Always use `output_format: 'yaml'` for `get_test_case`.

- **Upload:** `save_test_case`, `save_test_account`, `save_template`, `save_function`
- **Download:** `get_test_case`, `get_template`, `get_function`
- **Account:** `save_test_account` — create/update test account with optional `storage_state_path` to upload local browser session to cloud

### ID Tracking

After uploading, add the returned cloud ID to the local file so future saves update instead of creating duplicates:

| Artifact | Local file | ID field |
|----------|-----------|----------|
| Test case | `*.test.yaml` | `test_case_id: 123` (top-level YAML field) |
| Template | `templates/*.yaml` | `template_id: 45` (top-level YAML field) |
| Function | `helpers/*.ts` | `@function_id 67` (JSDoc tag per export) |

---

## REST API

Base URL: `https://api.shiplight.ai`

### Test Cases

#### List Test Cases

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-cases
```

**Query parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `ids` | string | Comma-separated test case IDs |
| `folderId` | number | Filter by exact folder |
| `folderIdRecursive` | number | Filter by folder and all descendants |
| `labelIds` | string | Comma-separated label IDs (OR logic — matches test cases with ANY of the labels) |
| `createdBy` | string | Filter by creator user ID |
| `orderBy` | string | Order by field (default: `"id"`) |
| `order` | `asc` \| `desc` | Order direction (default: `"desc"`) |
| `limit` | number | Max results to return |

**Response:** `{ data: [{ id, title, test_flow, folder_id, ... }], count: number }`

#### Get Test Case

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-cases/123
```

**Response:** `{ id, title, test_flow, folder_id }`

#### Delete Test Case (soft delete)

Marks the test case and its results as deleted (soft delete — records are retained but hidden from queries).

```bash
curl -X DELETE -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-cases/123
```

**Response:** `{ success: true, message: "Test case deleted" }`

#### Move Test Cases to Folder

Batch-update the folder assignment for multiple test cases. Set `folder_id` to `null` to move to root.

```bash
curl -X PUT -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test_ids": [101, 102], "folder_id": 5}' \
  https://api.shiplight.ai/v1/test-cases/batch-update-folder
```

**Body:** `{ test_ids: number[], folder_id: number | null }`

**Response:** `{ success: true, data: [/* updated test cases */], message: "Successfully updated 2 test cases" }`

---

### Test Data

#### List Test Data

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-data
```

Use `ids` to fetch specific files:

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/test-data?ids=1,2,3"
```

**Response:** array of `{ organization_id, id, name, s3_path, created_at, updated_at, usage_count? }`

#### Get Test Data

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-data/123
```

**Response:** `{ organization_id, id, name, s3_path, created_at, updated_at }`

#### Download Test Data File

Streams the file from S3 as `application/octet-stream`.

```bash
curl -L -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-data/123/download \
  -o ./filename.ext
```

---

### Test Runs

#### List Test Runs

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/test-runs?limit=10"
```

**Query parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `testPlanId` | number | Filter by test plan |
| `trigger` | string | Filter by trigger (`"API"`, `"MANUAL"`) |
| `result` | string | Filter by result (`"PASSED"`, `"FAILED"`) |
| `limit` | number | Max results to return |

**Response:** array of `{ id, status, result, trigger, start_time, end_time, duration, total_test_case_count, passed_test_case_count, failed_test_case_count }`

#### Get Test Run Details

**Note:** This endpoint has **no `/v1/` prefix**.

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/run-results/456
```

**Response:**
```json
{
  "testRun": { "id": 456, "status": "COMPLETED", "result": "PASSED" },
  "testCaseResults": [
    { "id": 789, "test_case_id": 123, "result": "PASSED", "duration": 45 }
  ]
}
```

#### Trigger Test Run

Run a test case, test suite, or a combination in the cloud.

**By test case:**

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger": "API"}' \
  https://api.shiplight.ai/v1/test-run/test-case/123
```

**By test suite:**

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger": "API"}' \
  https://api.shiplight.ai/v1/test-run/test-suite/1
```

**Generic (multiple test cases, suites, and/or labels):**

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger": "API", "test_case_ids": [101, 102], "test_suite_ids": [1]}' \
  https://api.shiplight.ai/v1/test-run
```

**By labels (run all test cases with any of the specified labels):**

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger": "API", "label_ids": [22, 18]}' \
  https://api.shiplight.ai/v1/test-run
```

**Body (all trigger endpoints):**

| Field | Type | Description |
|-------|------|-------------|
| `trigger` | string | Required. Use `"API"` |
| `test_case_ids` | number[] | Generic endpoint only — test case IDs to run |
| `test_suite_ids` | number[] | Generic endpoint only — test suite IDs to run |
| `label_ids` | number[] | Generic endpoint only — label IDs; resolves to test cases with ANY of these labels (OR logic). Can be combined with `test_case_ids` and `test_suite_ids` |
| `environment` | `{ id?: string }` | Override environment |

**Response (201):** test run object with `{ id, status, result, ... }`

After triggering, poll `GET /v1/test-runs?limit=1` or `GET /run-results/<id>` to check status.

#### Get Test Case Result

**Note:** This endpoint has **no `/v1/` prefix**.

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/test-case-results/789
```

**Response:** `{ id, test_case_id, test_run_id, result, status, duration, environment_name, environment_url, video, trace, report_s3_uri, report, error }`

The `video`, `trace`, and `report_s3_uri` fields contain S3 URIs — use the Artifacts endpoint to download them.

The `report` field contains step-by-step execution details in `report[0].resultJson` — each step has `description`, `status`, `message`, `duration`, and artifact S3 URIs (`screenshot_s3_path`, `messages_s3_path`, etc.).

---

### Environments

#### List Environments

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/environments
```

**Response:** array of `{ id, name, url }`

#### Get Environment

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/environments/1
```

**Response:** `{ id, name, url }`

---

### Variables

Environment-scoped variables — the cloud equivalent of `variables` in `playwright.config.ts`. Use `isSensitive: true` for secrets (passwords, API keys) so they're masked in logs.

#### List Variables

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/variables?environmentId=1"
```

**Response:** array of `{ id, name, value, environment_id, is_sensitive }`

---

### Test Accounts

#### List Test Accounts

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/test-accounts?environmentId=1"
```

**Query:** `environmentId` (number, optional but recommended) — filter by environment.

**Response:** array of `{ id, name, username, environmentId, loginConfig }`

#### Get Test Account

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-accounts/1
```

**Response:** `{ id, name, username, password, environmentId, loginConfig }`

---

### Forward Email Configs

Forward email configs store the Mailgun forwarding address and extraction filters used by email-based login and verification flows. All responses are scoped to the organization associated with `SHIPLIGHT_API_TOKEN`.

#### List Forward Email Configs

Returns all forward email configs for the organization, ordered by `created_at` descending.

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/forward-email-configs
```

**Response:** array of `{ id, organization_id, name, forward_email, extraction_type, prompt, filter_from_email, filter_to_email, filter_subject, filter_body_contains, created_at, updated_at }`

#### Get Forward Email Config

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/forward-email-configs/1
```

**Response:** `{ id, organization_id, name, forward_email, extraction_type, prompt, filter_from_email, filter_to_email, filter_subject, filter_body_contains, created_at, updated_at }`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Forward email config ID |
| `organization_id` | string | Organization that owns the config |
| `name` | string | Human-readable config name |
| `forward_email` | string | Mailgun forwarding inbox address |
| `extraction_type` | string | Extraction mode, such as `verification_code`, `activation_link`, or `custom` |
| `prompt` | string | Optional custom extraction prompt |
| `filter_from_email` | string | Optional sender filter |
| `filter_to_email` | string | Optional recipient filter |
| `filter_subject` | string | Optional subject filter |
| `filter_body_contains` | string | Optional body text filter |
| `created_at` | string | ISO timestamp |
| `updated_at` | string | ISO timestamp |

---

### Folders

#### List All Folders

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-folders/all
```

Optional query: `?search=keyword`

**Response:** array of `{ id, name, description, parentId, pathIds }`

#### List Folders by Parent

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/test-folders?parentId=1"
```

Omit `parentId` entirely for root-level folders.

**Response:** array of `{ id, name, description, parentId }`

#### Get Folder

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-folders/1
```

**Response:** `{ id, name, description, parentId, pathIds }`

#### Create Folder

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Smoke Tests", "parentId": 1}' \
  https://api.shiplight.ai/v1/test-folders
```

**Body:** `{ name: string, description?: string, parentId?: number | null }`

**Response (201):** `{ success: true, data: { id, name, description, parentId } }`

#### Update Folder

```bash
curl -X PATCH -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Regression Tests"}' \
  https://api.shiplight.ai/v1/test-folders/1
```

**Body:** `{ name?: string, description?: string }`

**Response:** `{ success: true, data: { id, name, description } }`

#### Delete Folder

```bash
curl -X DELETE -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-folders/1
```

**Response:** `{ success: true }`

#### Move Folder

Move a folder to a different parent. Set `parentId` to `null` to move to root.

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"parentId": 5}' \
  https://api.shiplight.ai/v1/test-folders/1/move
```

**Body:** `{ parentId: number | null }`

**Response:** `{ success: true }`

---

### Test Suites

Test suites group test cases for organized execution. Use suites to manage which test cases run together.

#### List All Suites

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-suites
```

**Response:** array of `{ id, title, description, testCount, createdAt, updatedAt }`

#### Get Suite

Returns suite metadata and its test cases. **Always use `?fields=` to select only the columns you need** — without it, the endpoint returns full test case entities which is too expensive.

`?fields=` accepts a comma-separated list of columns: `id`, `title`, `description`, `status`, `folder_id`, `test_type`, `created_at`, `updated_at`, `url`

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/test-suites/1?fields=id,title,status"
```

**Response:**
```json
{
  "suite": { "id": 1, "title": "Smoke Tests", "description": "...", "testCount": 5 },
  "testCases": [
    { "id": 101, "title": "Login flow", "status": "Active" },
    { "id": 102, "title": "Search", "status": "Active" }
  ]
}
```

#### Create Suite

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Smoke Tests", "description": "Core user flows"}' \
  https://api.shiplight.ai/v1/test-suites
```

**Body:** `{ title: string, description?: string }`

**Response (201):** `{ id, title, description, createdAt, updatedAt }`

#### Update Suite

```bash
curl -X PUT -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Regression Tests"}' \
  https://api.shiplight.ai/v1/test-suites/1
```

**Body:** `{ title?: string, description?: string }`

**Response:** `{ success: true, message: "Test suite updated successfully" }`

#### Delete Suite

```bash
curl -X DELETE -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/test-suites/1
```

**Response:** `{ success: true, message: "Test suite deleted" }`

#### Add Test Cases to Suite

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"testCaseIds": [101, 102, 103]}' \
  https://api.shiplight.ai/v1/test-suites/1/test-cases
```

**Body:** `{ testCaseIds: number[] }`

**Response:** `{ success: true, message: "Test cases added to suite successfully" }`

#### Remove Test Cases from Suite

```bash
curl -X DELETE -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"testCaseIds": [101]}' \
  https://api.shiplight.ai/v1/test-suites/1/test-cases
```

**Body:** `{ testCaseIds: number[] }`

**Response:** `{ success: true, message: "Test cases removed from suite successfully" }`

---

### Labels

Labels let you tag test cases (e.g., `daily-regression`, `pre-merge`) and trigger runs by label instead of manually managing suites.

#### List Labels

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/labels
```

**Response:** `{ success: true, data: [{ id, name, color, organizationId, createdAt, updatedAt }] }`

#### Create Label

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "daily-regression", "color": "#4CAF50"}' \
  https://api.shiplight.ai/v1/labels
```

**Body:** `{ name: string, color: string }`

**Response (201):** `{ success: true, data: { id, name, color } }`

#### Update Label

```bash
curl -X PUT -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "nightly-regression"}' \
  https://api.shiplight.ai/v1/labels/22
```

**Body:** `{ name?: string, color?: string }`

#### Delete Label

```bash
curl -X DELETE -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/labels/22
```

#### Add Labels to Test Case

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"labelIds": [22, 18]}' \
  https://api.shiplight.ai/v1/labels/test-case/123/add
```

**Body:** `{ labelIds: number[] }`

#### Remove Labels from Test Case

```bash
curl -X POST -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"labelIds": [22]}' \
  https://api.shiplight.ai/v1/labels/test-case/123/remove
```

**Body:** `{ labelIds: number[] }`

#### Get Labels for Test Case

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/labels/test-case/123
```

**Response:** `{ success: true, data: [{ id, name, color }] }`

#### Get Test Case IDs by Label

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/labels/test-cases/22
```

**Response:** `{ success: true, data: [101, 102, 103] }`

---

### Templates (Reusable Steps)

Reusable test step sequences that can be referenced from test cases via `template:` in YAML or `reference_id` in the cloud. The API uses the legacy name "reusable-steps".

#### Get Template

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/reusable-steps/138
```

**Response:** `{ id, name, description, statements }`

---

### Test Functions

Custom TypeScript functions that can be called from test cases via `call: "file#export"` in YAML.

#### Get Test Function

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  https://api.shiplight.ai/v1/functions/42
```

**Response:** `{ id, name, description, code, status }`

---

### Artifacts

#### Download S3 File

Download test artifacts (videos, traces, reports) referenced by S3 URIs in test case results.

```bash
curl -H "Authorization: Bearer $SHIPLIGHT_API_TOKEN" \
  "https://api.shiplight.ai/v1/s3/file?uri=s3://bucket/path/video.webm"
```

**Query:** `uri` (string, required) — S3 URI from test result fields (`video`, `trace`, `report_s3_uri`).

**Response:** raw file contents with appropriate content-type. For binary files (videos, traces), use `curl -o <output_file>` to save to disk.

---

## Workflows

### Sync local project to cloud

1. **Sync test accounts:** call `save_test_account` with credentials and `storage_state_path` (if the local project uses storageState-based auth)
2. **Sync test cases:** find all `.test.yaml` files, call `save_test_case` with `file_path` for each. If the file already has a `test_case_id`, it updates; if not, it creates and returns an ID.
3. **Track IDs:** add the returned `test_case_id` to the YAML if not already present
4. **Sync templates and functions:** repeat with `save_template` and `save_function`

### Download test case from cloud

1. Call `get_test_case` with `test_case_id` and `output_format: 'yaml'`
2. **Convert the cloud `url:` to baseURL + relative paths.** Cloud test cases have a top-level `url:` field for the starting URL (e.g., `url: https://app.example.com/dashboard`). Local YAML tests split this into two parts:
   - **Base URL** — set once in playwright.config.ts at the project level (`use: { baseURL: 'https://app.example.com' }`) if all tests share the same origin, or per-test via `base_url: https://app.example.com`. Prefer project-level.
   - **Navigation** — use relative paths in the test steps (`URL: /dashboard`).

   Remove the top-level `url:` field from the downloaded YAML, ensure `baseURL` is configured, and convert any absolute URL statements to relative paths.
3. Save the returned YAML to a `.test.yaml` file

### Download test artifacts

1. `GET /test-case-results/<id>` → find `video`, `trace`, or `report_s3_uri` fields (S3 URIs)
2. `GET /v1/s3/file?uri=<S3_URI>` → download the artifact content

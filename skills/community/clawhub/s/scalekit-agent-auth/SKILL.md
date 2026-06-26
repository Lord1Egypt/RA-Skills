---
name: openclaw-tool-executor
description: |
  Use this skill whenever the user asks for information from, or wants to take an action in, a third-party tool or service. This includes — but is not limited to — searching the web, reading or writing documents, sending messages, querying databases, managing tasks, fetching data from APIs, or interacting with any connected SaaS product (e.g. "search Exa for...", "read my Notion page", "send a Slack message", "get my Google Sheet", "create a GitHub issue", "query Snowflake", "look up a HubSpot contact"). Trigger this skill any time the user's request involves an external service, integration, or data source — even if the provider is not explicitly named. Handles OAuth and non-OAuth (API Key, Bearer, Basic) connections, tool discovery, execution, and proxy fallback via Scalekit Connect.

  ## Provider Mapping

  Some services are accessed through a different provider name in Scalekit. Always use the mapped provider name below:

  | User asks about | Use provider |
  |---|---|
  | LinkedIn — profiles, jobs, companies, posts, people search, ads, groups | `HARVESTAPI` |
homepage: https://github.com/scalekit-inc/openclaw-skill
metadata:
  openclaw:
    requires:
      bins: ["python3", "uv"]
      env:
        - TOOL_CLIENT_ID
        - TOOL_CLIENT_SECRET
        - TOOL_ENV_URL
        - TOOL_IDENTIFIER
    primaryEnv: TOOL_CLIENT_ID
    config:
      requiredEnv:
        - TOOL_CLIENT_ID
        - TOOL_CLIENT_SECRET
        - TOOL_ENV_URL
      example: |
        TOOL_CLIENT_ID=skc_your_client_id
        TOOL_CLIENT_SECRET=your_client_secret
        TOOL_ENV_URL=https://your-env.scalekit.cloud
        TOOL_IDENTIFIER=your_default_identifier
    install:
      - id: python-deps
        kind: exec
        command: "uv sync"
        label: "Install Python dependencies"
---

# OpenClaw Tool Executor

General-purpose tool executor for OpenClaw agents. Uses Scalekit Connect to discover and run tools for any connected service — OAuth (Notion, Slack, Gmail, GitHub, etc.) or non-OAuth (API Key, Bearer, Basic auth).

## Environment Variables

Required in `.env`:

```
TOOL_CLIENT_ID=<scalekit_client_id>
TOOL_CLIENT_SECRET=<scalekit_client_secret>
TOOL_ENV_URL=<scalekit_environment_url>
TOOL_IDENTIFIER=<default_identifier>   # optional but recommended
```

`TOOL_IDENTIFIER` is used as the default `--identifier` for all operations. If not set, the script will prompt the user at runtime and display a warning advising them to set it in `.env`.

## Execution Flow

When the user asks to perform an action on a connected service, follow these steps **in order**:

### Step 1 — Discover the Connection

Dynamically resolve the `connection_name` by listing all configured connections for the provider. The API paginates automatically through all pages:

```bash
uv run tool_exec.py --list-connections --provider <PROVIDER>
```

- Only consider connections with `"status": "COMPLETED"` — ignore any with `DRAFT`, `PENDING`, or other non-completed statuses.
- Use the `key_id` from the first **COMPLETED** result as `<CONNECTION_NAME>` for all subsequent steps.
- If **no connection found** → inform the user that no `<PROVIDER>` connection is configured in Scalekit and stop.
- If **connections exist but none are COMPLETED** → inform the user of the connection `key_id`(s) found and tell them the connection configuration is not completed. Ask them to complete setup in the Scalekit Dashboard and stop.
- If **multiple COMPLETED connections found** → the first one is selected automatically (a warning is shown).

### Step 2 — Check & Authorize

Run `--generate-link` for the connection. The tool automatically detects the connection type (OAuth vs non-OAuth) and applies the correct auth flow:

```bash
uv run tool_exec.py --generate-link \
  --connection-name <CONNECTION_NAME>
```

**OAuth connections:**
- If already **ACTIVE** → proceed to Step 3.
- If **not active** → a magic link is generated. Present it to the user, wait for them to complete the flow, then proceed to Step 3.

**Non-OAuth connections (BEARER, BASIC, API Key, etc.):**
- If account **not found** → stop. Tell the user: *"Please create and configure the `<CONNECTION_NAME>` connection in the Scalekit Dashboard."*
- If account exists but **not active** → stop. Tell the user: *"Please activate the `<CONNECTION_NAME>` connection in the Scalekit Dashboard."*
- If **ACTIVE** → proceed to Step 3.

> Never use `--get-authorization` in the execution flow — that is only for inspecting raw OAuth tokens and does not work for non-OAuth connections.

### Step 3 — Discover Available Tools

Fetch the list of tools available for the provider:

```bash
uv run tool_exec.py --get-tool --provider <PROVIDER>
```

- Look for a tool that matches the user's intent (e.g. `notion_page_get` for reading a page).
- If a matching tool **exists** → go to Step 3b.
- If **no matching tool exists** → go to Step 5 (proxy fallback).

### Step 3b — Fetch Tool Schema (mandatory before executing)

**Always** fetch the schema of the matched tool before constructing the input. This tells you the exact parameter names, types, required vs optional fields, and valid enum values:

```bash
uv run tool_exec.py --get-tool --tool-name <TOOL_NAME>
```

- Read the `input_schema.properties` from the response — use **only** the parameter names defined there.
- Note which fields are in `required` — these must always be included in `--tool-input`.
- Use `description` and `display_properties` to understand what each field expects.
- **Never guess parameter names** — always derive them from the schema.

### Step 4 — Execute the Tool

Construct the tool input using only parameters from the schema fetched in Step 3b, then run:

```bash
uv run tool_exec.py --execute-tool \
  --tool-name <TOOL_NAME> \
  --connection-name <CONNECTION_NAME> \
  --tool-input '<JSON_INPUT>'
```

Return the result to the user.

### Step 5 — Proxy Fallback (only if no tool exists)

If no Scalekit tool covers the required action, attempt a proxied HTTP request directly to the provider's API:

```bash
uv run tool_exec.py --proxy-request \
  --connection-name <CONNECTION_NAME> \
  --path <API_PATH> \
  --method <GET|POST|PUT|DELETE> \
  --query-params '<JSON>' \   # optional
  --body '<JSON>'             # optional
```

> Note: Proxy may be disabled on some environments. If it returns `TOOL_PROXY_DISABLED`, inform the user that this action isn't supported by the current Scalekit tool catalog and suggest they request a new tool from Scalekit.

## Example: Search LinkedIn (via HarvestAPI)

```
User: "Find software engineers in San Francisco on LinkedIn"
```

1. `--list-connections --provider HARVESTAPI` → `key_id: harvestapi-xxxx`, `type: API_KEY`
2. `--generate-link --connection-name harvestapi-xxxx` → detects API_KEY, checks account → ACTIVE
3. `--get-tool --provider HARVESTAPI` → finds `harvestapi_search_people`
3b. `--get-tool --tool-name harvestapi_search_people` → schema shows valid params: `first_names`, `last_names`, `search`, `locations`, `current_job_titles`, etc.
4. `--execute-tool --tool-name harvestapi_search_people --connection-name harvestapi-xxxx --tool-input '{"first_names": "John", "locations": "San Francisco", "current_job_titles": "Software Engineer"}'`
   → returns matching LinkedIn profiles

> Any LinkedIn-related request (profiles, jobs, companies, posts, people search, ads, groups) → use provider `HARVESTAPI`.

## Example: Search the web with Exa (API Key connection)

```
User: "Search for latest AI news using Exa"
```

1. `--list-connections --provider EXA` → `key_id: exa`, `type: API_KEY`
2. `--generate-link --connection-name exa` → detects API_KEY, checks account → ACTIVE
3. `--get-tool --provider EXA` → finds `exa_search`
3b. `--get-tool --tool-name exa_search` → schema shows `query` (required), `num_results`, `type`, etc.
4. `--execute-tool --tool-name exa_search --connection-name exa --tool-input '{"query": "latest AI news"}'`
   → returns search results

## Example: Read a Notion Page (OAuth connection)

```
User: "Read my Notion page https://notion.so/..."
```

1. `--list-connections --provider NOTION` → `key_id: notion-ijIQedmJ`, `type: OAUTH`
2. `--generate-link --connection-name notion-ijIQedmJ` → detects OAuth, already ACTIVE
3. `--get-tool --provider NOTION` → finds `notion_page_get`
3b. `--get-tool --tool-name notion_page_get` → schema shows `page_id` (required)
4. `--execute-tool --tool-name notion_page_get --connection-name notion-ijIQedmJ --tool-input '{"page_id": "..."}'`
   → returns page metadata

## Example: Action Not Yet in Scalekit

```
User: "Fetch the blocks of a Notion page"
```

1. `--list-connections --provider NOTION` → `key_id: notion-ijIQedmJ`
2. `--generate-link --connection-name notion-ijIQedmJ` → ACTIVE
3. `--get-tool --provider NOTION` → no `notion_blocks_fetch` tool found
4. `--proxy-request --path "/blocks/<page_id>/children"` → fallback attempt
5. If proxy disabled → inform user the action isn't available yet

## File Uploads & Downloads

Some providers do not have Scalekit tools for file operations. Use `--proxy-request` with `--input-file` (upload) or direct S3/CDN URL download (download). Provider-specific flows are documented below.

> ⚠️ **Proxy token expiry:** `--proxy-request` passes the stored OAuth access token directly to the provider. If the token has expired, the provider will return `401 Unauthorized`. Unlike `--execute-tool` which auto-refreshes tokens, the proxy does not. If you get a 401, the token needs to be refreshed — re-run `--generate-link` to check status; if the connection is ACTIVE but proxy still returns 401, the user must re-authorize via a new magic link to obtain a fresh token.

---

### Notion

#### Upload a File to a Notion Page

Notion file uploads are a **3-step process** via proxy:

**Step 1 — Create an upload object**

```bash
uv run tool_exec.py --proxy-request \
  --connection-name <CONNECTION_NAME> \
  --path "/v1/file_uploads" \
  --method POST \
  --body '{"mode": "single_part"}' \
  --headers '{"Notion-Version": "2022-06-28", "Content-Type": "application/json"}'
```

Returns a `file_upload` object with an `id` and `upload_url`. The upload is valid for **1 hour**.

**Step 2 — Send the file**

```bash
uv run tool_exec.py --proxy-request \
  --connection-name <CONNECTION_NAME> \
  --path "/v1/file_uploads/<file_upload_id>/send" \
  --method POST \
  --input-file /path/to/file \
  --headers '{"Notion-Version": "2022-06-28"}'
```

- The file is sent as `multipart/form-data`. On success, `status` becomes `uploaded`.
- ⚠️ Notion rejects `application/octet-stream`. If the file extension is not recognized (e.g. `.md`), copy it to a `.txt` extension first so the MIME type resolves to `text/plain`.

**Step 3 — Attach the file block to a page**

```bash
uv run tool_exec.py --proxy-request \
  --connection-name <CONNECTION_NAME> \
  --path "/v1/blocks/<page_id>/children" \
  --method PATCH \
  --body '{
    "children": [{
      "object": "block",
      "type": "file",
      "file": {
        "type": "file_upload",
        "file_upload": {"id": "<file_upload_id>"},
        "name": "<display_filename>"
      }
    }]
  }' \
  --headers '{"Notion-Version": "2022-06-28", "Content-Type": "application/json"}'
```

> Do **not** use `notion_page_content_append` for file blocks — it does not support the `file_upload` block type and will return an `INTERNAL_ERROR`. Always use the proxy for file attachment.

---

#### Download a File from a Notion Page

Notion files are stored on S3 with pre-signed URLs that expire in **1 hour**. The download is a 2-step process:

**Step 1 — Get a fresh pre-signed URL**

List the page blocks to find the file block and its current URL:

```bash
uv run tool_exec.py --proxy-request \
  --connection-name <CONNECTION_NAME> \
  --path "/v1/blocks/<page_id>/children" \
  --method GET \
  --headers '{"Notion-Version": "2022-06-28"}'
```

Find the block with `"type": "file"` — the URL is at `file.file.url`. Always fetch a fresh URL; never reuse a URL from a previous response as it may be expired.

**Step 2 — Download directly from S3**

The S3 URL is public (pre-signed) — no Scalekit proxy needed. Download it directly:

```python
import urllib.request
urllib.request.urlretrieve("<s3_url>", "/local/path/filename")
```

Or use `--output-file` if going through the proxy:

```bash
uv run tool_exec.py --proxy-request \
  --connection-name <CONNECTION_NAME> \
  --path "/v1/blocks/<block_id>" \
  --method GET \
  --headers '{"Notion-Version": "2022-06-28"}' \
  --output-file /local/path/filename
```

> Note: `--output-file` saves the raw API response (JSON block object), not the file itself. Use direct S3 download for the actual file content.

---

### Google Drive

> *Coming soon*

---

### OneDrive / SharePoint

> *Coming soon*

---

## Supported Providers

Any provider configured in Scalekit (Notion, Slack, Gmail, Google Sheets, GitHub, Salesforce, HubSpot, Linear, and 50+ more). Use the provider name in uppercase for `--provider` (e.g. `NOTION`, `SLACK`, `GOOGLE`).

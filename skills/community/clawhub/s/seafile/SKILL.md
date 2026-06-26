---
name: seafile-skill
description: Search, download, and upload files in a single Seafile library using a repo token. Use when an agent needs library-scoped filename or path search, exact-path downloads, or uploads into a Seafile library via the repo-token API.
homepage: https://github.com/andrewreid/seafile-skill
metadata: {"clawdbot":{"emoji":"🗂️","requires":{"bins":["curl","jq"],"env":["SEAFILE_BASE_URL","SEAFILE_REPO_TOKEN"]},"primaryEnv":"SEAFILE_REPO_TOKEN"}}
compatibility: Requires curl, jq, a valid Seafile repo token, and network access to the target Seafile server.
---

# Seafile Skill

## Overview

Use this skill to interact with one Seafile library through the repo-token API.
It is designed for three tasks only:

- Search for files or folders by filename or path fragment inside the token's library scope
- Download a file by exact Seafile path
- Upload a local file into an existing Seafile directory

This skill does not cover full-text content search, cross-library discovery, deletes, renames, moves, or share-link management.

For endpoint details, see [references/seafile-api.md](references/seafile-api.md).
For reusable shell patterns, see [references/command-patterns.md](references/command-patterns.md).

## Prerequisites

Required:

- `curl`
- `jq`
- Network access to the Seafile server
- `SEAFILE_BASE_URL`
- `SEAFILE_REPO_TOKEN` with access to the target library

Optional with defaults:

- `SEAFILE_LIBRARY_ROOT`, which defaults to `/`
- `SEAFILE_OUTPUT_DIR`, which is only needed when saving downloaded files locally

Export the required variables before running commands. The optional variables below are shown with their recommended defaults:

```bash
export SEAFILE_BASE_URL="https://seafile.example.com"
export SEAFILE_REPO_TOKEN="<repo-token>"
export SEAFILE_LIBRARY_ROOT="/"        # optional
export SEAFILE_OUTPUT_DIR="$PWD/downloads"  # optional, used for downloads
mkdir -p "$SEAFILE_OUTPUT_DIR"
```

Defaults and expectations:

- `SEAFILE_BASE_URL` should be the server origin without a trailing slash
- `SEAFILE_LIBRARY_ROOT` defaults to `/` if you do not override it
- `SEAFILE_OUTPUT_DIR` is only needed for downloads
- All Seafile paths in this skill are absolute library paths such as `/`, `/docs`, or `/docs/report.pdf`

## Authentication

The repo-token endpoints use the repo token in the `Authorization` header.
Use this default form unless your deployment documents a different token scheme:

```bash
AUTH_HEADER="Authorization: Token $SEAFILE_REPO_TOKEN"
API_BASE="${SEAFILE_BASE_URL%/}/api/v2.1/via-repo-token"
```

Before doing search, download, or upload, verify the token and library scope:

```bash
curl --fail --silent --show-error \
  -H "$AUTH_HEADER" \
  "$API_BASE/repo-info/" | jq
```

If this fails with `401` or `403`, stop and fix the token, permissions, or server URL before continuing.

## Search Workflow

Use repo-token directory listing and filter locally with `jq`. This is filename and path search, not full-text search.

### 1. List items from a starting path

```bash
START_PATH="${SEAFILE_LIBRARY_ROOT:-/}"

curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  "$API_BASE/dir/"
```

Useful query parameters:

- `path`: directory to inspect, default `/`
- `recursive=1`: walk the subtree recursively
- `type=f`: files only
- `type=d`: directories only

### 2. Filter by filename fragment

```bash
NEEDLE="report"
START_PATH="${SEAFILE_LIBRARY_ROOT:-/}"

curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  "$API_BASE/dir/" |
  jq -r --arg needle "$NEEDLE" '
    .dirent_list[]
    | select((.name // "") | ascii_downcase | contains($needle | ascii_downcase))
    | [.type, .parent_dir, .name]
    | @tsv
  '
```

### 3. Filter by full path fragment

```bash
PATH_FRAGMENT="2026/q2"
START_PATH="${SEAFILE_LIBRARY_ROOT:-/}"

curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  "$API_BASE/dir/" |
  jq -r --arg needle "$PATH_FRAGMENT" '
    .dirent_list[]
    | (.parent_dir + "/" + .name | gsub("//+"; "/")) as $full_path
    | select($full_path | ascii_downcase | contains($needle | ascii_downcase))
    | [$full_path, .type]
    | @tsv
  '
```

When you need exact metadata for one known file path, consult the repo-token file-info section in [references/seafile-api.md](references/seafile-api.md) and confirm the route shape against the target deployment if needed.

## Download Workflow

Downloads are exact-path only.
`SEAFILE_OUTPUT_DIR` is optional overall and only matters if you want this skill to save the downloaded file to a local directory.

### 1. Request a one-time download link

```bash
REMOTE_FILE="/docs/report.pdf"

DOWNLOAD_LINK=$(curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$REMOTE_FILE" \
  "$API_BASE/download-link/" |
  jq -r '.')
```

### 2. Download the file to a local path

```bash
LOCAL_FILE="$SEAFILE_OUTPUT_DIR/$(basename "$REMOTE_FILE")"

curl --fail --silent --show-error --location \
  "$DOWNLOAD_LINK" \
  -o "$LOCAL_FILE"
```

Notes:

- `download-link/` returns a URL string, not a JSON object
- Use `--location` because the returned URL may redirect
- Keep the remote path exact, including spaces, case, and file extension

## Upload Workflow

Uploads send a local file into an existing Seafile directory.

### 1. Request an upload link

```bash
UPLOAD_LINK=$(curl --fail --silent --show-error \
  -H "$AUTH_HEADER" \
  "$API_BASE/upload-link/" |
  jq -r '.')
```

### 2. Upload one local file

```bash
LOCAL_FILE="./artifact.zip"
TARGET_DIR="/incoming"

curl --fail --silent --show-error \
  -F "file=@${LOCAL_FILE}" \
  -F "parent_dir=${TARGET_DIR}" \
  -F "replace=0" \
  "${UPLOAD_LINK}?ret-json=1" |
  jq
```

Upload behavior:

- `parent_dir` must be an absolute library path like `/incoming`
- `replace=1` overwrites an existing file with the same name
- `replace=0` preserves the existing file and lets Seafile rename the new upload if needed
- `?ret-json=1` returns structured JSON and should be used by default

If you need Seafile to create nested folders beneath an existing parent, add `-F "relative_path=subdir1/subdir2/"` to the upload request.

## Error Handling

Check failures in this order:

- `401` or `403`
  The token is missing, expired, malformed, or does not allow the requested action.
- `404`
  The base URL or endpoint is wrong, or the server is not exposing that API path.
- `440` or similar upload validation errors
  The filename is invalid for the target server.
- `442` or `443`
  The file is too large or the library is out of quota.
- Directory listing or download returns no match
  Re-check the starting directory, exact remote path, and case sensitivity.
- Upload succeeds but lands in the wrong place
  Re-check `parent_dir` and any `relative_path` value.

When a request is failing and the server output is unclear, remove `--silent` temporarily and inspect headers with `curl -i`.

## Examples

### Find files matching a name fragment

```bash
NEEDLE="invoice"
START_PATH="/finance"

curl --fail --silent --show-error \
  -G \
  -H "Authorization: Token $SEAFILE_REPO_TOKEN" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  --data-urlencode "type=f" \
  "${SEAFILE_BASE_URL%/}/api/v2.1/via-repo-token/dir/" |
  jq -r --arg needle "$NEEDLE" '
    .dirent_list[]
    | select((.name // "") | ascii_downcase | contains($needle | ascii_downcase))
    | (.parent_dir + "/" + .name | gsub("//+"; "/"))
  '
```

### Download one file by exact path

```bash
REMOTE_FILE="/finance/invoices/april-2026.pdf"
DOWNLOAD_LINK=$(curl --fail --silent --show-error \
  -G \
  -H "Authorization: Token $SEAFILE_REPO_TOKEN" \
  --data-urlencode "path=$REMOTE_FILE" \
  "${SEAFILE_BASE_URL%/}/api/v2.1/via-repo-token/download-link/" |
  jq -r '.')

curl --fail --silent --show-error --location \
  "$DOWNLOAD_LINK" \
  -o "$SEAFILE_OUTPUT_DIR/april-2026.pdf"
```

### Upload one local file into a target folder

```bash
TARGET_DIR="/incoming/reports"
LOCAL_FILE="./build/report.csv"
UPLOAD_LINK=$(curl --fail --silent --show-error \
  -H "Authorization: Token $SEAFILE_REPO_TOKEN" \
  "${SEAFILE_BASE_URL%/}/api/v2.1/via-repo-token/upload-link/" |
  jq -r '.')

curl --fail --silent --show-error \
  -F "file=@${LOCAL_FILE}" \
  -F "parent_dir=${TARGET_DIR}" \
  -F "replace=1" \
  "${UPLOAD_LINK}?ret-json=1" |
  jq
```

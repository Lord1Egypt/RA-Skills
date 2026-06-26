# Command Patterns

These snippets are meant to be copied into a shell session and adapted per task.

## Normalize Base Variables

```bash
SEAFILE_BASE_URL="${SEAFILE_BASE_URL%/}"
SEAFILE_LIBRARY_ROOT="${SEAFILE_LIBRARY_ROOT:-/}"
AUTH_HEADER="Authorization: Token $SEAFILE_REPO_TOKEN"
API_BASE="$SEAFILE_BASE_URL/api/v2.1/via-repo-token"
```

## Safe URL Joining

Use `${VAR%/}` when constructing the API base so endpoint paths do not become `//api/...`.

```bash
API_BASE="${SEAFILE_BASE_URL%/}/api/v2.1/via-repo-token"
```

## Repo-Info Health Check

```bash
curl --fail --silent --show-error \
  -H "$AUTH_HEADER" \
  "$API_BASE/repo-info/" | jq
```

## Recursive Directory Listing

```bash
START_PATH="${SEAFILE_LIBRARY_ROOT:-/}"

curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  "$API_BASE/dir/"
```

Files only:

```bash
curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  --data-urlencode "type=f" \
  "$API_BASE/dir/"
```

Directories only:

```bash
curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  --data-urlencode "type=d" \
  "$API_BASE/dir/"
```

## Filter JSON With `jq`

Match by filename fragment:

```bash
NEEDLE="report"

curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  --data-urlencode "recursive=1" \
  "$API_BASE/dir/" |
  jq -r --arg needle "$NEEDLE" '
    .dirent_list[]
    | select((.name // "") | ascii_downcase | contains($needle | ascii_downcase))
    | (.parent_dir + "/" + .name | gsub("//+"; "/"))
  '
```

Match by full path fragment:

```bash
PATH_FRAGMENT="2026/q2"

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
    | $full_path
  '
```

## Download To A Chosen Local Filename

```bash
REMOTE_FILE="/docs/report final.pdf"
LOCAL_FILE="$SEAFILE_OUTPUT_DIR/report-final.pdf"

DOWNLOAD_LINK=$(curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$REMOTE_FILE" \
  "$API_BASE/download-link/" |
  jq -r '.')

curl --fail --silent --show-error --location \
  "$DOWNLOAD_LINK" \
  -o "$LOCAL_FILE"
```

## Multipart Upload To A Directory

```bash
LOCAL_FILE="./build/report.csv"
TARGET_DIR="/incoming/reports"

UPLOAD_LINK=$(curl --fail --silent --show-error \
  -H "$AUTH_HEADER" \
  "$API_BASE/upload-link/" |
  jq -r '.')

curl --fail --silent --show-error \
  -F "file=@${LOCAL_FILE}" \
  -F "parent_dir=${TARGET_DIR}" \
  -F "replace=1" \
  "${UPLOAD_LINK}?ret-json=1" |
  jq
```

Upload below an existing parent with automatic subdirectory creation:

```bash
LOCAL_FILE="./dist/site.zip"
TARGET_DIR="/incoming"
RELATIVE_PATH="releases/2026-04-17/"

curl --fail --silent --show-error \
  -F "file=@${LOCAL_FILE}" \
  -F "parent_dir=${TARGET_DIR}" \
  -F "relative_path=${RELATIVE_PATH}" \
  -F "replace=0" \
  "${UPLOAD_LINK}?ret-json=1" |
  jq
```

## Emit More Readable Error Output

When the server response is unclear, keep the body and headers together.

```bash
curl -i \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  "$API_BASE/dir/"
```

If you expect JSON but the server might return HTML, dump the raw body first:

```bash
RESPONSE=$(curl --silent --show-error -G -H "$AUTH_HEADER" \
  --data-urlencode "path=$START_PATH" \
  "$API_BASE/dir/")
printf '%s\n' "$RESPONSE"
```

## Quick Triage Checklist

- Run `repo-info/` first to validate the base URL and token
- Confirm all Seafile paths begin with `/`
- Use `--data-urlencode` for all path query parameters
- Use `--location` for the actual download request
- Use `?ret-json=1` for uploads so the response is machine-readable

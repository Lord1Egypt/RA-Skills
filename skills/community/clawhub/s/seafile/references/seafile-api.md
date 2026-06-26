# Seafile Repo-Token API Notes

This reference narrows the Seafile API down to the repo-token endpoints this skill uses.

## Base API Pattern

Use the repo-token API base:

```text
{SEAFILE_BASE_URL}/api/v2.1/via-repo-token/
```

All examples in this skill assume:

```bash
AUTH_HEADER="Authorization: Token $SEAFILE_REPO_TOKEN"
API_BASE="${SEAFILE_BASE_URL%/}/api/v2.1/via-repo-token"
```

The official docs describe these endpoints under the Seafile API reference:

- `GET /repo-info/`
- `GET /dir/`
- `GET /download-link/`
- `GET /upload-link/`
- A repo-token file-info endpoint listed as `Get file info`

## Authentication

Send the repo token in the authorization header.

```http
Authorization: Token <repo-token>
```

The Seafile docs label repo-token auth as bearer-style credentials in the API explorer, but the web API examples and common Seafile usage use `Authorization: Token ...`. This skill defaults to that form.

## Repo Info

Use repo info as a connectivity and scope check.

```bash
curl --fail --silent --show-error \
  -H "$AUTH_HEADER" \
  "$API_BASE/repo-info/"
```

Expected use:

- Verify the server URL is correct
- Confirm the token is valid
- Confirm the token points to the intended library

## Directory Listing

List files and folders in a directory.

```bash
curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=/" \
  --data-urlencode "recursive=1" \
  "$API_BASE/dir/"
```

Supported query parameters called out by the docs:

- `path`: required directory path, defaults to `/`
- `type`: optional item filter, usually `f` for files or `d` for directories
- `recursive`: optional, `1` to recurse
- `with_thumbnail`: optional
- `thumbnail_size`: optional

The response is typically a JSON object containing a `dirent_list` array of directory entries. Commonly useful fields include:

- `type`
- `name`
- `parent_dir`
- `size`
- `mtime`
- `id`

Field availability may vary by server version or deployment.

## Download Link

Get a one-time link for a specific file path.

```bash
curl --fail --silent --show-error \
  -G \
  -H "$AUTH_HEADER" \
  --data-urlencode "path=/docs/report.pdf" \
  "$API_BASE/download-link/"
```

Important behavior:

- The input path must be the exact file path inside the library
- The response is a URL string
- The returned URL may redirect, so use `curl --location` for the actual download

## Upload Link

Get an upload URL for posting multipart file data.

```bash
curl --fail --silent --show-error \
  -H "$AUTH_HEADER" \
  "$API_BASE/upload-link/"
```

Important behavior:

- The response is a URL string
- The upload itself is a second request to that returned URL
- The upload request should usually append `?ret-json=1`

## Upload Request Shape

The multipart upload request typically includes:

- `file=@/local/path/to/file`
- `parent_dir=/target-directory`
- `replace=0` or `replace=1`
- optional `relative_path=subdir1/subdir2/`

Example:

```bash
curl --fail --silent --show-error \
  -F "file=@./artifact.zip" \
  -F "parent_dir=/incoming" \
  -F "replace=1" \
  "${UPLOAD_LINK}?ret-json=1"
```

Useful semantics from the published Seafile upload docs:

- `parent_dir` is the absolute destination directory in the library
- `replace=1` overwrites an existing file with the same name
- `replace=0` avoids overwrite and allows Seafile to rename the incoming file
- `relative_path` lets Seafile create nested folders below `parent_dir`
- `ret-json=1` returns a JSON array with uploaded file metadata

## File Info

The repo-token documentation includes a `Get file info` operation for exact-path metadata.
Use it only when you already know the exact file path and need metadata beyond the recursive directory listing.

Before scripting against it, confirm the exact route and query parameter shape in the live Seafile API explorer for the target deployment, because the public search results expose the operation name more clearly than the final request example.

---
name: synology-dsm
description: >
  Manage Synology NAS via DSM Web API. Authenticate, browse and manage files
  (FileStation), manage download tasks (DownloadStation), and query system info.
  Use when the user mentions Synology, NAS, DSM, FileStation, DownloadStation,
  or wants to interact with their NAS device.
---

# Synology DSM Skill

Interact with a Synology NAS through the DSM Web API using `curl`.

## Prerequisites

The user must have these environment variables set (or provide them inline):

- `SYNOLOGY_HOST` — NAS hostname or IP (e.g., `192.168.1.100`)
- `SYNOLOGY_PORT` — DSM port (`5000` for HTTP, `5001` for HTTPS)
- `SYNOLOGY_USER` — DSM username
- `SYNOLOGY_PASS` — DSM password

Base URL: `http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi`

> **Security**: Always prefer HTTPS (port 5001). Never hardcode credentials in commands shown to the user — use `$SYNOLOGY_PASS` references. If the user hasn't set env vars, ask them to provide connection details.

## Step 1: Authentication

Every session starts with login. Use `format=sid` to get a session ID.

### Login

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.API.Auth&version=6&method=login\
&account=$SYNOLOGY_USER&passwd=$SYNOLOGY_PASS\
&session=FileStation&format=sid" | jq .
```

Response:
```json
{"data": {"sid": "YOUR_SESSION_ID"}, "success": true}
```

Save the `sid` for all subsequent requests: `SID=<value from response>`

### Logout

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.API.Auth&version=6&method=logout\
&session=FileStation&_sid=$SID"
```

### 2FA Handling

If login returns error code `406`, the account has 2FA enabled. Ask the user for their OTP code, then include `&otp_code=<CODE>` in the login request.

### Session Notes

- Sessions timeout after ~15 minutes of inactivity
- If you get error code `106` (session timeout), re-authenticate
- Always logout when done to clean up sessions

## Step 2: API Discovery (Optional)

Query all available APIs on the NAS:

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/query.cgi?\
api=SYNO.API.Info&version=1&method=query" | jq .
```

This returns every API name, path, and supported version range. Useful for checking what packages are installed.

## Step 3: FileStation — File Management

All FileStation calls use `_sid=$SID` for authentication.

### List shared folders (root)

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.List&version=2&method=list_share&_sid=$SID" | jq .
```

### List files in a folder

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.List&version=2&method=list\
&folder_path=/volume1/homes&additional=size,time&_sid=$SID" | jq .
```

Parameters: `folder_path` (required), `offset`, `limit`, `sort_by` (name|size|mtime), `sort_direction` (asc|desc), `additional` (size,time,perm,type)

### Create folder

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.CreateFolder&version=2&method=create\
&folder_path=/volume1/homes&name=new_folder&_sid=$SID" | jq .
```

### Rename file or folder

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Rename&version=2&method=rename\
&path=/volume1/homes/old_name&name=new_name&_sid=$SID" | jq .
```

### Delete file or folder

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Delete&version=2&method=delete\
&path=/volume1/homes/unwanted_file&_sid=$SID" | jq .
```

For large deletions, use `method=start` to get a task ID, then poll with `method=status&taskid=<id>`.

### Upload file

```bash
curl -s -X POST \
  -F "api=SYNO.FileStation.Upload" \
  -F "version=2" \
  -F "method=upload" \
  -F "path=/volume1/homes" \
  -F "overwrite=true" \
  -F "file=@/local/path/to/file.txt" \
  -F "_sid=$SID" \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi"
```

### Download file

```bash
curl -s -o output_file.txt \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Download&version=2&method=download\
&path=/volume1/homes/file.txt&mode=download&_sid=$SID"
```

### Search files

```bash
# Start search
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Search&version=2&method=start\
&folder_path=/volume1&pattern=*.pdf&_sid=$SID" | jq .
# Returns taskid

# Get results
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Search&version=2&method=list\
&taskid=<TASK_ID>&_sid=$SID" | jq .
```

### Get file/folder info

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.List&version=2&method=getinfo\
&path=/volume1/homes/file.txt&additional=size,time&_sid=$SID" | jq .
```

For full FileStation API reference, see [references/filestation-api.md](references/filestation-api.md).

## Step 4: DownloadStation — Download Management

### Get DownloadStation info

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Info&version=1&method=getinfo&_sid=$SID" | jq .
```

### List all download tasks

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=list\
&additional=transfer&_sid=$SID" | jq .
```

The `additional=transfer` parameter includes download/upload speed and progress.

### Add download task (URL)

```bash
curl -s -X POST \
  -d "api=SYNO.DownloadStation.Task&version=1&method=create\
&uri=https://example.com/file.zip&_sid=$SID" \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi"
```

### Add download task (torrent file)

```bash
curl -s -X POST \
  -F "api=SYNO.DownloadStation.Task" \
  -F "version=1" \
  -F "method=create" \
  -F "file=@/local/path/to/file.torrent" \
  -F "_sid=$SID" \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi"
```

### Pause / Resume / Delete tasks

```bash
# Pause
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=pause\
&id=<TASK_ID>&_sid=$SID"

# Resume
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=resume\
&id=<TASK_ID>&_sid=$SID"

# Delete (force_complete=false keeps downloaded files)
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=delete\
&id=<TASK_ID>&force_complete=false&_sid=$SID"
```

Multiple task IDs can be comma-separated: `&id=task1,task2,task3`

For full DownloadStation API reference, see [references/downloadstation-api.md](references/downloadstation-api.md).

## Step 5: System Info

### Get DSM system information

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DSM.Info&version=2&method=getinfo&_sid=$SID" | jq .
```

Returns: model, RAM, serial, DSM version, uptime, temperature.

### Get storage/volume info

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.Storage.CGI.Storage&version=1&method=load_info&_sid=$SID" | jq .
```

### Get network info

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DSM.Network&version=1&method=list&_sid=$SID" | jq .
```

## Error Handling

All API responses follow: `{"success": true/false, "data": {...}, "error": {"code": N}}`

### Common error codes

| Code | Meaning | Action |
|------|---------|--------|
| 100 | Unknown error | Retry once |
| 101 | Bad request | Check parameters |
| 102 | No such API | Package not installed |
| 103 | No such method | Check API version |
| 104 | Version not supported | Use lower version |
| 105 | No permission | Check user privileges |
| 106 | Session timeout | Re-authenticate |
| 107 | Session interrupted | Re-authenticate |

### Auth-specific error codes

| Code | Meaning |
|------|---------|
| 400 | Incorrect password |
| 401 | Account disabled |
| 402 | Permission denied |
| 406 | 2FA code required |

For full error code reference, see [references/error-codes.md](references/error-codes.md).

## Workflow Example

A typical session:

1. Login and capture SID
2. Perform operations (list files, add downloads, etc.)
3. Logout when done

Always check `"success": true` in responses before proceeding. On error 106/107, re-login automatically.

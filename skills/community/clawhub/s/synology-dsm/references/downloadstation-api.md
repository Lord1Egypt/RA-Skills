# DownloadStation API Reference

Complete parameter reference for SYNO.DownloadStation APIs. All requests require `_sid=$SID`.

## SYNO.DownloadStation.Info

### method=getinfo

No additional parameters. Returns version and running status.

### method=getconfig

Returns default destination, max tasks, and other settings.

### method=setserverconfig

| Parameter | Required | Description |
|-----------|----------|-------------|
| default_destination | No | Default download folder |
| emule_default_destination | No | eMule download folder |

## SYNO.DownloadStation.Task

### method=list — List all tasks

| Parameter | Required | Description |
|-----------|----------|-------------|
| offset | No | Start index (default 0) |
| limit | No | Max items (default -1 = all) |
| additional | No | Comma-separated: `detail`, `transfer`, `file`, `tracker`, `peer` |

`additional` values:
- `detail` — URI, destination, creation time, priority, etc.
- `transfer` — Speed, downloaded/uploaded bytes, progress
- `file` — Files within the task
- `tracker` — Tracker info (BT tasks)
- `peer` — Peer info (BT tasks)

### method=getinfo — Get specific task details

| Parameter | Required | Description |
|-----------|----------|-------------|
| id | Yes | Task ID(s), comma-separated |
| additional | No | Same as list |

### method=create — Add download task

**Via URL (GET or POST form-encoded):**

| Parameter | Required | Description |
|-----------|----------|-------------|
| uri | Yes* | Download URL(s), comma-separated. Supports HTTP, FTP, magnet, ed2k, thunder |
| destination | No | Download folder path (relative to shared folder) |
| username | No | Credentials for the download URL |
| password | No | Credentials for the download URL |

**Via file upload (POST multipart/form-data):**

| Parameter | Required | Description |
|-----------|----------|-------------|
| file | Yes* | `.torrent` or `.nzb` file |
| destination | No | Download folder path |

*Either `uri` or `file` is required.

### method=pause — Pause task(s)

| Parameter | Required | Description |
|-----------|----------|-------------|
| id | Yes | Task ID(s), comma-separated |

### method=resume — Resume task(s)

| Parameter | Required | Description |
|-----------|----------|-------------|
| id | Yes | Task ID(s), comma-separated |

### method=delete — Delete task(s)

| Parameter | Required | Description |
|-----------|----------|-------------|
| id | Yes | Task ID(s), comma-separated |
| force_complete | No | Move incomplete download to destination (default false) |

### method=edit — Edit task settings

| Parameter | Required | Description |
|-----------|----------|-------------|
| id | Yes | Task ID(s), comma-separated |
| destination | No | New download destination |

## SYNO.DownloadStation.Schedule

### method=getconfig

Returns schedule settings (enabled, emule enabled).

### method=setconfig

| Parameter | Required | Description |
|-----------|----------|-------------|
| enabled | No | Enable/disable schedule |
| emule_enabled | No | Enable/disable eMule schedule |

## Task Status Values

| Status | Description |
|--------|-------------|
| `waiting` | Queued, not started |
| `downloading` | In progress |
| `paused` | User paused |
| `finishing` | Almost done (seeding, extracting) |
| `finished` | Complete |
| `hash_checking` | Verifying file integrity |
| `seeding` | BT seeding |
| `filehosting_waiting` | Waiting for file host |
| `extracting` | Extracting archive |
| `error` | Error occurred |

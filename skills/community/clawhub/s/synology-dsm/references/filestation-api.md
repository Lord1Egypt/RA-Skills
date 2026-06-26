# FileStation API Reference

Complete parameter reference for SYNO.FileStation APIs. All requests require `_sid=$SID`.

## SYNO.FileStation.List

### method=list_share — List shared folders

| Parameter | Required | Description |
|-----------|----------|-------------|
| offset | No | Start index (default 0) |
| limit | No | Max items to return (default 0 = all) |
| sort_by | No | `name`, `size`, `user`, `group`, `mtime`, `atime`, `ctime`, `crtime`, `posix` |
| sort_direction | No | `asc` or `desc` |
| additional | No | Comma-separated: `real_path`, `size`, `owner`, `time`, `perm`, `mount_point_type`, `volume_status` |

### method=list — List files in folder

| Parameter | Required | Description |
|-----------|----------|-------------|
| folder_path | Yes | Full path (e.g., `/volume1/homes`) |
| offset | No | Start index |
| limit | No | Max items |
| sort_by | No | `name`, `size`, `user`, `group`, `mtime`, `atime`, `ctime`, `crtime`, `posix`, `type` |
| sort_direction | No | `asc` or `desc` |
| pattern | No | Filename glob filter (e.g., `*.jpg`) |
| filetype | No | `file`, `dir`, or `all` (default `all`) |
| additional | No | `real_path`, `size`, `owner`, `time`, `perm`, `type`, `mount_point_type` |

### method=getinfo — Get file/folder metadata

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Comma-separated paths or JSON array |
| additional | No | Same as list |

## SYNO.FileStation.CreateFolder

### method=create

| Parameter | Required | Description |
|-----------|----------|-------------|
| folder_path | Yes | Parent path(s), comma-separated for batch |
| name | Yes | New folder name(s), comma-separated for batch |
| force_parent | No | Create parent dirs if missing (default false) |

## SYNO.FileStation.Rename

### method=rename

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Full path of file/folder to rename |
| name | Yes | New name |

## SYNO.FileStation.Delete

### method=delete — Synchronous delete (small items)

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Comma-separated paths to delete |
| recursive | No | Delete non-empty folders (default true) |

### method=start — Async delete (large items)

Returns `taskid`. Poll with `method=status&taskid=<id>`.

## SYNO.FileStation.Upload

### method=upload (POST multipart/form-data)

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Destination folder path |
| file | Yes | File to upload (multipart) |
| overwrite | No | `true` to overwrite, `false` to skip (default) |
| create_parents | No | Create missing parent dirs |

## SYNO.FileStation.Download

### method=download

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | File path to download |
| mode | Yes | `download` (full file) or `open` (browser preview) |

## SYNO.FileStation.Search

### method=start — Begin search

| Parameter | Required | Description |
|-----------|----------|-------------|
| folder_path | Yes | Root folder to search from |
| pattern | No | Filename glob (e.g., `*.pdf`) |
| extension | No | File extension filter |
| recursive | No | Search subdirectories (default true) |

Returns `taskid`.

### method=list — Get search results

| Parameter | Required | Description |
|-----------|----------|-------------|
| taskid | Yes | From search start |
| offset | No | Start index |
| limit | No | Max results |

### method=stop — Cancel search

| Parameter | Required | Description |
|-----------|----------|-------------|
| taskid | Yes | Task to cancel |

## SYNO.FileStation.CopyMove

### method=start

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Source path(s), comma-separated |
| dest_folder_path | Yes | Destination folder |
| overwrite | No | Overwrite existing (default false) |
| remove_src | No | Move instead of copy (default false) |

Returns `taskid`. Poll with `method=status`.

## SYNO.FileStation.Compress

### method=start

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Path(s) to compress |
| dest_file_path | Yes | Output archive path (e.g., `/volume1/archive.zip`) |
| format | No | `zip`, `7z` (default `zip`) |

## SYNO.FileStation.Extract

### method=start

| Parameter | Required | Description |
|-----------|----------|-------------|
| file_path | Yes | Archive to extract |
| dest_folder_path | Yes | Extraction destination |
| overwrite | No | Overwrite existing |

## SYNO.FileStation.DirSize

### method=start

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | Yes | Folder path(s) |

Returns `taskid`. Poll with `method=status` to get total size.

## SYNO.FileStation.MD5

### method=start

| Parameter | Required | Description |
|-----------|----------|-------------|
| file_path | Yes | File to hash |

Returns `taskid`. Poll with `method=status` to get MD5 hash.

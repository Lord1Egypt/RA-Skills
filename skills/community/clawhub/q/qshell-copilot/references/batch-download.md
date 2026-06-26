# Batch Download Configuration

`qdownload` requires a JSON config file specifying what to download and where to save it.

## Config Format

```json
{
  "dest_dir": "/path/to/save",
  "bucket": "your-bucket",
  "prefix": "optional-prefix/",
  "suffixes": ".jpg,.png",
  "thread_count": 5
}
```

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| `dest_dir` | Yes | Local directory to save downloaded files |
| `bucket` | Yes | Source bucket name |
| `prefix` | No | Only download files with this key prefix |
| `suffixes` | No | Only download files with these extensions (comma-separated) |
| `thread_count` | No | Number of parallel download threads (default: 5) |

## Usage

```bash
qshell qdownload <ThreadCount> <ConfigFile>
```

Example:
```bash
qshell qdownload 5 download-config.json
```

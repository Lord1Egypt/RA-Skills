# vod_describe_sub_app_ids — Parameters & Examples

> Corresponding script: `scripts/vod_describe_sub_app_ids.py`
>
> Query all sub-application lists under the current account, with support for filtering by name and tags.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--name` | string | - | Filter by application name (fuzzy match) |
| `--tag` | string | - | Filter by tag, format `KEY=VALUE` (can be specified multiple times; multiple tags use AND logic) |
| `--offset` | int | - | Pagination start offset (default: 0) |
| `--limit` | int | - | Number of results to return per page (range: 1–200) |
| `--region` | string | - | Region (default: `ap-guangzhou`) |
| `--json` | flag | - | Output in JSON format |
| `--dry-run` | flag | - | Preview request parameters without actually executing |

---

## Usage Examples

#### Query all sub-applications under the current account
```bash
python scripts/vod_describe_sub_app_ids.py
```

#### Filter by name
```bash
python scripts/vod_describe_sub_app_ids.py --name "My App Name"
```

#### Output in JSON format
```bash
python scripts/vod_describe_sub_app_ids.py --json
```

#### dry-run to preview request parameters
```bash
python scripts/vod_describe_sub_app_ids.py \
    --name "My App Name" \
    --tag env=prod \
    --dry-run
```

#### Filter by a single tag
```bash
python scripts/vod_describe_sub_app_ids.py --tag env=prod
```

#### Filter by multiple tags (AND logic)
```bash
python scripts/vod_describe_sub_app_ids.py \
    --tag env=prod \
    --tag team=media
```

#### Paginate and retrieve the first 20 records
```bash
python scripts/vod_describe_sub_app_ids.py \
    --offset 0 \
    --limit 20
```

#### Combined query with name, tags, and pagination
```bash
python scripts/vod_describe_sub_app_ids.py \
    --name "My App Name" \
    --tag env=prod \
    --tag owner=video-team \
    --offset 20 \
    --limit 20
```

#### Save results to a JSON file
```bash
python scripts/vod_describe_sub_app_ids.py --json > sub_apps.json
```

#### Use jq to extract the list of sub-application IDs
```bash
python scripts/vod_describe_sub_app_ids.py --json | jq -r '.Sub AppId Info Set[].Sub AppId'
```

#### Use jq to extract names of enabled sub-applications
```bash
python scripts/vod_describe_sub_app_ids.py --json | \
    jq -r '.Sub AppId Info Set[] | select(.Status == "On") | .Sub AppId Name'
```

#### Query all sub-applications bound to a specific tag and extract region info
```bash
python scripts/vod_describe_sub_app_ids.py \
    --tag env=prod \
    --json | jq -r '.Sub AppId Info Set[] | {name: .Sub AppId Name, regions: .StorageRegions}'
```

---

## Response Field Descriptions

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `Sub AppId Info Set` | object list | Collection of sub-application information |
| `TotalCount` | int | Total number of applications |
| `RequestId` | string | Request ID |

### Sub AppId Info Set (Sub-Application Info)

| Field | Type | Description |
|-------|------|-------------|
| `Sub AppId` | int | Sub-application ID |
| `Sub AppId Name` | string | Sub-application name (preferred field) |
| `Name` | string | Legacy sub-application name field (deprecated; prefer `Sub AppId Name`) |
| `Description` | string | Sub-application description |
| `Status` | string | Sub-application status; common values: `On`, `Off`, `Destroying`, `Destroyed` |
| `Mode` | string | Sub-application mode; common values: `fileid`, `fileid+path` |
| `CreateTime` | string | Creation time (ISO 8601 format) |
| `StorageRegions` | string list | List of enabled storage regions |
| `Tags` | object list | Tag list; each element contains `TagKey` and `TagValue` |

---

## Error Handling

| Error Type | Cause | Recommended Action |
|------------|-------|--------------------|
| Invalid tag format | `--tag` not using `KEY=VALUE` format (missing `=`) | Check tag format, e.g., `env=prod` |
| Empty tag key | Key before `=` in `--tag` is empty | Ensure the key is not empty, e.g., `env=prod` |
| Invalid offset | `--offset` is less than 0 | Use an integer greater than or equal to 0 |
| Invalid limit | `--limit` is out of the 1–200 range | Use an integer between 1 and 200 |

---

## API Reference

| Feature | API | Documentation |
|---------|-----|---------------|
| Query sub-application list | `Describe Sub App Ids` | https://cloud.tencent.com/document/api/266/35152 |
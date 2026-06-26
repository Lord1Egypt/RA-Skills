---
name: youtube-reporting
description: |
  YouTube Reporting API integration with managed OAuth. Schedule and download bulk YouTube Analytics reports as CSV files.
  Use this skill when users want to schedule bulk reporting jobs, list available report types, download daily generated reports, or manage reporting jobs for their YouTube channel.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# YouTube Reporting

Access the YouTube Reporting API with managed OAuth authentication. Schedule bulk reporting jobs that generate daily downloadable CSV reports containing channel or playlist analytics data.

## Quick Start

```bash
# List available report types
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/reportTypes')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/youtube-reporting/{native-api-path}
```

Maton proxies requests to `youtubereporting.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your YouTube Reporting OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=youtube-reporting&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'youtube-reporting'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "youtube-reporting",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple YouTube Reporting connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/reportTypes')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to the YouTube channel(s) associated with the connected Google account.
- Report data is read-only (downloaded CSV files).
- **Job creation and deletion require explicit user approval.** Before creating or deleting a reporting job, confirm the report type and intended effect with the user.

## API Reference

### Report Types

#### List Report Types

```bash
GET /youtube-reporting/v1/reportTypes
```

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageSize` | number | Number of results per page |
| `pageToken` | string | Token for retrieving next page |
| `includeSystemManaged` | boolean | Include system-managed report types (default: `false`) |

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/reportTypes')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "reportTypes": [
    {
      "id": "channel_basic_a3",
      "name": "User activity"
    },
    {
      "id": "channel_demographics_a1",
      "name": "Demographics"
    },
    {
      "id": "channel_device_os_a3",
      "name": "Device and OS"
    },
    {
      "id": "channel_traffic_source_a3",
      "name": "Traffic sources"
    }
  ],
  "nextPageToken": "..."
}
```

**Available Channel Report Types:**

| Report Type ID | Name |
|----------------|------|
| `channel_basic_a3` | User activity |
| `channel_combined_a3` | Combined |
| `channel_demographics_a1` | Demographics |
| `channel_device_os_a3` | Device and OS |
| `channel_annotations_a1` | Annotations |
| `channel_cards_a1` | Cards |
| `channel_end_screens_a1` | End screens |
| `channel_playback_location_a3` | Playback locations |
| `channel_province_a3` | Province |
| `channel_reach_basic_a1` | Reach basic |
| `channel_reach_combined_a1` | Reach combined |
| `channel_sharing_service_a1` | Sharing service |
| `channel_subtitles_a3` | Subtitles |
| `channel_traffic_source_a3` | Traffic sources |

**Available Playlist Report Types:**

| Report Type ID | Name |
|----------------|------|
| `playlist_basic_a2` | Playlist user activity |
| `playlist_combined_a2` | Playlist combined |
| `playlist_device_os_a2` | Playlist device and OS |
| `playlist_playback_location_a2` | Playlist playback locations |
| `playlist_province_a2` | Playlist province |
| `playlist_traffic_source_a2` | Playlist traffic sources |

### Jobs

#### List Jobs

```bash
GET /youtube-reporting/v1/jobs
```

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageSize` | number | Number of results per page |
| `pageToken` | string | Token for retrieving next page |
| `includeSystemManaged` | boolean | Include system-managed jobs (default: `false`) |

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/jobs')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "jobs": [
    {
      "id": "92f0f65f-18c4-4d15-a815-82223ae93ead",
      "reportTypeId": "channel_basic_a3",
      "name": "Test User Activity Report",
      "createTime": "2026-05-04T22:21:48Z"
    }
  ],
  "nextPageToken": "..."
}
```

#### Get Job

```bash
GET /youtube-reporting/v1/jobs/{jobId}
```

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/jobs/{job_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "id": "92f0f65f-18c4-4d15-a815-82223ae93ead",
  "reportTypeId": "channel_basic_a3",
  "name": "Test User Activity Report",
  "createTime": "2026-05-04T22:21:48Z"
}
```

#### Create Job

```bash
POST /youtube-reporting/v1/jobs
Content-Type: application/json

{
  "reportTypeId": "channel_basic_a3",
  "name": "My Daily User Activity Report"
}
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reportTypeId` | string | Yes | Report type ID from `reportTypes.list` |
| `name` | string | Yes | Display name for the job |

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "reportTypeId": "channel_basic_a3",
    "name": "Daily User Activity"
}).encode()
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/jobs', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "id": "92f0f65f-18c4-4d15-a815-82223ae93ead",
  "reportTypeId": "channel_basic_a3",
  "name": "Daily User Activity",
  "createTime": "2026-05-04T22:21:48.331114Z"
}
```

#### Delete Job

```bash
DELETE /youtube-reporting/v1/jobs/{jobId}
```

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/jobs/{job_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
resp = urllib.request.urlopen(req)
print(f"Status: {resp.status}")
EOF
```

Returns empty response on success.

### Reports

#### List Reports for a Job

```bash
GET /youtube-reporting/v1/jobs/{jobId}/reports
```

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `createdAfter` | string | Filter reports created after this timestamp (RFC3339 UTC) |
| `startTimeAtOrAfter` | string | Filter by report data start time (on or after) |
| `startTimeBefore` | string | Filter by report data start time (before) |
| `pageSize` | number | Number of results per page |
| `pageToken` | string | Token for retrieving next page |

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/jobs/{job_id}/reports')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "reports": [
    {
      "id": "report-id-123",
      "startTime": "2025-04-01T07:00:00Z",
      "endTime": "2025-04-02T07:00:00Z",
      "downloadUrl": "https://youtubereporting.googleapis.com/...",
      "createTime": "2025-04-02T10:00:00Z"
    }
  ],
  "nextPageToken": "..."
}
```

#### Get Report

```bash
GET /youtube-reporting/v1/jobs/{jobId}/reports/{reportId}
```

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-reporting/v1/jobs/{job_id}/reports/{report_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Download Report

Reports provide a `downloadUrl` that returns a CSV file. Download via an authorized GET request:

```bash
python <<'EOF'
import urllib.request, os
req = urllib.request.Request('{download_url}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode('utf-8')
    print(data[:2000])
EOF
```

## Pagination

All list endpoints use token-based pagination:

```bash
GET /youtube-reporting/v1/reportTypes?pageSize=5&pageToken={nextPageToken}
```

Response includes `nextPageToken` when more results exist:

```json
{
  "reportTypes": [...],
  "nextPageToken": "channel_device_os_a3"
}
```

Pass the `nextPageToken` value as `pageToken` in the next request to retrieve subsequent pages.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/youtube-reporting/v1/jobs',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.jobs);
```

### Python

```python
import os
import requests

# List all jobs
response = requests.get(
    'https://api.maton.ai/youtube-reporting/v1/jobs',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
jobs = response.json().get('jobs', [])

# List reports for first job
if jobs:
    reports_resp = requests.get(
        f'https://api.maton.ai/youtube-reporting/v1/jobs/{jobs[0]["id"]}/reports',
        headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
    )
    print(reports_resp.json())
```

## Notes

- Reports are generated daily; the first report is available within 24 hours of job creation
- Report data covers a single day (startTime to endTime spans 24 hours)
- Downloaded reports are CSV files with headers in the first row
- A job with a given `reportTypeId` can only exist once; creating a duplicate returns 409 Conflict
- System-managed jobs are auto-generated by YouTube and cannot be created or deleted (403 Forbidden)
- After deleting a job, previously generated reports remain downloadable for up to 60 days
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request (missing name or reportTypeId, invalid reportTypeId, deprecated report type) |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden (cannot create/delete system-managed jobs) |
| 404 | Job or report not found |
| 409 | Conflict (job with same reportTypeId already exists) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from YouTube Reporting API |

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `youtube-reporting`. For example:

- Correct: `https://api.maton.ai/youtube-reporting/v1/jobs`
- Incorrect: `https://api.maton.ai/v1/jobs`

## Resources

- [YouTube Reporting API Overview](https://developers.google.com/youtube/reporting)
- [YouTube Reporting API Reference](https://developers.google.com/youtube/reporting/v1/reference/rest)
- [Bulk Reports](https://developers.google.com/youtube/reporting/v1/reports)
- [Report Types](https://developers.google.com/youtube/reporting/v1/report_types)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)

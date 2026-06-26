---
name: youtube-analytics
description: |
  YouTube Analytics API integration with managed OAuth. Retrieve channel analytics reports and manage video/playlist/channel groups.
  Use this skill when users want to query YouTube channel metrics (views, watch time, subscribers), analyze performance by dimension (day, country, video), or manage analytics groups.
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

# YouTube Analytics

Access the YouTube Analytics API with managed OAuth authentication. Retrieve channel performance reports (views, watch time, subscribers, revenue) and manage analytics groups for aggregating videos, playlists, or channels.

## Quick Start

```bash
# Get channel views and watch time for the last 30 days
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-analytics/v2/reports?ids=channel==MINE&startDate=2025-04-01&endDate=2025-04-30&metrics=views,estimatedMinutesWatched,averageViewDuration')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/youtube-analytics/{native-api-path}
```

Maton proxies requests to `youtubeanalytics.googleapis.com` and automatically injects your OAuth token.

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

Manage your YouTube Analytics OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=youtube-analytics&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'youtube-analytics'}).encode()
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
    "app": "youtube-analytics",
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

If you have multiple YouTube Analytics connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-analytics/v2/reports?ids=channel==MINE&startDate=2025-01-01&endDate=2025-01-31&metrics=views')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to the YouTube channel(s) associated with the connected Google account.
- Reports are read-only and do not modify channel data.
- **Group management operations (create, update, delete) require explicit user approval.** Before executing any group or group item modification, confirm the target resource and intended effect with the user.

## API Reference

### Reports

#### Query Reports

```bash
GET /youtube-analytics/v2/reports?ids={channel_id}&startDate={start}&endDate={end}&metrics={metrics}
```

**Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | string | Channel identifier: `channel==MINE` or `channel==CHANNEL_ID` |
| `startDate` | string | Start date in `YYYY-MM-DD` format |
| `endDate` | string | End date in `YYYY-MM-DD` format |
| `metrics` | string | Comma-separated metrics (e.g., `views,likes,comments`) |

**Optional Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `dimensions` | string | Comma-separated dimensions (e.g., `day`, `month`, `country`, `video`) |
| `filters` | string | Filters in format `dimension==value` (e.g., `country==US`) |
| `sort` | string | Sort field; prefix with `-` for descending (e.g., `-views`) |
| `maxResults` | integer | Maximum rows to return |
| `startIndex` | integer | 1-based pagination start index |
| `currency` | string | ISO 4217 currency code for revenue metrics (default: USD) |

**Example - Daily views for a month:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-analytics/v2/reports?ids=channel==MINE&startDate=2025-03-01&endDate=2025-03-31&metrics=views,estimatedMinutesWatched,averageViewDuration&dimensions=day&sort=-views&maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Example - Monthly summary:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube-analytics/v2/reports?ids=channel==MINE&startDate=2024-01-01&endDate=2024-12-01&metrics=views,likes,shares,subscribersGained,subscribersLost&dimensions=month&sort=-views')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "kind": "youtubeAnalytics#resultTable",
  "columnHeaders": [
    {
      "name": "day",
      "columnType": "DIMENSION",
      "dataType": "STRING"
    },
    {
      "name": "views",
      "columnType": "METRIC",
      "dataType": "INTEGER"
    }
  ],
  "rows": [
    ["2025-03-12", 4],
    ["2025-03-15", 2]
  ]
}
```

**Common Metrics:**
- `views` - Total video views
- `likes` - Total likes
- `dislikes` - Total dislikes
- `comments` - Total comments
- `shares` - Total shares
- `estimatedMinutesWatched` - Total watch time in minutes
- `averageViewDuration` - Average view duration in seconds
- `subscribersGained` - New subscribers gained
- `subscribersLost` - Subscribers lost
- `averageViewPercentage` - Average percentage of video watched
- `cardClickRate` - Card click rate

**Common Dimensions:**
- `day` - Daily aggregation (YYYY-MM-DD)
- `month` - Monthly aggregation (YYYY-MM); endDate must align to 1st of month
- `country` - ISO 3166-1 alpha-2 country code
- `video` - Per-video breakdown
- `deviceType` - Device type (DESKTOP, MOBILE, TABLET, TV, etc.)
- `operatingSystem` - OS (ANDROID, IOS, WINDOWS, etc.)
- `liveOrOnDemand` - LIVE or ON_DEMAND
- `subscribedStatus` - SUBSCRIBED or UNSUBSCRIBED

### Groups

#### List Groups

```bash
GET /youtube-analytics/v2/groups?mine=true
```

Or by specific IDs:

```bash
GET /youtube-analytics/v2/groups?id={group_id}
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `mine` | boolean | Set to `true` to retrieve all groups owned by authenticated user |
| `id` | string | Comma-separated group IDs to retrieve |
| `pageToken` | string | Token for paginating results |

**Response:**
```json
{
  "kind": "youtube#groupListResponse",
  "items": [
    {
      "kind": "youtube#group",
      "etag": "CQVfQEQY1xqZ2O8xKat5QfS2cik",
      "id": "JiAz5ne9Wwk",
      "snippet": {
        "title": "My Video Group",
        "publishedAt": "2026-05-04T22:02:12Z"
      },
      "contentDetails": {
        "itemType": "youtube#video"
      }
    }
  ],
  "nextPageToken": "..."
}
```

#### Create Group

```bash
POST /youtube-analytics/v2/groups
Content-Type: application/json

{
  "snippet": {
    "title": "My New Group"
  },
  "contentDetails": {
    "itemType": "youtube#video"
  }
}
```

**Valid item types:** `youtube#video`, `youtube#playlist`, `youtube#channel`, `youtubePartner#asset`

**Example:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "snippet": {"title": "Top Performers"},
    "contentDetails": {"itemType": "youtube#video"}
}).encode()
req = urllib.request.Request('https://api.maton.ai/youtube-analytics/v2/groups', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### Update Group

```bash
PUT /youtube-analytics/v2/groups
Content-Type: application/json

{
  "id": "{group_id}",
  "snippet": {
    "title": "Updated Title"
  },
  "contentDetails": {
    "itemType": "youtube#video"
  }
}
```

Only the group title can be updated.

#### Delete Group

```bash
DELETE /youtube-analytics/v2/groups?id={group_id}
```

### Group Items

#### List Group Items

```bash
GET /youtube-analytics/v2/groupItems?groupId={group_id}
```

**Response:**
```json
{
  "kind": "youtube#groupItemListResponse",
  "etag": "...",
  "items": [
    {
      "kind": "youtube#groupItem",
      "etag": "...",
      "groupId": "JiAz5ne9Wwk",
      "resource": {
        "kind": "youtube#video",
        "id": "VIDEO_ID"
      }
    }
  ]
}
```

#### Add Item to Group

```bash
POST /youtube-analytics/v2/groupItems
Content-Type: application/json

{
  "groupId": "{group_id}",
  "resource": {
    "kind": "youtube#video",
    "id": "{video_id}"
  }
}
```

Returns 201 on success, 204 if item already exists in group. Maximum 500 items per group.

#### Remove Item from Group

```bash
DELETE /youtube-analytics/v2/groupItems?id={group_item_id}
```

## Pagination

### Reports

Use `startIndex` and `maxResults` for paginating report results:

```bash
GET /youtube-analytics/v2/reports?ids=channel==MINE&startDate=2025-01-01&endDate=2025-03-31&metrics=views&dimensions=day&maxResults=30&startIndex=1
```

`startIndex` is 1-based. Increment by `maxResults` for subsequent pages.

### Groups

Use token-based pagination:

```bash
GET /youtube-analytics/v2/groups?mine=true&pageToken={nextPageToken}
```

Response includes `nextPageToken` when more results exist.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/youtube-analytics/v2/reports?ids=channel==MINE&startDate=2025-01-01&endDate=2025-01-31&metrics=views,likes,comments&dimensions=day&sort=-views',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.rows);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/youtube-analytics/v2/reports',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={
        'ids': 'channel==MINE',
        'startDate': '2025-01-01',
        'endDate': '2025-01-31',
        'metrics': 'views,likes,comments',
        'dimensions': 'day',
        'sort': '-views'
    }
)
data = response.json()
for row in data.get('rows', []):
    print(row)
```

## Notes

- Dates must be in `YYYY-MM-DD` format
- When using `month` dimension, `endDate` must align to the 1st of a month (e.g., `2024-12-01` not `2024-12-31`)
- `ids=channel==MINE` uses the authenticated user's channel; use `channel==CHANNEL_ID` for a specific channel
- Groups can contain a maximum of 500 items, all of the same resource type
- Only the group title can be updated via `groups.update`; use `groupItems` methods to manage membership
- Adding items to a group requires the items to be owned by the authenticated channel
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request (invalid date range, misaligned month dimension, missing required params) |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden (insufficient permissions or trying to add items not owned by channel) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from YouTube Analytics API |

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

1. Ensure your URL path starts with `youtube-analytics`. For example:

- Correct: `https://api.maton.ai/youtube-analytics/v2/reports?...`
- Incorrect: `https://api.maton.ai/v2/reports?...`

## Resources

- [YouTube Analytics API Overview](https://developers.google.com/youtube/analytics)
- [YouTube Analytics API Reference](https://developers.google.com/youtube/analytics/reference)
- [Channel Reports](https://developers.google.com/youtube/analytics/channel_reports)
- [Available Metrics](https://developers.google.com/youtube/analytics/metrics)
- [Available Dimensions](https://developers.google.com/youtube/analytics/dimensions)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)

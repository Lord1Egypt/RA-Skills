---
name: youtube
description: |
  YouTube Data API integration with managed OAuth. Search videos, manage playlists, access channel data, and interact with comments. Use this skill when users want to interact with YouTube. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# YouTube

Access the YouTube Data API v3 with managed OAuth authentication. Search videos, manage playlists, access channel information, and interact with comments and subscriptions.

## Quick Start

**CLI:**

```bash
maton youtube search videos 'coding tutorial' --limit 10
```

```bash
maton api '/youtube/youtube/v3/search?part=snippet&q=coding+tutorial&type=video&maxResults=10'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube/youtube/v3/search?part=snippet&q=coding+tutorial&type=video&maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/youtube/{native-api-path}
```

Maton proxies requests to `www.googleapis.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton-ai/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Google OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list youtube --status ACTIVE
```

```bash
maton api -X GET /connections -f app=youtube -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=youtube&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create youtube
```

```bash
maton api /connections -f app=youtube
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'youtube'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

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
    "app": "youtube",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple YouTube connections, specify which one to use:

**CLI:**

```bash
maton youtube channel mine --connection {connection_id}
```

```bash
maton api '/youtube/youtube/v3/channels?part=snippet&mine=true' --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/youtube/youtube/v3/channels?part=snippet&mine=true')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to videos, channels, playlists, comments, and captions within the connected YouTube account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Search

#### Search Videos, Channels, or Playlists

```bash
GET /youtube/youtube/v3/search
```

Query parameters:
- `part` - Required: `snippet`
- `q` - Search query
- `type` - Filter by type: `video`, `channel`, `playlist`
- `maxResults` - Results per page (1-50, default 5)
- `order` - Sort order: `date`, `rating`, `relevance`, `title`, `viewCount`
- `publishedAfter` - Filter by publish date (RFC 3339)
- `publishedBefore` - Filter by publish date (RFC 3339)
- `channelId` - Filter by channel
- `videoDuration` - `short` (<4min), `medium` (4-20min), `long` (>20min)
- `pageToken` - Pagination token

Example:

```bash
maton youtube search videos 'machine learning' --limit 10 --order viewCount
```

```bash
maton youtube search channels 'rob pike'
```

```bash
maton youtube search playlists 'study music'
```

### Videos

#### Get Video Details

```bash
GET /youtube/youtube/v3/videos?part=snippet,statistics,contentDetails&id=dQw4w9WgXcQ
```

Parts available:
- `snippet` - Title, description, thumbnails, channel info
- `statistics` - View count, likes, comments
- `contentDetails` - Duration, dimension, definition
- `status` - Upload status, privacy status
- `player` - Embedded player HTML

Example:

```bash
maton youtube video view dQw4w9WgXcQ
```

#### Get My Videos (Uploaded)

```bash
GET /youtube/youtube/v3/search?part=snippet&forMine=true&type=video&order=viewCount&maxResults=25
```

Example:

```bash
maton youtube search mine --order viewCount --limit 25
```

#### Rate Video (Like/Dislike)

```bash
POST /youtube/youtube/v3/videos/rate?id=dQw4w9WgXcQ&rating=like
```

Rating values: `like`, `dislike`, `none`

Example:

```bash
maton youtube video rate dQw4w9WgXcQ --rating like
```

#### Get Trending Videos

```bash
GET /youtube/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=10
```

Example:

```bash
maton youtube video list --region US --limit 10
```

#### Get Video Categories

```bash
GET /youtube/youtube/v3/videoCategories?part=snippet&regionCode=US
```

Example:

```bash
maton youtube video-category list --region US
```

### Channels

#### Get Channel Details

```bash
GET /youtube/youtube/v3/channels?part=snippet,statistics,contentDetails&id=UCBJycsmduvYEL83R_U4JriQ
```

Example:

```bash
maton youtube channel view UCBJycsmduvYEL83R_U4JriQ
```

#### Get My Channel

```bash
GET /youtube/youtube/v3/channels?part=snippet,statistics,contentDetails&mine=true
```

Example:

```bash
maton youtube channel mine
```

**Response:**
```json
{
  "items": [
    {
      "id": "UCxyz123",
      "snippet": {
        "title": "My Channel",
        "description": "Channel description",
        "customUrl": "@mychannel",
        "publishedAt": "2020-01-01T00:00:00Z",
        "thumbnails": {...}
      },
      "statistics": {
        "viewCount": "1000000",
        "subscriberCount": "50000",
        "videoCount": "100"
      },
      "contentDetails": {
        "relatedPlaylists": {
          "uploads": "UUxyz123"
        }
      }
    }
  ]
}
```

#### Get Channel by Username

```bash
GET /youtube/youtube/v3/channels?part=snippet,statistics&forUsername=GoogleDevelopers
```

Example:

```bash
maton youtube channel view --username GoogleDevelopers
```

To look up by `@handle` instead, use `maton youtube channel view --handle GoogleDevelopers`.

### Playlists

#### List My Playlists

```bash
GET /youtube/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults=25
```

Example:

```bash
maton youtube playlist list --limit 25
```

#### Get Playlist

```bash
GET /youtube/youtube/v3/playlists?part=snippet,contentDetails&id={playlistId}
```

Example:

```bash
maton youtube playlist view {playlistId}
```

#### Create Playlist

```bash
POST /youtube/youtube/v3/playlists?part=snippet,status
Content-Type: application/json

{
  "snippet": {
    "title": "My New Playlist",
    "description": "A collection of videos",
    "defaultLanguage": "en"
  },
  "status": {
    "privacyStatus": "private"
  }
}
```

Privacy values: `public`, `private`, `unlisted`

Example:

```bash
maton youtube playlist create --title 'My New Playlist' --description 'A collection of videos' --privacy private
```

#### Update Playlist

```bash
PUT /youtube/youtube/v3/playlists?part=snippet,status
Content-Type: application/json

{
  "id": "PLxyz123",
  "snippet": {
    "title": "Updated Playlist Title",
    "description": "Updated description"
  },
  "status": {
    "privacyStatus": "public"
  }
}
```

Example:

```bash
maton youtube playlist update PLxyz123 --title 'Updated Playlist Title' --description 'Updated description' --privacy public
```

#### Delete Playlist

```bash
DELETE /youtube/youtube/v3/playlists?id=PLxyz123
```

Example:

```bash
maton youtube playlist delete PLxyz123
```

### Playlist Items

#### List Playlist Items

```bash
GET /youtube/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={playlistId}&maxResults=50
```

Example:

```bash
maton youtube playlist items {playlistId} --limit 50
```

#### Add Video to Playlist

```bash
POST /youtube/youtube/v3/playlistItems?part=snippet
Content-Type: application/json

{
  "snippet": {
    "playlistId": "PLxyz123",
    "resourceId": {
      "kind": "youtube#video",
      "videoId": "abc123xyz"
    },
    "position": 0
  }
}
```

Example:

```bash
maton youtube playlist add-video --playlist PLxyz123 --video abc123xyz --position 0
```

#### Remove from Playlist

```bash
DELETE /youtube/youtube/v3/playlistItems?id=UEx5dGVzdAAA
```

Example:

```bash
maton youtube playlist remove-video UEx5dGVzdAAA
```

The argument is the **playlistItem ID** (from `maton youtube playlist items {playlistId}`), not the video ID.

### Subscriptions

#### List My Subscriptions

```bash
GET /youtube/youtube/v3/subscriptions?part=snippet&mine=true&maxResults=50
```

Example:

```bash
maton youtube subscription list --limit 50
```

#### Check Subscription to Channel

```bash
GET /youtube/youtube/v3/subscriptions?part=snippet&mine=true&forChannelId={channelId}
```

Example:

```bash
maton youtube subscription list --for-channel {channelId}
```

The response is empty when no subscription exists.

#### Subscribe to Channel

```bash
POST /youtube/youtube/v3/subscriptions?part=snippet
Content-Type: application/json

{
  "snippet": {
    "resourceId": {
      "kind": "youtube#channel",
      "channelId": "UCxyz123"
    }
  }
}
```

Example:

```bash
maton youtube subscription create --channel UCxyz123
```

#### Unsubscribe

```bash
DELETE /youtube/youtube/v3/subscriptions?id={subscriptionId}
```

Example:

```bash
maton youtube subscription delete {subscriptionId}
```

The argument is the **subscription ID** (from `maton youtube subscription list`), not the channel ID.

### Comments

#### List Video Comments

```bash
GET /youtube/youtube/v3/commentThreads?part=snippet,replies&videoId={videoId}&order=time&maxResults=100
```

Example:

```bash
maton youtube comment list --video {videoId} --order time --limit 100
```

#### Add Comment to Video

```bash
POST /youtube/youtube/v3/commentThreads?part=snippet
Content-Type: application/json

{
  "snippet": {
    "videoId": "{videoId}",
    "topLevelComment": {
      "snippet": {
        "textOriginal": "Great video!"
      }
    }
  }
}
```

Example:

```bash
maton youtube comment create --video {videoId} --text 'Great video!'
```

#### Reply to Comment

```bash
POST /youtube/youtube/v3/comments?part=snippet
Content-Type: application/json

{
  "snippet": {
    "parentId": "{commentId}",
    "textOriginal": "Thanks for your comment!"
  }
}
```

Example:

```bash
maton youtube comment create --parent {commentId} --text 'Thanks for your comment!'
```

#### Delete Comment

```bash
DELETE /youtube/youtube/v3/comments?id={commentId}
```

Example:

```bash
maton youtube comment delete {commentId}
```

## Pagination

YouTube uses cursor-based pagination via `pageToken`. The CLI automatically paginates with `--paginate`.

Example:

```bash
maton youtube playlist items {playlistId} --paginate
```

## Code Examples

### CLI

```bash
# Search videos as JSON (default format)
maton youtube search videos 'tutorial' --limit 10

# Filter with jq — e.g., extract just video IDs and titles
# Note: --jq requires --json
maton youtube search videos 'tutorial' --limit 10 \
  --json --jq '.items[] | {id: .id.videoId, title: .snippet.title}'

# List your playlists and extract titles only
maton youtube playlist list --json --jq '.items[].snippet.title'
```

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`
};

// Search videos
const results = await fetch(
  'https://api.maton.ai/youtube/youtube/v3/search?part=snippet&q=tutorial&type=video&maxResults=10',
  { headers }
).then(r => r.json());

// Get video details
const video = await fetch(
  'https://api.maton.ai/youtube/youtube/v3/videos?part=snippet,statistics&id=dQw4w9WgXcQ',
  { headers }
).then(r => r.json());

// Create playlist
await fetch(
  'https://api.maton.ai/youtube/youtube/v3/playlists?part=snippet,status',
  {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      snippet: { title: 'My Playlist', description: 'Videos I like' },
      status: { privacyStatus: 'private' }
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Search videos
results = requests.get(
    'https://api.maton.ai/youtube/youtube/v3/search',
    headers=headers,
    params={'part': 'snippet', 'q': 'tutorial', 'type': 'video', 'maxResults': 10}
).json()

# Get video details
video = requests.get(
    'https://api.maton.ai/youtube/youtube/v3/videos',
    headers=headers,
    params={'part': 'snippet,statistics', 'id': 'dQw4w9WgXcQ'}
).json()

# Create playlist
response = requests.post(
    'https://api.maton.ai/youtube/youtube/v3/playlists?part=snippet,status',
    headers=headers,
    json={
        'snippet': {'title': 'My Playlist', 'description': 'Videos I like'},
        'status': {'privacyStatus': 'private'}
    }
)
```

## Notes

- Video IDs are 11 characters (e.g., `dQw4w9WgXcQ`)
- Channel IDs start with `UC` (e.g., `UCxyz123`)
- Playlist IDs start with `PL` (user) or `UU` (uploads)
- Use `pageToken` for pagination through large result sets
- The `part` parameter is required and determines what data is returned
- Quota costs vary by endpoint - search is expensive (100 units), reads are cheap (1 unit)
- Some write operations require channel verification
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing YouTube connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden - quota exceeded or insufficient permissions |
| 404 | Video, channel, or playlist not found |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from YouTube API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

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

1. Ensure your URL path starts with `youtube`. For example:

- Correct: `https://api.maton.ai/youtube/youtube/v3/search`
- Incorrect: `https://api.maton.ai/v3/search`

## Resources

- [YouTube Data API Overview](https://developers.google.com/youtube/v3)
- [Search](https://developers.google.com/youtube/v3/docs/search/list)
- [Videos](https://developers.google.com/youtube/v3/docs/videos)
- [Channels](https://developers.google.com/youtube/v3/docs/channels)
- [Playlists](https://developers.google.com/youtube/v3/docs/playlists)
- [PlaylistItems](https://developers.google.com/youtube/v3/docs/playlistItems)
- [Subscriptions](https://developers.google.com/youtube/v3/docs/subscriptions)
- [Comments](https://developers.google.com/youtube/v3/docs/comments)
- [Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)

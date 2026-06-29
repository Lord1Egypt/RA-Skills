# SoundCloud API Endpoints Reference

## Base URL
```
https://api.soundcloud.com
```

## Authentication

### Client ID (Public API)
```
?client_id=YOUR_CLIENT_ID
```
- Required for all public API calls
- Get from https://soundcloud.com/you/apps

### OAuth 2.0 (Authenticated API)
```
Authorization: OAuth YOUR_ACCESS_TOKEN
```
- Required for user-specific actions
- Scope: `non-expiring` for permanent access

## Core Endpoints

### Tracks

#### Search Tracks
```
GET /tracks
```
**Parameters:**
- `q` - Search query
- `genres` - Filter by genre
- `bpm[from]` / `bpm[to]` - BPM range
- `duration[from]` / `duration[to]` - Duration in milliseconds
- `created_at[from]` - Filter by creation date
- `tags` - Filter by tags
- `filter` - `public` or `all` (requires auth)
- `license` - Filter by license
- `limit` - Results per page (max 200)
- `offset` - Pagination offset
- `linked_partitioning` - Enable pagination

**Example:**
```bash
curl -X GET "https://api.soundcloud.com/tracks?q=lofi&genres=chillhop&bpm[from]=70&bpm[to]=90&client_id=CLIENT_ID&limit=10"
```

#### Get Track
```
GET /tracks/{track_id}
```
**Response includes:**
- Basic metadata (title, description, duration)
- User information (artist)
- Stats (plays, likes, reposts, comments)
- URLs (stream, download, artwork)
- Audio metadata (BPM, key, genre, tags)
- License and permissions

#### Resolve Track URL
```
GET /resolve
```
**Parameters:**
- `url` - SoundCloud track URL

**Example:**
```bash
curl -X GET "https://api.soundcloud.com/resolve?url=https://soundcloud.com/artist/track&client_id=CLIENT_ID"
```

### Playlists

#### Get Playlist
```
GET /playlists/{playlist_id}
```
**Parameters:**
- `show_tracks` - Include track details (default: true)

#### Create Playlist (Authenticated)
```
POST /playlists
```
**Required payload:**
```json
{
  "playlist": {
    "title": "Playlist Name",
    "sharing": "public",
    "tracks": [
      {"id": 123},
      {"id": 456}
    ]
  }
}
```

#### Update Playlist (Authenticated)
```
PUT /playlists/{playlist_id}
```
**Updateable fields:**
- `title`
- `description`
- `sharing` (`public` or `private`)
- `genre`
- `tag_list`
- `tracks` (array of track objects)

#### Delete Playlist (Authenticated)
```
DELETE /playlists/{playlist_id}
```

### Users

#### Get User
```
GET /users/{user_id}
```
**Alternative:**
```
GET /resolve?url=https://soundcloud.com/username
```

#### Get User's Tracks
```
GET /users/{user_id}/tracks
```
**Parameters:**
- `limit`, `offset` - Pagination
- `linked_partitioning` - Enable pagination

#### Get User's Playlists
```
GET /users/{user_id}/playlists
```
**Parameters:**
- `show_tracks` - Include track details
- `public` - Only public playlists

#### Get User's Favorites/Likes
```
GET /users/{user_id}/favorites
```

#### Get User's Followings
```
GET /users/{user_id}/followings
```

#### Get User's Followers
```
GET /users/{user_id}/followers
```

### Me (Authenticated User)

#### Get Current User
```
GET /me
```
**Requires:** OAuth token

#### Get My Tracks
```
GET /me/tracks
```
**Includes:** Private tracks

#### Get My Playlists
```
GET /me/playlists
```
**Includes:** Private playlists

#### Get My Favorites
```
GET /me/favorites
```

#### Like/Unlike Track
```
PUT /me/favorites/{track_id}    # Like
DELETE /me/favorites/{track_id} # Unlike
```

#### Follow/Unfollow User
```
PUT /me/followings/{user_id}    # Follow
DELETE /me/followings/{user_id} # Unfollow
```

#### Repost Track
```
POST /me/track_reposts/{track_id}
```

## Search & Discovery

### General Search
```
GET /search
```
**Parameters:**
- `q` - Search query
- `limit` - Results per page
- `offset` - Pagination
- `linked_partitioning` - Enable pagination

### Search by Type
```
GET /search/tracks
GET /search/users
GET /search/playlists
GET /search/groups
```

**Example - Search users:**
```bash
curl -X GET "https://api.soundcloud.com/search/users?q=producer&client_id=CLIENT_ID&limit=10"
```

## Comments

### Get Track Comments
```
GET /tracks/{track_id}/comments
```
**Parameters:**
- `threaded` - Thread comments (default: false)
- `limit`, `offset` - Pagination

### Post Comment (Authenticated)
```
POST /tracks/{track_id}/comments
```
**Payload:**
```json
{
  "comment": {
    "body": "Great track!",
    "timestamp": 15000
  }
}
```

## OEmbed

### Get oEmbed Data
```
GET /oembed
```
**Parameters:**
- `url` - SoundCloud URL
- `format` - `json` or `xml`
- `maxwidth` / `maxheight` - Embed size
- `color` - Hex color for player
- `auto_play` - `true` or `false`
- `show_comments` - `true` or `false`
- `show_user` - `true` or `false`

**Example:**
```bash
curl -X GET "https://soundcloud.com/oembed?url=https://soundcloud.com/artist/track&format=json"
```

## Webhooks (Pro/Enterprise)

### Create Webhook
```
POST /webhooks
```
**Payload:**
```json
{
  "webhook": {
    "event": "track.created",
    "url": "https://your-server.com/webhook"
  }
}
```

### Available Events:
- `track.created` - New track uploaded
- `track.updated` - Track metadata changed
- `track.deleted` - Track deleted
- `playlist.created` - New playlist
- `playlist.updated` - Playlist modified
- `playlist.deleted` - Playlist deleted
- `user.followed` - User followed
- `user.unfollowed` - User unfollowed

## Rate Limits

### Public API (Client ID)
- ~5000 requests per day
- No strict per-minute limit
- Varies by app tier

### Authenticated API (OAuth)
- Higher limits than public API
- Pro/Enterprise: Increased limits
- Implement exponential backoff for 429

### Headers to Monitor:
- `X-RateLimit-Limit` - Requests per period
- `X-RateLimit-Remaining` - Remaining requests
- `X-RateLimit-Reset` - Reset timestamp

## Error Codes

### Common HTTP Status Codes

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| 200 | OK | Success |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing/invalid client_id or token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | SoundCloud API issue |
| 503 | Service Unavailable | API maintenance |

### Error Response Format
```json
{
  "error": "Invalid client identifier",
  "error_description": "The client identifier provided is invalid."
}
```

## Pagination

### Linked Partitioning
Enable with `linked_partitioning=true`

**Response includes:**
```json
{
  "collection": [...],
  "next_href": "https://api.soundcloud.com/...&offset=50",
  "future_href": "..."
}
```

### Manual Pagination
Use `limit` and `offset` parameters:
- `limit` - Items per page (max 200)
- `offset` - Starting position

**Example - Page 3 with 50 items per page:**
```bash
curl -X GET "https://api.soundcloud.com/tracks?client_id=CLIENT_ID&limit=50&offset=100"
```

## Best Practices

### 1. Efficient Requests
- Use `fields` parameter to request only needed data
- Cache responses when possible
- Batch operations for multiple items

### 2. Error Handling
- Always check HTTP status codes
- Implement retry logic for 5xx errors
- Use exponential backoff for rate limits

### 3. Data Freshness
- Track metadata can change (plays, likes)
- Consider cache duration based on use case
- Use webhooks for real-time updates (Pro/Enterprise)

### 4. User Experience
- Show loading states during API calls
- Handle network errors gracefully
- Provide fallback content when data unavailable

## Example Workflows

### 1. Track Discovery Pipeline
```bash
# 1. Search for tracks
GET /tracks?q=ambient&genres=electronic&limit=50

# 2. Filter by engagement
# (client-side filtering based on plays/likes)

# 3. Get detailed metadata for selected tracks
GET /tracks/{id1}
GET /tracks/{id2}
# ... or batch requests
```

### 2. User Profile Analysis
```bash
# 1. Resolve username to ID
GET /resolve?url=https://soundcloud.com/username

# 2. Get user info
GET /users/{user_id}

# 3. Get user's top tracks
GET /users/{user_id}/tracks?limit=100&order=hotness

# 4. Get user's playlists
GET /users/{user_id}/playlists?show_tracks=true
```

### 3. Playlist Creation Flow
```bash
# 1. Search for candidate tracks
GET /tracks?q=study&genres=lofi&bpm[from]=60&bpm[to]=80&limit=100

# 2. Create playlist (authenticated)
POST /playlists
{
  "playlist": {
    "title": "Study Focus",
    "sharing": "public",
    "tracks": [...]
  }
}

# 3. Update playlist (add/remove tracks)
PUT /playlists/{playlist_id}
{
  "playlist": {
    "tracks": [...]
  }
}
```

## Tools & SDKs

### Official SDKs
- **JavaScript:** `soundcloud-api.js` (browser/Node.js)
- **Python:** `soundcloud` package (PyPI)
- **Ruby:** `soundcloud` gem

### Community Libraries
- **PHP:** `soundcloud/soundcloud`
- **Java:** `soundcloud-api`
- **.NET:** `SoundCloud.NET`

### Command Line Tools
- **soundcloud-dl:** Download tracks
- **scdl:** SoundCloud downloader
- **soundcloud-api-cli:** CLI wrapper

## Additional Resources

- [Official Documentation](https://developers.soundcloud.com/docs)
- [API Explorer](https://developers.soundcloud.com/docs/api/explorer/open-api)
- [GitHub Issues](https://github.com/soundcloud/api/issues)
- [Community Forum](https://community.soundcloud.com/c/developers)
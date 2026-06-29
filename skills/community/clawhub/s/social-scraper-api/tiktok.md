# TikTok API — ClaWHub / EnsembleData

> Real-time TikTok data scraping for publicly available content.  
> **Base URL:** `https://ensembledata.com/apis`  
> **Prefix:** `/tt/`  
> **Auth:** `?token=YOUR_TOKEN` on every request

---

## Endpoints

### 1. Hashtag Search
`GET /tt/hashtag/posts`

Fetches a page of posts (~20) containing a given hashtag directly from `tiktok.com/tag/{name}`.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Hashtag without `#`, e.g. `magic` |
| `cursor` | integer | — | Pagination cursor (default `0`). Increment by 20 per page. Max ~4000–5000. |
| `token` | string | ✅ | API token |

**Response shape:**
```json
{
  "data": {
    "nextCursor": 20,
    "data": [ /* array of post objects */ ]
  }
}
```

**Example:**
```python
import requests
res = requests.get("https://ensembledata.com/apis/tt/hashtag/posts", params={
    "name": "magic", "cursor": 0, "token": "YOUR-TOKEN"
})
```

---

### 2. Full Hashtag Search
`GET /tt/hashtag/posts/full`

Convenience wrapper that calls Hashtag Search repeatedly to collect all posts from the last N days. Internally iterates the cursor up to `max_depth` times (max 250, ~5000 posts).

**Cost:** `max_depth / 10` units (discounted vs manual pagination). Min 1 unit if hashtag doesn't exist.

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Hashtag without `#` |
| `days` | integer | ✅ | Only return posts from last N days |
| `max_depth` | integer | ✅ | Max number of internal calls (1–250) |
| `token` | string | ✅ | API token |

---

### 3. Keyword Search
`GET /tt/keyword/search`

Searches TikTok posts by keyword. Returns ~20 results per call.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search keyword |
| `cursor` | integer | — | Pagination cursor (default `0`) |
| `token` | string | ✅ | API token |

---

### 4. Full Keyword Search
`GET /tt/keyword/search/full`

Bulk version of Keyword Search — collects all results up to `max_depth` pages.

**Cost:** `max_depth / 10` units

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search keyword |
| `max_depth` | integer | ✅ | Max internal calls (1–250) |
| `token` | string | ✅ | API token |

---

### 5. User Posts From Username
`GET /tt/user/posts`

Returns a page of posts for a TikTok user identified by username.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | TikTok username (without `@`) |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 6. User Posts From SecUID
`GET /tt/user/posts/from-secuid`

Same as above but identified by internal `secuid`.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `secuid` | string | ✅ | TikTok user secuid |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 7. User Info From Username
`GET /tt/user/info`

Returns profile info for a TikTok user: bio, follower/following counts, engagement stats, avatar, country, language, etc.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | TikTok username |
| `token` | string | ✅ | API token |

**Example:**
```python
res = requests.get("https://ensembledata.com/apis/tt/user/info", params={
    "username": "daviddobrik", "token": "YOUR-TOKEN"
})
```

---

### 8. User Info From SecUID
`GET /tt/user/info/from-secuid`

Same as User Info but using the internal `secuid`.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `secuid` | string | ✅ | TikTok user secuid |
| `token` | string | ✅ | API token |

---

### 9. User Search
`GET /tt/user/search`

Search TikTok for users by keyword. Returns a list of matching user profiles.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search query |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 10. Post Info
`GET /tt/post/info`

Returns full metadata and stats for a single TikTok post (video stats, hashtags, music, author info, engagement metrics).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `aweme_id` | string | ✅ | TikTok post/video ID |
| `token` | string | ✅ | API token |

---

### 11. Multiple Post Info
`GET /tt/post/multi-info`

Fetch metadata for multiple posts in one call.

**Cost:** varies by count

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `aweme_ids` | string | ✅ | Comma-separated list of post IDs |
| `token` | string | ✅ | API token |

---

### 12. Post Comments
`GET /tt/post/comments`

Returns comments on a TikTok post, paginated.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `aweme_id` | string | ✅ | Post ID |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 13. Post Comment Replies
`GET /tt/post/comments/replies`

Returns replies to a specific comment on a post.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `aweme_id` | string | ✅ | Post ID |
| `comment_id` | string | ✅ | Comment ID |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 14. Music Search
`GET /tt/music/search`

Search for music tracks on TikTok by name/keyword.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Music search query |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 15. Music Posts
`GET /tt/music/posts`

Returns posts that use a specific music track.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `music_id` | string | ✅ | TikTok music ID |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 16. Music Details
`GET /tt/music/details`

Returns metadata for a TikTok music track (title, artist, duration, usage count, etc.).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `music_id` | string | ✅ | TikTok music ID |
| `token` | string | ✅ | API token |

---

### 17. User Followers
`GET /tt/user/followers`

Returns a page of followers for a TikTok user.

**Cost:** varies

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `secuid` | string | ✅ | User secuid |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 18. User Followings
`GET /tt/user/followings`

Returns accounts that a TikTok user follows.

**Cost:** varies

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `secuid` | string | ✅ | User secuid |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 19. User Liked Posts
`GET /tt/user/liked-posts`

Returns posts that a user has liked (if their likes are public).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `secuid` | string | ✅ | User secuid |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 20. Lives Search
`GET /tt/live/search`

Search for active or recent TikTok live streams by keyword.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search keyword |
| `cursor` | integer | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

## Python SDK

```python
from ensembledata.api import EDClient
client = EDClient("YOUR-TOKEN")

# User info
result = client.tiktok.user_info_from_username(username="daviddobrik")

# Hashtag posts
result = client.tiktok.hashtag_posts(name="magic", cursor=0)

# Post comments
result = client.tiktok.post_comments(aweme_id="7123267514972294406")
```

---

## Use Cases

- **Influencer marketing** — profile analytics, follower counts, engagement rates
- **Content analysis** — trending hashtags, keyword search, music trends
- **Competitor research** — monitor competitor accounts and their engagement
- **Sentiment analysis** — extract and analyze post comments
- **Trend discovery** — live search, full hashtag scraping, keyword monitoring

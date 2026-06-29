# Instagram API — ClaWHub / EnsembleData

> Real-time Instagram data scraping for publicly available content.  
> **Base URL:** `https://ensembledata.com/apis`  
> **Prefix:** `/instagram/`  
> **Auth:** `?token=YOUR_TOKEN` on every request

---

## Endpoints

### 1. User Posts
`GET /instagram/user/posts`

Returns a page of posts published by an Instagram user.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username (without `@`) |
| `cursor` | string | — | Pagination cursor from previous response |
| `token` | string | ✅ | API token |

**Pagination:** Each response includes a `nextCursor`. Pass it back as `cursor` to get the next page. When absent, all posts have been retrieved.

---

### 2. User Basic Stats
`GET /instagram/user/basic-stats`

Returns lightweight stats for a user: follower count, following count, post count, and profile picture.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username |
| `token` | string | ✅ | API token |

**Example:**
```python
import requests
res = requests.get("https://ensembledata.com/apis/instagram/user/basic-stats", params={
    "username": "natgeo", "token": "YOUR-TOKEN"
})
print(res.json())
```

---

### 3. User Info
`GET /instagram/user/info`

Returns standard user profile: bio, external URL, follower/following/post counts, profile picture, verified status.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username |
| `token` | string | ✅ | API token |

---

### 4. User Detailed Info
`GET /instagram/user/detailed-info`

Returns a richer profile including category, contact info, business information, highlights, and more.

**Cost:** 1–2 units

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username |
| `token` | string | ✅ | API token |

---

### 5. User Follower Count
`GET /instagram/user/follower-count`

Returns only the follower count for an account — lightweight and inexpensive.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username |
| `token` | string | ✅ | API token |

---

### 6. User Reels
`GET /instagram/user/reels`

Returns a page of Reels published by a user.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 7. User Tagged Posts
`GET /instagram/user/tagged-posts`

Returns posts in which a given user has been tagged by others.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Instagram username |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 8. Post Info & Comments
`GET /instagram/post/info-and-comments`

Returns full post metadata (caption, likes, media type, author info) along with the first page of comments.

**Cost:** 2 units

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | ✅ | Instagram post shortcode (from URL: `instagram.com/p/{code}/`) |
| `token` | string | ✅ | API token |

---

### 9. Post Comments
`GET /instagram/post/comments`

Returns paginated comments for a post.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | ✅ | Post shortcode |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 10. Music Posts
`GET /instagram/music/posts`

Returns posts using a specific music/audio track.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `music_id` | string | ✅ | Instagram music/audio ID |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 11. Search
`GET /instagram/search`

General search across Instagram (users, hashtags, places).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search query |
| `token` | string | ✅ | API token |

---

## Python SDK

```python
from ensembledata.api import EDClient
client = EDClient("YOUR-TOKEN")

# User info
result = client.instagram.user_info(username="natgeo")

# User posts
result = client.instagram.user_posts(username="natgeo")

# Post comments
result = client.instagram.post_comments(code="CuABCDEFGHI")
```

---

## How to Find Post Shortcode

Given a post URL like `https://www.instagram.com/p/CuABCDEFGHI/`, the shortcode is `CuABCDEFGHI`.

---

## Use Cases

- **Influencer discovery** — follower counts, engagement metrics, detailed profiles
- **Brand monitoring** — track tagged posts, mentions via search
- **Content auditing** — pull all posts or reels for an account
- **Sentiment analysis** — scrape and analyze post comments
- **Audience research** — user detailed info, category, bio analysis
- **Trend tracking** — music posts (viral audio correlation)

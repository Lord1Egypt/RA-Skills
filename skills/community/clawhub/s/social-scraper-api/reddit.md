# Reddit API — ClaWHub / EnsembleData

> Real-time Reddit data scraping for publicly available content.  
> **Base URL:** `https://ensembledata.com/apis`  
> **Prefix:** `/reddit/`  
> **Auth:** `?token=YOUR_TOKEN` on every request

---

## Endpoints

### 1. Keyword Search
`GET /reddit/keyword/search`

Searches Reddit for posts matching a keyword across all subreddits.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search keyword or phrase |
| `cursor` | string | — | Pagination cursor from previous response |
| `token` | string | ✅ | API token |

**Response:** Returns a list of post objects with title, author, subreddit, score, comment count, URL, and post content.

**Example:**
```python
import requests
res = requests.get("https://ensembledata.com/apis/reddit/keyword/search", params={
    "name": "machine learning", "token": "YOUR-TOKEN"
})
print(res.json())
```

**Pagination:**
```python
data = res.json()
next_cursor = data.get("data", {}).get("nextCursor")
# Pass next_cursor as cursor= in subsequent requests
```

---

### 2. Subreddit Posts
`GET /reddit/subreddit/posts`

Returns a page of posts from a specific subreddit, sorted by new/hot (default: hot).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Subreddit name (without `r/`), e.g. `python` |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

**Example:**
```python
res = requests.get("https://ensembledata.com/apis/reddit/subreddit/posts", params={
    "name": "MachineLearning", "token": "YOUR-TOKEN"
})
```

---

### 3. Post Comments
`GET /reddit/post/comments`

Returns comments on a specific Reddit post.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `post_id` | string | ✅ | Reddit post ID (the alphanumeric part of the URL, e.g. `t3_abc123` or just `abc123`) |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

**Example:**
```python
res = requests.get("https://ensembledata.com/apis/reddit/post/comments", params={
    "post_id": "abc123", "token": "YOUR-TOKEN"
})
```

---

## Python SDK

```python
from ensembledata.api import EDClient
client = EDClient("YOUR-TOKEN")

# Search posts
result = client.reddit.keyword_search(name="machine learning")

# Subreddit posts
result = client.reddit.subreddit_posts(name="MachineLearning")

# Post comments
result = client.reddit.post_comments(post_id="abc123")
```

---

## How to Find a Post ID

From a Reddit URL like:
```
https://www.reddit.com/r/MachineLearning/comments/abc123/some_post_title/
```
The post ID is `abc123`.

---

## Common Error Codes

| Code | Meaning |
|------|---------|
| 422 | Invalid parameters |
| 491 | Token not found |
| 493 | Subscription expired |
| 495 | Daily units exhausted |
| 500 | Server error (not charged) |

---

## Use Cases

- **Brand monitoring** — track mentions of a brand or product across Reddit
- **Market research** — mine community discussions for consumer sentiment
- **Trend discovery** — keyword search to surface viral topics
- **Competitive intelligence** — monitor subreddits related to competitor products
- **Academic research** — gather public discussion data for NLP and social studies
- **Sentiment analysis** — extract and analyze comments on specific posts
- **Community analytics** — monitor subreddit activity and top posts

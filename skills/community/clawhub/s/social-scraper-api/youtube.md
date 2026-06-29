# YouTube API — ClaWHub / EnsembleData

> Real-time YouTube data scraping for publicly available content.  
> **Base URL:** `https://ensembledata.com/apis`  
> **Prefix:** `/youtube/`  
> **Auth:** `?token=YOUR_TOKEN` on every request

---

## Endpoints

### 1. Keyword Search
`GET /youtube/keyword/search`

Search YouTube for videos matching a keyword. Returns ~20 results per call.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Search keyword |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

**Example:**
```python
import requests
res = requests.get("https://ensembledata.com/apis/youtube/keyword/search", params={
    "name": "python tutorial", "token": "YOUR-TOKEN"
})
```

---

### 2. Featured Categories Search
`GET /youtube/search/featured-categories`

Browse videos by YouTube's featured categories (e.g., Music, Gaming, Sports).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Category name or keyword |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 3. Hashtag Search
`GET /youtube/hashtag/search`

Returns videos tagged with a specific YouTube hashtag.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Hashtag (without `#`) |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 4. Channel Detailed Info
`GET /youtube/channel/detailed-info`

Returns comprehensive channel metadata: description, creation date, subscriber count, video count, view count, country, links, banner images, keywords, and more.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_id` | string | ✅ | YouTube channel ID (e.g. `UCnQghMm3Z164JFhScQYFTBw`) |
| `token` | string | ✅ | API token |

---

### 5. Channel Videos
`GET /youtube/channel/videos`

Returns a page of videos uploaded by a channel, sorted by date (newest first).

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_id` | string | ✅ | YouTube channel ID |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 6. Channel Shorts
`GET /youtube/channel/shorts`

Returns a page of YouTube Shorts published by a channel.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_id` | string | ✅ | YouTube channel ID |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 7. Channel Streams
`GET /youtube/channel/streams`

Returns a page of live streams (current and past) from a channel.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_id` | string | ✅ | YouTube channel ID |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 8. Video / Short Details
`GET /youtube/video/details`

Returns full metadata and stats for a single YouTube video or Short: title, description, view count, like count, comment count, duration, tags, thumbnails, publish date.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `video_id` | string | ✅ | YouTube video ID (e.g. `dQw4w9WgXcQ`) |
| `token` | string | ✅ | API token |

**Example:**
```python
res = requests.get("https://ensembledata.com/apis/youtube/video/details", params={
    "video_id": "dQw4w9WgXcQ", "token": "YOUR-TOKEN"
})
```

---

### 9. Channel Subscriber Count
`GET /youtube/channel/subscriber-count`

Returns just the subscriber count for a channel — lightweight and cheap.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_id` | string | ✅ | YouTube channel ID |
| `token` | string | ✅ | API token |

---

### 10. Channel Username to ID
`GET /youtube/channel/username-to-id`

Resolves a YouTube channel username (e.g. `@MrBeast`) to its internal channel ID.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | ✅ | Channel username (with or without `@`) |
| `token` | string | ✅ | API token |

---

### 11. Channel ID to Username
`GET /youtube/channel/id-to-username`

Resolves a YouTube channel ID to its public username/handle.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_id` | string | ✅ | YouTube channel ID |
| `token` | string | ✅ | API token |

---

### 12. Music ID to Shorts
`GET /youtube/music/id-to-shorts`

Returns Shorts that use a specific audio/music track, identified by its YouTube music ID.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `music_id` | string | ✅ | YouTube music/audio ID |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

### 13. Video / Short Comments
`GET /youtube/video/comments`

Returns paginated comments on a YouTube video or Short.

**Cost:** 1 unit

**Params:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `video_id` | string | ✅ | YouTube video ID |
| `cursor` | string | — | Pagination cursor |
| `token` | string | ✅ | API token |

---

## Python SDK

```python
from ensembledata.api import EDClient
client = EDClient("YOUR-TOKEN")

# Channel info
result = client.youtube.channel_detailed_info(channel_id="UCnQghMm3Z164JFhScQYFTBw")

# Subscriber count
result = client.youtube.channel_subscribers(channel_id="UCnQghMm3Z164JFhScQYFTBw")

# Video details
result = client.youtube.video_details(video_id="dQw4w9WgXcQ")
```

---

## How to Find a Channel ID

From a channel URL:
- `https://www.youtube.com/channel/UCnQghMm3Z164JFhScQYFTBw` → ID is `UCnQghMm3Z164JFhScQYFTBw`
- For username-based URLs like `https://www.youtube.com/@MrBeast`, use the **Channel Username to ID** endpoint first.

---

## Use Cases

- **Influencer analytics** — subscriber counts, video stats, channel growth
- **Content research** — keyword and hashtag search, trending categories
- **Campaign tracking** — video details, engagement (views, likes, comments)
- **Competitor analysis** — channel detailed info, video/shorts catalog
- **Audience insights** — comment extraction and sentiment analysis
- **Shorts trends** — music-driven Shorts discovery via Music ID to Shorts

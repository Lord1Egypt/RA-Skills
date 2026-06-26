
```yaml
---
name: websim-api
description: Access WebSim's public REST API to retrieve users, projects, comments, trending feeds, social graphs, and searchable assets. Supports reading platform data for discovery, analysis, and community interaction. WebSim is a popular platform for AI generated websites, with a community similar to Scratch.
author: upintheairsheep
version: 1.0.1
base_url: https://websim.com
endpoints:

  - name: get_user
    url: /api/v1/users/{username}
    method: GET
    description: Retrieve detailed profile information for a specific WebSim user.
    params:
      - name: username
        type: string
        in: path
        description: The exact WebSim username (case-sensitive).
        required: true

  - name: get_user_projects
    url: /api/v1/users/{username}/projects
    method: GET
    description: Get a paginated list of projects created by a specific user.
    params:
      - name: username
        type: string
        in: path
        description: The exact WebSim username.
        required: true
      - name: first
        type: integer
        in: query
        description: Number of projects to return per page (default 10).
        required: false
      - name: posted
        type: boolean
        in: query
        description: Filter to only posted/published projects when true.
        required: false
      - name: after
        type: string
        in: query
        description: Cursor string for fetching the next page of results.
        required: false

  - name: get_project
    url: /api/v1/projects/{id}
    method: GET
    description: Retrieve complete information about a single project including its current revision, site data, and metadata.
    params:
      - name: id
        type: string
        in: path
        description: The project ID (alphanumeric slug, e.g. "n9gw5x7w6rlcl48m2aks").
        required: true

  - name: get_project_comments
    url: /api/v1/projects/{id}/comments
    method: GET
    description: Fetch comments on a project with pagination and sorting.
    params:
      - name: id
        type: string
        in: path
        description: The project ID.
        required: true
      - name: sort_by
        type: string
        in: query
        description: "Sort order for comments. Known values: 'best', 'newest', 'oldest'."
        required: false
      - name: first
        type: integer
        in: query
        description: Number of comments to return per page (default 20).
        required: false
      - name: after
        type: string
        in: query
        description: Cursor string for pagination.
        required: false

  - name: post_comment
    url: /api/v1/projects/{id}/comments
    method: POST
    description: Create a new comment on a project. Requires authentication.
    params:
      - name: id
        type: string
        in: path
        description: The project ID to comment on.
        required: true
      - name: content
        type: string
        in: body
        description: The text content of the comment.
        required: true
      - name: parent_comment_id
        type: string
        in: body
        description: ID of the comment to reply to. Set to null for a top-level comment.
        required: false
    headers:
      - name: Authorization
        value: "Bearer {token}"
        description: User authentication token. Required.
      - name: Content-Type
        value: application/json

  - name: get_trending
    url: /api/v1/feed/trending
    method: GET
    description: Get trending projects and sites with various sorting options.
    params:
      - name: feed
        type: string
        in: query
        description: "Feed type. Known values: 'hot', 'new', 'top'."
        required: false
      - name: limit
        type: integer
        in: query
        description: Number of items to return (default 12).
        required: false
      - name: range
        type: string
        in: query
        description: "Time range filter. Known values: 'day', 'week', 'month', 'all'."
        required: false

  - name: get_user_following
    url: /api/v1/users/{username}/following
    method: GET
    description: Get the list of users that a specific user is following.
    params:
      - name: username
        type: string
        in: path
        description: The exact WebSim username.
        required: true
      - name: first
        type: integer
        in: query
        description: Number of results per page (default 50).
        required: false
      - name: after
        type: string
        in: query
        description: Cursor string for pagination.
        required: false

  - name: search_assets
    url: /api/v1/search/assets
    method: GET
    description: Search uploaded assets (images, audio, models) across all public projects.
    params:
      - name: q
        type: string
        in: query
        description: Search query string (matched against filenames and metadata).
        required: true
      - name: limit
        type: integer
        in: query
        description: Maximum number of results to return (default 20).
        required: false
      - name: offset
        type: integer
        in: query
        description: Offset for pagination (default 0).
        required: false
      - name: mime_type_prefix
        type: string
        in: query
        description: "Filter by MIME type prefix, e.g. 'image', 'audio', 'video', 'model'."
        required: false
---
```

# WebSim API — Agent Instructions

Use this skill whenever a user asks about WebSim projects, users, trending content, community comments, or uploaded assets. All endpoints are read-only except `post_comment`, which requires authentication.

---

## General Rules

1. **Base URL:** All endpoints are relative to `https://websim.com`. Always prepend this to every path.
2. **No Authentication Required** for all GET endpoints. Only `POST /api/v1/projects/{id}/comments` requires a Bearer token.
3. **Pagination:** Many endpoints use cursor-based pagination. Look for a `cursor` field in each result item and pass it as the `after` query parameter to fetch the next page.
4. **Rate Limiting:** Be respectful. Do not fire rapid sequential requests. One request at a time is sufficient.

---

## Endpoint Usage Guide

### 1. Look Up a User — `get_user`

**When to use:** The user asks "who is [username] on WebSim?", "does this user exist?", or "show me their profile."

**Request:**
```
GET https://websim.com/api/v1/users/{username}
```

**Key response fields:**
| Field | Type | Meaning |
|---|---|---|
| `id` | string (UUID) | Unique user identifier |
| `username` | string | Display username |
| `avatar_url` | string | URL to user's profile image |
| `is_admin` | boolean | Whether the user is a WebSim admin |
| `created_at` | ISO 8601 | Account creation date |
| `discord_username` | string or null | Linked Discord handle |

**Example:**
```
GET https://websim.com/api/v1/users/sean
```

---

### 2. Browse a User's Projects — `get_user_projects`

**When to use:** The user asks "what has [username] built?", "show me their projects", or "find projects by [username]."

**Request:**
```
GET https://websim.com/api/v1/users/{username}/projects?first=10&posted=true
```

**Key response fields** (each item in the array):
| Field Path | Type | Meaning |
|---|---|---|
| `project.id` | string | Project identifier (use for other endpoints) |
| `project.title` | string | Human-readable project title |
| `project.slug` | string | URL-safe project slug |
| `project.stats.views` | integer | Total view count |
| `project.stats.likes` | integer | Total like count |
| `project.stats.comments` | integer | Total comment count |
| `project.visibility` | string | `"public"` or `"private"` |
| `project.posted` | boolean | Whether the project has been published |
| `project.description` | string or null | Author-written description |
| `project.generated_description` | string or null | AI-generated description |
| `project.domains` | array | Custom domains (e.g. `"emoji-merger.on.websim.ai"`) |
| `project.current_version` | integer | Latest version number |
| `site.link_url` | string | Relative public URL (prepend base_url to open) |
| `site.model` | string | AI model used (e.g. `"gemini-3-pro"`, `"gpt-5"`) |
| `site.prompt.text` | string | The last prompt used to generate/edit the project |
| `cursor` | string | Pagination cursor — pass as `after` for next page |

**Pagination:** If the array length equals your `first` value, there may be more pages. Take the `cursor` from the last item and pass it as `?after={cursor}`.

---

### 3. Get Project Details — `get_project`

**When to use:** The user gives you a specific project ID and asks for details, or you need full metadata on a single project.

**Request:**
```
GET https://websim.com/api/v1/projects/{id}
```

**Key response fields:**
| Field Path | Type | Meaning |
|---|---|---|
| `project.title` | string | Project title |
| `project.created_by.username` | string | Creator's username |
| `project.stats` | object | `{ views, likes, comments }` |
| `project.parent_id` | string or null | If remixed, the original project ID |
| `project_revision.version` | integer | Current version number |
| `project_revision.current_screenshot_url` | string | URL to a screenshot of the current version |
| `site.model` | string | AI model used |
| `site.prompt.text` | string | Generation prompt |
| `site.link_url` | string | Relative link to view the project |
| `site.yapping` | string | The AI's internal reasoning/thinking log |

**Constructing a viewable URL:**
```
https://websim.com{site.link_url}
```
For example: `https://websim.com/p/n9gw5x7w6rlcl48m2aks`

---

### 4. Read Project Comments — `get_project_comments`

**When to use:** The user asks "what are people saying about this project?", "show me comments", or "read the feedback."

**Request:**
```
GET https://websim.com/api/v1/projects/{id}/comments?sort_by=best&first=20
```

**Key response fields** (each item in the array):
| Field Path | Type | Meaning |
|---|---|---|
| `comment.id` | string (UUID) | Comment identifier |
| `comment.raw_content` | string | Plain text content of the comment |
| `comment.content` | object | Rich text document structure (has `children` with `type` and `text`) |
| `comment.author.username` | string | Commenter's username |
| `comment.author.avatar_url` | string | Commenter's avatar |
| `comment.created_at` | ISO 8601 | When the comment was posted |
| `comment.reply_count` | integer | Number of replies to this comment |
| `comment.parent_comment_id` | string or null | `null` if top-level; otherwise the parent comment ID |
| `comment.reactions` | array | Emoji reactions with `emoji.name` and `user_ids` |
| `comment.pinned` | boolean | Whether the comment is pinned |
| `comment.card_data` | object or null | Special data (e.g. tip comments with `credits_spent`) |

**Reading comment text:** Use `comment.raw_content` for plain text. The `comment.content` field contains a structured document — iterate `content.children[].children[].text` to extract text segments.

---

### 5. Post a Comment — `post_comment`

**When to use:** The user explicitly asks you to leave a comment on a project. **Requires authentication.**

**Request:**
```
POST https://websim.com/api/v1/projects/{id}/comments
Content-Type: application/json
Authorization: Bearer {token}

{
  "content": "Great project!",
  "parent_comment_id": null
}
```

Set `parent_comment_id` to a comment ID string to reply to a specific comment, or `null` for a top-level comment.

> ⚠️ **Only use this when the user explicitly requests it.** Never post comments autonomously.

---

### 6. Discover Trending Projects — `get_trending`

**When to use:** The user asks "what's popular on WebSim?", "show me trending projects", or "what's new?"

**Request:**
```
GET https://websim.com/api/v1/feed/trending?feed=hot&limit=12&range=week
```

**Key response fields** (each item in the `feed.data` array):
| Field Path | Type | Meaning |
|---|---|---|
| `site.title` | string | Project/site title |
| `project.title` | string | Project title |
| `project.id` | string | Project ID (for deeper lookup) |
| `project.created_by.username` | string | Creator |
| `views` | integer | View count in the time range |
| `likes` | integer | Like count |
| `active_players` | integer | Current multiplayer player count |

**Feed types:**
- `hot` — Currently popular (engagement-weighted)
- `new` — Most recently published
- `top` — Highest overall stats

**Range values:** `day`, `week`, `month`, `all`

---

### 7. View a User's Social Graph — `get_user_following`

**When to use:** The user asks "who does [username] follow?" or "show me their connections."

**Request:**
```
GET https://websim.com/api/v1/users/{username}/following?first=50
```

**Key response fields** (each item in the `following.data` array):
| Field Path | Type | Meaning |
|---|---|---|
| `follow.user.username` | string | Username of the followed account |
| `follow.user.avatar_url` | string | Their avatar |
| `follow.user.is_admin` | boolean | Whether they're an admin |
| `follow.created_at` | ISO 8601 | When the follow relationship began |

---

### 8. Search for Assets — `search_assets`

**When to use:** The user asks "find me images of X", "search for audio files", "find assets for my project", or any asset discovery request.

**Request:**
```
GET https://websim.com/api/v1/search/assets?q={query}&limit=20
```

**Optional filters:**
- `mime_type_prefix=image` — Only images (PNG, JPEG, WebP, etc.)
- `mime_type_prefix=audio` — Only audio files (MP3, WAV, etc.)
- `mime_type_prefix=video` — Only video files
- `mime_type_prefix=model` — Only 3D models

**Key response fields** (each item in the `data` array):
| Field | Type | Meaning |
|---|---|---|
| `id` | string (UUID) | Asset identifier |
| `asset_url` | string | Direct download URL for the asset |
| `content_type` | string | Full MIME type (e.g. `"image/png"`, `"audio/mpeg"`) |
| `filename` | string | Original filename |
| `project_id` | string | The project this asset belongs to |
| `created_at` | ISO 8601 | Upload date |
| `score` | integer | Relevance score (higher = better match) |

**Pagination:** Use `offset` and `limit`. Check `meta.offset` and `meta.limit` in the response to calculate the next page:
```
next_offset = meta.offset + meta.limit
```

**The asset URL is directly usable.** For example (an image of a retro-Roblox-themed white bunny rabbit):
```
https://project-assets.websim.com/0196c3b6-c5fc-7bbf-b59b-a53857ec2fa8
```

---

## Output Formatting Guidelines

Present your findings in a clear, structured, and user-friendly manner:

- **User lookups:** Show username, avatar (as a link or image), join date, and admin status.
- **Project lists:** Use a numbered or bulleted list with title, view/like counts, and a direct link (`https://websim.com/p/{project_id}`).
- **Comments:** Quote the comment text, attribute the author, and note any reactions or reply counts.
- **Trending:** Present as a ranked list with title, creator, and engagement stats.
- **Assets:** Show filename, type (image/audio/etc.), a direct link to the asset, and which project it came from.
- **Pagination:** If more results are available, inform the user and offer to fetch the next page.

---

## Common Patterns

**Constructing project URLs:**
```
View:       https://websim.com/p/{project_id}
Versioned:  https://websim.com/p/{project_id}/{version}
```

**Constructing user profile URLs:**
```
https://websim.com/@{username}
```

**Chaining requests:** To give a full picture of a user's work, you may:
1. Call `get_user` to confirm they exist and get profile data.
2. Call `get_user_projects` to list their published work.
3. Call `get_project` on a specific project for deep details.
4. Call `get_project_comments` to read community feedback.
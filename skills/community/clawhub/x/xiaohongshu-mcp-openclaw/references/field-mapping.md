# Field Mapping (Raw -> Normalized)

为适配 `xiaohongshu-mcp` 不同版本和不同工具返回结构，客户端做了宽松字段映射。

## Note fields

- `note_id`: `note_id` | `noteId` | `id` | `feed_id` | `item_id`
- `title`: `title` | `note_title` | `display_title`
- `author`: `author` | `nickname` | `user_name` | `user.nickname`
- `like_count`: `liked_count` | `like_count` | `likes` | `digg_count`
- `comment_count`: `comment_count` | `comments_count` | `reply_count`
- `content`: `content` | `desc` | `text`

## Comment fields

- `comment_id`: `comment_id` | `id`
- `author`: `nickname` | `user_name` | `user.nickname`
- `content`: `content` | `text`
- `like_count`: `like_count` | `likes`

## Selection rules

- 优先取语义更明确的字段（如 `note_id` 优先于 `id`）。
- 找不到时回退到近义字段。
- 若同层无值，递归查找嵌套对象。

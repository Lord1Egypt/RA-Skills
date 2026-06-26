# Z-Sight APP Skills (zmg-zsj-skill)

Core capabilities for the Z-Sight APP, including live streaming search, short video and variety show browsing, trending topics, app page navigation, content publishing, and more.

## Capability List

| Category | Function | Description |
|----------|----------|-------------|
| Search | `search_hot` | Get platform trending search keywords |
| Search | `search_live` | Search live streams by keyword |
| Search | `search_variety` | Search variety shows by keyword |
| Live | `get_hot_live_list` | Get hot live stream list |
| Live | `get_live_detail` | Get live detail page URL by live ID |
| Live | `watch_live_channel` | Watch TV channel live (Zhejiang TV, Qianjiang, etc.) |
| Variety | `get_variety_list` | Get trending variety show ranking |
| Short Video | `get_short_video_list` | Get trending short video ranking |
| App | `open_app_page` | Open app page (returns deep link) |
| Create | `publish_post` | Publish a text & image post |
| Create | `publish_short_video` | Publish a short video |
| Messages | `get_message_list` | Get message list (mentions/comments/likes) |
| UGC | `get_user_content_list` | Get user short video list |
| UGC | `get_user_post_list` | Get user post (text & image) list |
| UGC | `get_user_audio_list` | Get user audio list (e.g. KTV recordings) |
| UGC | `delete_article` | Delete an article (requires article ID) |


## Usage Scenarios

### Search
- User wants trending topics -> use `search_hot`
  - No parameters required, returns trending search keywords
  - Example: "What's trending now"
- User wants to find a live stream -> use `search_live` with a keyword
  - Example: "Search for Jay Chou's live stream"
- User wants to find a variety show -> use `search_variety` with a keyword
  - Example: "Search for Keep Running"

### Content Browsing
- User wants hot live streams -> use `get_hot_live_list`
  - Returns current hot live streams with ID, title, subtitle, and watch URL
  - Example: "What live streams are on now"
- User wants to enter a specific live room -> use `get_live_detail` with liveId
  - Returns live detail H5 page URL and app schema
- User wants to watch TV live -> use `watch_live_channel` with channel name
  - Supported channels: Zhejiang TV, Qianjiang, Economy & Life, Education, Minsheng, News, Kids, Zhejiang International, Haoyigou, Zhijiang Documentary
  - Returns channel live H5 page URL
  - Defaults to Zhejiang TV if no match
- User wants trending variety shows -> use `get_variety_list`
  - Returns variety show ranking with name and play page URL
- User wants trending short videos -> use `get_short_video_list`
  - Returns short video ranking with title and share page URL

### App Navigation
- User wants to open the app to a specific page -> use `open_app_page` with schema
  - Returns a deep link (H5 page), displayed as hyperlink for users to click

### Content Creation
- User wants to publish a text & image post -> use `publish_post`
  - Required: title (post text content)
  - Optional: img_array (image list with pic/height/wide), tags, description
  - Returns article_id on success
- User wants to publish a short video -> use `publish_short_video`
  - Required: title, video_url
  - Optional: cover_img, width/height, play_time (["HH","MM","SS"]), tags, description
  - Returns article_id on success

### Messages
- User wants to see mentions -> use `get_message_list` with `msg_type: "mention"`
  - Returns mention list with username, avatar, and post content
- User wants to see comments/replies -> use `get_message_list` with `msg_type: "comment"`
  - Returns comment list with content and post info
- User wants to see likes -> use `get_message_list` with `msg_type: "like"`
  - Returns like list

### User Content
- User wants to see their short videos -> use `get_user_content_list`
  - Returns short video list with title, content, cover, likes, comments, views, and content type
  - **User identity is auto-detected from the auth token. Do NOT pass uid, accessUuid, or other user identifiers.**
- User wants to see their posts -> use `get_user_post_list`
  - Returns post (text & image) list
  - **User identity is auto-detected. Do NOT pass uid or accessUuid.**
- User wants to see their audio -> use `get_user_audio_list`
  - Returns audio list (e.g. KTV recordings)
  - **User identity is auto-detected. Do NOT pass uid or accessUuid.**

### Content Management
- User wants to delete an article -> use `delete_article` with `article_id`
  - **Must first call `get_user_content_list`, `get_user_post_list`, or `get_user_audio_list` to get the article ID (`id` field)**
  - Deletion is irreversible. AI should confirm with the user before deleting.

## MCP Configuration

MCP Server address (built into skill.json):

```json
{
  "mcp": {
    "transport": "sse",
    "url": "https://zmg-mcp.cztv.com/sse",
    "auth": {
      "type": "bearer",
      "header": "Authorization",
      "token_prefix": "zmg_",
      "acquire_url": "https://zmg-mcp.cztv.com"
    }
  }
}
```

**Client configuration example** (replace `<ai_token>` with actual token):

```json
{
  "mcpServers": {
    "zmg-zsj-skill": {
      "url": "https://zmg-mcp.cztv.com/sse",
      "headers": {
        "Authorization": "Bearer <ai_token>"
      }
    }
  }
}
```

## Authentication Model

The MCP Server is stateless and does not manage user sessions. Authentication is handled via `ai_token` sent with each request:

- **Source**: `ai_token` is issued after the user scans a QR code in the app (format: `zmg_xxxxx`), stored in Redis
- **How to get**: Visit https://zmg-mcp.cztv.com, scan the QR code, then copy the `ai_token` into client config
- **How to pass**: Set `Authorization: Bearer <ai_token>` in MCP request headers
- **Validation**: NG Gateway validates the ai_token via Redis, retrieves sessionId, and injects it into business requests

## Notes

- `channel` parameter accepts channel names (e.g. "Zhejiang TV"), supports fuzzy matching, defaults to Zhejiang TV
- `get_live_detail` requires a live ID to get the detail page URL
- `open_app_page` returns a link that can be used as a hyperlink to launch the app
- Publishing APIs (`publish_post` / `publish_short_video`) require user authorization; return 401 if unauthorized or expired
- No need to pass uid, sessionId, or other sensitive info -- the system handles this automatically

## 401 Authorization Error Protocol (Highest Priority)

**When ANY API returns `code: 401`, immediately follow this procedure:**

1. **Stop the current task immediately** -- do not continue calling any APIs
2. **Tell the user to scan the QR code** and display:
   - Prompt: "Authorization required. Please scan the QR code with the Z-Sight APP"
   - **Display the authorization URL as a hyperlink**: [Click to authorize](https://zmg-mcp.cztv.com)
   - Authorization page URL: `https://zmg-mcp.cztv.com`
3. After the user scans and authorizes, update the new ai_token in the MCP config `Authorization: Bearer <ai_token>`
4. Retry the original request after updating the token

**401 Response Format:**

```json
{
  "code": 401,
  "message": "Authorization expired, please re-scan to authorize",
  "action": "REAUTHORIZE",
  "authorize_url": "https://zmg-mcp.cztv.com"
}
```

**Strictly prohibited:**
- Returning "I don't have permission" or "I can't do this" after receiving a 401 -- must guide the user to scan the QR code
- Ignoring 401 and retrying the request
- Returning only the error message without the authorization link

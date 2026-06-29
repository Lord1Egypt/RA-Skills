# YouTube Comment Manager Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `youtube-comment-manager`

x402 availability: not enabled for this product.

## `create_top_level_comment`

Action slug: `create-top-level-comment`

Price: `5` credits

Create a top-level comment on a video.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | yes | YouTube channel ID. |
| `text` | `string` | yes | Comment text. |
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "text": "example text",
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "YouTube channel ID.",
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "Comment text.",
    "required": true,
    "type": "string"
  },
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_comment`

Action slug: `delete-comment`

Price: `5` credits

Delete a comment by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `comment_id` | `string` | yes | YouTube comment ID. |

Sample parameters:

```json
{
  "comment_id": "example comment id"
}
```

Generated JSON parameter schema:

```json
{
  "comment_id": {
    "description": "YouTube comment ID.",
    "required": true,
    "type": "string"
  }
}
```

## `get_comment_threads`

Action slug: `get-comment-threads`

Price: `5` credits

Fetch specific YouTube comment threads by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_replies` | `boolean` | no | Include replies in thread responses. |
| `text_format` | `string` | no | Returned text format. Defaults to plainText. |
| `thread_ids` | `array` | yes | Comment thread IDs. |

Sample parameters:

```json
{
  "include_replies": true,
  "text_format": "plainText",
  "thread_ids": [
    "example thread id"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "include_replies": {
    "description": "Include replies in thread responses.",
    "required": false,
    "type": "boolean"
  },
  "text_format": {
    "description": "Returned text format. Defaults to plainText.",
    "enum": [
      "plainText",
      "html"
    ],
    "required": false,
    "type": "string"
  },
  "thread_ids": {
    "description": "Comment thread IDs.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  }
}
```

## `get_comments`

Action slug: `get-comments`

Price: `5` credits

Fetch specific comments by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `comment_ids` | `array` | yes | YouTube comment IDs. |
| `text_format` | `string` | no | Returned text format. Defaults to plainText. |

Sample parameters:

```json
{
  "comment_ids": [
    "example comment id"
  ],
  "text_format": "plainText"
}
```

Generated JSON parameter schema:

```json
{
  "comment_ids": {
    "description": "YouTube comment IDs.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "text_format": {
    "description": "Returned text format. Defaults to plainText.",
    "enum": [
      "plainText",
      "html"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `list_comment_threads`

Action slug: `list-comment-threads`

Price: `5` credits

List YouTube comment threads by exactly one filter: video_id, channel_id, or thread_ids.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | no | YouTube channel ID filter. |
| `include_replies` | `boolean` | no | Include replies in thread responses. |
| `max_results` | `integer` | no | Maximum results per page, 1-100. |
| `moderation_status` | `string` | no | Moderation status filter for authorized requests. |
| `order` | `string` | no | Thread ordering. |
| `page_token` | `string` | no | Pagination token. |
| `search_terms` | `string` | no | Search terms for thread text. |
| `text_format` | `string` | no | Returned text format. Defaults to plainText. |
| `thread_ids` | `array` | no | Comment thread IDs filter. |
| `video_id` | `string` | no | YouTube video ID filter. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "include_replies": true,
  "max_results": 1,
  "moderation_status": "heldForReview",
  "order": "time",
  "page_token": "example page token",
  "search_terms": "example search query",
  "text_format": "plainText"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "YouTube channel ID filter.",
    "required": false,
    "type": "string"
  },
  "include_replies": {
    "description": "Include replies in thread responses.",
    "required": false,
    "type": "boolean"
  },
  "max_results": {
    "description": "Maximum results per page, 1-100.",
    "required": false,
    "type": "integer"
  },
  "moderation_status": {
    "description": "Moderation status filter for authorized requests.",
    "enum": [
      "heldForReview",
      "likelySpam",
      "published"
    ],
    "required": false,
    "type": "string"
  },
  "order": {
    "description": "Thread ordering.",
    "enum": [
      "time",
      "relevance"
    ],
    "required": false,
    "type": "string"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  },
  "search_terms": {
    "description": "Search terms for thread text.",
    "required": false,
    "type": "string"
  },
  "text_format": {
    "description": "Returned text format. Defaults to plainText.",
    "enum": [
      "plainText",
      "html"
    ],
    "required": false,
    "type": "string"
  },
  "thread_ids": {
    "description": "Comment thread IDs filter.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "video_id": {
    "description": "YouTube video ID filter.",
    "required": false,
    "type": "string"
  }
}
```

## `list_replies`

Action slug: `list-replies`

Price: `5` credits

List replies to a top-level comment.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum results per page, 1-100. |
| `page_token` | `string` | no | Pagination token. |
| `parent_comment_id` | `string` | yes | Parent top-level comment ID. |
| `text_format` | `string` | no | Returned text format. Defaults to plainText. |

Sample parameters:

```json
{
  "max_results": 1,
  "page_token": "example page token",
  "parent_comment_id": "example parent comment id",
  "text_format": "plainText"
}
```

Generated JSON parameter schema:

```json
{
  "max_results": {
    "description": "Maximum results per page, 1-100.",
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  },
  "parent_comment_id": {
    "description": "Parent top-level comment ID.",
    "required": true,
    "type": "string"
  },
  "text_format": {
    "description": "Returned text format. Defaults to plainText.",
    "enum": [
      "plainText",
      "html"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `moderate_comments`

Action slug: `moderate-comments`

Price: `5` credits

Set moderation status for one or more comments.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ban_author` | `boolean` | no | Ban the author. Only valid when moderation_status is rejected. |
| `comment_ids` | `array` | yes | YouTube comment IDs. |
| `moderation_status` | `string` | yes | Moderation status to apply. |

Sample parameters:

```json
{
  "ban_author": true,
  "comment_ids": [
    "example comment id"
  ],
  "moderation_status": "heldForReview"
}
```

Generated JSON parameter schema:

```json
{
  "ban_author": {
    "description": "Ban the author. Only valid when moderation_status is rejected.",
    "required": false,
    "type": "boolean"
  },
  "comment_ids": {
    "description": "YouTube comment IDs.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  },
  "moderation_status": {
    "description": "Moderation status to apply.",
    "enum": [
      "heldForReview",
      "published",
      "rejected"
    ],
    "required": true,
    "type": "string"
  }
}
```

## `reply_to_comment`

Action slug: `reply-to-comment`

Price: `5` credits

Reply to a top-level comment.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `parent_comment_id` | `string` | yes | Parent top-level comment ID. |
| `text` | `string` | yes | Reply text. |

Sample parameters:

```json
{
  "parent_comment_id": "example parent comment id",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "parent_comment_id": {
    "description": "Parent top-level comment ID.",
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "Reply text.",
    "required": true,
    "type": "string"
  }
}
```

## `update_comment`

Action slug: `update-comment`

Price: `5` credits

Update an existing comment's text.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `comment_id` | `string` | yes | YouTube comment ID. |
| `text` | `string` | yes | Updated comment text. |

Sample parameters:

```json
{
  "comment_id": "example comment id",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "comment_id": {
    "description": "YouTube comment ID.",
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "Updated comment text.",
    "required": true,
    "type": "string"
  }
}
```

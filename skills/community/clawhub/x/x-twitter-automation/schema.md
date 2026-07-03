# X / Twitter Automation Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `x-twitter-automation`

x402 availability: not enabled for this product.

## `create_list`

Action slug: `create-list`

Price: `1` credits

Create a new X List for the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `list_description` | `string` | no | Optional List description, max 100 characters. |
| `list_name` | `string` | yes | List name, 1-25 characters. |
| `list_private` | `boolean` | no | True to create a private List. |

Sample parameters:

```json
{
  "list_description": "example list description",
  "list_name": "example list name",
  "list_private": true
}
```

Generated JSON parameter schema:

```json
{
  "list_description": {
    "description": "Optional List description, max 100 characters.",
    "required": false,
    "type": "string"
  },
  "list_name": {
    "description": "List name, 1-25 characters.",
    "required": true,
    "type": "string"
  },
  "list_private": {
    "description": "True to create a private List.",
    "required": false,
    "type": "boolean"
  }
}
```

## `create_post`

Action slug: `create-post`

Price: `5` credits

Create a top-level X post without links. Use create_post_with_link for text containing web links. Quote-post creation is not supported.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `media_ids` | `array` | no | Media IDs to attach, max 4. |
| `text` | `string` | no | Link-free post text. Required unless media_ids is provided. |

Sample parameters:

```json
{
  "media_ids": [
    "example media id"
  ],
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "media_ids": {
    "description": "Media IDs to attach, max 4.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "text": {
    "description": "Link-free post text. Required unless media_ids is provided.",
    "required": false,
    "type": "string"
  }
}
```

## `create_post_with_link`

Action slug: `create-post-with-link`

Price: `25` credits

Create a top-level X post whose text contains at least one web link. Quote-post creation is not supported.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `media_ids` | `array` | no | Media IDs to attach, max 4. |
| `text` | `string` | yes | Post text containing at least one web link. |

Sample parameters:

```json
{
  "media_ids": [
    "example media id"
  ],
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "media_ids": {
    "description": "Media IDs to attach, max 4.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "text": {
    "description": "Post text containing at least one web link.",
    "required": true,
    "type": "string"
  }
}
```

## `create_reply`

Action slug: `create-reply`

Price: `5` credits

Reply to another X post without links. X self-serve plans may restrict replies unless the original author has summoned the authenticated account.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `media_ids` | `array` | no | Media IDs to attach, max 4. |
| `reply_to_post_id` | `string` | yes | Post ID to reply to. |
| `text` | `string` | no | Link-free reply text. Required unless media_ids is provided. |

Sample parameters:

```json
{
  "media_ids": [
    "example media id"
  ],
  "reply_to_post_id": "example reply to post id",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "media_ids": {
    "description": "Media IDs to attach, max 4.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "reply_to_post_id": {
    "description": "Post ID to reply to.",
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "Link-free reply text. Required unless media_ids is provided.",
    "required": false,
    "type": "string"
  }
}
```

## `create_reply_with_link`

Action slug: `create-reply-with-link`

Price: `25` credits

Reply to another X post with text containing at least one web link. X self-serve plans may restrict replies unless the original author has summoned the authenticated account.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `media_ids` | `array` | no | Media IDs to attach, max 4. |
| `reply_to_post_id` | `string` | yes | Post ID to reply to. |
| `text` | `string` | yes | Reply text containing at least one web link. |

Sample parameters:

```json
{
  "media_ids": [
    "example media id"
  ],
  "reply_to_post_id": "example reply to post id",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "media_ids": {
    "description": "Media IDs to attach, max 4.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "reply_to_post_id": {
    "description": "Post ID to reply to.",
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "Reply text containing at least one web link.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_list`

Action slug: `delete-list`

Price: `1` credits

Delete a List owned by the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `list_id` | `string` | yes | List ID to delete. |

Sample parameters:

```json
{
  "list_id": "example list id"
}
```

Generated JSON parameter schema:

```json
{
  "list_id": {
    "description": "List ID to delete.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_post`

Action slug: `delete-post`

Price: `5` credits

Delete a post by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `post_id` | `string` | yes | Post ID to delete. |

Sample parameters:

```json
{
  "post_id": "example post id"
}
```

Generated JSON parameter schema:

```json
{
  "post_id": {
    "description": "Post ID to delete.",
    "required": true,
    "type": "string"
  }
}
```

## `lookup_dms`

Action slug: `lookup-dms`

Price: `5` credits

Read DM events by scope: all, conversation, participant, or event_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversation_id` | `string` | no | Conversation ID for conversation scope. |
| `event_id` | `string` | no | DM event ID for event_id scope. |
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `participant_user_id` | `string` | no | Participant user ID for participant scope. |
| `scope` | `string` | yes | DM lookup scope: all, conversation, participant, or event_id. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "conversation_id": "example conversation id",
  "event_id": "example event id",
  "max_results": 1,
  "pagination_token": "example pagination token",
  "participant_user_id": "example participant user id",
  "scope": "all",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "conversation_id": {
    "description": "Conversation ID for conversation scope.",
    "required": false,
    "type": "string"
  },
  "event_id": {
    "description": "DM event ID for event_id scope.",
    "required": false,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "participant_user_id": {
    "description": "Participant user ID for participant scope.",
    "required": false,
    "type": "string"
  },
  "scope": {
    "description": "DM lookup scope: all, conversation, participant, or event_id.",
    "enum": [
      "all",
      "conversation",
      "participant",
      "event_id"
    ],
    "required": true,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_follows`

Action slug: `lookup-follows`

Price: `5` credits

List followers or followed users for a user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `relationship` | `string` | yes | Relationship list to retrieve: followers or following. |
| `user_id` | `string` | yes | User ID to inspect. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "max_results": 1,
  "pagination_token": "example pagination token",
  "relationship": "followers",
  "user_id": "example user id",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "relationship": {
    "description": "Relationship list to retrieve: followers or following.",
    "enum": [
      "followers",
      "following"
    ],
    "required": true,
    "type": "string"
  },
  "user_id": {
    "description": "User ID to inspect.",
    "required": true,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_list_contents`

Action slug: `lookup-list-contents`

Price: `1` credits

List members, followers, or posts for a List.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `list_id` | `string` | yes | List ID to inspect. |
| `list_view` | `string` | yes | Content view: members, followers, or posts. |
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "list_id": "example list id",
  "list_view": "members",
  "max_results": 1,
  "pagination_token": "example pagination token",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "list_id": {
    "description": "List ID to inspect.",
    "required": true,
    "type": "string"
  },
  "list_view": {
    "description": "Content view: members, followers, or posts.",
    "enum": [
      "members",
      "followers",
      "posts"
    ],
    "required": true,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_lists`

Action slug: `lookup-lists`

Price: `1` credits

Look up one List or list owned, membership, followed, or pinned Lists.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `list_id` | `string` | no | Required when list_scope is id. |
| `list_scope` | `string` | yes | Lookup scope: id, owned, memberships, followed, or pinned. |
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `user_id` | `string` | no | Optional for owned, memberships, and followed scopes. Omit for pinned because pinned Lists use the authenticated user. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "list_id": "example list id",
  "list_scope": "id",
  "max_results": 1,
  "pagination_token": "example pagination token",
  "user_id": "example user id",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "list_id": {
    "description": "Required when list_scope is id.",
    "required": false,
    "type": "string"
  },
  "list_scope": {
    "description": "Lookup scope: id, owned, memberships, followed, or pinned.",
    "enum": [
      "id",
      "owned",
      "memberships",
      "followed",
      "pinned"
    ],
    "required": true,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "user_id": {
    "description": "Optional for owned, memberships, and followed scopes. Omit for pinned because pinned Lists use the authenticated user.",
    "required": false,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_post_engagers`

Action slug: `lookup-post-engagers`

Price: `5` credits

List users who liked or reposted a post, or list quote posts.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `engagement_type` | `string` | yes | Engagement to retrieve: likes, reposts, or quotes. |
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `post_id` | `string` | yes | Post ID to inspect. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "engagement_type": "likes",
  "max_results": 1,
  "pagination_token": "example pagination token",
  "post_id": "example post id",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "engagement_type": {
    "description": "Engagement to retrieve: likes, reposts, or quotes.",
    "enum": [
      "likes",
      "reposts",
      "quotes"
    ],
    "required": true,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "post_id": {
    "description": "Post ID to inspect.",
    "required": true,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_posts`

Action slug: `lookup-posts`

Price: `5` credits

Get one or more X posts by ID with curated field verbosity.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `post_id` | `string` | no | Single post ID to fetch. |
| `post_ids` | `array` | no | Multiple post IDs to fetch. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "post_id": "example post id",
  "post_ids": [
    "example post id"
  ],
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "post_id": {
    "description": "Single post ID to fetch.",
    "required": false,
    "type": "string"
  },
  "post_ids": {
    "description": "Multiple post IDs to fetch.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_timeline`

Action slug: `lookup-timeline`

Price: `5` credits

Read user posts, mentions, or authenticated home timeline.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `timeline_type` | `string` | yes | Timeline mode: user_posts, mentions, or home. |
| `user_id` | `string` | no | User ID required for user_posts and mentions; optional for home. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "max_results": 1,
  "pagination_token": "example pagination token",
  "timeline_type": "user_posts",
  "user_id": "example user id",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "timeline_type": {
    "description": "Timeline mode: user_posts, mentions, or home.",
    "enum": [
      "user_posts",
      "mentions",
      "home"
    ],
    "required": true,
    "type": "string"
  },
  "user_id": {
    "description": "User ID required for user_posts and mentions; optional for home.",
    "required": false,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `lookup_users`

Action slug: `lookup-users`

Price: `5` credits

Resolve users by ID, username, or the authenticated account.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lookup_by` | `string` | yes | Lookup mode: ids, usernames, or me. |
| `user_id` | `string` | no | Single user ID for ids mode. |
| `user_ids` | `array` | no | Multiple user IDs for ids mode. |
| `username` | `string` | no | Single username without @ for usernames mode. |
| `usernames` | `array` | no | Multiple usernames without @ for usernames mode. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "lookup_by": "ids",
  "user_id": "example user id",
  "user_ids": [
    "example user id"
  ],
  "username": "example username",
  "usernames": [
    "example username"
  ],
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "lookup_by": {
    "description": "Lookup mode: ids, usernames, or me.",
    "enum": [
      "ids",
      "usernames",
      "me"
    ],
    "required": true,
    "type": "string"
  },
  "user_id": {
    "description": "Single user ID for ids mode.",
    "required": false,
    "type": "string"
  },
  "user_ids": {
    "description": "Multiple user IDs for ids mode.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "username": {
    "description": "Single username without @ for usernames mode.",
    "required": false,
    "type": "string"
  },
  "usernames": {
    "description": "Multiple usernames without @ for usernames mode.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `search_posts`

Action slug: `search-posts`

Price: `5` credits

Search recent X posts from the last 7 days.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `end_time` | `string` | no | RFC3339 end time for recent search, for example 2026-05-14T19:00:00Z. |
| `max_results` | `integer` | no | Maximum results to return, 1-100. |
| `pagination_token` | `string` | no | Pagination token from a previous response. |
| `query` | `string` | yes | X recent-search query. |
| `start_time` | `string` | no | RFC3339 start time for recent search, for example 2026-05-14T18:00:00Z. |
| `verbosity` | `string` | no | Response detail level: minimal, standard, or expanded. |

Sample parameters:

```json
{
  "end_time": "example end time",
  "max_results": 1,
  "pagination_token": "example pagination token",
  "query": "example search query",
  "start_time": "example start time",
  "verbosity": "minimal"
}
```

Generated JSON parameter schema:

```json
{
  "end_time": {
    "description": "RFC3339 end time for recent search, for example 2026-05-14T19:00:00Z.",
    "required": false,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum results to return, 1-100.",
    "required": false,
    "type": "integer"
  },
  "pagination_token": {
    "description": "Pagination token from a previous response.",
    "required": false,
    "type": "string"
  },
  "query": {
    "description": "X recent-search query.",
    "required": true,
    "type": "string"
  },
  "start_time": {
    "description": "RFC3339 start time for recent search, for example 2026-05-14T18:00:00Z.",
    "required": false,
    "type": "string"
  },
  "verbosity": {
    "description": "Response detail level: minimal, standard, or expanded.",
    "enum": [
      "minimal",
      "standard",
      "expanded"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `send_dm`

Action slug: `send-dm`

Price: `5` credits

Send a DM to a participant, existing conversation, or new group.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversation_id` | `string` | no | Conversation ID for conversation mode. |
| `media_id` | `string` | no | Optional uploaded DM media ID. One media attachment is supported. |
| `participant_user_id` | `string` | no | Participant user ID for participant mode. |
| `participant_user_ids` | `array` | no | Participant user IDs for new_group mode. |
| `target_type` | `string` | yes | Target mode: participant, conversation, or new_group. |
| `text` | `string` | no | DM text. Required unless media_id is provided. |

Sample parameters:

```json
{
  "conversation_id": "example conversation id",
  "media_id": "example media id",
  "participant_user_id": "example participant user id",
  "participant_user_ids": [
    "example participant user id"
  ],
  "target_type": "participant",
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "conversation_id": {
    "description": "Conversation ID for conversation mode.",
    "required": false,
    "type": "string"
  },
  "media_id": {
    "description": "Optional uploaded DM media ID. One media attachment is supported.",
    "required": false,
    "type": "string"
  },
  "participant_user_id": {
    "description": "Participant user ID for participant mode.",
    "required": false,
    "type": "string"
  },
  "participant_user_ids": {
    "description": "Participant user IDs for new_group mode.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "target_type": {
    "description": "Target mode: participant, conversation, or new_group.",
    "enum": [
      "participant",
      "conversation",
      "new_group"
    ],
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "DM text. Required unless media_id is provided.",
    "required": false,
    "type": "string"
  }
}
```

## `set_follow`

Action slug: `set-follow`

Price: `5` credits

Follow or unfollow a user as the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `following` | `boolean` | yes | True to follow, false to unfollow. |
| `user_id` | `string` | yes | Target user ID to follow or unfollow. |

Sample parameters:

```json
{
  "following": true,
  "user_id": "example user id"
}
```

Generated JSON parameter schema:

```json
{
  "following": {
    "description": "True to follow, false to unfollow.",
    "required": true,
    "type": "boolean"
  },
  "user_id": {
    "description": "Target user ID to follow or unfollow.",
    "required": true,
    "type": "string"
  }
}
```

## `set_like`

Action slug: `set-like`

Price: `5` credits

Like or unlike a post as the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `liked` | `boolean` | yes | True to like, false to unlike. |
| `post_id` | `string` | yes | Post ID to like or unlike. |

Sample parameters:

```json
{
  "liked": true,
  "post_id": "example post id"
}
```

Generated JSON parameter schema:

```json
{
  "liked": {
    "description": "True to like, false to unlike.",
    "required": true,
    "type": "boolean"
  },
  "post_id": {
    "description": "Post ID to like or unlike.",
    "required": true,
    "type": "string"
  }
}
```

## `set_list_follow`

Action slug: `set-list-follow`

Price: `1` credits

Follow or unfollow a List as the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `following` | `boolean` | yes | True to follow, false to unfollow. |
| `list_id` | `string` | yes | List ID to follow or unfollow. |

Sample parameters:

```json
{
  "following": true,
  "list_id": "example list id"
}
```

Generated JSON parameter schema:

```json
{
  "following": {
    "description": "True to follow, false to unfollow.",
    "required": true,
    "type": "boolean"
  },
  "list_id": {
    "description": "List ID to follow or unfollow.",
    "required": true,
    "type": "string"
  }
}
```

## `set_list_membership`

Action slug: `set-list-membership`

Price: `1` credits

Add or remove a user as a member of a List owned by the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `is_member` | `boolean` | yes | True to add, false to remove. |
| `list_id` | `string` | yes | List ID to modify. |
| `user_id` | `string` | yes | User ID to add or remove. |

Sample parameters:

```json
{
  "is_member": true,
  "list_id": "example list id",
  "user_id": "example user id"
}
```

Generated JSON parameter schema:

```json
{
  "is_member": {
    "description": "True to add, false to remove.",
    "required": true,
    "type": "boolean"
  },
  "list_id": {
    "description": "List ID to modify.",
    "required": true,
    "type": "string"
  },
  "user_id": {
    "description": "User ID to add or remove.",
    "required": true,
    "type": "string"
  }
}
```

## `set_list_pin`

Action slug: `set-list-pin`

Price: `1` credits

Pin or unpin a followed or owned List for the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `list_id` | `string` | yes | List ID to pin or unpin. |
| `pinned` | `boolean` | yes | True to pin, false to unpin. |

Sample parameters:

```json
{
  "list_id": "example list id",
  "pinned": true
}
```

Generated JSON parameter schema:

```json
{
  "list_id": {
    "description": "List ID to pin or unpin.",
    "required": true,
    "type": "string"
  },
  "pinned": {
    "description": "True to pin, false to unpin.",
    "required": true,
    "type": "boolean"
  }
}
```

## `set_reply_hidden`

Action slug: `set-reply-hidden`

Price: `5` credits

Hide or unhide a reply on your post.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hidden` | `boolean` | yes | True to hide, false to unhide. |
| `reply_post_id` | `string` | yes | Reply post ID to hide or unhide. |

Sample parameters:

```json
{
  "hidden": true,
  "reply_post_id": "example reply post id"
}
```

Generated JSON parameter schema:

```json
{
  "hidden": {
    "description": "True to hide, false to unhide.",
    "required": true,
    "type": "boolean"
  },
  "reply_post_id": {
    "description": "Reply post ID to hide or unhide.",
    "required": true,
    "type": "string"
  }
}
```

## `set_repost`

Action slug: `set-repost`

Price: `5` credits

Repost or undo repost as the authenticated user.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `post_id` | `string` | yes | Post ID to repost or undo repost. |
| `reposted` | `boolean` | yes | True to repost, false to undo repost. |

Sample parameters:

```json
{
  "post_id": "example post id",
  "reposted": true
}
```

Generated JSON parameter schema:

```json
{
  "post_id": {
    "description": "Post ID to repost or undo repost.",
    "required": true,
    "type": "string"
  },
  "reposted": {
    "description": "True to repost, false to undo repost.",
    "required": true,
    "type": "boolean"
  }
}
```

## `update_list`

Action slug: `update-list`

Price: `1` credits

Update a List's name, description, or privacy setting.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `list_description` | `string` | no | New List description, max 100 characters. Use an empty string to clear. |
| `list_id` | `string` | yes | List ID to update. |
| `list_name` | `string` | no | New List name, 1-25 characters. |
| `list_private` | `boolean` | no | True for private, false for public. |

Sample parameters:

```json
{
  "list_description": "example list description",
  "list_id": "example list id",
  "list_name": "example list name",
  "list_private": true
}
```

Generated JSON parameter schema:

```json
{
  "list_description": {
    "description": "New List description, max 100 characters. Use an empty string to clear.",
    "required": false,
    "type": "string"
  },
  "list_id": {
    "description": "List ID to update.",
    "required": true,
    "type": "string"
  },
  "list_name": {
    "description": "New List name, 1-25 characters.",
    "required": false,
    "type": "string"
  },
  "list_private": {
    "description": "True for private, false for public.",
    "required": false,
    "type": "boolean"
  }
}
```

## `upload_media`

Action slug: `upload-media`

Price: `5` credits

Upload image, GIF, or video media for posts or DMs and return a media ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | AgentPMT File Manager file ID to upload. |
| `media_type` | `string` | yes | Media kind: image, gif, or video. |
| `source_url` | `string` | no | Public URL to fetch and upload. |
| `usage_context` | `string` | yes | Where the media will be used: post or dm. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "media_type": "image",
  "source_url": "https://example.com",
  "usage_context": "post"
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "AgentPMT File Manager file ID to upload.",
    "required": false,
    "type": "string"
  },
  "media_type": {
    "description": "Media kind: image, gif, or video.",
    "enum": [
      "image",
      "gif",
      "video"
    ],
    "required": true,
    "type": "string"
  },
  "source_url": {
    "description": "Public URL to fetch and upload.",
    "required": false,
    "type": "string"
  },
  "usage_context": {
    "description": "Where the media will be used: post or dm.",
    "enum": [
      "post",
      "dm"
    ],
    "required": true,
    "type": "string"
  }
}
```

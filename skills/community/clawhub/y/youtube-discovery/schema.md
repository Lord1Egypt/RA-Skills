# YouTube Discovery Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `youtube-discovery`

x402 action routes are enabled for this product through `https://www.agentpmt.com/api/external`.

## `get_channel_details`

Action slug: `get-channel-details`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/get-channel-details/invoke`

Price: `5` credits

Retrieve one public channel by channel id, handle, or legacy username.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_handle` | `string` | no | YouTube channel handle, with or without @. |
| `channel_id` | `string` | no | YouTube channel id. |
| `channel_username` | `string` | no | Legacy YouTube username. |

Sample parameters:

```json
{
  "channel_handle": "example channel handle",
  "channel_id": "example channel id",
  "channel_username": "example channel username"
}
```

Generated JSON parameter schema:

```json
{
  "channel_handle": {
    "description": "YouTube channel handle, with or without @.",
    "required": false,
    "type": "string"
  },
  "channel_id": {
    "description": "YouTube channel id.",
    "required": false,
    "type": "string"
  },
  "channel_username": {
    "description": "Legacy YouTube username.",
    "required": false,
    "type": "string"
  }
}
```

## `get_trending_videos`

Action slug: `get-trending-videos`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/get-trending-videos/invoke`

Price: `5` credits

Retrieve public trending videos by region or category.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hl` | `string` | no | Localized language code for returned category metadata when supported. |
| `max_results` | `integer` | no | Maximum videos to return, 1 to 50. |
| `page_token` | `string` | no | Pagination token. |
| `region_code` | `string` | no | ISO 3166-1 alpha-2 region code. |
| `video_category_id` | `string` | no | Video category id. |

Sample parameters:

```json
{
  "hl": "example hl",
  "max_results": 1,
  "page_token": "example page token",
  "region_code": "example region code",
  "video_category_id": "example video category id"
}
```

Generated JSON parameter schema:

```json
{
  "hl": {
    "description": "Localized language code for returned category metadata when supported.",
    "required": false,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum videos to return, 1 to 50.",
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  },
  "region_code": {
    "description": "ISO 3166-1 alpha-2 region code.",
    "required": false,
    "type": "string"
  },
  "video_category_id": {
    "description": "Video category id.",
    "required": false,
    "type": "string"
  }
}
```

## `get_video_details`

Action slug: `get-video-details`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/get-video-details/invoke`

Price: `5` credits

Retrieve public metadata and statistics for up to 50 videos.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `video_ids` | `array` | yes | One to 50 YouTube video ids. |

Sample parameters:

```json
{
  "video_ids": [
    "example video id"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "video_ids": {
    "description": "One to 50 YouTube video ids.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  }
}
```

## `list_channel_playlists`

Action slug: `list-channel-playlists`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/list-channel-playlists/invoke`

Price: `5` credits

List public playlists for a channel.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | yes | YouTube channel id. |
| `hl` | `string` | no | Localized language code. |
| `max_results` | `integer` | no | Maximum playlists to return, 1 to 50. |
| `page_token` | `string` | no | Pagination token. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "hl": "example hl",
  "max_results": 1,
  "page_token": "example page token"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "YouTube channel id.",
    "required": true,
    "type": "string"
  },
  "hl": {
    "description": "Localized language code.",
    "required": false,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum playlists to return, 1 to 50.",
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  }
}
```

## `list_playlist_items`

Action slug: `list-playlist-items`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/list-playlist-items/invoke`

Price: `5` credits

List public items in a playlist.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum items to return, 1 to 50. |
| `page_token` | `string` | no | Pagination token. |
| `playlist_id` | `string` | yes | YouTube playlist id. |

Sample parameters:

```json
{
  "max_results": 1,
  "page_token": "example page token",
  "playlist_id": "example playlist id"
}
```

Generated JSON parameter schema:

```json
{
  "max_results": {
    "description": "Maximum items to return, 1 to 50.",
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  },
  "playlist_id": {
    "description": "YouTube playlist id.",
    "required": true,
    "type": "string"
  }
}
```

## `list_public_comments`

Action slug: `list-public-comments`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/list-public-comments/invoke`

Price: `5` credits

List public comment threads for a video, channel, or explicit thread ids.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | no | YouTube channel id for all related threads. |
| `comment_order` | `string` | no | Comment thread order when listing by video or channel. |
| `include_replies` | `boolean` | no | If true, include embedded replies returned by YouTube. |
| `max_results` | `integer` | no | Maximum comment threads to return, 1 to 100. |
| `page_token` | `string` | no | Pagination token. |
| `search_terms` | `string` | no | Search terms for public comment thread text. |
| `text_format` | `string` | no | Returned comment text format. |
| `thread_ids` | `array` | no | Explicit comment thread ids. |
| `video_id` | `string` | no | YouTube video id. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "comment_order": "time",
  "include_replies": true,
  "max_results": 1,
  "page_token": "example page token",
  "search_terms": "example search query",
  "text_format": "plainText",
  "thread_ids": [
    "example thread id"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "YouTube channel id for all related threads.",
    "required": false,
    "type": "string"
  },
  "comment_order": {
    "description": "Comment thread order when listing by video or channel.",
    "enum": [
      "time",
      "relevance"
    ],
    "required": false,
    "type": "string"
  },
  "include_replies": {
    "description": "If true, include embedded replies returned by YouTube.",
    "required": false,
    "type": "boolean"
  },
  "max_results": {
    "description": "Maximum comment threads to return, 1 to 100.",
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  },
  "search_terms": {
    "description": "Search terms for public comment thread text.",
    "required": false,
    "type": "string"
  },
  "text_format": {
    "description": "Returned comment text format.",
    "enum": [
      "plainText",
      "html"
    ],
    "required": false,
    "type": "string"
  },
  "thread_ids": {
    "description": "Explicit comment thread ids.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "video_id": {
    "description": "YouTube video id.",
    "required": false,
    "type": "string"
  }
}
```

## `list_supported_languages`

Action slug: `list-supported-languages`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/list-supported-languages/invoke`

Price: `5` credits

List supported YouTube interface languages.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hl` | `string` | no | Localized language code for returned names. |

Sample parameters:

```json
{
  "hl": "example hl"
}
```

Generated JSON parameter schema:

```json
{
  "hl": {
    "description": "Localized language code for returned names.",
    "required": false,
    "type": "string"
  }
}
```

## `list_supported_regions`

Action slug: `list-supported-regions`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/list-supported-regions/invoke`

Price: `5` credits

List supported YouTube regions.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hl` | `string` | no | Localized language code for returned names. |

Sample parameters:

```json
{
  "hl": "example hl"
}
```

Generated JSON parameter schema:

```json
{
  "hl": {
    "description": "Localized language code for returned names.",
    "required": false,
    "type": "string"
  }
}
```

## `list_video_categories`

Action slug: `list-video-categories`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/list-video-categories/invoke`

Price: `5` credits

List public YouTube video categories by region or explicit ids.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category_ids` | `array` | no | Explicit category ids. |
| `hl` | `string` | no | Localized language code. |
| `region_code` | `string` | no | ISO 3166-1 alpha-2 region code. |

Sample parameters:

```json
{
  "category_ids": [
    "example category id"
  ],
  "hl": "example hl",
  "region_code": "example region code"
}
```

Generated JSON parameter schema:

```json
{
  "category_ids": {
    "description": "Explicit category ids.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "hl": {
    "description": "Localized language code.",
    "required": false,
    "type": "string"
  },
  "region_code": {
    "description": "ISO 3166-1 alpha-2 region code.",
    "required": false,
    "type": "string"
  }
}
```

## `search`

Action slug: `search`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/youtube-discovery/actions/search/invoke`

Price: `5` credits

Search public YouTube videos, channels, or playlists with filters and pagination.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | no | Limit search to a public channel id. |
| `channel_type` | `string` | no | Channel search filter; valid only when searching channels. |
| `event_type` | `string` | no | Livestream event filter for video searches. |
| `include_video_details` | `boolean` | no | If true, enrich current-page video search results with public video details. |
| `location` | `string` | no | Latitude and longitude for location-based video search, formatted as lat,lng. |
| `location_radius` | `string` | no | Radius for location-based search, such as 10km or 5mi. Required with location. |
| `max_results` | `integer` | no | Maximum results to return, 1 to 50. Defaults to 10. |
| `order` | `string` | no | Result order. |
| `page_token` | `string` | no | Pagination token returned by a prior search. |
| `published_after` | `string` | no | Only include resources published after this RFC3339 timestamp. |
| `published_before` | `string` | no | Only include resources published before this RFC3339 timestamp. |
| `query` | `string` | no | Search query. Required unless another selector such as channel_id, topic_id, video_category_id, location, or event_type is provided. |
| `region_code` | `string` | no | ISO 3166-1 alpha-2 region code for localized search results. |
| `relevance_language` | `string` | no | ISO 639-1 language code for relevance ranking. |
| `resource_types` | `array` | no | Resource types to search. Defaults to video. |
| `safe_search` | `string` | no | Safe search level. |
| `topic_id` | `string` | no | Limit search to a YouTube topic id. |
| `video_caption` | `string` | no | Caption availability filter for video searches. |
| `video_category_id` | `string` | no | Video category id for video searches. |
| `video_definition` | `string` | no | Video definition filter. |
| `video_dimension` | `string` | no | Video dimension filter. |
| `video_duration` | `string` | no | Video duration filter. |
| `video_embeddable` | `string` | no | Set to true to return only embeddable videos. |
| `video_license` | `string` | no | Video license filter. |
| `video_paid_product_placement` | `string` | no | Set to true to filter videos with paid product placement. |
| `video_syndicated` | `string` | no | Set to true to return videos playable outside YouTube. |
| `video_type` | `string` | no | Video type filter. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "channel_type": "any",
  "event_type": "upcoming",
  "include_video_details": true,
  "location": "example location",
  "location_radius": "example location radius",
  "max_results": 1,
  "order": "date"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "Limit search to a public channel id.",
    "required": false,
    "type": "string"
  },
  "channel_type": {
    "description": "Channel search filter; valid only when searching channels.",
    "enum": [
      "any",
      "show"
    ],
    "required": false,
    "type": "string"
  },
  "event_type": {
    "description": "Livestream event filter for video searches.",
    "enum": [
      "upcoming",
      "live",
      "completed"
    ],
    "required": false,
    "type": "string"
  },
  "include_video_details": {
    "description": "If true, enrich current-page video search results with public video details.",
    "required": false,
    "type": "boolean"
  },
  "location": {
    "description": "Latitude and longitude for location-based video search, formatted as lat,lng.",
    "required": false,
    "type": "string"
  },
  "location_radius": {
    "description": "Radius for location-based search, such as 10km or 5mi. Required with location.",
    "required": false,
    "type": "string"
  },
  "max_results": {
    "description": "Maximum results to return, 1 to 50. Defaults to 10.",
    "required": false,
    "type": "integer"
  },
  "order": {
    "description": "Result order.",
    "enum": [
      "date",
      "rating",
      "viewCount",
      "relevance",
      "title",
      "videoCount"
    ],
    "required": false,
    "type": "string"
  },
  "page_token": {
    "description": "Pagination token returned by a prior search.",
    "required": false,
    "type": "string"
  },
  "published_after": {
    "description": "Only include resources published after this RFC3339 timestamp.",
    "required": false,
    "type": "string"
  },
  "published_before": {
    "description": "Only include resources published before this RFC3339 timestamp.",
    "required": false,
    "type": "string"
  },
  "query": {
    "description": "Search query. Required unless another selector such as channel_id, topic_id, video_category_id, location, or event_type is provided.",
    "required": false,
    "type": "string"
  },
  "region_code": {
    "description": "ISO 3166-1 alpha-2 region code for localized search results.",
    "required": false,
    "type": "string"
  },
  "relevance_language": {
    "description": "ISO 639-1 language code for relevance ranking.",
    "required": false,
    "type": "string"
  },
  "resource_types": {
    "description": "Resource types to search. Defaults to video.",
    "items": {
      "enum": [
        "video",
        "channel",
        "playlist"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "safe_search": {
    "description": "Safe search level.",
    "enum": [
      "none",
      "moderate",
      "strict"
    ],
    "required": false,
    "type": "string"
  },
  "topic_id": {
    "description": "Limit search to a YouTube topic id.",
    "required": false,
    "type": "string"
  },
  "video_caption": {
    "description": "Caption availability filter for video searches.",
    "enum": [
      "any",
      "closedCaption",
      "none"
    ],
    "required": false,
    "type": "string"
  },
  "video_category_id": {
    "description": "Video category id for video searches.",
    "required": false,
    "type": "string"
  },
  "video_definition": {
    "description": "Video definition filter.",
    "enum": [
      "any",
      "standard",
      "high"
    ],
    "required": false,
    "type": "string"
  },
  "video_dimension": {
    "description": "Video dimension filter.",
    "enum": [
      "any",
      "2d",
      "3d"
    ],
    "required": false,
    "type": "string"
  },
  "video_duration": {
    "description": "Video duration filter.",
    "enum": [
      "any",
      "short",
      "medium",
      "long"
    ],
    "required": false,
    "type": "string"
  },
  "video_embeddable": {
    "description": "Set to true to return only embeddable videos.",
    "enum": [
      "true"
    ],
    "required": false,
    "type": "string"
  },
  "video_license": {
    "description": "Video license filter.",
    "enum": [
      "any",
      "youtube",
      "creativeCommon"
    ],
    "required": false,
    "type": "string"
  },
  "video_paid_product_placement": {
    "description": "Set to true to filter videos with paid product placement.",
    "enum": [
      "true"
    ],
    "required": false,
    "type": "string"
  },
  "video_syndicated": {
    "description": "Set to true to return videos playable outside YouTube.",
    "enum": [
      "true"
    ],
    "required": false,
    "type": "string"
  },
  "video_type": {
    "description": "Video type filter.",
    "enum": [
      "any",
      "movie",
      "episode"
    ],
    "required": false,
    "type": "string"
  }
}
```

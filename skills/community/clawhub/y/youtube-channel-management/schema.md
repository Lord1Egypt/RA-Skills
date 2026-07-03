# YouTube Channel Management Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `youtube-api`

x402 availability: not enabled for this product.

## `add_video_to_playlist`

Action slug: `add-video-to-playlist`

Price: `25` credits

Add a YouTube video to a playlist.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `playlist_id` | `string` | yes | YouTube playlist ID. |
| `position` | `integer` | no | Optional playlist item position. |
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "playlist_id": "example playlist id",
  "position": 1,
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "playlist_id": {
    "description": "YouTube playlist ID.",
    "required": true,
    "type": "string"
  },
  "position": {
    "description": "Optional playlist item position.",
    "required": false,
    "type": "integer"
  },
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `create_channel_section`

Action slug: `create-channel-section`

Price: `25` credits

Create a channel section such as singlePlaylist, multiplePlaylists, multipleChannels, recentUploads, or popularUploads.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_ids` | `array` | no | Channel IDs for multipleChannels sections. |
| `playlist_id` | `string` | no | Single playlist ID shortcut. |
| `playlist_ids` | `array` | no | Playlist IDs for playlist-based sections. |
| `section_position` | `integer` | no | Section position. |
| `section_title` | `string` | no | Section title, required by multiplePlaylists and multipleChannels. |
| `section_type` | `string` | yes | Channel section type. |

Sample parameters:

```json
{
  "channel_ids": [
    "example channel id"
  ],
  "playlist_id": "example playlist id",
  "playlist_ids": [
    "example playlist id"
  ],
  "section_position": 1,
  "section_title": "example section title",
  "section_type": "example section type"
}
```

Generated JSON parameter schema:

```json
{
  "channel_ids": {
    "description": "Channel IDs for multipleChannels sections.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "playlist_id": {
    "description": "Single playlist ID shortcut.",
    "required": false,
    "type": "string"
  },
  "playlist_ids": {
    "description": "Playlist IDs for playlist-based sections.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "section_position": {
    "description": "Section position.",
    "required": false,
    "type": "integer"
  },
  "section_title": {
    "description": "Section title, required by multiplePlaylists and multipleChannels.",
    "required": false,
    "type": "string"
  },
  "section_type": {
    "description": "Channel section type.",
    "required": true,
    "type": "string"
  }
}
```

## `create_playlist`

Action slug: `create-playlist`

Price: `25` credits

Create a YouTube playlist.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `description` | `string` | no | Playlist description. |
| `privacy_status` | `string` | no | Playlist privacy status. Defaults to unlisted. |
| `tags` | `array` | no | Playlist tags. |
| `title` | `string` | yes | Playlist title. |

Sample parameters:

```json
{
  "description": "example description",
  "privacy_status": "public",
  "tags": [
    "example tag"
  ],
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "description": {
    "description": "Playlist description.",
    "required": false,
    "type": "string"
  },
  "privacy_status": {
    "description": "Playlist privacy status. Defaults to unlisted.",
    "enum": [
      "public",
      "unlisted",
      "private"
    ],
    "required": false,
    "type": "string"
  },
  "tags": {
    "description": "Playlist tags.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "title": {
    "description": "Playlist title.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_caption`

Action slug: `delete-caption`

Price: `25` credits

Delete a caption track.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption_id` | `string` | yes | YouTube caption track ID. |

Sample parameters:

```json
{
  "caption_id": "example caption id"
}
```

Generated JSON parameter schema:

```json
{
  "caption_id": {
    "description": "YouTube caption track ID.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_channel_section`

Action slug: `delete-channel-section`

Price: `25` credits

Delete a channel section.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_section_id` | `string` | yes | YouTube channelSection ID. |

Sample parameters:

```json
{
  "channel_section_id": "example channel section id"
}
```

Generated JSON parameter schema:

```json
{
  "channel_section_id": {
    "description": "YouTube channelSection ID.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_playlist`

Action slug: `delete-playlist`

Price: `25` credits

Delete a playlist.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `playlist_id` | `string` | yes | YouTube playlist ID. |

Sample parameters:

```json
{
  "playlist_id": "example playlist id"
}
```

Generated JSON parameter schema:

```json
{
  "playlist_id": {
    "description": "YouTube playlist ID.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_video`

Action slug: `delete-video`

Price: `25` credits

Delete a YouTube video by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `download_caption`

Action slug: `download-caption`

Price: `25` credits

Download a caption track and save it to AgentPMT File Manager.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption_format` | `string` | no | Caption output format. |
| `caption_id` | `string` | yes | YouTube caption track ID. |
| `output_filename` | `string` | no | Output filename in File Manager. |
| `translation_language` | `string` | no | Optional translation language. |

Sample parameters:

```json
{
  "caption_format": "sbv",
  "caption_id": "example caption id",
  "output_filename": "example output filename",
  "translation_language": "example translation language"
}
```

Generated JSON parameter schema:

```json
{
  "caption_format": {
    "description": "Caption output format.",
    "enum": [
      "sbv",
      "scc",
      "srt",
      "ttml",
      "vtt"
    ],
    "required": false,
    "type": "string"
  },
  "caption_id": {
    "description": "YouTube caption track ID.",
    "required": true,
    "type": "string"
  },
  "output_filename": {
    "description": "Output filename in File Manager.",
    "required": false,
    "type": "string"
  },
  "translation_language": {
    "description": "Optional translation language.",
    "required": false,
    "type": "string"
  }
}
```

## `get_my_channel`

Action slug: `get-my-channel`

Price: `25` credits

Fetch channel details for the connected account or a supplied channel ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | no | Optional YouTube channel ID. Omit for mine=true. |

Sample parameters:

```json
{
  "channel_id": "example channel id"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "Optional YouTube channel ID. Omit for mine=true.",
    "required": false,
    "type": "string"
  }
}
```

## `get_playlist`

Action slug: `get-playlist`

Price: `25` credits

Fetch a playlist by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `playlist_id` | `string` | yes | YouTube playlist ID. |

Sample parameters:

```json
{
  "playlist_id": "example playlist id"
}
```

Generated JSON parameter schema:

```json
{
  "playlist_id": {
    "description": "YouTube playlist ID.",
    "required": true,
    "type": "string"
  }
}
```

## `get_video`

Action slug: `get-video`

Price: `25` credits

Fetch a YouTube video by ID with supported read parts.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `get_youtube_capabilities`

Action slug: `get-youtube-capabilities`

Price: `25` credits

Return supported and unsupported YouTube public API capabilities.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_captions`

Action slug: `list-captions`

Price: `25` credits

List caption tracks associated with a video.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `list_channel_sections`

Action slug: `list-channel-sections`

Price: `25` credits

List channel sections for the connected account, a channel, or a section ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | no | Optional YouTube channel ID. |
| `channel_section_id` | `string` | no | Optional YouTube channelSection ID. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "channel_section_id": "example channel section id"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "Optional YouTube channel ID.",
    "required": false,
    "type": "string"
  },
  "channel_section_id": {
    "description": "Optional YouTube channelSection ID.",
    "required": false,
    "type": "string"
  }
}
```

## `list_playlist_items`

Action slug: `list-playlist-items`

Price: `25` credits

List items in a playlist.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum results per page, 1-50. |
| `page_token` | `string` | no | Pagination token. |
| `playlist_id` | `string` | yes | YouTube playlist ID. |

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
    "description": "Maximum results per page, 1-50.",
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Pagination token.",
    "required": false,
    "type": "string"
  },
  "playlist_id": {
    "description": "YouTube playlist ID.",
    "required": true,
    "type": "string"
  }
}
```

## `list_playlists`

Action slug: `list-playlists`

Price: `25` credits

List playlists for the connected YouTube channel.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_results` | `integer` | no | Maximum results per page, 1-50. |
| `page_token` | `string` | no | Pagination token. |

Sample parameters:

```json
{
  "max_results": 1,
  "page_token": "example page token"
}
```

Generated JSON parameter schema:

```json
{
  "max_results": {
    "description": "Maximum results per page, 1-50.",
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

## `list_video_categories`

Action slug: `list-video-categories`

Price: `25` credits

List supported YouTube video categories for a region.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hl` | `string` | no | Localized category language. |
| `region_code` | `string` | no | ISO region code. Defaults to US. |

Sample parameters:

```json
{
  "hl": "example hl",
  "region_code": "example region code"
}
```

Generated JSON parameter schema:

```json
{
  "hl": {
    "description": "Localized category language.",
    "required": false,
    "type": "string"
  },
  "region_code": {
    "description": "ISO region code. Defaults to US.",
    "required": false,
    "type": "string"
  }
}
```

## `remove_playlist_item`

Action slug: `remove-playlist-item`

Price: `25` credits

Remove a playlist item by playlistItem ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `playlist_item_id` | `string` | yes | YouTube playlistItem ID. |

Sample parameters:

```json
{
  "playlist_item_id": "example playlist item id"
}
```

Generated JSON parameter schema:

```json
{
  "playlist_item_id": {
    "description": "YouTube playlistItem ID.",
    "required": true,
    "type": "string"
  }
}
```

## `remove_video_from_playlist`

Action slug: `remove-video-from-playlist`

Price: `25` credits

Remove one or all playlist items matching a video ID from a playlist.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `playlist_id` | `string` | yes | YouTube playlist ID. |
| `remove_all` | `boolean` | no | Remove all matching playlist items. Defaults to true. |
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "playlist_id": "example playlist id",
  "remove_all": true,
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "playlist_id": {
    "description": "YouTube playlist ID.",
    "required": true,
    "type": "string"
  },
  "remove_all": {
    "description": "Remove all matching playlist items. Defaults to true.",
    "required": false,
    "type": "boolean"
  },
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `set_channel_watermark`

Action slug: `set-channel-watermark`

Price: `25` credits

Set a channel watermark from an AgentPMT File Manager image.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | yes | YouTube channel ID. |
| `target_channel_id` | `string` | no | Target channel ID linked from the watermark. |
| `watermark_content_type` | `string` | no | Optional watermark MIME type override. |
| `watermark_duration_ms` | `integer` | no | Watermark duration in milliseconds. |
| `watermark_file_id` | `string` | yes | File Manager image file_id. |
| `watermark_offset_ms` | `integer` | no | Watermark offset in milliseconds. |
| `watermark_timing_type` | `string` | no | Watermark timing type. |

Sample parameters:

```json
{
  "channel_id": "example channel id",
  "target_channel_id": "example target channel id",
  "watermark_content_type": "Draft marketing copy to check for banned phrases.",
  "watermark_duration_ms": 1,
  "watermark_file_id": "example watermark file id",
  "watermark_offset_ms": 1,
  "watermark_timing_type": "offsetFromStart"
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
  "target_channel_id": {
    "description": "Target channel ID linked from the watermark.",
    "required": false,
    "type": "string"
  },
  "watermark_content_type": {
    "description": "Optional watermark MIME type override.",
    "required": false,
    "type": "string"
  },
  "watermark_duration_ms": {
    "description": "Watermark duration in milliseconds.",
    "required": false,
    "type": "integer"
  },
  "watermark_file_id": {
    "description": "File Manager image file_id.",
    "required": true,
    "type": "string"
  },
  "watermark_offset_ms": {
    "description": "Watermark offset in milliseconds.",
    "required": false,
    "type": "integer"
  },
  "watermark_timing_type": {
    "description": "Watermark timing type.",
    "enum": [
      "offsetFromStart",
      "offsetFromEnd"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `set_video_thumbnail`

Action slug: `set-video-thumbnail`

Price: `25` credits

Set a custom video thumbnail from an AgentPMT File Manager image.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `thumbnail_content_type` | `string` | no | Optional thumbnail MIME type override. |
| `thumbnail_file_id` | `string` | yes | File Manager image file_id. |
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "thumbnail_content_type": "Draft marketing copy to check for banned phrases.",
  "thumbnail_file_id": "example thumbnail file id",
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "thumbnail_content_type": {
    "description": "Optional thumbnail MIME type override.",
    "required": false,
    "type": "string"
  },
  "thumbnail_file_id": {
    "description": "File Manager image file_id.",
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

## `unset_channel_watermark`

Action slug: `unset-channel-watermark`

Price: `25` credits

Remove a channel watermark.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_id` | `string` | yes | YouTube channel ID. |

Sample parameters:

```json
{
  "channel_id": "example channel id"
}
```

Generated JSON parameter schema:

```json
{
  "channel_id": {
    "description": "YouTube channel ID.",
    "required": true,
    "type": "string"
  }
}
```

## `update_caption`

Action slug: `update-caption`

Price: `25` credits

Update a caption file, draft status, or both.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption_content_type` | `string` | no | Optional caption MIME type override. |
| `caption_file_id` | `string` | no | Optional File Manager caption file_id. |
| `caption_id` | `string` | yes | YouTube caption track ID. |
| `is_draft` | `boolean` | no | Caption draft status. |

Sample parameters:

```json
{
  "caption_content_type": "Draft marketing copy to check for banned phrases.",
  "caption_file_id": "example caption file id",
  "caption_id": "example caption id",
  "is_draft": true
}
```

Generated JSON parameter schema:

```json
{
  "caption_content_type": {
    "description": "Optional caption MIME type override.",
    "required": false,
    "type": "string"
  },
  "caption_file_id": {
    "description": "Optional File Manager caption file_id.",
    "required": false,
    "type": "string"
  },
  "caption_id": {
    "description": "YouTube caption track ID.",
    "required": true,
    "type": "string"
  },
  "is_draft": {
    "description": "Caption draft status.",
    "required": false,
    "type": "boolean"
  }
}
```

## `update_channel_branding`

Action slug: `update-channel-branding`

Price: `25` credits

Update safe channel branding fields using fetch-merge-update semantics.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_description` | `string` | no | Channel branding description. |
| `channel_id` | `string` | no | Optional YouTube channel ID. Omit for mine=true. |
| `country` | `string` | no | Channel country code. |
| `default_language` | `string` | no | Channel default language. |
| `keywords` | `string` | no | Channel keywords. |
| `unsubscribed_trailer_video_id` | `string` | no | Channel trailer video ID. |

Sample parameters:

```json
{
  "channel_description": "example channel description",
  "channel_id": "example channel id",
  "country": "example country",
  "default_language": "example default language",
  "keywords": "example keywords",
  "unsubscribed_trailer_video_id": "example unsubscribed trailer video id"
}
```

Generated JSON parameter schema:

```json
{
  "channel_description": {
    "description": "Channel branding description.",
    "required": false,
    "type": "string"
  },
  "channel_id": {
    "description": "Optional YouTube channel ID. Omit for mine=true.",
    "required": false,
    "type": "string"
  },
  "country": {
    "description": "Channel country code.",
    "required": false,
    "type": "string"
  },
  "default_language": {
    "description": "Channel default language.",
    "required": false,
    "type": "string"
  },
  "keywords": {
    "description": "Channel keywords.",
    "required": false,
    "type": "string"
  },
  "unsubscribed_trailer_video_id": {
    "description": "Channel trailer video ID.",
    "required": false,
    "type": "string"
  }
}
```

## `update_channel_section`

Action slug: `update-channel-section`

Price: `25` credits

Update a channel section.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `channel_ids` | `array` | no | Channel IDs for multipleChannels sections. |
| `channel_section_id` | `string` | yes | YouTube channelSection ID. |
| `playlist_id` | `string` | no | Single playlist ID shortcut. |
| `playlist_ids` | `array` | no | Playlist IDs for playlist-based sections. |
| `section_position` | `integer` | no | Section position. |
| `section_title` | `string` | no | Section title. |
| `section_type` | `string` | yes | Channel section type. |

Sample parameters:

```json
{
  "channel_ids": [
    "example channel id"
  ],
  "channel_section_id": "example channel section id",
  "playlist_id": "example playlist id",
  "playlist_ids": [
    "example playlist id"
  ],
  "section_position": 1,
  "section_title": "example section title",
  "section_type": "example section type"
}
```

Generated JSON parameter schema:

```json
{
  "channel_ids": {
    "description": "Channel IDs for multipleChannels sections.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "channel_section_id": {
    "description": "YouTube channelSection ID.",
    "required": true,
    "type": "string"
  },
  "playlist_id": {
    "description": "Single playlist ID shortcut.",
    "required": false,
    "type": "string"
  },
  "playlist_ids": {
    "description": "Playlist IDs for playlist-based sections.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "section_position": {
    "description": "Section position.",
    "required": false,
    "type": "integer"
  },
  "section_title": {
    "description": "Section title.",
    "required": false,
    "type": "string"
  },
  "section_type": {
    "description": "Channel section type.",
    "required": true,
    "type": "string"
  }
}
```

## `update_playlist`

Action slug: `update-playlist`

Price: `25` credits

Update mutable playlist fields using fetch-merge-update semantics.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `description` | `string` | no | Playlist description. |
| `playlist_id` | `string` | yes | YouTube playlist ID. |
| `privacy_status` | `string` | no | Playlist privacy status. |
| `tags` | `array` | no | Playlist tags. |
| `title` | `string` | no | Playlist title. |

Sample parameters:

```json
{
  "description": "example description",
  "playlist_id": "example playlist id",
  "privacy_status": "public",
  "tags": [
    "example tag"
  ],
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "description": {
    "description": "Playlist description.",
    "required": false,
    "type": "string"
  },
  "playlist_id": {
    "description": "YouTube playlist ID.",
    "required": true,
    "type": "string"
  },
  "privacy_status": {
    "description": "Playlist privacy status.",
    "enum": [
      "public",
      "unlisted",
      "private"
    ],
    "required": false,
    "type": "string"
  },
  "tags": {
    "description": "Playlist tags.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "title": {
    "description": "Playlist title.",
    "required": false,
    "type": "string"
  }
}
```

## `update_video`

Action slug: `update-video`

Price: `25` credits

Update mutable YouTube video fields using fetch-merge-update semantics to preserve omitted metadata.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category_id` | `string` | no | YouTube video category ID. |
| `contains_synthetic_media` | `boolean` | no | Synthetic media disclosure. |
| `default_language` | `string` | no | Default metadata language. |
| `description` | `string` | no | Video description. |
| `embeddable` | `boolean` | no | Whether the video can be embedded. |
| `license` | `string` | no | Video license. |
| `localizations` | `object` | no | Localized metadata keyed by locale. Each value may contain title and description. |
| `made_for_kids` | `boolean` | no | Set status.selfDeclaredMadeForKids. |
| `privacy_status` | `string` | no | Video privacy status. |
| `public_stats_viewable` | `boolean` | no | Whether public stats are visible. |
| `publish_at` | `string` | no | Scheduled publish time. Requires privacy_status private. |
| `recording_date` | `string` | no | Recording date. |
| `tags` | `array` | no | Video tags. |
| `title` | `string` | no | Video title. |
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "category_id": "example category id",
  "contains_synthetic_media": true,
  "default_language": "example default language",
  "description": "example description",
  "embeddable": true,
  "license": "youtube",
  "localizations": {},
  "made_for_kids": true
}
```

Generated JSON parameter schema:

```json
{
  "category_id": {
    "description": "YouTube video category ID.",
    "required": false,
    "type": "string"
  },
  "contains_synthetic_media": {
    "description": "Synthetic media disclosure.",
    "required": false,
    "type": "boolean"
  },
  "default_language": {
    "description": "Default metadata language.",
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Video description.",
    "required": false,
    "type": "string"
  },
  "embeddable": {
    "description": "Whether the video can be embedded.",
    "required": false,
    "type": "boolean"
  },
  "license": {
    "description": "Video license.",
    "enum": [
      "youtube",
      "creativeCommon"
    ],
    "required": false,
    "type": "string"
  },
  "localizations": {
    "description": "Localized metadata keyed by locale. Each value may contain title and description.",
    "required": false,
    "type": "object"
  },
  "made_for_kids": {
    "description": "Set status.selfDeclaredMadeForKids.",
    "required": false,
    "type": "boolean"
  },
  "privacy_status": {
    "description": "Video privacy status.",
    "enum": [
      "public",
      "unlisted",
      "private"
    ],
    "required": false,
    "type": "string"
  },
  "public_stats_viewable": {
    "description": "Whether public stats are visible.",
    "required": false,
    "type": "boolean"
  },
  "publish_at": {
    "description": "Scheduled publish time. Requires privacy_status private.",
    "required": false,
    "type": "string"
  },
  "recording_date": {
    "description": "Recording date.",
    "required": false,
    "type": "string"
  },
  "tags": {
    "description": "Video tags.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "title": {
    "description": "Video title.",
    "required": false,
    "type": "string"
  },
  "video_id": {
    "description": "YouTube video ID.",
    "required": true,
    "type": "string"
  }
}
```

## `upload_caption`

Action slug: `upload-caption`

Price: `25` credits

Upload a caption file from AgentPMT File Manager.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption_content_type` | `string` | no | Optional caption MIME type override. |
| `caption_file_id` | `string` | yes | File Manager caption file_id. |
| `is_draft` | `boolean` | no | Caption draft status. |
| `language` | `string` | yes | Caption language code. |
| `name` | `string` | yes | Caption track name. |
| `video_id` | `string` | yes | YouTube video ID. |

Sample parameters:

```json
{
  "caption_content_type": "Draft marketing copy to check for banned phrases.",
  "caption_file_id": "example caption file id",
  "is_draft": true,
  "language": "example language",
  "name": "example name",
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "caption_content_type": {
    "description": "Optional caption MIME type override.",
    "required": false,
    "type": "string"
  },
  "caption_file_id": {
    "description": "File Manager caption file_id.",
    "required": true,
    "type": "string"
  },
  "is_draft": {
    "description": "Caption draft status.",
    "required": false,
    "type": "boolean"
  },
  "language": {
    "description": "Caption language code.",
    "required": true,
    "type": "string"
  },
  "name": {
    "description": "Caption track name.",
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

## `upload_video`

Action slug: `upload-video`

Price: `25` credits

Upload a video from AgentPMT File Manager to YouTube with metadata, privacy, scheduling, and optional playlist placement.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category_id` | `string` | no | YouTube video category ID. |
| `chunk_size_bytes` | `integer` | no | Resumable upload chunk size in bytes. |
| `contains_synthetic_media` | `boolean` | no | Synthetic media disclosure. |
| `default_language` | `string` | no | Default metadata language such as en. |
| `description` | `string` | no | Video description. Plain text links are supported here. |
| `embeddable` | `boolean` | no | Whether the video can be embedded. |
| `license` | `string` | no | Video license. |
| `localizations` | `object` | no | Localized metadata keyed by locale. Each value may contain title and description. |
| `made_for_kids` | `boolean` | no | Set status.selfDeclaredMadeForKids. |
| `notify_subscribers` | `boolean` | no | Notify subscribers on upload. Defaults to false. |
| `playlist_id` | `string` | no | Optional playlist ID to add the uploaded video to. |
| `position` | `integer` | no | Optional playlist item position. |
| `privacy_status` | `string` | no | Video privacy status. Defaults to unlisted. |
| `public_stats_viewable` | `boolean` | no | Whether public stats are visible. |
| `publish_at` | `string` | no | Scheduled publish time. Requires privacy_status private. |
| `recording_date` | `string` | no | Recording date for recordingDetails.recordingDate. |
| `source_content_type` | `string` | no | Optional video MIME type override. |
| `source_file_id` | `string` | yes | File Manager video file_id. |
| `tags` | `array` | no | Video tags. |
| `title` | `string` | yes | Video title. |

Sample parameters:

```json
{
  "category_id": "example category id",
  "chunk_size_bytes": 1,
  "contains_synthetic_media": true,
  "default_language": "example default language",
  "description": "example description",
  "embeddable": true,
  "license": "youtube",
  "localizations": {}
}
```

Generated JSON parameter schema:

```json
{
  "category_id": {
    "description": "YouTube video category ID.",
    "required": false,
    "type": "string"
  },
  "chunk_size_bytes": {
    "description": "Resumable upload chunk size in bytes.",
    "required": false,
    "type": "integer"
  },
  "contains_synthetic_media": {
    "description": "Synthetic media disclosure.",
    "required": false,
    "type": "boolean"
  },
  "default_language": {
    "description": "Default metadata language such as en.",
    "required": false,
    "type": "string"
  },
  "description": {
    "description": "Video description. Plain text links are supported here.",
    "required": false,
    "type": "string"
  },
  "embeddable": {
    "description": "Whether the video can be embedded.",
    "required": false,
    "type": "boolean"
  },
  "license": {
    "description": "Video license.",
    "enum": [
      "youtube",
      "creativeCommon"
    ],
    "required": false,
    "type": "string"
  },
  "localizations": {
    "description": "Localized metadata keyed by locale. Each value may contain title and description.",
    "required": false,
    "type": "object"
  },
  "made_for_kids": {
    "description": "Set status.selfDeclaredMadeForKids.",
    "required": false,
    "type": "boolean"
  },
  "notify_subscribers": {
    "description": "Notify subscribers on upload. Defaults to false.",
    "required": false,
    "type": "boolean"
  },
  "playlist_id": {
    "description": "Optional playlist ID to add the uploaded video to.",
    "required": false,
    "type": "string"
  },
  "position": {
    "description": "Optional playlist item position.",
    "required": false,
    "type": "integer"
  },
  "privacy_status": {
    "description": "Video privacy status. Defaults to unlisted.",
    "enum": [
      "public",
      "unlisted",
      "private"
    ],
    "required": false,
    "type": "string"
  },
  "public_stats_viewable": {
    "description": "Whether public stats are visible.",
    "required": false,
    "type": "boolean"
  },
  "publish_at": {
    "description": "Scheduled publish time. Requires privacy_status private.",
    "required": false,
    "type": "string"
  },
  "recording_date": {
    "description": "Recording date for recordingDetails.recordingDate.",
    "required": false,
    "type": "string"
  },
  "source_content_type": {
    "description": "Optional video MIME type override.",
    "required": false,
    "type": "string"
  },
  "source_file_id": {
    "description": "File Manager video file_id.",
    "required": true,
    "type": "string"
  },
  "tags": {
    "description": "Video tags.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "title": {
    "description": "Video title.",
    "required": true,
    "type": "string"
  }
}
```

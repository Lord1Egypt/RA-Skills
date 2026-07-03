---
name: youtube-channel-management
description: "YouTube Channel Management: Upload File Manager videos, update video metadata, privacy, localizations, thumbnails, captions, playlists, playlist items, channel sections, channel branding, watermarks, and discover YouTube categories/capabilities. Use when an agent needs youtube channel management, youtube api, upload youtube shorts or standard videos from file manager; update titles, descriptions, tags, privacy, add video to playlist, playlist id through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/youtube-api
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/youtube-api"}}
---
# YouTube Channel Management

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Upload File Manager videos to YouTube, set metadata, thumbnails, captions, privacy, and publish timing, then organize channel content with playlists, channel sections, branding, and watermarks.

## Product Instructions
### YouTube Channel Management

Upload File Manager videos, edit video metadata/privacy, manage thumbnails, captions, playlists, channel sections, branding, and watermarks.

#### Video Actions

##### `upload_video`
Required: `source_file_id`, `title`
Optional: `description`, `tags`, `category_id`, `default_language`, `localizations`, `privacy_status` (`public`/`unlisted`/`private`, default `unlisted`), `publish_at`, `made_for_kids`, `license` (`youtube`/`creativeCommon`), `embeddable`, `public_stats_viewable`, `contains_synthetic_media`, `recording_date`, `notify_subscribers` (default `false`), `playlist_id`, `position`, `source_content_type`, `chunk_size_bytes`

```json
{"action":"upload_video","source_file_id":"file_abc123","title":"Product Demo","description":"Short walkthrough","privacy_status":"unlisted","notify_subscribers":false}
```

##### `get_video`
Required: `video_id`

```json
{"action":"get_video","video_id":"dQw4w9WgXcQ"}
```

##### `update_video`
Required: `video_id` plus at least one video metadata/status field from `upload_video`.

```json
{"action":"update_video","video_id":"dQw4w9WgXcQ","title":"Updated Title","license":"creativeCommon","embeddable":true}
```

##### `delete_video`
Required: `video_id`

```json
{"action":"delete_video","video_id":"dQw4w9WgXcQ"}
```

##### `set_video_thumbnail`
Required: `video_id`, `thumbnail_file_id`
Optional: `thumbnail_content_type`

```json
{"action":"set_video_thumbnail","video_id":"dQw4w9WgXcQ","thumbnail_file_id":"file_thumb123"}
```

#### Caption Actions

##### `list_captions`
Required: `video_id`

```json
{"action":"list_captions","video_id":"dQw4w9WgXcQ"}
```

##### `upload_caption`
Required: `video_id`, `caption_file_id`, `language`, `name`
Optional: `is_draft`, `caption_content_type`

```json
{"action":"upload_caption","video_id":"dQw4w9WgXcQ","caption_file_id":"file_srt123","language":"en","name":"English","is_draft":false}
```

##### `update_caption`
Required: `caption_id` and at least one of `caption_file_id`, `is_draft`
Optional: `caption_content_type`

```json
{"action":"update_caption","caption_id":"caption123","is_draft":true}
```

##### `download_caption`
Required: `caption_id`
Optional: `caption_format` (`sbv`/`scc`/`srt`/`ttml`/`vtt`), `translation_language`, `output_filename`

```json
{"action":"download_caption","caption_id":"caption123","caption_format":"srt","output_filename":"captions.srt"}
```

##### `delete_caption`
Required: `caption_id`

```json
{"action":"delete_caption","caption_id":"caption123"}
```

#### Playlist Actions

##### `create_playlist`
Required: `title`
Optional: `description`, `tags`, `privacy_status` (`public`/`unlisted`/`private`, default `unlisted`)

```json
{"action":"create_playlist","title":"Customer Stories Q2","privacy_status":"private"}
```

##### `list_playlists`
Optional: `max_results` (1-50, default `25`), `page_token`

```json
{"action":"list_playlists","max_results":10}
```

##### `get_playlist`, `update_playlist`, `delete_playlist`
Required: `playlist_id`; update also needs one of `title`, `description`, `tags`, `privacy_status`.

```json
{"action":"update_playlist","playlist_id":"PLxxxxxxxx","title":"Updated Playlist"}
```

##### `add_video_to_playlist`
Required: `playlist_id`, `video_id`
Optional: `position`

```json
{"action":"add_video_to_playlist","playlist_id":"PLxxxxxxxx","video_id":"dQw4w9WgXcQ","position":0}
```

##### `list_playlist_items`
Required: `playlist_id`
Optional: `max_results` (1-50), `page_token`

```json
{"action":"list_playlist_items","playlist_id":"PLxxxxxxxx","max_results":50}
```

##### `remove_playlist_item`, `remove_video_from_playlist`
Use `remove_playlist_item` with `playlist_item_id`, or `remove_video_from_playlist` with `playlist_id`, `video_id`, optional `remove_all`.

```json
{"action":"remove_video_from_playlist","playlist_id":"PLxxxxxxxx","video_id":"dQw4w9WgXcQ","remove_all":true}
```

#### Channel Actions

##### `get_my_channel`
Optional: `channel_id` (omit to use the connected account's channel)

```json
{"action":"get_my_channel"}
```

##### `update_channel_branding`
Optional filter: `channel_id`
Required: at least one of `channel_description`, `keywords`, `country`, `default_language`, `unsubscribed_trailer_video_id`

```json
{"action":"update_channel_branding","channel_description":"Official product videos and tutorials","country":"US"}
```

##### Channel sections
Actions: `list_channel_sections`, `create_channel_section`, `update_channel_section`, `delete_channel_section`
Use `section_type`, `section_title`, `section_position`, `playlist_ids`, `channel_ids`, and `channel_section_id` as required by the action.

```json
{"action":"create_channel_section","section_type":"multiplePlaylists","section_title":"Product Videos","playlist_ids":["PLxxxxxxxx"]}
```

##### Watermarks
Actions: `set_channel_watermark`, `unset_channel_watermark`
Set requires `channel_id`, `watermark_file_id`; optional `watermark_timing_type`, `watermark_offset_ms`, `watermark_duration_ms`, `target_channel_id`, `watermark_content_type`.
Watermark position is fixed to YouTube's top-right corner placement; timing is configurable.

```json
{"action":"set_channel_watermark","channel_id":"UCxxxx","watermark_file_id":"file_watermark123","watermark_offset_ms":0}
```

#### Discovery

##### `list_video_categories`
Optional: `region_code` (default `US`), `hl`

```json
{"action":"list_video_categories","region_code":"US"}
```

##### `get_youtube_capabilities`
Returns supported API-backed features and unsupported Studio-only surfaces.

```json
{"action":"get_youtube_capabilities"}
```

#### Notes

- Video, thumbnail, caption, and watermark uploads require File Manager file IDs.
- Update actions fetch current YouTube resources and merge supplied fields to avoid clearing omitted metadata.
- Links in descriptions are supported as description text. Public API support is not available for cards, end screens, or custom in-video linked-video elements; use playlists and channel sections for connected video organization.

## When To Use
- Use this skill for `YouTube Channel Management` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: youtube channel management, youtube api, upload youtube shorts or standard videos from file manager; update titles, descriptions, tags, privacy, add video to playlist, playlist id.
- Supported action names: `add_video_to_playlist`, `create_channel_section`, `create_playlist`, `delete_caption`, `delete_channel_section`, `delete_playlist`, `delete_video`, `download_caption`, `get_my_channel`, `get_playlist`, `get_video`, `get_youtube_capabilities`, `list_captions`, `list_channel_sections`, `list_playlist_items`, `list_playlists`, `list_video_categories`, `remove_playlist_item`, `remove_video_from_playlist`, `set_channel_watermark`, `set_video_thumbnail`, `unset_channel_watermark`, `update_caption`, `update_channel_branding`, `update_channel_section`, `update_playlist`, `update_video`, `upload_caption`, `upload_video`.

## Use Cases
- Upload YouTube Shorts or standard videos from File Manager; update titles
- descriptions
- tags
- privacy
- licensing
- synthetic media disclosure
- publish scheduling
- and localizations; set custom thumbnails; upload
- update
- download
- list
- and delete captions; create and manage playlists and playlist items; manage channel sections for connected video organization; update safe channel branding fields; set or unset channel watermarks; discover categories and API capability limits.

## Related Product Skills
- File Storage - 10MB or less: ../file-storage-10mb-or-less (ClawHub: `file-storage-10mb-or-less`, page: https://clawhub.ai/agentpmt/file-storage-10mb-or-less; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-10mb-or-less`)
- File Storage - Over 10MB: ../file-storage-over-10mb (ClawHub: `file-storage-over-10mb`, page: https://clawhub.ai/agentpmt/file-storage-over-10mb; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-over-10mb`)
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `29`.
x402 availability: not enabled for this product.

- `add_video_to_playlist` (action slug: `add-video-to-playlist`): Add a YouTube video to a playlist. Price: `25` credits. Parameters: `playlist_id`, `position`, `video_id`.
- `create_channel_section` (action slug: `create-channel-section`): Create a channel section such as singlePlaylist, multiplePlaylists, multipleChannels, recentUploads, or popularUploads. Price: `25` credits. Parameters: `channel_ids`, `playlist_id`, `playlist_ids`, `section_position`, `section_title`, `section_type`.
- `create_playlist` (action slug: `create-playlist`): Create a YouTube playlist. Price: `25` credits. Parameters: `description`, `privacy_status`, `tags`, `title`.
- `delete_caption` (action slug: `delete-caption`): Delete a caption track. Price: `25` credits. Parameters: `caption_id`.
- `delete_channel_section` (action slug: `delete-channel-section`): Delete a channel section. Price: `25` credits. Parameters: `channel_section_id`.
- `delete_playlist` (action slug: `delete-playlist`): Delete a playlist. Price: `25` credits. Parameters: `playlist_id`.
- `delete_video` (action slug: `delete-video`): Delete a YouTube video by ID. Price: `25` credits. Parameters: `video_id`.
- `download_caption` (action slug: `download-caption`): Download a caption track and save it to AgentPMT File Manager. Price: `25` credits. Parameters: `caption_format`, `caption_id`, `output_filename`, `translation_language`.
- `get_my_channel` (action slug: `get-my-channel`): Fetch channel details for the connected account or a supplied channel ID. Price: `25` credits. Parameters: `channel_id`.
- `get_playlist` (action slug: `get-playlist`): Fetch a playlist by ID. Price: `25` credits. Parameters: `playlist_id`.
- `get_video` (action slug: `get-video`): Fetch a YouTube video by ID with supported read parts. Price: `25` credits. Parameters: `video_id`.
- `get_youtube_capabilities` (action slug: `get-youtube-capabilities`): Return supported and unsupported YouTube public API capabilities. Price: `25` credits. Parameters: none.
- `list_captions` (action slug: `list-captions`): List caption tracks associated with a video. Price: `25` credits. Parameters: `video_id`.
- `list_channel_sections` (action slug: `list-channel-sections`): List channel sections for the connected account, a channel, or a section ID. Price: `25` credits. Parameters: `channel_id`, `channel_section_id`.
- `list_playlist_items` (action slug: `list-playlist-items`): List items in a playlist. Price: `25` credits. Parameters: `max_results`, `page_token`, `playlist_id`.
- `list_playlists` (action slug: `list-playlists`): List playlists for the connected YouTube channel. Price: `25` credits. Parameters: `max_results`, `page_token`.
- `list_video_categories` (action slug: `list-video-categories`): List supported YouTube video categories for a region. Price: `25` credits. Parameters: `hl`, `region_code`.
- `remove_playlist_item` (action slug: `remove-playlist-item`): Remove a playlist item by playlistItem ID. Price: `25` credits. Parameters: `playlist_item_id`.
- `remove_video_from_playlist` (action slug: `remove-video-from-playlist`): Remove one or all playlist items matching a video ID from a playlist. Price: `25` credits. Parameters: `playlist_id`, `remove_all`, `video_id`.
- `set_channel_watermark` (action slug: `set-channel-watermark`): Set a channel watermark from an AgentPMT File Manager image. Price: `25` credits. Parameters: `channel_id`, `target_channel_id`, `watermark_content_type`, `watermark_duration_ms`, `watermark_file_id`, `watermark_offset_ms`, `watermark_timing_type`.
- `set_video_thumbnail` (action slug: `set-video-thumbnail`): Set a custom video thumbnail from an AgentPMT File Manager image. Price: `25` credits. Parameters: `thumbnail_content_type`, `thumbnail_file_id`, `video_id`.
- `unset_channel_watermark` (action slug: `unset-channel-watermark`): Remove a channel watermark. Price: `25` credits. Parameters: `channel_id`.
- `update_caption` (action slug: `update-caption`): Update a caption file, draft status, or both. Price: `25` credits. Parameters: `caption_content_type`, `caption_file_id`, `caption_id`, `is_draft`.
- `update_channel_branding` (action slug: `update-channel-branding`): Update safe channel branding fields using fetch-merge-update semantics. Price: `25` credits. Parameters: `channel_description`, `channel_id`, `country`, `default_language`, `keywords`, `unsubscribed_trailer_video_id`.
- `update_channel_section` (action slug: `update-channel-section`): Update a channel section. Price: `25` credits. Parameters: `channel_ids`, `channel_section_id`, `playlist_id`, `playlist_ids`, `section_position`, `section_title`, `section_type`.
- `update_playlist` (action slug: `update-playlist`): Update mutable playlist fields using fetch-merge-update semantics. Price: `25` credits. Parameters: `description`, `playlist_id`, `privacy_status`, `tags`, `title`.
- `update_video` (action slug: `update-video`): Update mutable YouTube video fields using fetch-merge-update semantics to preserve omitted metadata. Price: `25` credits. Parameters: `category_id`, `contains_synthetic_media`, `default_language`, `description`, `embeddable`, `license`, `localizations`, `made_for_kids`, plus 7 more.
- `upload_caption` (action slug: `upload-caption`): Upload a caption file from AgentPMT File Manager. Price: `25` credits. Parameters: `caption_content_type`, `caption_file_id`, `is_draft`, `language`, `name`, `video_id`.
- `upload_video` (action slug: `upload-video`): Upload a video from AgentPMT File Manager to YouTube with metadata, privacy, scheduling, and optional playlist placement. Price: `25` credits. Parameters: `category_id`, `chunk_size_bytes`, `contains_synthetic_media`, `default_language`, `description`, `embeddable`, `license`, `localizations`, plus 12 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "youtube-api"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "youtube-api"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "youtube-api"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "youtube-api"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "youtube-api"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "youtube-api"
  }
}
```

## Call This Tool
Product slug: `youtube-api`

Marketplace page: https://www.agentpmt.com/marketplace/youtube-api

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "YouTube-Channel-Management",
    "arguments": {
      "action": "add_video_to_playlist",
      "playlist_id": "example playlist id",
      "position": 1,
      "video_id": "example video id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "youtube-api",
  "parameters": {
    "action": "add_video_to_playlist",
    "playlist_id": "example playlist id",
    "position": 1,
    "video_id": "example video id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `add_video_to_playlist` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/youtube-api
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase

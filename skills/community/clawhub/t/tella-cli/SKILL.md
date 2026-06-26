---
name: tella
description: "Manage Tella via CLI - videos, clips, playlists, webhooks. Use when user mentions 'tella', 'tella.tv', 'tella video', 'screen recording', 'video transcript', 'clip thumbnail', 'video export', 'remove filler words', 'add zoom to video', 'blur video', 'highlight video', 'playlist of videos', or wants to interact with the Tella video recording/editing API."
category: video
---

# tella-cli

## When To Use This Skill

Use the `tella-cli` skill when you need to:

- List, fetch, update, or delete videos in a Tella workspace
- Pull transcripts (cut or uncut) for a clip with word-level timestamps
- Generate video or clip thumbnails (jpg/png/webp/gif/mp4) at custom sizes/timestamps
- Trigger video exports at 1080p or 4k, 30/60fps, with optional burned-in subtitles
- Duplicate a video or clip, optionally trimmed
- Edit clips: cut time ranges, reorder, remove filler words, find silent ranges
- Add or update visual edits: blurs, highlights, layouts, zooms (manual or tracking)
- Manage playlists and add/remove videos from them
- Add workspace collaborators (editor or viewer) to a video
- Create webhook endpoints, fetch signing secrets, and inspect recent deliveries

## Capabilities

- Read every video and playlist in the workspace, including metadata, view counts, and share links
- Push fine-grained edits to clips (cuts, reorders, blurs, highlights, layouts, zooms) without opening the Tella editor
- Pull transcripts for downstream search, summarization, or accessibility workflows
- Start exports and poll/list webhook deliveries to know when files are ready
- Manage sharing: `linkScope`, password, allowed embed domains, search-engine indexing
- Subscribe to events (`video.created`, `export.ready`, `transcript.ready`, etc.) and recover delivery messages

## Common Use Cases

- "List my last 20 Tella videos and dump them as JSON for a content audit"
- "Get the uncut transcript for clip X so I can generate chapter timestamps"
- "Export video Y at 4k 60fps with subtitles burned in"
- "Add a blur over the credentials shown between 4.2s and 7.8s on this clip"
- "Create a playlist 'Tutorials' and add these 5 videos to it"
- "Wire up a webhook so I get notified when an export is ready"
- "Remove filler words from this clip and then fetch the cleaned transcript"

## Setup

If `tella-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle tella
npx api2cli link tella
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` when calling commands programmatically.

## Working Rules

- Always use `--json` for agent-driven calls so downstream steps can parse the result
- Run `<resource> --help` or `<resource> <action> --help` when unsure of flags rather than guessing
- For destructive actions (`delete`, `remove-*`), read first with `get`/`list` to confirm the target
- Most clip mutations require both `<videoId>` and `<clipId>` as positional args (in that order)
- Coordinates for masks (blurs, highlights) and zoom focus points are normalized to `0-1` of the canvas
- Times are in milliseconds (`*-ms` flags) unless the docs say otherwise

## Authentication

```bash
tella-cli auth set "tella_pk_xxx..."   # API key from https://www.tella.tv/settings/api-keys
tella-cli auth test                     # Verify the key works
tella-cli auth show                     # Show masked token
tella-cli auth remove                   # Delete stored token
```

Token is stored at `~/.config/tokens/tella-cli.txt` (chmod 600).

## Resources

### videos

| Action | Description | Key Flags |
|--------|-------------|-----------|
| `list` | List videos in the workspace | `--cursor`, `--limit`, `--playlist-id`, `--fields` |
| `get <id>` | Get a single video's metadata | - |
| `update <id>` | Update title, description, sharing, playback | `--name`, `--description`, `--link-scope`, `--password`, `--allowed-embed-domains`, `--custom-thumbnail-url`, `--default-playback-rate`, `--captions-default-enabled`, `--comments-enabled`, `--comment-emails-enabled`, `--downloads-enabled`, `--raw-downloads-enabled`, `--publish-date-enabled`, `--search-engine-indexing-enabled`, `--transcripts-enabled`, `--view-count-enabled` |
| `delete <id>` | Delete a video | - |
| `duplicate <id>` | Duplicate, optionally trimmed | `--name`, `--trim-start-ms`, `--trim-end-ms` |
| `export <id>` | Start an export job | `--resolution` (1080p/4k), `--fps` (30/60), `--speed`, `--granularity` (video/clips/raw), `--subtitles` |
| `thumbnail <id>` | Get thumbnail/animated preview | `--format` (jpg/png/webp/gif/mp4), `--inpoint-ms`, `--duration-ms`, `--width`, `--height`, `--download`, `--response json` |
| `add-collaborator <id>` | Add a workspace member | `--email` (required), `--role editor\|viewer` (required) |

### clips

Most clip commands take `<videoId> <clipId>` as positional args.

| Action | Description | Key Flags |
|--------|-------------|-----------|
| `list <videoId>` | List clips for a video | `--fields` |
| `get <videoId> <clipId>` | Get a single clip | - |
| `update <videoId> <clipId>` | Rename or reorder | `--name`, `--order` |
| `delete <videoId> <clipId>` | Delete a clip | - |
| `duplicate <videoId> <clipId>` | Duplicate the clip | `--name`, `--order` |
| `cut <videoId> <clipId>` | Cut a time range out | `--from-ms` (req), `--to-ms` (req) |
| `reorder <videoId> <clipId>` | Move to new position | `--order` (req) |
| `remove-fillers <videoId> <clipId>` | Auto-remove filler words | - |
| `silences <videoId> <clipId>` | List silent ranges | `--min-duration-ms` |
| `transcript-cut <videoId> <clipId>` | Edited transcript (post-cuts) | - |
| `transcript-uncut <videoId> <clipId>` | Original transcript | - |
| `thumbnail <videoId> <clipId>` | Clip thumbnail/preview | `--format`, `--inpoint-ms`, `--duration-ms`, `--width`, `--height`, `--download`, `--response` |
| `list-sources <videoId> <clipId>` | List recording sources | `--fields` |
| `source-thumbnail <videoId> <clipId> <sourceId>` | Source thumbnail | same as clip `thumbnail` |
| `source-waveform <videoId> <clipId> <sourceId>` | Audio waveform JSON | - |
| `list-blurs <videoId> <clipId>` | List blur masks | - |
| `add-blur <videoId> <clipId>` | Add a blur mask | `--start-time-ms`, `--duration-ms`, `--point-x`, `--point-y`, `--dim-width`, `--dim-height` (all required) |
| `update-blur <videoId> <clipId> <maskId>` | Update a blur | any of the mask flags above |
| `remove-blur <videoId> <clipId> <maskId>` | Remove a blur | - |
| `list-highlights <videoId> <clipId>` | List highlight masks | - |
| `add-highlight <videoId> <clipId>` | Add a highlight | same mask flags as `add-blur` |
| `update-highlight <videoId> <clipId> <maskId>` | Update a highlight | mask flags |
| `remove-highlight <videoId> <clipId> <maskId>` | Remove a highlight | - |
| `list-layouts <videoId> <clipId>` | List layouts | - |
| `add-layout <videoId> <clipId>` | Add a layout (JSON shape) | `--layout` (JSON, req), `--start-time-ms`, `--duration-ms`, `--transition-style` |
| `update-layout <videoId> <clipId> <layoutId>` | Update a layout | `--layout`, time flags, `--transition-style` |
| `remove-layout <videoId> <clipId> <layoutId>` | Remove a layout | - |
| `list-zooms <videoId> <clipId>` | List zooms | - |
| `add-zoom <videoId> <clipId>` | Add a zoom | `--type manualZoom\|trackingZoom` (req), `--start-time-ms` (req), `--duration-ms` (req), `--scale`, `--focus-x`, `--focus-y` |
| `update-zoom <videoId> <clipId> <zoomId>` | Update a zoom | same as `add-zoom` |
| `remove-zoom <videoId> <clipId> <zoomId>` | Remove a zoom | - |

Mask coordinates (`--point-*`, `--dim-*`, `--focus-*`) are normalized `0-1` of the canvas.

### playlists

| Action | Description | Key Flags |
|--------|-------------|-----------|
| `list` | List all playlists | `--visibility` (personal/org), `--cursor`, `--limit`, `--fields` |
| `get <id>` | Get playlist details | - |
| `create` | Create a new playlist | `--name` (req), `--description`, `--emoji`, `--link-scope`, `--password`, `--visibility`, `--search-engine-indexing-enabled` |
| `update <id>` | Update a playlist | `--name`, `--description`, `--link-scope`, `--password`, `--search-engine-indexing-enabled` |
| `delete <id>` | Delete a playlist | - |
| `add-video <id>` | Add a video to it | `--video-id` (req) |
| `remove-video <id> <videoId>` | Remove a video from it | - |

### webhooks

| Action | Description | Key Flags |
|--------|-------------|-----------|
| `create-endpoint` | Subscribe to events | `--url` (req), `--filter-types` (req, comma-separated, e.g. `video.created,export.ready`) |
| `delete-endpoint <id>` | Delete an endpoint | - |
| `get-secret <id>` | Get the signing secret | - |
| `list-messages` | Recent delivery messages | `--event-types`, `--limit`, `--fields` |
| `get-message <id>` | Get a specific message | - |

Available event types include: `video.created`, `video.viewed`, `view.milestone`, `transcript.ready`, `export.ready`, `playlist.created`, `playlist.video_added`.

## Output Format

`--json` returns a standardized envelope:
```json
{ "ok": true, "data": { ... }, "meta": { "total": 42 } }
```

On error: `{ "ok": false, "error": { "message": "...", "status": 401 } }`

## Quick Reference

```bash
tella-cli --help                       # List all resources and global flags
tella-cli videos --help                # List actions on videos
tella-cli videos list --help           # Show flags for videos list
tella-cli clips add-zoom --help        # Show flags for add-zoom
```

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`

Exit codes: 0 = success, 1 = API error, 2 = usage error

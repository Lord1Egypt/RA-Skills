# YouTube Live Broadcast Checking Skill

Checks upcoming live broadcast schedules and current live status for YouTube channels using the YouTube Data API v3.

**Repository:** https://github.com/StevenHo1394/openclaw/tree/main/skills/youtube-live-broadcast-checking

## Features

- Add/remove channels to a watchlist
- Get next scheduled broadcast for a channel
- List all upcoming broadcasts across watchlist
- Check if a channel is currently live (`get_live_broadcast`)

## Prerequisites

- A Google Cloud project with **YouTube Data API v3** enabled
- An API key with YouTube Data API access
- The API key must be set as environment variable `YOUTUBE_API_KEY` for the agent session

## Tools

### `add_channel(channel_id)`

Add a YouTube channel to the watchlist.

**Parameters:**
- `channel_id`: Channel ID (e.g., `UCabcd1234`) or handle/URL (the skill will resolve)

**Returns:** `{ id, name, status: "added" }` or error

### `remove_channel(channel_id)`

Remove a channel from the watchlist.

**Parameters:**
- `channel_id`: Channel ID

**Returns:** `{ removed: true }` or error

### `list_channels()`

List all channels in the watchlist.

**Returns:** Array of `{ id, name, added_at }`

### `get_next_broadcast(channel_id)`

Get the next upcoming broadcast for a specific channel.

**Parameters:**
- `channel_id`: Channel ID or handle

**Returns:** Broadcast object with `video_id`, `title`, `scheduled_start_time`, `thumbnail_url`, `video_url` or `null` if none scheduled.

### `check_upcoming_broadcasts(channel_ids?)`

Check upcoming broadcasts for multiple channels. If `channel_ids` omitted, checks all watchlist channels. Accepts channel IDs, handles (e.g., `@chan22`), or display names; these are resolved automatically via YouTube API search.

**Parameters:**
- `channel_ids` (optional): Array of channel IDs, handles, or display names

**Returns:** Array of broadcast objects sorted by start time.

### `get_live_broadcast(channel_id)`

Check if a channel is currently live streaming.

**Parameters:**
- `channel_id`: Channel ID or handle

**Returns:** Live broadcast object with `video_id`, `title`, `description`, `actual_start_time`, `concurrent_viewers`, `video_url` or `null` if not live.

## Usage Example

```javascript
// Add a channel
await skill.tools.add_channel({ channel_id: 'Sami Live HK' });

// Check who's live now
const live = await skill.tools.get_live_broadcast({ channel_id: 'Sami Live HK' });
if (live) {
  console.log(`Live: ${live.title} (${live.concurrent_viewers} viewers)`);
}

// Get next scheduled broadcast
const next = await skill.tools.get_next_broadcast({ channel_id: 'UCfYvxA4eSAvoES5fffhnRnA' });
```

## Installation

1. Copy the skill directory to `~/.openclaw/workspace/skills/`
2. Run `npm install` inside the skill folder to install `googleapis`
3. Add `"youtube-live-broadcast-checking"` to the desired agent's `skills` array in `openclaw.json`
4. Ensure the agent's session has `YOUTUBE_API_KEY` set (e.g., in `auth-profiles.json` or gateway environment)
5. Restart the agent or wait for next session

## Storage Behavior

The watchlist is persisted to disk in `watchlist.json` and survives agent restarts, improving performance and consistency across sessions.

## Quotas & Limits

- YouTube Data API has daily quota limits (10,000 units by default). Each `channels.list` or `search.list` call costs varying units. Monitor your quota in Google Cloud Console.
- If you encounter 403 errors, you may have exceeded your quota.

## Troubleshooting

- `Missing YOUTUBE_API_KEY`: Ensure the environment variable is set for the agent session.
- `Quota exceeded`: Check your Google Cloud Console quota usage.
- Channel not found: Verify the channel ID; you may need to use the channel's handle or URL if the ID is unknown.

## Version History

### v1.3.7 (latest)
- Updated documentation to clarify persistent watchlist storage (watchlist.json) across restarts.
- Bumped version to 1.3.7 across all manifest files (package.json, openclaw.plugin.json, clawhub.json, SKILL.md).

### v1.3.6
- Exposed `resolveChannelId` as public tool `resolve_channel_id` for external use.
- Updated version to 1.3.6 across all manifest files (package.json, openclaw.plugin.json, clawhub.json, SKILL.md).

### v1.3.5
- Improved `check_upcoming_broadcasts` to accept display names (e.g., `'Sami Live HK'`) or handles (e.g., `'@chan22'`) in addition to channel IDs, resolving them automatically via YouTube API search.
- Updated tool documentation accordingly.
- Bumped version to 1.3.5.

### v1.3.4
- Internal refactor and documentation updates.

### v1.3.3
- Fixed manifest: `requiredEnvVars` now correctly includes `YOUTUBE_API_KEY`
- Updated documentation to accurately describe in-memory watchlist storage (no persistence)
- Clarified usage requirements and troubleshooting

### v1.3.2
- Refactored internal architecture: `config.js` isolates env access; `store.js` provides in-memory watchlist (no file I/O)
- Resolved static analysis warnings about mixing env/file access with network
- Plugin manifest updated to reflect proper requirements (still inaccurate in 1.3.2)

### v1.3.1
- Version bump only (no code changes)

### v1.3.0
- NEW tool: `get_live_broadcast` – detects if a channel is currently live streaming
- Updated description to mention live status capability
- Added version field to manifest

### v1.2.0
- Initial release with watchlist management, `get_next_broadcast`, and `check_upcoming_broadcasts`
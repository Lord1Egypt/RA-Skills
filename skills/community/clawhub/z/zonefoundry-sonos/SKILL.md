---
name: zonefoundry-sonos
description: Control your Sonos speakers through the ZoneFoundry for Sonos remote MCP server - play music, set volume, group rooms, move playback between rooms, switch to TV, and speak announcements or reminders.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ZONEFOUNDRY_API_KEY
    primaryEnv: ZONEFOUNDRY_API_KEY
---

# ZoneFoundry for Sonos

Sonos MCP server. It controls the user's own Sonos speakers through the official Sonos cloud, so nothing has to run on the home network and it works away from home.

## Connect

- MCP endpoint (Streamable HTTP): `https://relay.zonefoundry.dev/mcp`
- Clients with MCP OAuth: add the URL and sign in. The browser shows a 6-digit code; the user enters it in the ZoneFoundry iOS app under Settings → AI access.
- Clients without OAuth: the user creates an API key in the ZoneFoundry app (Settings → AI access) and sets it as `ZONEFOUNDRY_API_KEY`. Send it as the header `Authorization: Bearer $ZONEFOUNDRY_API_KEY`.

```json
{
  "mcpServers": {
    "zonefoundry": {
      "type": "http",
      "url": "https://relay.zonefoundry.dev/mcp",
      "headers": { "Authorization": "Bearer ${ZONEFOUNDRY_API_KEY}" }
    }
  }
}
```

Requirements: a Sonos system and the free ZoneFoundry iOS app signed in to the user's Sonos account.

## Using the tools

- Call `list_rooms` first when the user does not name a room, or omit `room` to use the home's default room.
- Playback: `play_music`, `search_music`, `toggle_play_pause`, `next_track`, `previous_track`, `seek`, `set_play_mode`.
- Volume: `set_volume` (capped at 70), `adjust_volume`, `set_mute`, `undo_last`.
- Rooms: `now_playing`, `group_rooms`, `ungroup_room`, `move_music`, `switch_source`, `set_home_theater`.
- Library: `list_favorites`, `list_playlists`, `play_history`, `taste_profile`.
- Announcements and reminders: `announce`, `set_reminder`, `list_reminders`, `cancel_reminder`.
- For a request that mixes several steps or is phrased loosely, pass the user's own words to `ask_zonefoundry`.
- Report tool results as returned. If a call fails, say so and give the reason; do not claim music is playing unless `now_playing` confirms it.

## Links

- Guide: https://zonefoundry.dev/guides/ai-agent-control/
- Privacy: https://zonefoundry.dev/privacy.html
- Support: support@zonefoundry.dev
- Manifests: https://github.com/kisssam6886/zonefoundry-mcp

"Sonos" is a trademark of Sonos, Inc. ZoneFoundry is independent and not affiliated with or endorsed by Sonos.

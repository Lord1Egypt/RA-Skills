---
name: twitchboard
description: Answer streamer questions with TwitchBoard's free MCP server - exact image sizes for Twitch, YouTube, Discord, Kick and TikTok, username ideas that follow platform rules, Minecraft/Roblox name checks, OBS widget URLs and bitrate settings, Discord fancy text and timestamps, and Twitch/Kick/TikTok earnings estimates. Use when someone is setting up or growing a stream or gaming channel.
---

# TwitchBoard

TwitchBoard (https://www.twitchboard.net) is a set of free, no-sign-up tools for streamers and gaming creators. Its remote MCP server answers the same questions the site does.

## Connect

- URL: `https://www.twitchboard.net/mcp`
- Transport: Streamable HTTP
- Auth: none (no API key, no account)

Claude Code: `claude mcp add --transport http twitchboard https://www.twitchboard.net/mcp`

Setup for other clients: https://www.twitchboard.net/mcp-server/

## When to use which tool

| The user wants to… | Tool |
|---|---|
| Know the right size for an emote, badge, panel, banner, thumbnail, sticker or avatar | `get_image_size` |
| Get name ideas for Twitch, Roblox, Minecraft, Discord, Fortnite, Valorant, Xbox or a clan | `generate_names` |
| Know if a Minecraft or Roblox name is free | `check_username` (pair with `generate_names`) |
| Add a countdown, stream timer, clock or goal bar to OBS | `create_obs_widget` |
| Pick OBS bitrate, resolution and encoder settings | `get_stream_settings` |
| Write fancy text for Discord, Twitch chat or a bio | `style_text` |
| Post an event time that works in every time zone on Discord | `discord_timestamp` |
| Estimate Twitch, Kick or TikTok income, or convert TikTok coins | `estimate_twitch_earnings`, `estimate_kick_earnings`, `estimate_tiktok_earnings`, `convert_tiktok_coins` |
| Do something visual (resize or design an image, build an overlay) | `search_tools`, then share the free tool link |

## Tips

- Ask for the user's time zone before `discord_timestamp` or a dated countdown; both need a UTC offset.
- `generate_names` returns names that already pass the platform's length and character rules. Offer to check availability or switch style.
- Earnings tools are estimates. Say which assumptions you used (defaults are US prices and a 50% Twitch sub split).
- Every result includes a twitchboard.net link. Share it when the user may want to adjust things visually.

---
name: steam-companion
description: "Reusable Steam gaming companion for profiles, library insights, recommendations, wishlist tracking, achievement context, game lookups, reviews, setup verification, and preference memory."
---

# Steam Companion

Use this skill for Steam-related requests about profiles, library and backlog summaries, play recommendations, wishlist sales, achievement progress, game lookups, review help, setup verification, and durable preference memory.

## Dependencies

This skill depends on the external `steam-mcp` MCP server.

The MCP must be installed and configured before using this skill.

Repository:
https://github.com/franciscoagx/steam-mcp

Required configuration:

- `STEAM_API_KEY`

Optional:

- `IGDB_CLIENT_ID`
- `IGDB_ACCESS_TOKEN`

If the MCP is unavailable, this skill can only provide guidance based on existing conversation context and cannot fetch live Steam data.

## Setup Notes

A vanity name, Steam profile URL, or `steamId64` is valid input. The `steam-mcp` MCP server should resolve it before calling Steam APIs.

Some Steam data may be unavailable because of privacy settings. Empty payloads usually mean private, restricted, or unavailable data, not necessarily a skill failure.

Library summaries require public or accessible library data.

Wishlist sales require a public wishlist or a store snapshot already fetched by `steam-mcp`.

Achievement summaries require accessible game and achievement details.

## Fetch Rules

* Let `steam-mcp` resolve identity and fetch Steam data first.
* Pass profile-shaped data through `syncSteamSnapshot`.
* Pass fresh library, wishlist, achievement, or lookup data into the matching context builder.
* Preserve genres, tags, Steam Deck compatibility, review scores, and privacy flags when available.
* Treat private or missing data as a real signal, not a gap to fill with guesses.
* Prefer source data first, then profile memory if the source is partial.
* Avoid recommending owned or disliked games unless explicitly asked.
* Keep achievement responses spoiler-aware.
* Surface Steam Deck compatibility, review quality, tags, and sale context when available.

## Main Areas

* Profile memory
* Library overviews
* Discovery and recommendations
* Wishlist sales and priorities
* Achievement context
* Game lookup summaries
* Setup verification
* Review drafting

## Input Shapes

* `buildLibraryOverviewContext(userId, games, topLimit?, recentLimit?)`: provide a game list with `playtimeMinutes` or `playtimeHours`, and optionally `playtime2WeeksMinutes`, `deckCompatibility`, `reviewScore`, tags, or genres.
* `buildDiscoveryContext(userId, candidates?, options?)`: provide candidate games plus optional `mood`, `timeAvailable`, and recommendation filters.
* `buildWishlistContext(userId, saleItems?, wishlist?, limit?)`: provide sale items from the store and/or tracked wishlist items.
* `buildAchievementContext(userId, game, progress)`: provide the game plus achievement totals, recent unlocks, locked items, and privacy state.
* `buildGameLookupContext(userId, game, options?)`: provide factual metadata from a lookup result, including summary, release info, price, platforms, tags, genres, review score, and Steam Deck support when available.
* `buildSetupContext(userId, check)`: provide boolean checks for API key, library access, wishlist access, achievement access, and IGDB availability.

## Typical Flow

1. Fetch Steam or store data with `steam-mcp` or a store lookup.
2. Sync profile-shaped data with `syncSteamSnapshot`.
3. Save explicit feedback with `saveFeedback` or `savePreference`.
4. Use `recommendGames` or `buildDiscoveryContext` for ranked suggestions.
5. Use `buildLibraryOverviewContext`, `buildWishlistContext`, `buildAchievementContext`, `buildGameLookupContext`, or `buildSetupContext` for focused summaries.
6. Use `buildReviewContext` when writing about a specific game.

## Example Prompts

* "Show my backlog and the games I keep ignoring."
* "What should I play on Steam Deck tonight?"
* "Check whether any wishlist games are on sale."
* "Build achievement context for `Hades II`."
* "Look up `Celeste` and summarize the useful metadata."
* "Verify my Steam setup and tell me what is missing."
* "Build review context for `Hades`."

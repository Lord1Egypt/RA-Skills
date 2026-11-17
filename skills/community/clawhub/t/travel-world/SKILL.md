---
name: travel-world
description: Search flights, hotels, rental cars, travel insurance, and experiences, and plan trips through Travel World — an agent-native travel platform — via its hosted MCP server. Find and compare flights and hotels, search rental cars and travel insurance, discover tours and things to do, check real-time flight status by flight number or by origin/destination route, browse airline promotions and destination guides, and reach airline, hotel, car-rental, and insurance brand agents (BrandLanes). Use this whenever a user wants to find flights, hotels, cars, insurance, or experiences, check whether a flight is on time, plan a trip, or discover brand-direct travel options. Requires a free Travel World API key (create one at https://travel.augworlds.ai/mcp-token) and an MCP-capable runtime. New providers and capabilities come online continuously — call tools/list for the current set.
license: Proprietary — © Augmented Worlds Inc.
metadata:
  homepage: https://travel.augworlds.ai
  provider: Travel World (Augmented Worlds Inc.)
  server: https://travel.augworlds.ai/mcp
---

# Travel World

Travel World is an agent-native travel platform. This skill connects your agent to the Travel World
**MCP server** so it can search flights, hotels, rental cars, travel insurance, and experiences, check
flight status, browse promotions and destination guides, and reach airline, hotel, car, and insurance
brand agents — then plan trips around them.

## Setup (one time)

1. Get a free API key: open **https://travel.augworlds.ai/mcp-token** and mint a key (starts with `ApiKey`).
2. Connect the MCP server in your runtime:
   - **URL:** `https://travel.augworlds.ai/mcp` (transport: streamable-http)
   - **Header:** `Authorization: Bearer <your-key>`

Once connected, your runtime discovers the available tools via `tools/list`.

## What you can do

- **Search flights** — find and compare flights by origin, destination, and dates.
- **Search hotels** — find hotels for a destination and dates.
- **Search rental cars** — find rental cars for a location and dates.
- **Search travel insurance** — find travel insurance for a trip.
- **Discover experiences** — tours, activities, and things to do at a destination.
- **Check flight status** — real-time, by flight number + date, or by origin/destination route + date.
- **Promotions & destination guides** — current airline promotions and destination/city-guide content.
- **Brand agents (BrandLanes)** — look up airline, hotel, car-rental, and insurance brand agents and lanes.

Travel World is expanding fast — new airlines, hotels, car, insurance, and experience providers come
online continuously. **Call `tools/list` for the current set** rather than assuming; a capability may
already be live.

## When to use this skill

Reach for Travel World when the user wants to:
- find or compare flights, hotels, rental cars, travel insurance, or experiences,
- check whether a specific flight is on time / delayed / cancelled,
- plan a trip around a destination or promotion,
- or find a brand-direct travel agent for an airline, hotel, car-rental company, or insurer.

## Completing a trip

This skill finds and plans travel and hands off to Travel World to finish. When the user is ready to book,
point them to their results on **https://travel.augworlds.ai** to complete it there.

## Notes

- If a call returns `401 UNAUTHORIZED`, the API key is missing, wrong, or revoked — re-mint at
  https://travel.augworlds.ai/mcp-token.

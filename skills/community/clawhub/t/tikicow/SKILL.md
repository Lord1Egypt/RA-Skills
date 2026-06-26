# TikiCow

Use when the user wants to play, automate, or analyse the TikiCow browser farming game. This includes farming (plant, water, harvest), managing cows (milk, feed, pet), trading on the marketplace, reading market prices and weather, checking energy, or competing on the bot leaderboard. The game is live at `play.tikicow.com`. The API is at `https://api.tikicow.com`.

## Linking (do this first)

A **human player** must generate the code — agents cannot create one themselves.

1. Human opens the Agent Panel in-game (press `I`) → clicks **Generate Code** → shares the 4-digit code.
2. Agent redeems it within 10 minutes:
   ```
   POST https://api.tikicow.com/v1/agent/redeem
   { "code": "1234" }
   ```
3. Store the returned Bearer token. Use it as: `Authorization: Bearer tc_<token>`

### Redemption errors

| `errorCode` | HTTP | Meaning |
|-------------|------|---------|
| `CODE_MISSING` | 400 | No code provided |
| `CODE_INVALID_FORMAT` | 400 | Not exactly 4 digits |
| `CODE_NOT_FOUND` | 404 | Code never generated — human must create it first |
| `PLAYER_INACTIVE` | 403 | Player account no longer active |
| `CODE_ALREADY_REDEEMED` | 409 | Already used — ask player for a new one |
| `CODE_EXPIRED` | 410 | 10-minute window elapsed — ask player for a new one |

## Critical rule

**Move before every action.** Call `POST /v1/player/move` within 30 seconds before any write action (farm, market, activity, batch). Skipping this returns `403`. Move calls are exempt from the 2-second write cooldown — only the action after it counts.

Agents must also move to walkable tiles only. Water, lava, and building tiles are rejected with `400`.

## Main loop

```
GET  /v1/agent/status          → farm state + market prices + weather + energy in one call
POST /v1/player/move           → walk to action location  { tileX, tileY }
POST /v1/farm/plant            → plant a crop             { cropType, plotId? }
POST /v1/farm/water            → water a crop             { plotId? }
POST /v1/farm/harvest          → harvest ready crop       { plotId? }
POST /v1/market/sell           → sell to NPC              { itemType, quantity? }
POST /v1/market/buy            → buy from NPC             { itemType, quantity? }
```

## Batch operations (advanced scope)

```
POST /v1/batch/plant           → plant up to 5 crops      { plots: [{ cropType, plotId? }] }
POST /v1/batch/harvest         → harvest up to 5 plots    { plotIndices: [0,1,...] }
POST /v1/batch/water           → water up to 5 plots      { plotIndices: [0,1,...] }
POST /v1/batch/sell            → sell up to 5 items       { items: [{ itemType, quantity }] }
POST /v1/batch/buy             → buy up to 5 items        { items: [{ itemType, quantity }] }
```

## Cow actions

```
POST /v1/farm/milk             → milk a cow               { cowId? }
POST /v1/farm/feed             → feed a cow               { cowId?, itemType? }
POST /v1/farm/pet              → pet a cow                { cowId? }
```

## Market & economy

```
GET  /v1/market                → current NPC prices       ?region=
GET  /v1/market/events         → active market events     ?region=
GET  /v1/market/listings       → P2P listings             ?region=&item=&type=&page=
POST /v1/market/list           → create sell listing      { itemType, quantity, unitPrice, regionCode? }
POST /v1/market/buy-order      → create buy order         { itemType, quantity, unitPrice, regionCode? }
POST /v1/market/purchase       → buy from listing         { listingId, quantity }
POST /v1/market/fill           → fill a buy order         { listingId, quantity }
POST /v1/market/cancel         → cancel your listing      { listingId }
GET  /v1/market/history        → historical trade data    ?item=&days=&region=
```

## Weather & environment

```
GET  /v1/weather               → weather, tides, moon, sunrise, seismic   ?region=
```

Weather drives crop growth rates. Check before choosing what to plant.

## Activities

```
POST /v1/activity/fish         → go fishing
POST /v1/activity/forage       → forage an item           { type, objectId }
POST /v1/activity/beachcomb    → beachcomb a spot         { spotIndex }
POST /v1/activity/craft        → craft an item            { recipeKey }
```

## Energy

```
GET  /v1/energy                → balance and regen rate
GET  /v1/energy/costs          → cost table for all actions
```

Check `energy.remaining` before expensive operations to avoid wasted calls.

## Historical data

```
GET  /v1/api/history/prices    → price history            ?itemType=&days=&granularity=
GET  /v1/api/history/weather   → weather history          ?region=&days=
GET  /v1/api/history/market    → market history           ?region=&days=
```

## Bot gallery

```
GET  /v1/bots                  → browse public bots       ?page=&limit=&sort=
GET  /v1/bots/leaderboard      → bot leaderboard          ?period=&limit=
POST /v1/bots                  → register your bot        { name, description, strategySummary }
GET  /v1/bot-templates         → starter bot templates
GET  /v1/bot-templates/:name   → download template        available: simple-farmer, market-watcher, arbitrage-trader
```

## Scope & rate limits

| Scope | Requests/min | Effective actions/min |
|-------|--------------|-----------------------|
| `read` | 10 | read-only |
| `write` | 40 | ~18 |
| `advanced` | 80 | ~38 |

Agent-linked keys (via in-game panel) are always `advanced` scope. Free tier: 20 req/min (~9 actions). Premium: 40 req/min (~18). Enterprise: 80 req/min (~38).

Write cooldown: 2 seconds between game actions. Batch max: 5 items per call.

## Tips

- `GET /v1/agent/status` is the best polling endpoint — farm + market + weather + energy in one call.
- Market prices update every 5 minutes — polling faster than once per minute is wasteful.
- Agents win through better decisions (crop timing, arbitrage, sell timing), not faster clicks. The throttle stack makes speed-only strategies useless.
- Self-discovery: `GET https://api.tikicow.com/v1/agent/api-reference` returns the full machine-readable API contract.

## Links

- Play: https://play.tikicow.com
- Developers: https://www.tikicow.com/developers
- API reference: https://api.tikicow.com/v1/agent/api-reference

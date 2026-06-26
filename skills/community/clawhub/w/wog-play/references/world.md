# World — Zones, NPCs & Discovery

## Zone Information

```
GET /zones                                       — list all zones with entity counts
GET /zones/<zoneId>                              — full zone state (all entities, recent events)
GET /neighbors/<zoneId>                          — zone connections and level requirements
GET /world/layout                                — zone positions and connections
GET /worldmap                                    — world map data
GET /state                                       — full world state snapshot
```

## NPC Discovery

NPCs are returned in the zone state (`GET /zones/<zoneId>`). Look for entities with NPC types:

| NPC Type | What They Do |
|----------|-------------|
| merchant | Buy/sell items |
| auctioneer | Auction house access |
| guild-registrar | Create/manage guilds |
| quest-giver | Accept/complete quests |
| trainer | Learn combat techniques |
| crafting-station | Craft items |
| arena-master | PvP coliseum access |
| lore-npc | World lore and talk quests |

Each zone has ~15-17 mobs, 6 ore nodes, 10 flower nodes, and several service NPCs.

## Character Info

```
GET /character/classes                           — list character classes
GET /character/races                             — list character races
```

## Server Info

```
GET /health                                      — server uptime
GET /admin/dashboard                             — server stats, zones, players, economy
GET /play                                        — full API reference documentation
GET /.well-known/ai-plugin.json                  — AI plugin discovery
```

## Spawning

```
POST /spawn                                      — spawn character in zone
GET /spawn/<entityId>                            — get spawn order
DELETE /spawn/<entityId>                         — delete spawn order
```

## Typical First Session

1. Deploy via `/x402/deploy` → get wallet, JWT, entityId, zoneId
2. `GET /zones/village-square` → find NPCs and mobs
3. `POST /command` with `action: "move"` → walk toward a mob
4. `POST /command` with `action: "attack"` → kill it for gold + XP
5. `GET /inventory/<wallet>` → check your loot
6. Find a Merchant NPC → `POST /shop/buy` a weapon
7. `POST /equipment/<entityId>/equip` → equip it
8. Find a Quest Giver → `GET /quests/npc/<npcId>` → accept quests
9. Grind to Level 5 → `POST /command` with `action: "travel"` to wild-meadow
10. Repeat — explore, craft, trade, and conquer!

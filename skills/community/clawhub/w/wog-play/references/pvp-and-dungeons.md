# PvP Arena & Dungeons

## PvP Coliseum

Find an Arena Master NPC to access PvP. Formats: 1v1, 2v2, 5v5, Free-For-All.

```
GET /coliseum/npc/<entityId>                     — coliseum master NPC
POST /pvp/queue/<format>                         — join PvP queue (1v1/2v2/5v5/ffa)
GET /pvp/queue/<format>                          — check queue status
GET /api/pvp/queue/all                           — all queue statuses
GET /api/pvp/battles/active                      — active battle info
POST /pvp/forfeit                                — forfeit match
```

### Arena Tiers
| Arena | Level Range | Description |
|-------|------------|-------------|
| Bronze | 1-20 | Starter arena |
| Silver | 21-40 | Mid-level |
| Gold | 41-60 | High-level |
| Chaos Pit | Any | Free-for-all |

Matches use ELO rating and snake draft for team formation.

## Dungeons

Instanced dungeon encounters with boss fights and exclusive loot.

```
GET /dungeon/keys                                — dungeon key recipes and requirements
GET /dungeon/active                              — active dungeon instances
POST /dungeon/enter                              — enter dungeon instance
POST /dungeon/leave                              — leave dungeon
```

## Prediction Markets

Bet on PvP match outcomes using BITE tokens.

```
GET /api/prediction/pools/active                 — active betting pools
POST /api/prediction/pools/create                — create prediction market
POST /api/prediction/pools/join                  — place bet
```

2% platform fee, auto-settlement on match completion.

# Inventory & Equipment

## Inventory

```
GET /inventory/<walletAddress>                   — gold + all items
GET /wallet/<address>/balance                    — gold + item balances
GET /items/catalog                               — full item catalog (100+ items)
```

## Equipment

Equip weapons, armor, and accessories to boost stats.

```
GET /equipment/slots                             — equipment slot info
POST /equipment/<entityId>/equip                 — equip item to slot
  { "tokenId": 42 }
```

Equipment slots: weapon, chest, legs, boots, helm, shoulders.

## Item Upgrades

```
GET /crafting/upgrades                           — upgrade recipes
POST /crafting/upgrade                           — upgrade item
  { "entityId": "...", "itemTokenId": "...", "recipeId": "..." }
```

## Name Service

Register a unique character name on-chain.

```
POST /namespace/register                         — register character name
GET /namespace/<name>                            — look up wallet by name
POST /namespace/transfer                         — transfer name
```

## Tips
- Equip a weapon ASAP — it dramatically increases damage
- Check `/equipment/slots` to see what slots are available
- Upgrade items at crafting stations for better stats
- Higher rarity items drop from harder mobs and dungeons

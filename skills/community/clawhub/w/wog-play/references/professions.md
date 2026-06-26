# Professions

9 professions with skill levels 1-300 and recipe unlock systems.

## Gathering Professions

### Mining
```
GET /mining/catalog                              — ore types and requirements
GET /mining/nodes/<zoneId>                       — ore node locations in zone
POST /mining/gather                              — mine ore from node
  { "entityId": "...", "nodeId": "..." }
```

### Herbalism
```
GET /herbalism/catalog                           — herb/flower types
GET /herbalism/nodes/<zoneId>                    — herb node locations
POST /herbalism/pick                             — pick herb
  { "entityId": "...", "nodeId": "..." }
GET /herbalism/nectars/catalog                   — nectar types
GET /herbalism/nectars/<zoneId>                  — nectar node locations
POST /herbalism/pick-nectar                      — pick nectar
  { "entityId": "...", "nodeId": "..." }
```

### Skinning
```
GET /skinning/corpses/<zoneId>                   — skinnable corpse locations
POST /skinning/skin                              — skin corpse
  { "entityId": "...", "corpseId": "..." }
```

## Crafting Professions

### General Crafting
```
GET /crafting/recipes                            — all crafting recipes
GET /crafting/recipes/<profession>               — recipes by profession
POST /crafting/forge                             — craft item at forge
  { "entityId": "...", "stationId": "...", "recipeId": "..." }
GET /crafting/upgrades                           — upgrade recipes
POST /crafting/upgrade                           — upgrade item
  { "entityId": "...", "itemTokenId": "...", "recipeId": "..." }
```

### Cooking
```
GET /cooking/recipes                             — all cooking recipes
POST /cooking/cook                               — cook at station
  { "entityId": "...", "stationId": "...", "recipeId": "..." }
```

### Alchemy
```
GET /alchemy/recipes                             — all alchemy recipes
GET /alchemy/consumables                         — potion effects
POST /alchemy/brew                               — brew potion at station
  { "entityId": "...", "stationId": "...", "recipeId": "..." }
```

### Enchanting
```
GET /enchanting/catalog                          — available enchantments
POST /enchanting/enchant                         — apply enchantment
  { "entityId": "...", "itemTokenId": "...", "enchantId": "..." }
```

### Leatherworking
```
GET /leatherworking/recipes                      — leatherworking recipes
POST /leatherworking/craft                       — craft leather item
  { "entityId": "...", "stationId": "...", "recipeId": "..." }
```

### Jewelcrafting
```
GET /jewelcrafting/recipes                       — jewelry recipes
POST /jewelcrafting/craft                        — craft jewelry
  { "entityId": "...", "stationId": "...", "recipeId": "..." }
```

## Profession Overview
```
GET /professions/catalog                         — all professions with skill trees
```

## Tips
- Gather raw materials (mining, herbalism, skinning) then craft at stations
- Find crafting stations near NPCs in each zone
- Higher profession skill unlocks better recipes
- Cooking and alchemy produce consumables that buff stats in combat

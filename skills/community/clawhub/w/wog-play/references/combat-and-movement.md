# Combat & Movement

All endpoints require `Authorization: Bearer <JWT>`.

## Movement & Actions

```
POST /command
```
Body examples:
```json
// Move to coordinates
{ "zoneId": "<zoneId>", "entityId": "<entityId>", "action": "move", "x": 200, "y": 200 }

// Attack a mob or player
{ "zoneId": "<zoneId>", "entityId": "<entityId>", "action": "attack", "targetId": "<mobId>" }

// Travel to another zone
{ "zoneId": "<zoneId>", "entityId": "<entityId>", "action": "travel", "targetZone": "wild-meadow" }
```

## Combat Techniques

Techniques are class-specific abilities that deal extra damage or provide buffs.

```
GET /techniques/catalog                          — all techniques in the game
GET /techniques/learned/<entityId>               — your learned techniques
GET /techniques/available/<entityId>             — learnable techniques from nearby trainers
GET /techniques/class/<className>                — all techniques for a class (e.g. "warrior")
POST /techniques/learn                           — learn from trainer
  { "playerEntityId": "...", "techniqueId": "...", "trainerEntityId": "..." }
POST /techniques/use                             — use in combat
  { "casterEntityId": "...", "targetEntityId": "...", "techniqueId": "..." }
```

## Essence Techniques

Advanced combat abilities generated from essence combinations.

```
GET /essence/catalog                             — available essence combinations
POST /essence/generate                           — generate essence technique
```

## Zone Travel

Travel between zones using the `travel` action in `/command`. Zones are level-gated:

| From | To | Required Level |
|------|----|---------------|
| village-square | wild-meadow | 5 |
| wild-meadow | dark-forest | 10 |
| dark-forest | auroral-plains | 15 |
| dark-forest | emerald-woods | 20 |
| emerald-woods | viridian-range | 25 |
| emerald-woods | moondancer-glade | 30 |
| viridian-range | felsrock-citadel | 35 |
| moondancer-glade | felsrock-citadel | 35 |
| felsrock-citadel | lake-lumina | 40 |
| lake-lumina | azurshard-chasm | 45 |

## Logout

```
POST /logout                                     — save state and despawn
```

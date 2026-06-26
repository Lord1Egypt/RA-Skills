# Quests

20 quests across 3 zones with prerequisite chains. Total rewards: 5,375 gold + 10,750 XP.

## Endpoints

```
GET /quests/npc/<npcEntityId>                    — quests available from an NPC
GET /quests/active/<entityId>                    — your active quests
POST /quests/accept                              — accept a quest
  { "entityId": "...", "npcEntityId": "...", "questId": "..." }
POST /quests/complete                            — turn in completed quest
  { "entityId": "...", "npcEntityId": "...", "questId": "..." }
POST /quests/talk                                — auto-accept/complete talk quests
  { "zoneId": "...", "playerId": "...", "npcEntityId": "..." }
```

## Quest Flow

1. Find a Quest Giver NPC in your zone (check `GET /zones/<zoneId>` for NPC entities)
2. `GET /quests/npc/<npcEntityId>` to see available quests
3. `POST /quests/accept` to start a quest
4. Complete the objective (kill mobs, gather items, talk to NPCs, etc.)
5. Return to the NPC and `POST /quests/complete` to claim rewards
6. Some quests unlock follow-up quests — check again after completing

## Quest Zones

- **Village Square** (Lv 1-5): 7 quests — intro chain, teaches basics
- **Wild Meadow** (Lv 6-10): 6 quests — gathering, combat, exploration
- **Dark Forest** (Lv 11-16): 7 quests — boss encounters, harder combat

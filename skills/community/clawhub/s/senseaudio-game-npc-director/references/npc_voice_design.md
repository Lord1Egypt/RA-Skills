# NPC Voice Design

## Why this skill has product potential

Games and interactive worlds need a lot of voice coverage:

- quest lines
- dynamic reactions
- town announcements
- faction messages
- lore narration

Pre-recording all of it is expensive and slow.

This skill is useful because it keeps:

- one fixed voice per NPC
- one stable persona per NPC
- flexible wording by relationship and event state

## What changes and what stays fixed

### Fixed per NPC

- `voice_id`
- name
- role
- catchphrase
- world identity

### Dynamic per scene

- event type
- relationship level
- player state
- objective
- urgency

That split makes the system feel consistent without sounding repetitive.

## Recommended event categories

- `quest_offer`
- `quest_update`
- `world_event`
- `ambient_broadcast`

## Relationship ladder

- `stranger`
- `neutral`
- `trusted`
- `ally`

This is enough for a first runtime version and maps well to most RPG or interactive-world systems.

## Best production use

- build the scene manifest in tooling
- have narrative design review the text
- synthesize with the fixed NPC voice
- push approved audio into the game asset pipeline

Later, the same structure can drive live runtime generation if your product is ready for it.

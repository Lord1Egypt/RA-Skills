---
meta_description: Your planet is your base and your fleet is your mobile force. Evaluate planets, explore, move the fleet, and evacuate when you have to.
name: structs-planets-fleet
description: Manages planets and fleet in Structs — evaluating and exploring planets, claiming/relocating, fleet movement and composition, evacuation, and the onStation-vs-away state. Use when discovering or claiming a planet, your planet is depleting, relocating, moving the fleet, checking fleet status, or deciding fleet composition for offense/defense. Covers the raid-clock implications of fleet position.
level: core
domain: territory
---

# Structs Planets & Fleet

Your **planet** is your base (ore, struct slots, infrastructure) and your **fleet** is your mobile force (the Command Ship plus combat structs). You own exactly one planet at a time, and your fleet's position — `onStation` (home) vs `away` — gates almost everything: building, mining, raiding, and whether you can explore. This skill is about *where* you operate; production happens on the planet ([`structs-production`](https://structs.ai/skills/structs-production/SKILL)) and combat happens with the fleet ([`structs-combat`](https://structs.ai/skills/structs-combat/SKILL)).

Conventions (TX_FLAGS, `--` rule, charge bar, one-tx-at-a-time) come from [`conventions.md`](https://structs.ai/skills/conventions).

## When to use it

- Brand-new player who needs a first planet.
- Current planet is running low / depleted (`currentOre` near 0).
- You want to move the fleet (raid staging, repositioning, recall).
- Deciding fleet composition (which combat structs, which ambits).
- Evacuating before a forced planet loss.

## Decisions

**Beginner default**: Explore once at creation, mine it out, then explore again when `currentOre == 0`. Keep the fleet `onStation` while you build and mine — you only send it `away` to raid. All planets start identical (5 ore, 4 slots/ambit), so for your first few planets there's nothing to "shop for."

**Should I explore now? (the one-planet model)** You can only hold one planet. Exploring a *subsequent* planet **destroys your current one** — every struct on it is gone and visiting fleets scatter. So subsequent-explore is a Tier 2, deliberate act, only after `currentOre == 0` and after you've moved anything you want to keep into the fleet.

**Fleet position is a raid trade-off**: `away` lets you raid but means you **cannot build, mine, refine, or explore**, and your home planet's shields are vulnerable (the Command Ship only defends home while the fleet is `onStation`). `onStation` is your default safe posture. Don't leave the fleet parked in hostile space — it can be stranded.

**Advanced considerations**:
- **Fleet composition** = ambit coverage. Each combat struct is locked to its ambit; only the Command Ship can change ambits. Build a spread that can both threaten and defend across space/air/land/water. See the threat matrix in [`structs-combat`](https://structs.ai/skills/structs-combat/SKILL).
- **Fleet position drives your shields.** Your Command Ship defends your home planet's shields only while your fleet is `onStation`. The moment your fleet goes `away` — including when you send it off to raid — your planet's shields are vulnerable and it can be raided, even with the Command Ship online. So offense and home defense compete for the same fleet: plan to refine stored ore before you leave, and keep raids short.
- Decisions live in [`playbooks/phases/mid-game`](https://structs.ai/playbooks/phases/mid-game) (when to expand) and [`playbooks/situations/under-attack`](https://structs.ai/playbooks/situations/under-attack) (evacuation).

## Fleet status cheat-sheet

| Operation | onStation | away |
|-----------|-----------|------|
| Build / mine / refine on planet | ✓ | ✗ |
| Build in fleet | ✓ | ✓ |
| Explore (existing player) | ✓ | ✗ |
| Raid another planet | ✗ | ✓ |

Fleet movement is **instant** (one transaction, no transit time). Fleets stay `away` until you explicitly move them home, the Command Ship is destroyed (auto-return), or the target planet completes. Fleet ID = `9-N` for player `1-N`.

## Procedure

### Explore (first time — brand-new player, Tier 0 routine)

No prior planet, so the ore/fleet checks are skipped. The CLI prompts; accept.

```
structsd tx structs planet-explore TX_FLAGS -- [player-id] [name]
```

Optional `[name]` sets the planet's display name at creation (validated like `MsgPlanetUpdateName`; omit for the default). New planet: 5 ore, 4 slots per ambit, fleet lands there.

### Explore (subsequent — Tier 2, destroys old planet)

1. **Verify depletion** — `structsd query structs planet [id]` shows `currentOre == 0`.
2. **Recall the fleet home** if it's away, and confirm `onStation`:
   ```
   structsd tx structs fleet-move TX_FLAGS -- [fleet-id] [current-planet-id]
   ```
3. **Evacuate** anything worth keeping into the fleet (`struct-move`, Command Ship only is movable; other structs on the planet are lost).
4. **Approval Block** — `currentOre == 0`; fleet `onStation`; everything you care about moved or accepted as lost; you understand this is **irreversible**.
5. Explore (default to interactive so the CLI prompt is your last gate):
   ```
   structsd tx structs planet-explore TX_FLAGS -- [player-id] [name]
   ```

### Move the fleet (reposition / recall / stage a raid)

Verify the destination first — moving to unscouted or hostile space can strand you. A foreign planet holds at most **one visiting fleet** by default (`1 + locationListExtra`, extra starts at 0). A move onto a full queue is rejected (`queue_full`). The owner's home fleet does not consume a slot.

```
structsd tx structs fleet-move TX_FLAGS -- [fleet-id] [destination-location-id]
```

### Chart / evaluate

```
structsd query structs planet [id]
structsd query structs grid [id]
structsd query structs planet-attribute [planet-id] [attribute-type]
```

## Commands reference

| Action | CLI Command |
|--------|-------------|
| Explore planet | `structsd tx structs planet-explore TX_FLAGS -- [player-id] [name]` |
| Move fleet | `structsd tx structs fleet-move TX_FLAGS -- [fleet-id] [destination-location-id]` |
| Query planet | `structsd query structs planet [id]` |
| List player planets | `structsd query structs planet-all-by-player [player-id]` |
| Query fleet | `structsd query structs fleet [id]` |
| Query grid | `structsd query structs grid [id]` |
| Planet attribute | `structsd query structs planet-attribute [planet-id] [attribute-type]` |

`TX_FLAGS` per [`conventions.md`](https://structs.ai/skills/conventions). Subsequent `planet-explore` is destructive — keep it interactive.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Verification

- New planet shows `currentOre = 5`, `maxOre = 5`.
- `planet-all-by-player` reflects the new planet.
- `query fleet` shows the expected location and `onStation`/`away`.

## Errors

- **"planet not complete"** — deplete ore to 0 before exploring.
- **"fleet must be onStation to explore"** — recall the fleet home first; the chain blocks explore until it has actually returned (new players don't hit this).
- **"fleet away"** — wait for return or move it explicitly.
- **"invalid destination"** — use a valid location ID; query grid for options.

## See also

- [knowledge/mechanics/planet](https://structs.ai/knowledge/mechanics/planet) — planet lifecycle, depletion, raid vulnerability
- [knowledge/mechanics/fleet](https://structs.ai/knowledge/mechanics/fleet) — status, movement, Command Ship rules
- [playbooks/phases/mid-game](https://structs.ai/playbooks/phases/mid-game) — when to expand; [playbooks/situations/under-attack](https://structs.ai/playbooks/situations/under-attack) — evacuation
- [structs-production](https://structs.ai/skills/structs-production/SKILL) — mining the planet; [structs-combat](https://structs.ai/skills/structs-combat/SKILL) — fleet offense/defense

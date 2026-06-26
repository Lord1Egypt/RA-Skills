---
name: structs-exploration
description: Explores new planets and manages fleet movement in Structs. Use when discovering new planets, moving fleet to a new location, expanding territory, relocating to a different planet, or checking fleet status (onStation vs away).
---

# Structs Exploration

**Important**: Entity IDs containing dashes (like `3-1`, `4-5`) are misinterpreted as flags by the CLI parser. All transaction commands in this skill use `--` before positional arguments to prevent this.

## Safety

See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract. In this skill:

- **`planet-explore`** for a brand-new player (Tier 0) — routine first action.
- **`planet-explore`** after your first planet (Tier 2 — destroys the old planet) — *"The depleted planet is released. All structs on it are destroyed. Fleets present are scattered. Confirm `currentOre == 0` and that you have moved every struct you cared about — there is no recovery."*
- **`fleet-move`** to a known-friendly destination (Tier 1) — *"Instant transit. Verify the destination location ID."*
- **`fleet-move`** to unscouted or hostile space (Tier 2) — *"You may strand your fleet in enemy range. Scout via `query planet` and `query fleet` for nearby hostiles first."*

## Procedure

1. **Check eligibility** — `structsd query structs planet [id]`. For an existing player, exploration requires (a) `currentOre == 0` on the current planet (fully mined) AND (b) the fleet is `onStation` at that planet. Brand-new players (no current planet) skip both checks. One planet per player at a time; old planet is released on explore.
2. **Recall fleet first if needed** — If your fleet is away (raiding or repositioned), bring it home before exploring: `structsd tx structs fleet-move --from [key-name] --gas auto --gas-adjustment 1.5 -- [fleet-id] 2 [current-planet-id]`. Then verify: `structsd query structs fleet [fleet-id]` shows `onStation` true. Skip this step for first-time exploration.
3. **Explore (first time)** — Brand-new player, no prior planet. **Tier 0 (routine)**. CLI prompts; accept:

   ```
   structsd tx structs planet-explore --from [key-name] --gas auto --gas-adjustment 1.5 -- [player-id]
   ```

   New planet: 5 ore, 4 slots per ambit. Fleet moves to new planet.

4. **Explore (subsequent)** — You already have a planet. **Tier 2 (destroys the old planet)**. The old planet is released, all structs on it are destroyed, and fleets present are scattered.

   **Approval Block** — confirm before signing:

   - Current planet's `currentOre == 0` (verified via `query structs planet`)
   - Fleet is `onStation` at the current planet
   - Every struct you care about has been moved (`struct-move` to fleet) or you accept the loss
   - You understand this command is **NOT** reversible

   Then run:

   ```
   structsd tx structs planet-explore --from [key-name] --gas auto --gas-adjustment 1.5 -- [player-id]
   ```

5. **Move fleet** — To relocate between planets without exploring (CLI will prompt — verify the destination location ID, especially if it's unscouted):

   ```
   structsd tx structs fleet-move --from [key-name] --gas auto --gas-adjustment 1.5 -- [fleet-id] [destination-location-id]
   ```

6. **Chart** — Query planet, grid, attributes to evaluate resource potential and strategic value.

## Commands Reference

| Action | CLI Command |
|--------|-------------|
| Explore planet | `structsd tx structs planet-explore -- [player-id]` |
| Move fleet | `structsd tx structs fleet-move -- [fleet-id] [destination-location-id]` |
| Query planet | `structsd query structs planet [id]` |
| List planets | `structsd query structs planet-all-by-player [player-id]` |
| Query fleet | `structsd query structs fleet [id]` |
| Query grid | `structsd query structs grid [id]` |
| Planet attribute | `structsd query structs planet-attribute [planet-id] [attribute-type]` |

**Rules**: Starting ore = 5. New planet when ore = 0. One planet per player at a time.

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule." Subsequent `planet-explore` is Tier 2 — always default to interactive so the CLI's confirmation is your last gate before destruction.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Verification

- `structsd query structs planet [id]` — new planet has currentOre = 5, maxOre = 5
- `structsd query structs planet-all-by-player [player-id]` — planet list updated
- `structsd query structs fleet [id]` — fleet location matches destination (onStation/away)

## Error Handling

- **"planet not complete"** — Deplete ore (currentOre = 0) before exploring.
- **"fleet must be onStation to explore"** — Recall the fleet to your current planet first via `fleet-move`. The chain blocks explore until the fleet has actually returned. (New players with no current planet do not see this error.)
- **"fleet away"** — Fleet must be available; wait for return or check fleet state.
- **"invalid destination"** — Use valid location ID; query grid for options.

## See Also

- [knowledge/mechanics/planet](https://structs.ai/knowledge/mechanics/planet) — Planet properties, ore, slots
- [knowledge/mechanics/fleet](https://structs.ai/knowledge/mechanics/fleet) — Fleet movement, on-station rules
- [knowledge/entities/entity-relationships](https://structs.ai/knowledge/entities/entity-relationships) — How entities connect

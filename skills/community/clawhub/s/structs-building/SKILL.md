---
name: structs-building
description: Builds and manages structures in Structs. Handles construction, activation, deactivation, movement, defense positioning, stealth, and generator infusion. Use when building a struct, activating or deactivating structs, moving structs between slots, setting defense assignments, enabling stealth, or infusing generators. Build times range from ~17 min (Command Ship) to ~6.4 hours (World Engine).
---

# Structs Building

**Important**: Entity IDs containing dashes (like `1-42`, `5-10`) are misinterpreted as flags by the CLI parser. All transaction commands in this skill use `--` before positional arguments to prevent this.

## Safety

See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract. In this skill:

- **`struct-build-initiate`** (Tier 0 for cheap structs; Tier 1 for long PoW like World Engine, Ore Bunker, PDC) — short builds (Command Ship, Starfighter, Ore Extractor, Refinery) are routine; anything > 1 hour to D=3 is a battle order.
- **`struct-build-compute`** (Tier 1 + expedition) — *"The build hashes for up to ~6.4 hours and auto-activates on completion."* Log the PID to `memory/jobs/`; recall with `kill <pid>` if needed. On reconnect, walk the four-state flow in [`awareness/async-operations`](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job) before launching anything new.
- **`struct-generator-infuse`** (Tier 2 — irreversible) — *"Alpha Matter is annihilated in the conversion. The energy is yours; the matter is gone. There is no defusion. And the generator is raidable — if it falls, the infused matter falls with it."* Always escalate, regardless of autonomy. Confirm the generator's defense posture before infusing.
- **`struct-deactivate`** of revenue-bearing structs (Tier 1) — taking an Extractor or Refinery offline halts your resource pipeline.

## Procedure

1. **Check requirements** — Player online, sufficient Alpha Matter, valid slot (0-3 per ambit), Command Ship online, fleet on station (for planet builds). Query player, planet, fleet.
2. **Initiate build** (CLI prompts for confirmation — review struct type, slot, ambit, and Alpha cost):

   ```
   structsd tx structs struct-build-initiate --from [key-name] --gas auto --gas-adjustment 1.5 -- [player-id] [struct-type-id] [operating-ambit] [slot]
   ```

   The `[operating-ambit]` argument must be a **lowercase string**: `"space"`, `"air"`, `"land"`, or `"water"` (not a bitmask number).

3. **Proof-of-work** — Build compute is an **expedition** that auto-activates the struct when the proof lands (this is why `-y` is present below).

   **Approval Block** — confirm before launching, especially for long-PoW structs (Ore Bunker, PDC, World Engine):

   - `struct-id` matches the build you just initiated
   - You have power headroom for the struct to auto-activate (load + struct's power-draw < capacity)
   - You will tolerate the auto-activation landing 17 min – 6.4 hrs from now even if game state shifts

   Launch in a background terminal:

   ```
   structsd tx structs struct-build-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]
   ```

   This calculates the hash, auto-submits complete, and the struct **auto-activates**. No separate activation step needed.

4. **Optional** — Move, set defense, or activate stealth as needed.

**Auto-activation**: Structs automatically activate after build-complete. Use `struct-activate` only to re-activate a struct that was previously deactivated with `struct-deactivate`.

## Compute vs Complete

`struct-build-compute` is a helper that performs proof-of-work and automatically submits `struct-build-complete` with the hash results. The struct then auto-activates. You only need `struct-build-complete` if you computed the hash through external tools and want to submit it manually.

## The -D Flag

The `-D` flag (range 1-64) tells compute to wait until difficulty drops to the specified level before starting the hash. Difficulty decreases logarithmically as the struct ages. **Use `-D 3`** — at D=3, the hash is trivially instant and zero CPU is wasted. Lower values wait longer but burn no compute on hard hashes.

## Charge Costs

Every action consumes charge. Charge accumulates passively at 1 per block (~6 sec/block).

| Action | Charge Cost | Wait Time |
|--------|------------|-----------|
| Build complete | 8 | ~48 seconds |
| Move | 8 | ~48 seconds |
| Activate (re-activation only) | 1 | ~6 seconds |
| Defend change | 1 | ~6 seconds |
| Primary weapon | 1-20 | Varies by struct |

If you get a "required charge X but player had Y" error, wait for charge to accumulate. See [knowledge/mechanics/building](https://structs.ai/knowledge/mechanics/building) for the complete charge table.

## Expected Build Times

Time from initiation until compute completes (assuming 6 sec/block, D=3):

| Struct | Type ID | Build Difficulty | Wait to D=3 |
|--------|---------|------------------|-------------|
| Command Ship | 1 | 200 | ~17 min |
| Starfighter | 3 | 250 | ~20 min |
| Ore Extractor | 14 | 700 | ~57 min |
| Ore Refinery | 15 | 700 | ~57 min |
| PDC | 19 | 2,880 | ~3.7 hr |
| Ore Bunker | 18 | 3,600 | ~4.6 hr |
| World Engine | 22 | 5,000 | ~6.4 hr |

**Initiate early, compute later.** The age clock starts at initiation. Batch-initiate all planned builds, then launch compute in background terminals. Do other things while waiting. See [awareness/async-operations](https://structs.ai/awareness/async-operations).

**One key, one compute at a time.** Never run two concurrent `*-compute` jobs with the same signing key. Both jobs may reach the target difficulty simultaneously and submit transactions with conflicting sequence numbers — one fails silently, leaving the struct stuck in build status. Use separate signing keys for separate players, and sequence compute jobs for the same player.

## Commands Reference

| Action | CLI Command |
|--------|-------------|
| Initiate build | `structsd tx structs struct-build-initiate --from [key-name] --gas auto --gas-adjustment 1.5 -- [player-id] [struct-type-id] [operating-ambit] [slot]` (`operating-ambit` = `space`/`air`/`land`/`water`, lowercase string) |
| Build compute (PoW + auto-complete + auto-activate) | `structsd tx structs struct-build-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` *(documented `-y` exception — auto-submits later)* |
| Build complete (manual, rarely needed) | `structsd tx structs struct-build-complete --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` |
| Build cancel | `structsd tx structs struct-build-cancel --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` |
| Re-activate (only after deactivation) | `structsd tx structs struct-activate --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` |
| Deactivate | `structsd tx structs struct-deactivate --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` |
| Move | `structsd tx structs struct-move --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id] [new-ambit] [new-slot] [new-location]` |
| Set defense | `structsd tx structs struct-defense-set --from [key-name] --gas auto --gas-adjustment 1.5 -- [defender-struct-id] [protected-struct-id]` |
| Clear defense | `structsd tx structs struct-defense-clear --from [key-name] --gas auto --gas-adjustment 1.5 -- [defender-struct-id]` |
| Stealth on | `structsd tx structs struct-stealth-activate --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` |
| Stealth off | `structsd tx structs struct-stealth-deactivate --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` |
| Generator infuse (Tier 2, irreversible) | `structsd tx structs struct-generator-infuse --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id] [amount]` |

**Limits**: 1 PDC per player, 1 Command Ship per player. Command Ship must be in fleet. Generator infusion is IRREVERSIBLE.

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule." `struct-build-compute` is the documented `-y` exception — it auto-activates the struct when the proof lands, with no shell attached.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Verification

- `structsd query structs struct [id]` — status = Online (or Built/Offline if not activated)
- Struct appears in planet/fleet struct list

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "required charge X but player had Y" | Not enough charge accumulated | Wait ~48s (8 blocks) between build actions |
| "insufficient resources" | Not enough Alpha Matter | Mine and refine ore first; check balance with `structsd query structs player [id]` |
| "power overload" | Capacity too low for struct to go online | Deactivate non-essential structs or increase capacity (see `structs-energy` skill) |
| "fleet not on station" | Fleet is away from planet | Wait for fleet return or `fleet-move` back |
| "Command Ship required" | Command Ship offline or not built | Build or re-activate Command Ship first |
| "invalid slot" | Slot already occupied | Check existing structs on planet; slots are 0-3 per ambit |
| "invalid ambit" | Struct type doesn't support chosen ambit | Check `possibleAmbit` bit-flags for the struct type |
| Connection refused on port 26657 | No local node; remote node not configured | Set `node` in `~/.structs/config/client.toml` or use `--node` flag (see TOOLS.md) |

## See Also

- [knowledge/mechanics/building](https://structs.ai/knowledge/mechanics/building) — Build times, difficulty, charge costs
- [knowledge/mechanics/power](https://structs.ai/knowledge/mechanics/power) — Capacity, load, online status
- [knowledge/entities/struct-types](https://structs.ai/knowledge/entities/struct-types) — All struct type IDs and properties
- [knowledge/entities/entity-relationships](https://structs.ai/knowledge/entities/entity-relationships) — How entities connect
- [awareness/async-operations](https://structs.ai/awareness/async-operations) — Background PoW, pipeline strategy

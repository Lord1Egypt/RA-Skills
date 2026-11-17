---
title: "Building structs: construct and position"
meta_description: "Turn power headroom and charge into capability: extractors, refineries, generators, and combat structs. Includes the full struct catalog."
name: structs-building
description: Builds and manages structs in Structs — construction, the build-order decision, activation/deactivation, movement, defense assignment, stealth, and generator infusion. Use when building a struct, deciding what to build next, activating/deactivating, moving the Command Ship, setting defenders, enabling stealth, or infusing a generator. Build times range ~17 min (Command Ship) to ~6.4 hr (World Engine) at D=3.
level: core
domain: building
---

# Building structs: construct and position

Building turns **power headroom + charge** into capability: extractors/refineries (production), generators (power), and combat/defense structs. Alpha Matter funds *power/infusion/trade*, not the build tx itself. The mechanics are simple — initiate, prove the work, it auto-activates — so the skill that matters is **deciding what to build, in what order, with the power to run it.**

Conventions (TX_FLAGS, `--` rule, the `-D 3` PoW policy, the per-player charge bar, one-tx-at-a-time) are in [`conventions.md`](https://structs.ai/skills/conventions).

## When to use it

- You have power headroom (and Alpha to infuse if you need more capacity) and want more infrastructure or military.
- Starting out and need the first base (Command Ship → extractor → refinery → power).
- Adding defense (shields, defenders, PDC) ahead of a refine window or a threat.
- Repositioning the Command Ship, assigning defenders, or stealthing a unit.
- Converting Alpha to power via generator infusion.

## Decisions

**Build-order by phase (beginner default):**

1. **Command Ship** (if you don't have one online) — required for *all* planet ops and your raid shield. Build in fleet, not on the planet.
2. **Ore Extractor → Ore Refinery** — start the production pipeline ([`structs-production`](https://structs.ai/skills/structs-production/SKILL)).
3. **Power** — a Reactor infusion or a Field Generator so the above stays online ([`structs-energy`](https://structs.ai/skills/structs-energy/SKILL)).
4. **Defense before your first big refine** — at least one shield struct; keep the Command Ship online.
5. **Expand** — more defense (Ore Bunkers/OSGs are unlimited now), then military.

**Always pre-check power.** Initiate needs headroom for **BuildDraw only**; complete then applies **PassiveDraw** (sequential — not summed). For equal draws (all current types), peak = one draw, not 2×. Use `scripts/power-budget.sh [player-id] --type [struct-type-id]` to project PassiveDraw after activation. If it won't fit, raise capacity first or the struct will materialize but never come online.

**Advanced considerations**:
- **Defense scaling**: Orbital Shield Generator and Ore Bunker are **unlimited per player** — stack them (power permitting) to drive your planetary shield well past a single set. Everything else is 1 per player.
- **What to build to kill what**: the Battleship is the armour-piercing answer to Tanks and to armoured power generators; planetary structs are tough (6/8/10 HP). Match builds to the threat — see [`structs-combat`](https://structs.ai/skills/structs-combat/SKILL).
- Decisions live in [`playbooks/phases/early-game`](https://structs.ai/playbooks/phases/early-game) and [`playbooks/meta/economy-of-force`](https://structs.ai/playbooks/meta/economy-of-force).

## Procedure

1. **Pre-check** — player online (capacity covers load); BuildDraw headroom; valid open slot (0-3 per ambit, correct ambit for the type); for planet builds: Command Ship online and fleet `onStation`. Run `scripts/power-budget.sh` to confirm headroom.
2. **Initiate** (CLI prompts — review type, ambit, slot; builds cost charge + power, not Alpha). `[operating-ambit]` is a lowercase string `space`/`air`/`land`/`water`, not a bitmask:
   ```
   structsd tx structs struct-build-initiate TX_FLAGS -- [player-id] [struct-type-id] [operating-ambit] [slot]
   ```
3. **Compute (expedition, auto-completes + auto-activates)** — this is the documented `-y` exception.

   **Approval Block** — struct id matches the build; you have power headroom for it to auto-activate; you accept the auto-activation landing minutes-to-hours later even if state shifts.

   ```bash
   nohup structsd tx structs struct-build-compute -D 3 --from [key] --gas auto --gas-adjustment 1.5 -y -- [struct-id] \
     > memory/jobs/build-[struct-id].log 2>&1 & echo $! > memory/jobs/build-[struct-id].pid
   ```
4. **Then** move / set defense / stealth as needed (below). No separate activate step — build-complete auto-activates. `struct-activate` is only for re-activating something you deactivated.

`struct-build-compute` performs the PoW and auto-submits `struct-build-complete`; you only call `struct-build-complete` directly if you hashed externally.

## Struct catalog (the numbers that drive decisions)

Full table: [knowledge/entities/struct-types](https://structs.ai/knowledge/entities/struct-types). Key current values:

| Group | HP | Build limit / player | Notes |
|-------|----|----|-------|
| Command Ship | 6 | 1 | movable; required for planet ops; build in fleet |
| Other fleet combat (IDs 2-13) | 3 | unlimited | ambit-locked; Battleship primary is armour-piercing |
| Ore Extractor / Refinery | 6 | 1 each | the production pipeline |
| Orbital Shield Generator | 6 | **unlimited** | shield-only → stack it |
| Ore Bunker | 6 | **unlimited** | raises planetary shield (raid PoW); does **not** vault ore; `canDefend: false` |
| Jamming Satellite / PDC | 6 | 1 each | shield + active defense |
| Field Generator | 8 | 1 | `armour` (DR 1); 2 kW/g |
| Continental Power Plant | 10 | 1 | `armour` (DR 1); 5 kW/g |
| World Engine | 10 | 1 | `armour` (DR 1); 10 kW/g |

Charge costs (from your **per-player** bar): build-initiate 8, trash 8, activate 2, defense-change 1, Command Ship move 3, stealth activate 2. Deactivate (single or batch) is free and works even while offline. Full charge table and PoW decay times: [knowledge/mechanics/building](https://structs.ai/knowledge/mechanics/building).

### Build times (initiation → D=3 complete, ~6 s/block)

| Struct | Type ID | Build Diff | Wait to D=3 |
|--------|---------|-----------|-------------|
| Command Ship | 1 | 200 | ~17 min |
| Starfighter | 3 | 250 | ~20 min |
| Ore Extractor / Refinery | 14 / 15 | 700 | ~57 min |
| PDC | 19 | 2,880 | ~3.7 hr |
| Ore Bunker | 18 | 3,600 | ~4.6 hr |
| World Engine | 22 | 5,000 | ~6.4 hr |

**Initiate early, compute later** — the age clock starts at initiation, and difficulty decays from 64 (fresh, impossible) to 1 (aged, instant). Batch-initiate, then compute in the background once it has decayed. **One compute at a time per key** (two concurrent computes on the same key collide on sequence numbers — one fails silently). Different keys run in parallel. See [hashing.md — fresh vs aged anchor](https://structs.ai/knowledge/mechanics/hashing#worked-example-fresh-vs-aged-anchor).

## Manage existing structs

- **Move (Command Ship only — it's the one movable struct):** `struct-move TX_FLAGS -- [cmd-ship-id] [new-ambit] [new-slot] [new-location]`. The chain rejects `struct-move` on any other struct.
- **Defense assignment:** `struct-defense-set TX_FLAGS -- [defender-id] [protected-id]` / `struct-defense-clear TX_FLAGS -- [defender-id]` (1 charge). Only fleet types (`canDefend: true`) can be assigned.
- **Stealth (Stealth Bomber, Submersible):** `struct-stealth-activate` / `struct-stealth-deactivate` (2 charge to activate).
- **Deactivate / re-activate:** `struct-deactivate` frees its power (free, and works even while you're offline — a recovery lever); `struct-activate` brings it back (2 charge, requires you online). Deactivate many at once with `struct-deactivate-batch -- [id1,id2,...]` (up to 65). Taking an Extractor/Refinery offline halts your pipeline (Tier 1).
- **Trash (Tier 2, IRREVERSIBLE):** `struct-trash TX_FLAGS -- [struct-id]` permanently destroys a **built** struct you own to free its slot (costs 8 charge, same as building it). There is no undo and nothing is refunded. To abort an **unfinished** build instead, use `struct-build-cancel`.
- **Generator infuse (Tier 2, IRREVERSIBLE):** `struct-generator-infuse TX_FLAGS -- [struct-id] [amount]ualpha`. Alpha Matter is annihilated into energy — no defusion, and a raided generator takes the infused matter with it. Always escalate; confirm the generator's defense posture first. See [`structs-energy`](https://structs.ai/skills/structs-energy/SKILL).

## Commands reference

| Action | CLI Command |
|--------|-------------|
| Initiate | `structsd tx structs struct-build-initiate TX_FLAGS -- [player-id] [type-id] [ambit] [slot]` |
| Compute (PoW + complete + activate) | `structsd tx structs struct-build-compute -D 3 TX_FLAGS_APPROVED -- [struct-id]` |
| Complete (manual, rare) | `structsd tx structs struct-build-complete TX_FLAGS -- [struct-id] [proof] [nonce]` |
| Cancel | `structsd tx structs struct-build-cancel TX_FLAGS -- [struct-id]` |
| Activate / Deactivate | `structsd tx structs struct-activate \| struct-deactivate TX_FLAGS -- [struct-id]` |
| Deactivate (batch, ≤65) | `structsd tx structs struct-deactivate-batch TX_FLAGS -- [id1,id2,...]` |
| Trash (destroy built struct, IRREVERSIBLE) | `structsd tx structs struct-trash TX_FLAGS -- [struct-id]` |
| Move (CMD ship) | `structsd tx structs struct-move TX_FLAGS -- [cmd-ship-id] [ambit] [slot] [location]` |
| Defense set / clear | `structsd tx structs struct-defense-set \| struct-defense-clear TX_FLAGS -- [defender-id] [protected-id]` |
| Stealth on / off | `structsd tx structs struct-stealth-activate \| struct-stealth-deactivate TX_FLAGS -- [struct-id]` |
| Generator infuse (Tier 2) | `structsd tx structs struct-generator-infuse TX_FLAGS -- [struct-id] [amount]ualpha` |

`TX_FLAGS` / `TX_FLAGS_APPROVED` per [`conventions.md`](https://structs.ai/skills/conventions). **Requires** [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a signing key.

## Verification

- `structsd query structs struct [id]` — status Online (or Built/Offline if power-starved).
- Struct appears in the planet/fleet struct list.
- After generator infuse: player `capacity` rises; broadcast ≠ success, so query to confirm.

## Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "required charge X but player had Y" | Per-player charge bar too low | Wait; space actions by their cost (see conventions) |
| "capacity_exceeded" / power errors | BuildDraw or PassiveDraw won't fit | Infuse / deactivate / wait ([structs-energy](https://structs.ai/skills/structs-energy/SKILL)) |
| "power overload" / won't go online | Capacity < load + draw | Raise capacity or deactivate something ([structs-energy](https://structs.ai/skills/structs-energy/SKILL)) |
| "fleet not on station" | Fleet away | Recall via `fleet-move` |
| "Command Ship required" | CMD ship offline/missing | Build or re-activate it first |
| "invalid slot" / "invalid ambit" | Slot taken or wrong ambit | Slots 0-3 per ambit; check the type's `possibleAmbit` |

## See also

- [knowledge/entities/struct-types](https://structs.ai/knowledge/entities/struct-types) — full catalog (HP, charge, limits, weapons)
- [knowledge/mechanics/building](https://structs.ai/knowledge/mechanics/building) — PoW decay, charge table
- [playbooks/phases/early-game](https://structs.ai/playbooks/phases/early-game) / [playbooks/meta/economy-of-force](https://structs.ai/playbooks/meta/economy-of-force) — build priorities
- [structs-energy](https://structs.ai/skills/structs-energy/SKILL) — power for builds; [structs-combat](https://structs.ai/skills/structs-combat/SKILL) — what to build vs threats
- [awareness/async-operations](https://structs.ai/awareness/async-operations) — background PoW

---
title: "Energy skill: capacity, load, infusion"
meta_description: Load above capacity means offline, and offline means you cannot act. Capacity management, substations, allocations, and reactor infusion.
name: structs-energy
description: "Power and capacity in Structs — getting more energy, fixing \"I'm offline\", substations and allocations, load budgeting, and reactor/generator infusion for your own capacity. Use when capacity is too low, a player or struct won't come online, you're load > capacity (offline), planning power for new builds, or wiring substations. For selling energy on the market, see structs-commerce."
level: core
domain: energy
---

# Energy skill: capacity, load, infusion

Every online struct draws power continuously, and **load > capacity = offline = you cannot act**. Energy is therefore the substrate of everything: no power, no mining, no building, no defense. This skill is "I need power / I'm offline / how do I budget power" — raising your own capacity (infusion), distributing it (substations/allocations), and recovering from overload. *Earning* from energy (running providers, selling, the flywheel) lives in [`structs-commerce`](https://structs.ai/skills/structs-commerce/SKILL).

Conventions (TX_FLAGS, `--` rule, charge bar, one-tx-at-a-time) are in [`conventions.md`](https://structs.ai/skills/conventions). **Interface:** if Structs Desktop MCP is connected, prefer `structs_intel` (power/economy reads) and `structs_action` (infuse, connect) — the `structsd` commands below are the complete fallback. See [interface routing](https://structs.ai/skills/conventions#choosing-your-interface-capability-aware).

> **Denomination footgun**: infusion amounts must carry the `ualpha` suffix — `60000000ualpha`, not `60000000`. Missing denom = failed tx.

## When to use it

- A struct won't go online, or you went offline (load exceeded capacity).
- You're about to build and need to confirm power headroom.
- You want more capacity (you have Alpha to infuse).
- You're setting up substations/allocations to distribute power.

## Decisions

### "I need more capacity" decision tree

```
Have Alpha Matter?
├── Yes → Infuse a reactor   → safest, immediate, reversible (cooldown), 1g ≈ 1 kW − commission   [default]
│         or Infuse a generator → 2-10 kW/g but IRREVERSIBLE and raidable (only with defense in place)
└── No  → Buy capacity via an agreement from a provider → ongoing cost; see structs-commerce
```

**Beginner default**: infuse your **guild's reactor**. Capacity rises automatically — no substation wiring needed for your own use. Pick the lowest commission you can.

> **Infusing a reactor powers *you*, not the guild substation.** Infusion adds ~96% (at 4% commission) to **your own** `capacity` and the commission to the reactor — it does **not** raise any substation's capacity or other members' `capacitySecondary`. To feed the shared guild pool, someone must route capacity in with an **allocation** (below). See [energy.md — infusion](https://structs.ai/knowledge/mechanics/energy#creating-capacity-infusion-splits-964).

**Reactor vs generator**: reactor is the safe default (reversible via a defusion cooldown, not raidable). Generators give far more kW per gram but the Alpha is **annihilated** (no defusion) and a raided generator takes the infused matter with it — only infuse generators you can defend (they're armoured with higher HP, but still a target). Decisions live in [`playbooks/situations/resource-rich`](https://structs.ai/playbooks/situations/resource-rich).

### "Am I about to go offline?"

Online requires `(load + structsLoad) ≤ (capacity + capacitySecondary)`. Player passive draw is 25,000 mW; each online struct adds its `passiveDraw`. Before building, confirm headroom — `scripts/power-budget.sh [player-id] --type [struct-type-id]` projects headroom-after-activation in one call. If you're already offline, that's an emergency (recovery below).

## Power math

```
availablePower = (capacity + capacitySecondary) - (load + structsLoad)
online         = (load + structsLoad) <= (capacity + capacitySecondary)
```

- `capacity` — your own generation (infusions); the only part you can allocate out.
- `capacitySecondary` — received from a substation you're connected to.
- `load` — power you've allocated to others.
- `structsLoad` — player passive (25,000 mW) + sum of `passiveDraw` of your online structs.

Units are milliwatts (1 W = 1,000 mW; 1 ualpha = 1 mW).

### Worked load budget

Command Ship (50,000 mW) + Ore Extractor (500,000) + Ore Refinery (500,000) + player passive (25,000) = **1,075,000 mW** of `structsLoad`. To keep all online you need `capacity + capacitySecondary ≥ 1,075,000`. Infusing ~1,120,000 ualpha into a 4%-commission reactor nets ~1,075,000 mW to you — just enough; leave a margin.

## Procedure — raise your own capacity (reactor infusion)

1. Check capacity: `structsd query structs player [id]`.
2. Pick a reactor and read its commission and **validator address**: `structsd query structs reactor [id]` (the `validator` field, `structsvaloper1...` — the command takes the validator address, not the reactor ID). A jailed validator produces **zero** energy from infusions until it is unjailed; `reactor-restart` resyncs after that.
3. Infuse (CLI prompts — review validator, commission, amount):
   ```
   structsd tx structs reactor-infuse TX_FLAGS -- [your-address] [validator-address] [amount]ualpha
   ```
   `reactor-infuse` is Tier 1 — commission is locked permanently for that infusion. Defusion takes the same three arguments as infusion (`reactor-defuse -- [your-address] [validator-address] [amount]ualpha`) and starts a cooldown before Alpha returns; `reactor-cancel-defusion` re-stakes during that cooldown.
4. Verify: re-query player; capacity increased.

## Procedure — generator infusion (Tier 2, irreversible)

Only with defense in place. **Approval Block**: struct id is your generator (type 20/21/22, online); amount is annihilated on success (no defusion); generator's defense posture is sound (shield up, defenders/PDC, no inbound fleet); `--from` owns it.

```
structsd tx structs struct-generator-infuse TX_FLAGS -- [struct-id] [amount]ualpha
```

Rates: Field Generator 2 kW/g, Continental Power Plant 5 kW/g, World Engine 10 kW/g.

## Procedure — distribute power (substations & allocations)

For pooling power across structs/players (e.g. a guild powering members). Cascading deletes can knock players offline mid-operation — these are Tier 2.

1. Create an allocation from your source: `structsd tx structs allocation-create --allocation-type static|dynamic|automated TX_FLAGS -- [source-id] [power]` (`--controller [player-id]` optional). Automated allocations auto-grow with capacity — **one per source**.
2. Create a substation: `structsd tx structs substation-create TX_FLAGS -- [owner-id] [allocation-id]`.
3. Connect/disconnect sources: `substation-allocation-connect|disconnect -- [substation-id] [allocation-id]`.
4. Connect/disconnect players: `substation-player-connect|disconnect -- [substation-id] [player-id]`.
5. Migrate players: `substation-player-migrate -- [substation-id] [player-id,player-id2,...]` (destination substation + player CSV; there is **no** source-substation argument).

> **Connecting/migrating another player needs `PermSubstationConnection` (1024) on the player too — not just the substation.** Connect and migrate run the same two checks (`1024` on the destination substation AND on each target player) and both call `MigrateSubstation`. A player object is owned by itself, so **owning the substation is not enough to move other members**: either the member **self-connects** (they own themselves; gate the substation with `permission-guild-rank-set [sub] [guild] 1024 [rank]`), or they grant you `permission-grant-on-object [player] [you] 1024` first. Repointing the guild entry substation (`guild-update-entry-substation-id`) only reroutes **new** join-proxy members — existing members are not auto-migrated. See [energy.md](https://structs.ai/knowledge/mechanics/energy).

**Three things that bite when pooling** (full detail in [energy.md](https://structs.ai/knowledge/mechanics/energy)):

- **A substation dilutes evenly.** Each connected player gets `connectionCapacity = (capacity − load) / connectionCount`, recomputed on every connect/disconnect. Every new player connection shrinks everyone's share — plan the pool against `connectionCount`, not a fixed per-member figure.
- **Anyone can contribute to any substation.** `substation-allocation-connect` checks permission only on **your own allocation**, not the destination substation's owner — no guild-owner veto, no membership needed. Contributing is open, but a contributed allocation raises *your own* connection by only `1/connectionCount`, so it's community behavior, not self-growth.
- **Over-committing triggers a brownout.** If an object's `load` exceeds its `capacity` (e.g. a substation loses a feed), the grid **destroys that object's outgoing allocations in creation order** until load fits — cascading downstream and knocking dependents offline. Leave headroom.

## Offline recovery (emergency)

1. **Free power now** — `struct-deactivate` non-essential structs until `load + structsLoad ≤ capacity + capacitySecondary`. Keep the **Command Ship online** if at all possible (offline CMD ship makes your planet raidable).
2. **Raise capacity** — infuse a reactor (fastest) or open an agreement.
3. **Reactivate** in priority order: Command Ship → defense → production.
4. Note: a player on a substation pool can show `capacity=0` while structs run fine — `structsLoad > 0` is the real "functioning" signal, not `capacity > 0`.

## Commands reference

| Action | Command |
|--------|---------|
| Reactor infuse | `structsd tx structs reactor-infuse TX_FLAGS -- [your-addr] [validator-addr] [amount]ualpha` |
| Reactor restart | `structsd tx structs reactor-restart TX_FLAGS -- [reactor-address]` |
| Reactor defuse | `structsd tx structs reactor-defuse TX_FLAGS -- [your-addr] [validator-addr] [amount]ualpha` |
| Reactor cancel defusion | `structsd tx structs reactor-cancel-defusion TX_FLAGS -- [your-addr] [validator-addr] [amount]ualpha [creation-height]` |
| Reactor migrate | `structsd tx structs reactor-begin-migration TX_FLAGS -- [player-addr] [src-val] [dest-val] [amount]ualpha` |
| Generator infuse (Tier 2) | `structsd tx structs struct-generator-infuse TX_FLAGS -- [struct-id] [amount]ualpha` |
| Allocation create / update / delete | `structsd tx structs allocation-create --allocation-type [t] TX_FLAGS -- [source-id] [power]` (and `allocation-update`/`allocation-delete -- [allocation-id] ...`) |
| Substation create / delete | `structsd tx structs substation-create \| substation-delete TX_FLAGS -- ...` |
| Substation allocation connect/disconnect | `structsd tx structs substation-allocation-connect \| disconnect TX_FLAGS -- [sub-id] [alloc-id]` |
| Substation player connect/disconnect/migrate | `structsd tx structs substation-player-connect \| disconnect \| migrate TX_FLAGS -- ...` |
| Query player power | `structsd query structs player [id]` |
| Query reactor | `structsd query structs reactor [id]` |
| Query substation / allocations | `structsd query structs substation [id]` / `allocation-all-by-source [id]` |

`TX_FLAGS` per [`conventions.md`](https://structs.ai/skills/conventions); power ops cascade, so default to interactive even on routine ones. **Requires** [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a signing key.

## Verification

- `structsd query structs player [id]` — `capacity`/`capacitySecondary`/`load`/`structsLoad`, online status.
- `structsd query structs substation [id]` — connected allocations/players.

## Errors

- **Going offline** — load > capacity; deactivate structs, then infuse/buy capacity.
- **"insufficient balance"** — not enough ualpha; refine ore first or buy via agreement.
- **"generator infuse failed"** — struct isn't a generator (20/21/22) or is offline.
- **Allocation exceeds source** — source capacity too small; allocate less or add capacity.
- **Automated allocation limit** — one automated per source; use static/dynamic for more.

## See also

- [knowledge/mechanics/energy](https://structs.ai/knowledge/mechanics/energy) — full energy system: units, infusion split, substation dilution, allocations, brownout
- [knowledge/mechanics/power](https://structs.ai/knowledge/mechanics/power) — capacity/load/online quick formula card
- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — Alpha → energy conversion rates
- [playbooks/situations/resource-rich](https://structs.ai/playbooks/situations/resource-rich) — infusion strategy
- [structs-commerce](https://structs.ai/skills/structs-commerce/SKILL) — selling energy, buying via agreement, the flywheel; [structs-building](https://structs.ai/skills/structs-building/SKILL) — power pre-check

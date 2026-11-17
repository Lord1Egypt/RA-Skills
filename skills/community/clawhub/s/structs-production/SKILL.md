---
title: "Production skill: mine, refine, stake"
meta_description: "The engine of everything: mine ore, refine it to Alpha Matter, stake it. Covers ore vulnerability and the handoff when a planet depletes."
name: structs-production
description: Runs the Alpha Matter production pipeline in Structs — mine ore, refine it to Alpha Matter, then put the Alpha to work. Use when mining or refining, starting or scheduling a mine→refine cycle, protecting stored ore, scaling output, deciding what to do with refined Alpha, or handling a planet running out of ore. Mining ~17h and refining ~34h are background expeditions; ore is stealable until refined.
level: core
domain: economy
---

# Structs Production

Production is the engine of everything: you mine **ore** from your planet, refine it into **Alpha Matter**, and Alpha Matter funds power, structs, trade, and guild collateral. The whole game's PvP tension lives in one fact — **ore is stealable, Alpha Matter is not** — and mining/refining are multi-hour proof-of-work expeditions, so production is fundamentally a *scheduling and risk* problem, not a clicking problem.

Conventions (TX_FLAGS, the `--` rule, the `-D 3` PoW policy, the per-player charge bar, one-tx-at-a-time) are assumed from [`conventions.md`](https://structs.ai/skills/conventions). Read it once.

## When to use it

- You have an Ore Extractor + Ore Refinery and a planet with `currentOre > 0`.
- A mine or refine job just landed (start the next stage immediately).
- You're sitting on `storedOre` (a liability — refine it).
- Your planet is depleting and you need to decide expand vs. squeeze the last ore.
- You're planning throughput, or scaling across multiple accounts.

## Decisions

**Beginner default**: One Ore Extractor + one Ore Refinery (both 1-per-player). Mine, and the *instant* mining lands, start refining — never let ore sit. Refine at `-D 3`. Keep your Command Ship online the whole time so the planet is unraidable (see [`structs-combat`](https://structs.ai/skills/structs-combat/SKILL)). That alone wins the early resource game.

**The core trade-off — ore exposure vs. CPU**: mined ore is vulnerable for the entire refine window. At `-D 3` that's ~34 hours but zero wasted CPU; at `-D 8` it's ~15 hours but burns real compute. Default to `-D 3` *and protect the window* rather than racing it.

**Advanced considerations**:
- **Throughput is capped per player** — 1 Ore Extractor, 1 Ore Refinery, fixed 1 ore/cycle. You don't scale by building more extractors (you can't). You scale by: tighter cycle cadence (always have something aging), refining during the owner's off-hours, and **multi-account orchestration** (separate keys mine in parallel — different accounts transact independently; see [`structs-permissions`](https://structs.ai/skills/structs-permissions/SKILL)).
- **Harden the window** with bunkers/OSGs (shield/PoW only — not ore vaults). Real protection: refine promptly + CMD online + fleet onStation. Mine and refine are **rejected** while a visitor heads the raid queue (`under_raid`); do not retry compute mid-raid. See [under-attack](https://structs.ai/playbooks/situations/under-attack).
- **Keep a reserve.** Hold ~20-30% of Alpha Matter liquid for emergencies (power, rebuilds) rather than infusing everything.
- Decisions live in [`playbooks/situations/resource-rich`](https://structs.ai/playbooks/situations/resource-rich) and [`resource-scarce`](https://structs.ai/playbooks/situations/resource-scarce).

## The pipeline

```
Ore Extractor ──mine (~17h)──▶ storedOre (STEALABLE) ──refine (~34h)──▶ Alpha Matter (SECURE) ──▶ power / build / trade / stake
```

Both stages are **expeditions**: the compute helper hashes for hours then auto-submits its completion transaction (this is why `-y` is required on compute commands — there's no shell to confirm when the proof lands). Log every job to `memory/jobs/` and never block on PoW.

## Procedure

1. **Check the planet** — `structsd query structs planet [planet-id]`. If `currentOre == 0`, the planet is spent → go to *Depletion* below. Otherwise continue.
2. **Confirm the extractor is online** — `structsd query structs struct [extractor-id]` (status Online). Activate if needed (`struct-activate`, 2 charge). **Activation *is* the start of the mining cycle when you are the first online extractor on the planet** — it stamps the shared `planetBlockStartOreMine`. There is no separate "begin mining" action. Deactivating decrements the planet's active-miner count; the clock stays until quantity returns to zero and a later activate re-anchors.
3. **Confirm the planet is not under raid** — if `locationListStart` is set, mine/refine compute and complete reject with `under_raid`. Wait for the visitor to leave; the planet clock's pre-raid age is preserved, not decayed through the raid. See [hashing.md — raid pause](https://structs.ai/knowledge/mechanics/hashing#raid-pause-mine-and-refine).
3. **Compute the mine completion** (background expedition, ~17h to D=3, difficulty 14,000). This hashes against the clock activation already armed and submits the *completion* — it does not "start" anything.

   **Approval Block** — confirm before launch: extractor id is correct; planet `currentOre > 0`; `--from` is the owner key; you accept an auto-submitted completion ~17h out even if state shifts.

   ```bash
   nohup structsd tx structs struct-ore-mine-compute -D 3 --from [key] --gas auto --gas-adjustment 1.5 -y -- [extractor-id] \
     > memory/jobs/mine-[extractor-id].log 2>&1 & echo $! > memory/jobs/mine-[extractor-id].pid
   ```

4. **Do other work while it ages** — scout, build defense, plan. Always keep something aging (activate early, compute later). The mine clock lives on the **planet** and resets after each successful mine (any extractor), so every cycle re-enters the full ~17h decay. Cycles **never expire**: an aged clock is *cheaper* to complete, not wedged — never "reset" or "clean up" an old mine/refine. See [hashing.md — cycle lifecycle](https://structs.ai/knowledge/mechanics/hashing#minerefine-cycle-lifecycle).
5. **Refine in parallel — don't wait for the mine.** A refinery can be activated with **0 ore**; ore mined (or received) mid-cycle counts at completion time. Activate and compute the refinery *alongside* the extractor rather than serially, and the pipeline completes faster (~34h to D=3, difficulty 28,000). Refined Alpha is secure; unrefined ore is stealable, so keep the refine cycle always running.

   **Approval Block** — same five checks, applied to the ~34h refine window.

   ```bash
   nohup structsd tx structs struct-ore-refine-compute -D 3 --from [key] --gas auto --gas-adjustment 1.5 -y -- [refinery-id] \
     > memory/jobs/refine-[refinery-id].log 2>&1 & echo $! > memory/jobs/refine-[refinery-id].pid
   ```

6. **Protect the window** — Command Ship online (unraidable), Ore Bunker(s) up, defenders assigned. See [`structs-combat`](https://structs.ai/skills/structs-combat/SKILL).
7. **Put the Alpha to work** — once refined (secure), infuse for power ([`structs-energy`](https://structs.ai/skills/structs-energy/SKILL)), stake/sell ([`structs-commerce`](https://structs.ai/skills/structs-commerce/SKILL)), or hold reserve.

### Charge-bar scheduling

Activating the extractor/refinery costs 2 charge each from your **shared per-player bar**. If you activate several structs back-to-back, space them by ~2 blocks. The compute (mine/refine) itself isn't charge-gated; the activation that precedes it is.

## Depletion → explore handoff

When `currentOre` hits 0 the planet becomes `complete`: all its structs are destroyed and fleets are sent away. Before the last ore is mined, decide:

- **Squeeze** the last ore if you can refine it before depletion forces you off, **or**
- **Move first** — relocate critical structs / evacuate, then explore.

Then hand off to [`structs-planets-fleet`](https://structs.ai/skills/structs-planets-fleet/SKILL) to chart and claim a new planet. If an extractor/refinery is destroyed mid-job, progress **pauses** (mined/refined amounts aren't lost) until you rebuild.

## Commands reference

| Action | CLI Command |
|--------|-------------|
| Mine (PoW + auto-complete) | `structsd tx structs struct-ore-mine-compute -D 3 TX_FLAGS_APPROVED -- [extractor-id]` |
| Refine (PoW + auto-complete) | `structsd tx structs struct-ore-refine-compute -D 3 TX_FLAGS_APPROVED -- [refinery-id]` |
| Mine/refine complete (manual, rare) | `structsd tx structs struct-ore-mine-complete TX_FLAGS -- [id] [proof] [nonce]` / `...refine-complete TX_FLAGS -- [id] [proof] [nonce]` |
| Query planet ore | `structsd query structs planet [planet-id]` |
| Query struct | `structsd query structs struct [id]` |
| Query player (Alpha + storedOre) | `structsd query structs player [player-id]` |

`TX_FLAGS` / `TX_FLAGS_APPROVED` and the `-D` policy are defined in [`conventions.md`](https://structs.ai/skills/conventions). Mine/refine compute are the documented `-y` exception (they auto-submit) — your Approval Block is the gate.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Verification

- Planet `currentOre` decreases after a mine lands.
- Player `storedOre` rises after mine, returns to 0 after refine.
- Player Alpha Matter (`ualpha`, 1g = 1,000,000) rises after refine.
- Broadcast ≠ success: query state to confirm before assuming a stage finished.

## Errors

- **"under_raid"** — a visiting fleet is in the planet's raid queue. Mine/refine compute and complete are rejected until it leaves. Do not retry; the clock's pre-raid age is preserved. See [under-attack](https://structs.ai/playbooks/situations/under-attack).
- **"struct offline"** — activate the extractor/refinery first.
- **"insufficient ore"** — planet depleted or nothing in `storedOre`; check `currentOre` / `storedOre`.
- **"proof invalid"** — re-run compute at the right difficulty; ensure the process wasn't interrupted.
- **Ore stolen** — you left it unrefined or your Command Ship went offline mid-window. Refine immediately and keep the CMD ship up. See the reconnect flow in [`awareness/async-operations`](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job).

## See also

- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — conversion rates, vulnerability window, security model
- [knowledge/mechanics/planet](https://structs.ai/knowledge/mechanics/planet) — depletion, raid vulnerability
- [playbooks/situations/resource-rich](https://structs.ai/playbooks/situations/resource-rich) / [resource-scarce](https://structs.ai/playbooks/situations/resource-scarce) — production strategy
- [awareness/async-operations](https://structs.ai/awareness/async-operations) — background PoW, job tracking, pipeline scheduling
- [structs-combat](https://structs.ai/skills/structs-combat/SKILL) — protecting the ore window; [structs-energy](https://structs.ai/skills/structs-energy/SKILL) / [structs-commerce](https://structs.ai/skills/structs-commerce/SKILL) — spending Alpha

---
title: "Combat skill: attacks, raids, defense"
meta_description: Combat exists to move ore. Raids and ore theft, ambit-gated counters, single-target weapons, and the defensive posture that keeps yours.
name: structs-combat
description: "Combat and raiding in Structs — raids (the way to steal ore), direct struct attacks, and defense. Use when raiding a planet for ore, deciding whether a target is worth raiding, attacking enemy structs, defending your planet, or preparing for an incoming attack. The rule that governs everything: a planet is only raidable while its shields are vulnerable — the defender's fleet is off-station, or their Command Ship is offline/destroyed."
level: core
domain: combat
---

# Combat skill: attacks, raids, defense

Combat exists to move ore. **Raiding** is how you take another player's mined ore; **attacks** soften defenses and kill structs; **defense** keeps your own ore and infrastructure alive. The single most important fact: **a planet can only be raided to completion while its shields are vulnerable** — the defender's **fleet is off-station**, or their **Command Ship is offline, destroyed, or non-existent**. Keep your fleet on station with the Command Ship online and you are effectively unraidable; to raid someone, you must **catch them vulnerable — or make them vulnerable** by destroying (or power-starving) their Command Ship. Vulnerability is a state you can force, not just one to wait for. (The Command Ship only defends home while the fleet is on station, so sending your fleet away to raid exposes your own planet until it returns.)

Conventions (TX_FLAGS, `--` rule, `-D 3` PoW, the per-player charge bar, one-tx-at-a-time) come from [`conventions.md`](https://structs.ai/skills/conventions). **Interface:** if Structs Desktop MCP is connected, prefer `structs_intel` (`scout`, `simulate`, `valid_targets`, `strike_options`) and `structs_action`/`structs_strike` for engagements — the `structsd` commands below are the complete fallback. See [interface routing](https://structs.ai/skills/conventions#choosing-your-interface-capability-aware).

## When to use it

- You spotted a target with stored ore and want to raid it.
- You're under attack or expect to be (a refine window, a hostile fleet nearby).
- You need to kill a specific enemy struct (a generator, a defender, a Tank).
- You're setting up standing defense for your planet.

## Decisions

### Two ways to raid: opportunistic vs siege

**Shield-vulnerability is a state you can create, not just one you wait for.** This is the most-missed idea in raiding. There are two modes:

- **Opportunistic** — the defender is *already* vulnerable when you scout (fleet off-station, or Command Ship already offline/destroyed/absent). Move in and grind. Cheap, but truly-vulnerable ore-holders are rare.
- **Siege (force vulnerability)** — the defender is shielded (Command Ship online, fleet on station). You **manufacture** the window: move in, strip same-ambit blockers, **destroy their Command Ship**, then complete before they rebuild. "Their Command Ship is online" is *not* a dead end — it is the thing you go and break.

An online Command Ship should trigger the question **"can I destroy it?"**, not "next target." See the siege procedure below.

### Idle is not vulnerable (and the fleet-move trap)

A **dormant** owner (idle for days) is not a **vulnerable** one. Powered structs stay online with no player action, so an idle owner's Command Ship keeps defending indefinitely — the opportunistic gate stays shut. **Never infer raidability from an inactivity signal or a UI "vulnerable"/"inactive" badge** (those are derived from activity, not the live shield predicate). Confirm the live state: Command Ship online + fleet on station.

The trap this avoids is real and strictly-negative: moving your fleet to a not-yet-vulnerable target drops **your own** shields (fleet off-station) and exposes **your** stored ore, for a raid that can never complete. If you move your fleet, commit to the *siege*, not just the move. (The upside: a dormant owner who holds ore and won't rebuild is the *best* siege target — the window you force open stays open.)

### Raid go/no-go (the most important decision)

Use `scripts/scout.sh [planet-id]` for a structured read, then decide by mode:

1. **Is there ore to take?** — defender's `storedOre > 0` (ideally a lot; a successful raid seizes **all** of it, not a share). No ore → no raid, in either mode.
2. **Are shields vulnerable right now?** — fleet off-station, or Command Ship offline/destroyed/absent.
   - **Yes → opportunistic go.** Confirm you out-damage the defenders within the window and the shield PoW is feasible (base 25, +online defense-struct contributions).
   - **No (Command Ship online, fleet on station) → siege decision.** Can you reach and destroy their Command Ship (6 HP, usually defended), and is the ore worth leaving your own home exposed while your fleet is away? A dormant defender who won't rebuild tips this toward go; a watchful, well-defended one tips it toward wait/watch.
3. **Will you survive the resolution and the window?** — your fleet must out-damage the defense, and (for a siege) kill the Command Ship before an active defender rebuilds it.

**When NOT to raid**: no/low stored ore; a shield so high the PoW outlasts your window; a well-defended Command Ship guarded by a bloc that will retaliate for less ore than you'd lose; or you cannot reach the Command Ship's ambit. Raiding is an *expedition* — it costs you a fleet locked `away` and your home undefended by fleet. Expected ore must beat that cost. An honest no-go (or "watch and wait") is a win, not a failure.

### Defense doctrine

- **Keep your Command Ship online and your fleet on station — always.** That combination makes you unraidable. Most "I got raided" stories are "my CMD ship went offline (usually power) and I didn't notice" — or "I sent my fleet off to raid and left my own shields down." Watch for it (`scripts/watch-defense.mjs` alerts on your CMD ship dropping and on raids against you). Treat raiding with your own fleet as a deliberate trade: while it's away, your home is exposed.
- **Stack shields.** Orbital Shield Generator and Ore Bunker are unlimited — build several to push raid difficulty up as a second layer behind the CMD-ship gate. Mid-raid: do **not** start a new refine (~34h); only finish one already completable — see [under-attack](https://structs.ai/playbooks/situations/under-attack).
- **Refine fast.** Defense protects *structs*, never *ore*. The only defense for ore is turning it into Alpha Matter ([`structs-production`](https://structs.ai/skills/structs-production/SKILL)).
- **Assign defenders** across ambits to protect the Command Ship and key structs.

Decisions live in [`playbooks/situations/under-attack`](https://structs.ai/playbooks/situations/under-attack), [`guild-war`](https://structs.ai/playbooks/situations/guild-war), and [`playbooks/meta/counter-strategies`](https://structs.ai/playbooks/meta/counter-strategies).

## How a raid resolves

`blockStartRaid` is the **defender's vulnerability clock**, and raid PoW age is measured from it:

- It starts when the defender's shields become vulnerable — their Command Ship goes offline or their fleet leaves station (or when you arrive to find it already vulnerable).
- It resets to 0 if the defender restores their shields (Command Ship back online with the fleet on station) — and completion is rejected (`raid_clock_unset` when 0; the raid status flips to `ongoing` with shields restored).
- Raid statuses you'll see: `initiated` → `shieldsVulnerable` (shields down, clock running, winnable) → `raidSuccessful` / `attackerRetreated`. `attackerDefeated` means your raiding Command Ship was destroyed while away. `demilitarized` means no defenders to resolve against.

The clock only runs **while your raider is present** at the target — it is set at arrival if the defender is already vulnerable (opportunistic), or the moment their Command Ship drops while you're there (siege). So a raid is a race against the defender noticing and restoring their shields. Scout the CMD ship and fleet position first. For an **opportunistic** raid, don't move your fleet until they're already vulnerable; for a **siege**, moving in is step one and you break the shield yourself.

**A raid steals ore.** A successful raid seizes **all** of the defender's `storedOre` and nothing more — it does not destroy the player or their structs. Killing the defender's Command Ship opens the `shieldsVulnerable` window so the raid can complete; if the defender restores or rebuilds it before you finish, completion is rejected (`shields_active`) and you get **nothing**. Beware the reverse: `trigger_raid_defeat_by_destruction` is on the Command Ship, so if **your** raiding CMD ship is destroyed while away, your fleet is defeated (`attackerDefeated`) and sent home. Win path for ore: strip same-ambit blockers → destroy the defender's CMD ship → complete the raid before they rebuild it (most reliable vs an offline defender).

## Procedure — opportunistic raid (defender already vulnerable)

1. **Scout** — `scripts/scout.sh [planet-id]` (or `structsd query structs planet [id]` + struct/player queries). Confirm the go conditions above, especially the defender's **Command Ship status** — it must already be offline/destroyed/absent, or their fleet off-station.
2. **Optional stealth** — stealth a unit before approach (`struct-stealth-activate`, 2 charge); attacking later auto-drops it.
3. **Move fleet to the target** (instant). Your fleet (and your Command Ship) is now `away`; you can't build/mine at home while away, **and your own planet's shields are now vulnerable** until the fleet returns — refine your home ore before you leave.
   ```
   structsd tx structs fleet-move TX_FLAGS -- [fleet-id] [destination-location-id]
   ```
4. **Approval Block** — fleet is your raider and now at the target; defender's CMD ship is down (verified); your home ore is refined or below your theft tolerance; you accept an auto-submitted completion landing minutes-to-hours out.
5. **Raid compute** (expedition, auto-submits completion — the documented `-y` exception):
   ```bash
   nohup structsd tx structs planet-raid-compute -D 3 --from [key] --gas auto --gas-adjustment 1.5 -y -- [fleet-id] \
     > memory/jobs/raid-[fleet-id].log 2>&1 & echo $! > memory/jobs/raid-[fleet-id].pid
   ```
6. **Move fleet home and refine the stolen ore immediately** — it's stealable in *your* hands now too.

If the defender restores their Command Ship mid-raid, the clock resets — withdraw or wait for it to drop again.

## Procedure — siege raid (force the window open)

Use this when the target holds ore but is shielded (Command Ship online, fleet on station) — the case an opportunistic raid can't touch. It costs a fleet engagement and leaves your home exposed, so run the go/no-go above first. Best against a dormant defender who won't rebuild.

1. **Scout the Command Ship's ambit and defenders** — `scripts/scout.sh [planet-id]` surfaces the defender's Command Ship id and status; query it directly with `structsd query structs struct [commandStruct-id]` for its `operatingAmbit`. To enumerate the **same-ambit** structs that can block for it, use the Guild Stack ("defenders by planet" — there is no `structsd` CLI command that lists a planet's structs). Confirm you have weapons that reach the Command Ship's ambit.
2. **Refine your own ore and move your fleet to the target.** Your home shields drop while away — accept that exposure as the cost of the siege. A planet holds **one visiting fleet** by default; if the slot is taken, `fleet-move` is `queue_full`.
   ```
   structsd tx structs fleet-move TX_FLAGS -- [fleet-id] [destination-location-id]
   ```
   At this point `planet-raid-compute` will still reject (`no active raid window`) — that is expected; the window isn't open yet.
3. **Strip same-ambit blockers, then destroy the Command Ship** with `struct-attack` (space repeated attacks; the charge bar is per-player and doesn't bank — coordinate multiple accounts to focus-fire if you have them). Destroying it fires the chain's vulnerability hook and opens `shieldsVulnerable` with your raider present.
   ```
   structsd tx structs struct-attack TX_FLAGS -- [operating-struct-id] [target-id] [weapon-system]
   ```
4. **Verify the window is open** — `structsd query structs planet [planet-id]` shows `blockStartRaid != 0` (raid status `shieldsVulnerable`). Only now is compute worthwhile.
5. **Raid compute** (same command as opportunistic step 5), then **move home and refine** the seized ore immediately.

Watch for the defender rebuilding the Command Ship (an active defender will) — if it comes back online with the fleet on station before your proof lands, the clock resets and completion fails. Never let **your** raiding Command Ship die while away (`attackerDefeated`).

## Procedure — direct attack

Scout the target's ambit and defense type, position (Command Ship only) into range, then fire. The attack needs only the attacking struct and its owner online — your Command Ship does not need to be online to attack, change defenders, or change stealth. The **target must be a built struct**: a struct that is still building cannot be attacked (`unbuilt`), and a destroyed one is rejected (`destroyed`); the target's online status is irrelevant. The CLI prompts; verify target IDs and that you aren't crossing guild lines you didn't intend to (attacking another guild's structs is a Tier 2 act of war). Note most weapons are single-target (`primaryWeaponTargets = 1`) — the comma list only spreads damage for weapons whose target count is > 1.

```
structsd tx structs struct-attack TX_FLAGS -- [operating-struct-id] [target-id,target-id2,...] [weapon-system]
```

Attacks cost 3-5 charge from your **per-player** bar; space repeated attacks accordingly.

## Procedure — defense setup

```
structsd tx structs struct-defense-set TX_FLAGS -- [defender-struct-id] [protected-struct-id]
structsd tx structs struct-defense-clear TX_FLAGS -- [defender-struct-id]
```

**Only fleet structs can be assigned as a defender** (`canDefend: true`; 1 charge each; stagger ~6 s on one key) as long as the defender is **built, online, and co-located** with the protected struct — ambit is **not** required to *assign*. Planetary types (Ore Extractor, Refinery, Ore Bunker, PDC, generators, …) are rejected. Ambit decides what the defender can do: **same-ambit** is required only to **block** (intercept a hit), while a **cross-ambit** defender still **counters** whenever its weapon can reach the attacker. Spread fleet defenders across ambits for counter coverage; keep same-ambit defenders where you need real interception. Minimum viable defense: at least one combat struct per ambit guarding the Command Ship (6 HP; most fleet structs are 3 HP).

## Tactical reference

### Targeting (which struct hits which ambit)

| Struct | Lives In | Primary | Secondary |
|--------|----------|---------|-----------|
| Command Ship | Any (movable) | current ambit only | — |
| Battleship | Space | Land, Water (**armour-piercing**) | Space |
| Starfighter | Space | Space | Space (Attack Run, ≥1 hit) |
| Frigate | Space | Space, Air | — |
| Pursuit Fighter | Air | Air | — |
| Stealth Bomber | Air | Land, Water | — |
| High Alt Interceptor | Air | Space, Air | — |
| Mobile Artillery | Land | Land, Water | — |
| Tank | Land | Land | — |
| SAM Launcher | Land | Space, Air | — |
| Cruiser | Water | Land, Water | Air |
| Destroyer | Water | Air, Water | — |
| Submersible | Water | Space, Water | — |

The Command Ship is the only struct that can change ambits (`struct-move`); it attacks only its current ambit. Reposition it into range to attack, or out of range to hide.

### Weapon control vs defense (evasion + armour-piercing)

| Target Defense | vs Guided | vs Unguided |
|----------------|-----------|-------------|
| Signal Jamming (Battleship, Pursuit Fighter, Cruiser) | **66% miss** | full hit |
| Defensive Maneuver (High Alt Interceptor) | full hit | **66% miss** |
| Armour (Tank, Field Generator, Continental Power Plant, World Engine) | full hit, −1 dmg | full hit, −1 dmg |
| Stealth Mode (Stealth Bomber, Submersible) | same-ambit only | same-ambit only |
| Indirect Combat (Mobile Artillery) | full hit | full hit |
| None | full hit | full hit |

Use unguided vs Signal Jamming, guided vs Defensive Maneuver. **Armour reduces damage by 1 — except against armour-piercing weapons (the Battleship primary), which ignore it.** The Battleship is the dedicated answer to Tanks and to the (now armoured) power generators. Minimum damage after reduction is always 1.

### Combat resolution notes

- **Counters are ambit-gated, blocks are ambit-matched.** A defender counters whenever its weapon can reach the **attacker's** ambit (regardless of what it's defending); it can only **block** when it shares the **target's** ambit. Consequence: attacking land structs from air/water/space (an ambit the defenders can't reach) takes **zero counter damage** — the single biggest combat lever. Pick your attacking ambit to dodge counters.
- Each struct counters at most **once per `struct-attack` invocation** (not per target/shot). Defender counter fires before block and even on evaded shots; target counter fires after all shots (destroyed targets can't counter).
- Block only fires on non-evaded shots and only from a defender in the **target's** ambit.
- **Counters are a backstop, not a damage plan** — counter values are small (typically 1; Command Ship 2) and a cross-ambit attacker takes none at all. Win with active `struct-attack` volleys from a safe ambit, not by baiting counters.
- **Single-target**: every weapon has `primaryWeaponTargets = 1` (one struct per volley) — no multi-target weapon exists. The comma-list in `struct-attack` doesn't make a single-target weapon spread.
- **No charge banking**: any action resets your shared charge bar to 0 and it refills ~1/block — you cannot stockpile for a multi-attack burst. Plan combat as spaced single actions. Because the bar is **per-player**, the way to land many hits at once is **parallel**: coordinate multiple accounts to focus-fire one target — N players land N attacks per charge cycle. See [team-operations](https://structs.ai/playbooks/meta/team-operations).
- **Planetary defenses (attacking a planet)**: the **Jamming Satellite** runs a low-orbit ballistic interceptor network that can **evade your _guided_ ordnance against planetary structs on their own planet — regardless of ambit** (`evadedByPlanetaryDefenses`). Ambit no longer matters and **unguided ordnance passes through untouched**, so bring unguided weapons against a planet with interceptors, or expect 0s from guided fire. This is on top of any unit-level `signalJamming` the target itself carries (both layers stack against guided). The PDC and the interceptor network are the planetary defenses that affect combat.
- PDC auto-fires after all targets resolve (it does not counter); multiple players' PDCs stack.
- A successful raid seizes **all** of the defender's `storedOre` and nothing else — there is no player-elimination outcome (see raid section). Destroyed structs are gone forever but can be rebuilt (full PoW). Losing your Command Ship disables the whole fleet until you build a new one — protect it above all, and never let your raiding CMD ship die while away (`attackerDefeated`).

## Commands reference

| Action | CLI Command |
|--------|-------------|
| Attack | `structsd tx structs struct-attack TX_FLAGS -- [struct-id] [target-ids] [weapon-system]` |
| Raid compute (PoW + auto-complete) | `structsd tx structs planet-raid-compute -D 3 TX_FLAGS_APPROVED -- [fleet-id]` |
| Raid complete (manual, rare) | `structsd tx structs planet-raid-complete TX_FLAGS -- [fleet-id] [proof] [nonce]` |
| Fleet move | `structsd tx structs fleet-move TX_FLAGS -- [fleet-id] [destination-location-id]` |
| Defense set / clear | `structsd tx structs struct-defense-set \| struct-defense-clear TX_FLAGS -- [defender-id] [protected-id]` |
| Stealth on / off | `structsd tx structs struct-stealth-activate \| struct-stealth-deactivate TX_FLAGS -- [struct-id]` |
| Move Command Ship (ambit) | `structsd tx structs struct-move TX_FLAGS -- [cmd-ship-id] [ambit] [slot] [location]` |

Raid flow: scout → (CMD ship down?) → fleet-move → raid-compute → fleet-move home → refine. `planet-raid-compute` is the documented `-y` exception; your Approval Block is the gate. `planet-raid-complete` does not consume charge.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a signing key.

## Verification

- `structsd query structs fleet [id]` — location and `onStation`/`away`.
- After a raid: your `storedOre` rose (refine it). For the exact grams seized, the **authoritative source is `ledger` rows with `action = 'seized'`**, not `planet_raid.seized_ore` — the ledger even records 0-gram seizures (a raid that reached the planet but took nothing, e.g. a repelled probe). See [database-schema.md — planet_raid](https://structs.ai/knowledge/infrastructure/database-schema).
- After attacks: events include remaining-health values — use them to assess damage.
- Broadcast ≠ success: a raid can land but resolve as `defeat`/`ongoing`. Query the raid status.

## Errors

- **"shields are not vulnerable: no active raid window (defending Command Ship may still be online)"** — the CLI-side `planet-raid-compute` pre-check when `blockStartRaid == 0`. This is the message you usually hit first. It does **not** mean "grind harder": the defender is shielded. Either wait/watch for them to slip (opportunistic), or open the window yourself by destroying their Command Ship with your fleet present (siege procedure above).
- **"cannot raid_complete while shields_active" / raid rejected** — the chain-side `planet-raid-complete` rejection: the defender is not vulnerable at completion (fleet on station with the Command Ship online). You cannot win until they're vulnerable again — force it or wait.
- **"cannot raid_complete while raid_clock_unset"** — `blockStartRaid` is 0 (no live raid window). Get your fleet to the target and make the defender vulnerable (their CMD ship offline/destroyed, or fleet off-station) before computing.
- **"unbuilt" / "destroyed" (attack)** — the target struct isn't a valid combat target: it's still building or already destroyed. Pick a built target.
- **"unreachable" / "out_of_range"** — your weapon can't reach that ambit; reposition the Command Ship or use a different struct.
- **"fleet not away"** — move the fleet to the target first.
- **"insufficient charge"** — per-player bar too low; wait (see conventions).
- **"queue_full"** — the destination planet already has its visiting-fleet cap (`1 + locationListExtra`, default 1). Wait for the parked fleet to leave, or pick another target.
- **"cannot defend" / StructCannotDefend** — you tried to assign a planetary struct as a defender. Only fleet types (`canDefend: true`) work.
- **"under_raid"** — mine/refine is paused while a visitor heads the queue. Do not retry those computes until they leave.

## See also

- [knowledge/mechanics/combat](https://structs.ai/knowledge/mechanics/combat) — damage, evasion, raid phases, SHIELDS_VULNERABLE
- [knowledge/mechanics/fleet](https://structs.ai/knowledge/mechanics/fleet) — fleet status, raid window
- [playbooks/situations/under-attack](https://structs.ai/playbooks/situations/under-attack) / [guild-war](https://structs.ai/playbooks/situations/guild-war) / [counter-strategies](https://structs.ai/playbooks/meta/counter-strategies)
- [structs-intel](https://structs.ai/skills/structs-intel/SKILL) — scouting + raid-worthiness scoring; [structs-production](https://structs.ai/skills/structs-production/SKILL) — refine to protect ore

---
name: structs-combat
description: Executes combat operations in Structs. Covers attacks, raids, defense setup, and stealth positioning. Use when attacking enemy structs, raiding a planet for ore, setting up defenders, activating stealth, moving fleet for raids, or preparing for incoming attacks. Raids require fleet movement and background PoW compute.
---

# Structs Combat

**Important**: Entity IDs containing dashes (like `5-10`, `9-3`) are misinterpreted as flags by the CLI parser. All transaction commands in this skill use `--` before positional arguments to prevent this.

## Safety

See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract. In this skill:

- **`struct-attack`** single-target (Tier 1) — *"Confirm the target ID before firing. The chain will not stop you from attacking a guild-mate."* Surface target ID(s), the weapon system, and the expected counter-attack ambit.
- **`struct-attack`** multi-target across guild boundaries (Tier 2 — act of war) — *"An act of war. The targets' guilds may retaliate as a bloc. Always escalate."*
- **`planet-raid-compute`** (Tier 1 + expedition) — *"A committed expedition. Your fleet locks 'away' while the proof grinds, and the completion transaction submits itself on landing. You cannot build on your planet during this window."* Secure your planet before launching; the auto-submit may invite retaliation. On reconnect, walk the four-state flow in [`awareness/async-operations`](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job) before launching anything new — a raid you forgot about may have completed (or failed) since.
- **`fleet-move`** to scouted destination (Tier 1) / to unscouted hostile space (Tier 2) — *"Instant transit. Verify the destination."*
- **`struct-stealth-activate`** before raids (Tier 0) — routine misdirection; attacking deactivates stealth automatically.

## Procedure

1. **Scout** — `structsd query structs planet [id]`, `structsd query structs struct [id]` for targets, shield, defenses.
2. **Optional stealth** — `structsd tx structs struct-stealth-activate --from [key-name] --gas auto --gas-adjustment 1.5 -- [struct-id]` before attack.
3. **Attack structs** — The CLI will prompt you to confirm. Verify the target IDs, weapon, and (for multi-target) that you are not crossing guild boundaries you did not intend to cross.

   ```
   structsd tx structs struct-attack --from [key-name] --gas auto --gas-adjustment 1.5 -- [operating-struct-id] [target-struct-id,target-id2,...] [weapon-system]
   ```

   Can target multiple structs. Multi-target across guild boundaries is **Tier 2 (act of war)**.

4. **Raid flow** — Raiding is an **expedition** that auto-submits its completion (this is why the compute step keeps `-y`).

   a. Move fleet to target (CLI prompts):

      ```
      structsd tx structs fleet-move --from [key-name] --gas auto --gas-adjustment 1.5 -- [fleet-id] [destination-location-id]
      ```

   b. **Approval Block** before launching raid compute:

      - `fleet-id` is your raiding fleet and it is now at the target planet
      - You accept that the planet you raid from is undefended by fleet for the duration
      - Stored ore at your home planet is refined or below your tolerance for theft
      - You will tolerate the auto-submitted completion landing minutes-to-hours from now even if the situation shifts

   c. Launch compute (auto-submits completion):

      ```
      structsd tx structs planet-raid-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [fleet-id]
      ```

   d. Move fleet home. Refine stolen ore immediately.

5. **Defense setup** — CLI will prompt for each assignment:

   ```
   structsd tx structs struct-defense-set --from [key] --gas auto -- [defender-struct-id] [protected-struct-id]
   structsd tx structs struct-defense-clear --from [key] --gas auto -- [defender-struct-id]
   ```

## Commands Reference

| Action | CLI Command |
|--------|-------------|
| Attack | `structsd tx structs struct-attack -- [operating-struct-id] [target-ids] [weapon-system]` |
| Raid compute (PoW + auto-complete) | `structsd tx structs planet-raid-compute -D 3 -- [fleet-id]` |
| Raid complete (manual, rarely needed) | `structsd tx structs planet-raid-complete -- [fleet-id]` |
| Fleet move | `structsd tx structs fleet-move -- [fleet-id] [destination-location-id]` |
| Set defense | `structsd tx structs struct-defense-set -- [defender-id] [protected-id]` |
| Clear defense | `structsd tx structs struct-defense-clear -- [defender-id]` |
| Stealth on | `structsd tx structs struct-stealth-activate -- [struct-id]` |
| Stealth off | `structsd tx structs struct-stealth-deactivate -- [struct-id]` |
| Move Command Ship (ambit) | `structsd tx structs struct-move -- [struct-id] [new-ambit] [new-slot] [new-location]` |

Raid flow: fleet-move → planet-raid-compute (auto-submits complete) → fleet-move home → refine stolen ore.

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule." `planet-raid-compute` is the documented `-y` exception — it auto-submits completion when no shell is attached, so use the Approval Block above as your gate.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Raid Timing

Fleet movement (`fleet-move`) is instant — no transit time. The only time cost in a raid cycle is the PoW compute.

`planet-raid-compute` uses `-D` flag (range 1-64) to wait until difficulty drops before hashing. Raid PoW difficulty depends on the target planet's properties. Launch raid compute in a background terminal — it may take minutes to hours depending on difficulty. Use `-D 3` for zero wasted CPU. Compute auto-submits the complete transaction.

**Important**: Your fleet is locked "away" during the raid compute. You cannot build on your planet while your fleet is away. Plan accordingly — complete all planet builds before moving fleet for a raid.

## Ambit Targeting

Each weapon can only hit specific ambits. Before attacking, verify your struct's weapon can reach the target's ambit.

| Struct | Lives In | Primary Targets | Secondary Targets |
|--------|----------|-----------------|-------------------|
| Command Ship | Any (movable) | Current ambit only | — |
| Battleship | Space | Space, Land, Water | — |
| Starfighter | Space | Space | Space |
| Frigate | Space | Space, Air | — |
| Pursuit Fighter | Air | Air | — |
| Stealth Bomber | Air | Land, Water | — |
| High Altitude Interceptor | Air | Space, Air | — |
| Mobile Artillery | Land | Land, Water | — |
| Tank | Land | Land | — |
| SAM Launcher | Land | Space, Air | — |
| Cruiser | Water | Land, Water | Air |
| Destroyer | Water | Air, Water | — |
| Submersible | Water | Space, Water | — |

**Command Ship positioning**: The Command Ship is the only struct that can change ambits via `struct-move`. It can only attack structs in its current ambit (ambit flag `32` = "Local"). Move it to the target's ambit before attacking. Move it away from enemy weapon ranges as a defensive tactic.

## Weapon Control vs Defense Type

The interaction between weapon control (guided/unguided) and target defense determines evasion. This is the core of combat tactics:

| Target Defense | vs Guided | vs Unguided |
|----------------|-----------|-------------|
| Signal Jamming (Battleship, Pursuit Fighter, Cruiser) | **66% miss** | Full hit |
| Defensive Maneuver (High Alt Interceptor) | Full hit | **66% miss** |
| Armour (Tank) | Full hit, -1 dmg | Full hit, -1 dmg |
| Stealth Mode (Stealth Bomber, Submersible) | Same-ambit only | Same-ambit only |
| Indirect Combat (Mobile Artillery) | Full hit | Full hit |
| None | Full hit | Full hit |

**Tactics**: Use unguided weapons vs Signal Jamming, guided vs Defensive Maneuver. Armour always reduces by 1.

**Stealth rules**:
- Stealthed structs can still be attacked from the **same ambit** -- stealth only blocks cross-ambit targeting
- Attacking **instantly deactivates** stealth (firing reveals position)
- Re-activation costs 1 charge (`struct-stealth-activate`)

## Strategic Positioning

**Offensive**: Move your Command Ship to the ambit where you want to deal damage. Use cross-ambit attackers (Battleship, Stealth Bomber, SAM Launcher, Submersible) for coverage without repositioning.

**Defensive**: If the enemy fleet can only target specific ambits, move your Command Ship to an ambit they cannot reach. Diversify defenders across ambits so you can block attacks from any direction.

**High-value cross-ambit units**: Battleship (Space→Space/Land/Water), SAM Launcher (Land→Space/Air), Stealth Bomber (Air→Land/Water), Submersible (Water→Space/Water), Cruiser (Water→Land/Water + Air secondary). These structs threaten multiple ambits and are the foundation of flexible fleet composition.

## Verification

- Query planet shield, struct health
- Query fleet location (onStation vs away)
- Stolen ore: refine immediately; verify with struct/player queries
- Attack results include health values (remaining health after attack) -- use to assess damage dealt
- Raid `seized_ore` is tracked on `planet_raid` record -- query to see total ore stolen

## Combat Notes

- Minimum damage after reduction is 1 -- attacks always deal at least 1 damage
- Offline/destroyed structs cannot counter-attack
- Each struct can counter-attack **at most once per `struct-attack` invocation** -- not per target, not per shot
- **Defender counter-attack fires before block**, and fires even on evaded shots
- **Target counter-attack fires after all shots resolve** -- destroyed targets cannot counter
- **Block does NOT fire on evaded shots** -- only counter-attacks happen on evasion
- Evasion is per-target (entire volley evaded), while shot accuracy is per-projectile
- Each projectile gets its own EventAttackShotDetail -- `targetPlayerId` is on EventAttackShotDetail (not EventAttackDetail)
- PDC does not counter-attack -- it only auto-fires after all targets are resolved
- Multiple players' PDCs on the same planet stack correctly
- Target struct existence is validated before attack proceeds
- Hashing for raid-compute is open by default -- any valid proof accepted
- Successful raids seize ALL of the target's storedOre -- one raid takes everything
- Destroyed structs are gone forever but can be replaced by building a new struct of the same type (full PoW required)
- Protect your Command Ship -- losing it disables your entire fleet until a replacement is built

## Combat Readiness Checklist

Before engaging in combat, verify all conditions:

- [ ] **Command Ship online** — `structsd query structs struct [cmd-ship-id]`, status = Online
- [ ] **Fleet on station** (for defense) or **fleet away** (for raids) — `structsd query structs fleet [fleet-id]`
- [ ] **Sufficient charge** — Weapons cost 1-20 charge. At ~6 sec/block, 20 charge = 2 minutes
- [ ] **Power capacity headroom** — Total load must stay below capacity during combat
- [ ] **Defense structs assigned** — PDC, Orbital Shield, defenders set via `struct-defense-set`
- [ ] **Available struct slot** — If building combat structs, check planet slots (0-3 per ambit)
- [ ] **Ore refined or secured** — Unrefined ore is stealable. Refine before engaging in raids that may invite retaliation

## Defense Formations

Assign defenders to protect high-value structs. Defenders absorb incoming attacks before the protected struct takes damage.

**Minimum viable defense**: Assign at least one combat struct per ambit to defend your Command Ship. Command Ship has 6 HP; most fleet structs have 3 HP. Without defenders, a Command Ship can be destroyed in just a few attacks.

**Example formation** (4 Starfighters defending Command Ship — CLI will prompt for each):

```
structsd tx structs struct-defense-set --from [key] --gas auto -- [starfighter-1-id] [command-ship-id]
structsd tx structs struct-defense-set --from [key] --gas auto -- [starfighter-2-id] [command-ship-id]
structsd tx structs struct-defense-set --from [key] --gas auto -- [starfighter-3-id] [command-ship-id]
structsd tx structs struct-defense-set --from [key] --gas auto -- [starfighter-4-id] [command-ship-id]
```

**Rules**:
- Defenders must be in the **same ambit as the target being defended** to block (not the attacker's ambit)
- A struct cannot block for a friendly in a different ambit
- Defenders counter-attack **once per `struct-attack` invocation** (before block, even on evaded shots) -- for multi-shot weapons (Attack Run with 3 projectiles), the defender counters on the first shot only but can attempt to block all 3 shots
- Counter-attacks are ambit-independent from the defended target (a space defender can counter a space attacker while defending a land struct)
- Attacking Signal Jamming targets (Battleship, Pursuit Fighter, Cruiser) with guided weapons is riskier -- you miss AND get countered
- Each defender assignment costs 1 charge -- stagger 6s apart (same account)
- Build defense BEFORE economy or offense -- always
- Defense protects structs from destruction but does **NOT** prevent ore seizure -- the only defense for ore is immediate refining

## Error Handling

- **"insufficient charge"** — Weapon needs charge; check struct state.
- **"target invalid"** — Target may be destroyed, stealthed, or out of range.
- **"unreachable" / "out_of_range"** — Your weapon cannot target that ambit. Check the targeting matrix above and reposition your Command Ship or use a different struct.
- **"fleet not away"** — Raids require fleet away; move fleet first.
- **"proof invalid"** — Re-run raid-compute with correct difficulty.
- **Stolen ore** — Refine immediately; ore is stealable until refined.

## See Also

- [knowledge/mechanics/combat](https://structs.ai/knowledge/mechanics/combat) — Damage, evasion, raids, defense
- [knowledge/mechanics/fleet](https://structs.ai/knowledge/mechanics/fleet) — Fleet movement, on-station rules
- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — Ore vulnerability, Alpha Matter

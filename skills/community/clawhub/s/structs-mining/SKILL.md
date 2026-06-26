---
name: structs-mining
description: Executes resource extraction in Structs. Mines ore and refines it into Alpha Matter. Use when mining ore, refining ore, starting a mine-refine cycle, checking planet ore levels, or managing resource extraction. Mining takes ~17 hours and refining ~34 hours — both are background operations. Ore is stealable until refined.
---

# Structs Mining

**Important**: Entity IDs containing dashes (like `3-1`, `4-5`) are misinterpreted as flags by the CLI parser. All transaction commands in this skill use `--` before positional arguments to prevent this.

## Safety

Mining and refining are **expeditions** — long-running background jobs that auto-submit completion transactions when their proof lands. See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract; in this skill:

- **`struct-ore-mine-compute`** (Tier 1 + expedition) — *"An expedition. The extractor hashes the planet for ~17 hours, then transmits completion back to the chain on its own."* Log the PID to `memory/jobs/`; recall with `kill <pid>` if the situation changes.
- **`struct-ore-refine-compute`** (Tier 1 + expedition) — *"~34 hours of grinding. The completion transaction is deferred consent — re-verify game state when it lands."* If your planet was raided mid-refine, your original approval may be stale.
- **Auto-submission risk** — the compute helper signs and broadcasts the complete transaction automatically. If you cannot guarantee the original consent will still be valid in 17-34 hours, treat the launch as Tier 2 and escalate.
- **Reconnect protocol** — if you resume a session with a mine or refine still listed as "running" in `memory/jobs/`, walk the four-state flow in [`awareness/async-operations`](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job) **before** doing anything else. A "running" PID may have died, succeeded, or failed silently.

## Procedure

1. **Check planet ore** — `structsd query structs planet [id]`. If `currentOre == 0`, explore new planet first.
2. **Initiate mine** — The mine action is implicit in `struct-ore-mine-compute`. Mining is an **expedition**: the compute runs ~17 hours and auto-submits its completion transaction (this is why `-y` is present below — there will be no shell prompt when the proof lands).

   **Approval Block** — confirm before launch:

   - `struct-id` is the Ore Extractor you intend
   - Planet currently shows `currentOre > 0` (worth mining)
   - `--from` key is the struct's owner
   - You will tolerate the auto-submitted completion ~17 hours from now even if game state shifts

   Launch in a background terminal:

   ```
   structsd tx structs struct-ore-mine-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]
   ```

   Mining difficulty is 14,000; expect **~17 hours** for difficulty to drop to D=3. Log the PID to `memory/jobs/`.

3. **Refine immediately after mine completes** — Ore is stealable. Refining is also an **expedition**: ~34 hours, auto-submitted completion.

   **Approval Block** — same five items as mine, applied to refining (~34 hour deferred-consent window).

   ```
   structsd tx structs struct-ore-refine-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]
   ```

   Refining difficulty is 28,000; expect **~34 hours** for D=3.

4. **Store or convert** — Alpha Matter is not stealable. Use reactor (1g = 1 kW) or generator infusion as needed.
5. **Verify** — Query planet (ore decreased), struct (ore/Alpha state), player (resources).

**CRITICAL**: Mining and refining are **multi-hour background operations**. Launch compute in a background terminal and do other things while waiting. Never sit idle watching a hash grind. See [awareness/async-operations](https://structs.ai/awareness/async-operations).

**CRITICAL**: Ore is stealable. Alpha Matter is not. Refine as soon as mining completes — every hour ore sits unrefined is an hour it can be stolen.

## Commands Reference

| Action | CLI Command |
|--------|-------------|
| Mine compute (PoW + auto-complete) | `structsd tx structs struct-ore-mine-compute -D 3 -- [struct-id]` |
| Mine complete (manual, rarely needed) | `structsd tx structs struct-ore-mine-complete -- [struct-id]` |
| Refine compute (PoW + auto-complete) | `structsd tx structs struct-ore-refine-compute -D 3 -- [struct-id]` |
| Refine complete (manual, rarely needed) | `structsd tx structs struct-ore-refine-complete -- [struct-id]` |
| Query planet | `structsd query structs planet [id]` |
| Query struct | `structsd query structs struct [id]` |
| Query player | `structsd query structs player [id]` |

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule." Mine-compute and refine-compute are the documented `-y` exception — they auto-submit completion when no shell is attached, so the Approval Block has to be your gate, not the CLI prompt.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Verification

- Planet `currentOre` decreases after mine-complete
- Struct ore inventory clears after refine-complete
- Player Alpha Matter increases after refine-complete

## Error Handling

- **"struct offline"** — Activate struct before mining.
- **"insufficient ore"** — Planet depleted or struct has no ore; check planet `currentOre`.
- **"proof invalid"** — Re-run compute with correct difficulty; ensure no interruption.
- **Ore stolen** — Refine immediately after every mine. Never leave ore unrefined.

## Timing

Mining and refining have high base difficulties, meaning they take **hours** for difficulty to drop to a feasible level. At D=3, the hash is trivially instant — the wait IS the time, and zero CPU is wasted on hard hashing.

| Operation | Difficulty | D=3 |
|-----------|------------|------|
| Mine | 14,000 | ~17 hr |
| Refine | 28,000 | ~34 hr |
| Full cycle (mine + refine) | -- | ~51 hr |

**Use `-D 3`** for mine/refine. The hash is trivially instant at D=3, wasting zero CPU cycles. Higher `-D` values start sooner but burn significant compute on hard hashes.

**Pipeline strategy**: After initiating a mine, immediately do other things — build structs, scout players, plan defense. When the mine completes, immediately start the refine. While refining runs (~34 hr), you have time to initiate the next mine so its age clock starts ticking. Always keep something aging.

## See Also

- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — Ore, Alpha Matter, conversion rates
- [knowledge/mechanics/planet](https://structs.ai/knowledge/mechanics/planet) — Planet ore, depletion
- [knowledge/lore/alpha-matter](https://structs.ai/knowledge/lore/alpha-matter) — Alpha Matter lore
- [awareness/async-operations](https://structs.ai/awareness/async-operations) — Background PoW, job tracking, pipeline strategy

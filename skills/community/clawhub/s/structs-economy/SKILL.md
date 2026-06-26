---
name: structs-economy
description: Manages economic operations in Structs. Covers reactor staking, energy providers, agreements, allocations, generator infusion, and token transfers. Use when staking Alpha Matter in reactors, creating or managing energy providers, negotiating agreements, allocating energy, infusing generators, transferring tokens, or managing economic infrastructure.
---

# Structs Economy

## Safety

See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract. In this skill:

- **`reactor-infuse`** (Tier 1) — *"Your alpha locks into the reactor. Commission rate is captured permanently at infusion time."* Surface the validator address, the commission, and the ualpha amount.
- **`struct-generator-infuse`** (Tier 2 — irreversible) — *"Annihilation. The matter is gone the moment the proof lands. See structs-building for the full story."*
- **`reactor-defuse`** (Tier 2 — cooldown lock-in) — *"Starts a cooldown clock. Your alpha is neither in the reactor nor in your wallet during the wait. Cannot be canceled cleanly except with `reactor-cancel-defusion`."*
- **`reactor-begin-migration`** (Tier 2) — *"Moves stake between validators. Verify the destination validator address — there is no 'undo migration' command."*
- **`player-send`** to a recipient with prior history (Tier 1) / to a new address (Tier 2) — *"Tokens leaving your address. A typo in the destination is permanent."*
- **`provider-delete`**, **`allocation-delete`** (Tier 2 — cascade) — *"Power stops flowing immediately. Connected substations may go offline; their players may go offline."* See structs-power.

## Procedure

1. **Assess position** — Query player, reactor, provider, agreement state via `structsd query structs player/reactor/provider/agreement [id]`.
2. **Reactor staking** — Stake Alpha Matter: `structsd tx structs reactor-infuse [player-address] [reactor-address] [amount] TX_FLAGS`. The `amount` **must include the denomination**, e.g. `60000000ualpha` (not just `60000000`). This **automatically increases the player's capacity** — no allocation setup needed. The reactor's commission rate determines the split: player receives `power * (1 - commission)`, reactor keeps the rest. Unstake: `reactor-defuse [reactor-id]` (cooldown applies). Cancel cooldown: `reactor-cancel-defusion [reactor-id]`. Migrate: `reactor-begin-migration [player-address] [source-validator-address] [dest-validator-address] [amount]`.
3. **Generator infusion** — `structsd tx structs struct-generator-infuse [struct-id] [amount] TX_FLAGS`. **IRREVERSIBLE** — Alpha cannot be recovered. Higher conversion rates than reactors (2-10x) but generator is vulnerable to raids.
4. **Provider lifecycle** — Create: `provider-create [substation-id] [rate] [access-policy] [provider-penalty] [consumer-penalty] [cap-min] [cap-max] [dur-min] [dur-max] TX_FLAGS`. Valid `access-policy` values: `open-market` (anyone can buy), `guild-market` (guild members with sufficient rank can buy -- managed via guild rank permissions on the provider), `closed-market` (only players with explicit PermProviderOpen on the provider). Update capacity/duration/access via `provider-update-capacity-maximum`, `provider-update-duration-minimum`, etc. Delete: `provider-delete [provider-id]`. Withdraw earnings: `provider-withdraw-balance [provider-id]`. To grant guild members access to a `guild-market` provider: `permission-guild-rank-set [provider-id] [guild-id] 262144 [rank]` (PermProviderOpen).
5. **Agreements** — Open: `agreement-open [provider-id] [duration] [capacity] TX_FLAGS`. Close: `agreement-close [agreement-id]`. Adjust: `agreement-capacity-increase/decrease`, `agreement-duration-increase`.
6. **Allocations** — Create: `allocation-create [source-id] [power] --allocation-type static|dynamic|automated TX_FLAGS`. The `--controller` flag accepts a **PlayerId** (e.g., `1-42`). If omitted, the creating player is the default controller. Update: `allocation-update [allocation-id] [new-power]`. Delete: `allocation-delete [allocation-id]` — only the controlling player can delete an allocation. Transfer: `allocation-transfer [allocation-id] [new-controller]`.

### Allocation Type Comparison

| Type | Updatable | Deletable | Auto-grows | Limit | Use Case |
|------|-----------|-----------|------------|-------|----------|
| `static` | No | No (while connected) | No | Unlimited | Fixed capacity routing |
| `dynamic` | Yes | Yes | No | Unlimited | Flexible, managed routing |
| `automated` | Yes | No | Yes (scales with source capacity) | One per source | Energy commerce (recommended) |
| `provider-agreement` | System-managed | System-managed | System-managed | System-created | Auto-created when agreements open; never create manually |

**Automated allocation limit**: Only one automated allocation per source is allowed. Attempting to create a second from the same source will error. Use `dynamic` type if you need multiple allocations from one source.

**Recommended for energy sales**: Use `automated` allocations. When you infuse more alpha into a reactor, your capacity grows, and automated allocations proportionally increase energy flowing to your substations with no manual intervention.
7. **Token transfer** — `player-send [from-address] [to-address] [amount] TX_FLAGS`.

## Commands Reference

| Action | Command |
|--------|---------|
| Reactor infuse | `structsd tx structs reactor-infuse [player-addr] [validator-addr] [amount]` (validator = `structsvaloper1...`, NOT reactor ID) |
| Reactor defuse | `structsd tx structs reactor-defuse [reactor-id]` |
| Reactor migrate | `structsd tx structs reactor-begin-migration [player-addr] [src-validator-addr] [dest-validator-addr] [amount]` |
| Reactor cancel defusion | `structsd tx structs reactor-cancel-defusion [reactor-id]` |
| Generator infuse | `structsd tx structs struct-generator-infuse [struct-id] [amount]` |
| Provider create | `structsd tx structs provider-create [substation-id] [rate] [access] [prov-penalty] [cons-penalty] [cap-min] [cap-max] [dur-min] [dur-max]` |
| Provider delete | `structsd tx structs provider-delete [provider-id]` |
| Provider withdraw | `structsd tx structs provider-withdraw-balance [provider-id]` |
| Agreement open | `structsd tx structs agreement-open [provider-id] [duration] [capacity]` |
| Agreement close | `structsd tx structs agreement-close [agreement-id]` |
| Allocation create | `structsd tx structs allocation-create [source-id] [power] --allocation-type [type]` |
| Allocation update | `structsd tx structs allocation-update [allocation-id] [power]` |
| Allocation delete | `structsd tx structs allocation-delete [allocation-id]` |
| Player send | `structsd tx structs player-send [from] [to] [amount]` |

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule." Every command in this skill is Tier 1 or Tier 2; default to interactive.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

**Important**: Entity IDs containing dashes (like `3-1`, `4-5`) are misinterpreted as flags by the CLI parser. Always place `--` between flags and positional args: `structsd tx structs command TX_FLAGS -- [entity-id] [other-args]`

## Verification

- **Reactor**: `structsd query structs reactor [id]` — check `infusedAmount`, `defusionCooldown`.
- **Provider**: `structsd query structs provider [id]` — verify capacity, rate, active agreements.
- **Agreement**: `structsd query structs agreement [id]` — check status, capacity, duration.
- **Allocation**: `structsd query structs allocation [id]` — confirm power, source, destination.
- **Player balance**: `structsd query structs player [id]` — verify Alpha Matter after transfers.

## Error Handling

- **Insufficient balance**: Check player Alpha Matter before infuse/send. Refine ore first.
- **Provider capacity exceeded**: Query provider `capacityMaximum`; reduce agreement capacity or create new provider.
- **Defusion cooldown**: Use `reactor-cancel-defusion` to re-stake during cooldown, or wait.
- **Generator infuse failed**: Cannot undo. Verify struct is a generator type and amount is correct before submitting.

## See Also

- [structs-energy skill](https://structs.ai/skills/structs-energy/SKILL) — "I need more energy" decision tree and workflows
- [knowledge/economy/energy-market](https://structs.ai/knowledge/economy/energy-market) — Provider/agreement flow, pricing
- [knowledge/economy/guild-banking](https://structs.ai/knowledge/economy/guild-banking) — Central Bank tokens
- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — Alpha Matter, conversion rates
- [knowledge/mechanics/power](https://structs.ai/knowledge/mechanics/power) — Capacity, load, online status

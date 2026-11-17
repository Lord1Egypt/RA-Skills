---
title: "Commerce skill: energy, banks, transfers"
meta_description: "How Alpha Matter compounds into economic power: providers, energy agreements, reactor staking, the guild Central Bank, and token transfers."
name: structs-commerce
description: Earning and trading in Structs — selling energy via providers, buying capacity via agreements, allocations, reactor staking economics, the guild Central Bank (mint/redeem/convert), and token transfers. Use when you want to monetize surplus energy, shop for an energy agreement, set provider pricing, stake Alpha into a reactor for capacity, mint/redeem/convert guild tokens, or send tokens. For just keeping your own structs powered, see structs-energy.
level: advanced
domain: economy
---

# Commerce skill: energy, banks, transfers

Commerce is how Alpha Matter compounds into economic power. The core loop: refine Alpha → infuse a reactor (capacity) → route it through an **allocation** to a **substation** → sell it through a **provider** → buyers pay in tokens via **agreements** → reinvest. Layered on top are guild Central Bank tokens (mint/redeem) and direct transfers. Where [`structs-energy`](https://structs.ai/skills/structs-energy/SKILL) is "power my own structs", this skill is "make Alpha and energy *earn*."

Conventions (TX_FLAGS, `--` rule, charge bar, one-tx-at-a-time, `ualpha` denom suffix) are in [`conventions.md`](https://structs.ai/skills/conventions). Every command here is Tier 1 or Tier 2 — default to interactive.

## When to use it

- You have surplus capacity and want revenue (run a provider).
- You need capacity but have no Alpha (buy via agreement).
- You're setting provider pricing / access policy.
- You want to stake Alpha into a reactor for capacity, mint/redeem guild tokens, or transfer tokens.

## Decisions

**Sell or hold?** Surplus capacity earns nothing idle. If you have headroom beyond your own structs, sell it. Price in **guild tokens** (`1uguild.0-N`) to create demand for your guild's currency, or in `ualpha` for direct value.

**Buyer-side: shop before you commit.** Opening an agreement **debits the entire cost in full, immediately, at open** — `rate × capacity × duration`, moved into the collateral pool (`x/structs/keeper/msg_server_agreement_open.go`). It is not metered per block. Closing early can incur a penalty. Compare providers on `rateAmount`, `capacityMaximum`, `durationMaximum`, and penalties before opening.

**The `rate_denom` trap.** The cost is charged in the **provider's** `rate_denom`, not in alpha. A provider that prices in a guild token (`uguild.0-N`) requires you to hold that token — a buyer holding only `ualpha` is **rejected at broadcast** (insufficient-funds error keyed `agreement_open`; read `rawLog` for the exact denom). Check the provider's `rateDenom` and acquire that denom (mint guild tokens / trade) *before* opening.

**Reactor staking economics — you are buying *capacity*, not a yield.** Infusing a reactor stakes your Alpha behind a validator at a locked commission and, in return, credits **energy capacity** to you (`1 − commission` of the infused amount; the commission share becomes the reactor's own capacity). There is **no delegator reward stream, no APR, no passive income** — the payoff is the capacity itself. Income is *indirect*: you turn that capacity into revenue only by selling it as energy through a provider. Lower commission = more capacity to you; staking also strengthens the guild's reactor. It's reversible only via a defusion cooldown — don't stake Alpha you'll need short-term. A jailed validator zeros the infusion ratio until unjail / `reactor-restart`. See [energy — reactor infusion](https://structs.ai/knowledge/mechanics/energy) for the 96/4 split.

**The energy flywheel (advanced default):** mine → refine → infuse guild reactor → automated allocation grows substation capacity → sell via provider for guild tokens → redeem/reinvest. Each turn compounds. Decisions live in [`knowledge/economy/valuation`](https://structs.ai/knowledge/economy/valuation), [`trading`](https://structs.ai/knowledge/economy/trading), and [`playbooks/phases/late-game`](https://structs.ai/playbooks/phases/late-game).

## Allocation types (the routing primitive)

| Type | Updatable | Deletable | Auto-grows | Limit | Use |
|------|-----------|-----------|------------|-------|-----|
| static | no | no (while connected) | no | unlimited | fixed routing |
| dynamic | yes | yes | no | unlimited | flexible/managed routing |
| automated | yes | no | yes (with source capacity) | **one per source** | energy sales (recommended) |
| provider-agreement | system | system | system | system-created | auto-made when agreements open — never create manually |

Only the **controlling** player can delete/transfer an allocation (`--controller [player-id]`, defaults to creator).

## Procedure — sell energy (provider pipeline)

1. **Have capacity** — infuse a reactor first ([`structs-energy`](https://structs.ai/skills/structs-energy/SKILL)).
2. **Automated allocation** (auto-grows as you infuse more):
   ```
   structsd tx structs allocation-create --allocation-type automated TX_FLAGS -- [your-player-id] [power]
   ```
3. **Substation** (distribution node):
   ```
   structsd tx structs substation-create TX_FLAGS -- [your-player-id] [allocation-id]
   ```
4. **Provider** (your storefront):
   ```
   structsd tx structs provider-create TX_FLAGS -- [substation-id] [rate] [access-policy] [provider-penalty] [consumer-penalty] [cap-min] [cap-max] [dur-min] [dur-max]
   ```
   Pricing/policy heuristics: `rate` `1uguild.0-N` (drives guild-token demand) or a `ualpha` rate; `access-policy` `open-market` (max reach), `guild-market` (members at/above a rank — grant via `permission-guild-rank-set [provider-id] [guild-id] 262144 [rank]`), or `closed-market` (explicit PermProviderOpen only); penalties `0` initially to lower friction; cap/dur ranges wide (e.g. `1000`–`1000000000` / `100`–`1000000`).
5. **Monitor & withdraw**: `structsd query structs provider [id]`; `provider-withdraw-balance TX_FLAGS -- [provider-id] [destination-address]`. Earnings drip from the provider's collateral (escrow) to its earnings address as blocks pass.

## Procedure — buy energy (agreement)

1. Find a provider: `structsd query structs provider-all` (or your guild's). Compare rate/capacity/duration/penalties.
2. Open (paid upfront; auto-creates a provider-agreement allocation):
   ```
   structsd tx structs agreement-open TX_FLAGS -- [provider-id] [duration-in-blocks] [capacity]
   ```
3. Connect the allocation to your substation:
   ```
   structsd tx structs substation-allocation-connect TX_FLAGS -- [substation-id] [allocation-id]
   ```
4. Adjust as needed: `agreement-capacity-increase|decrease`, `agreement-duration-increase`; `agreement-close [agreement-id]` (may penalize).

## Procedure — reactor staking

```
structsd tx structs reactor-infuse [your-address] [validator-address] [amount]ualpha TX_FLAGS
```
Validator address is `structsvaloper1...` (from `structsd query structs reactor [id]`, `validator` field) — not the reactor ID. Commission locks at infusion. Unstake: `reactor-defuse [your-address] [validator-address] [amount]ualpha` (cooldown); `reactor-cancel-defusion [your-address] [validator-address] [amount]ualpha [creation-height]` to re-stake during cooldown; `reactor-begin-migration [player-addr] [src-val] [dest-val] [amount]ualpha` to move stake (verify the destination — no undo). After an unjail, `reactor-restart [reactor-address]` resyncs energy output from live staking if hooks did not.

## Procedure — guild Central Bank & transfers

- **Mint** (guild-privileged) / **redeem** (`floor` payout plus `min-amount-alpha`) / **convert** ualpha→token or token→token — see [`structs-guild`](https://structs.ai/skills/structs-guild/SKILL) and [`knowledge/economy/guild-banking`](https://structs.ai/knowledge/economy/guild-banking). Convert needs `min-amount-token` slippage. `uguild.*` cannot go to IBC.
- **Transfer tokens**: `player-send [from-address] [to-address] [amount] TX_FLAGS`. A typo in the destination is permanent — to a brand-new address this is Tier 2. Guild denoms additionally require an eligible recipient.

## Commands reference

| Action | Command |
|--------|---------|
| Allocation create / update / delete / transfer | `structsd tx structs allocation-create --allocation-type [t] TX_FLAGS -- [source-id] [power]` (+ `allocation-update`/`allocation-delete`/`allocation-transfer`) |
| Substation create | `structsd tx structs substation-create TX_FLAGS -- [owner-id] [allocation-id]` |
| Provider create / delete / withdraw | `structsd tx structs provider-create \| provider-delete \| provider-withdraw-balance TX_FLAGS -- ...` |
| Agreement open / close / adjust | `structsd tx structs agreement-open \| agreement-close \| agreement-capacity-increase \| ... TX_FLAGS -- ...` |
| Reactor infuse / defuse / migrate / restart | `structsd tx structs reactor-infuse \| reactor-defuse \| reactor-begin-migration \| reactor-restart TX_FLAGS -- ...` |
| Bank convert / convert-token | `structsd tx structs guild-bank-convert TX_FLAGS -- [guild-id] [alpha-amount] [min-amount-token]` / `guild-bank-convert-token TX_FLAGS -- [amount]uguild.[src] [target-guild-id] [min-amount-token]` |
| Token transfer | `structsd tx structs player-send [from] [to] [amount] TX_FLAGS` |
| Query provider / agreement / reactor | `structsd query structs provider \| agreement \| reactor [id]` |

`TX_FLAGS` per [`conventions.md`](https://structs.ai/skills/conventions). **Requires** [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a signing key.

## Verification

- Provider: `structsd query structs provider [id]` — capacity, rate, active agreements, balance.
- Agreement: `structsd query structs agreement [id]` — status (OPEN→ACTIVE→EXPIRED), capacity, duration.
- Reactor: `structsd query structs reactor [id]` — infused amount, defusion cooldown.
- Player: `structsd query structs player [id]` — balance after transfers/withdrawals.

## Errors

- **Insufficient balance** — refine ore / acquire tokens before infuse/send.
- **Provider capacity exceeded** — reduce agreement capacity or add provider capacity.
- **Defusion cooldown** — `reactor-cancel-defusion` to re-stake, or wait it out.
- **recipient_not_eligible** — `uguild.*` cannot go to IBC escrow or an unregistered address.
- **Automated allocation limit** — one per source; use dynamic for additional routing.
- **Generator infuse / staking irreversibility** — staking has a cooldown; generator infusion has none (see [`structs-energy`](https://structs.ai/skills/structs-energy/SKILL)).

## See also

- [knowledge/economy/energy-market](https://structs.ai/knowledge/economy/energy-market) — provider/agreement flow, pricing
- [knowledge/economy/guild-banking](https://structs.ai/knowledge/economy/guild-banking) — Central Bank tokens, collateral
- [knowledge/economy/valuation](https://structs.ai/knowledge/economy/valuation) / [trading](https://structs.ai/knowledge/economy/trading) — what things are worth
- [playbooks/phases/late-game](https://structs.ai/playbooks/phases/late-game) — market control
- [structs-energy](https://structs.ai/skills/structs-energy/SKILL) — capacity for your own use; [structs-permissions](https://structs.ai/skills/structs-permissions/SKILL) — provider access grants

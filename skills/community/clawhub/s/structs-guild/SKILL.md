---
title: "Guild skill: join, ranks, Central Bank"
meta_description: A guild gives you a reactor, a substation, a market, a token, and allies. Choosing one, joining, ranks, membership, and UGC moderation.
name: structs-guild
description: Guilds in Structs — choosing and joining one, ranks and rank-permissions, membership flows, settings, UGC moderation, charter vs entitlement founding, and the Central Bank (mint/redeem/convert). Use when picking a guild to join, creating a guild, managing members or ranks, moderating member identity, or running guild token operations.
level: core
domain: social
---

# Guild skill: join, ranks, Central Bank

A guild is your faction: it gives you a reactor to infuse, a substation to draw power from, a market to sell into, a token to mint, and allies (or moderators). For a new player, **which guild you join is one of your most consequential early choices** — it shapes your power source, your economy, and who has your back. This skill covers choosing/joining, running a guild, ranks/permissions, identity moderation, and the Central Bank.

Conventions (TX_FLAGS, `--` rule, charge bar, one-tx-at-a-time) are in [`conventions.md`](https://structs.ai/skills/conventions).

## When to use it

- New player deciding which guild to join (or whether to go solo).
- Creating or administering a guild.
- Managing members, ranks, or moderating member identity.
- Minting/redeeming guild tokens or managing Central Bank collateral.

## Decisions

**Choosing a guild (beginner)** — evaluate candidates on:
- **Reactor commission** — lower = more capacity per gram you infuse (`structsd query structs reactor [id]`).
- **Join requirements** — `joinInfusionMinimum` you must meet (or get an invite to bypass).
- **Activity & size** — `guild-all` then inspect members; an active guild means a working market and defenders.
- **Token economy** — a guild whose token is actually used (providers priced in it) makes your earnings liquid.
- **Politics** — see [`knowledge/lore/factions`](https://structs.ai/knowledge/lore/factions) and your standing-orders. Joining a guild at war inherits its enemies.

A guild is rarely a trap, but its moderators gain reach into your name/pfp while you're a member (see UGC below). If you dislike a policy, you can leave.

**Creating a guild (advanced)** is either the **chain-global charter PoW** (`guild-create-compute`, weeks for a lone miner) or a **one-time reactor entitlement** (`guild-create` without proof: bonded validator past ~30 days, `PermReactorGuildCreate` on the reactor). A founder who **owns** a guild must transfer it first. Founding leaves your current guild if you are only a member. Third-party solvers need `guild-charter-consent`. See [hashing.md — Guild Charter](https://structs.ai/knowledge/mechanics/hashing#guild-charter).

## Rank system

Numeric ranks, **lower number = higher privilege**:

| Rank | Meaning |
|------|---------|
| 1 | Maximum (guild creator) |
| 2–100 | Custom ranks assigned by leadership |
| 101 | Default on join |
| 0 | Unset |

A player can only modify members whose rank is strictly **worse** (higher number) than their own. Rank-permissions (granting a permission to everyone at/above a rank) are the scalable way to delegate — see [`structs-permissions`](https://structs.ai/skills/structs-permissions/SKILL).

## Procedure

### Join

1. Discover: `structsd query structs guild-all`, then `guild [id]` and `reactor [id]` for the candidates.
2. Meet the infusion minimum (or secure an invite). Join:
   ```
   structsd tx structs guild-membership-join TX_FLAGS -- [guild-id] [infusion-id,...]
   ```
   You get the default entry rank (101). Flows: **invite** (`guild-membership-invite` → invitee `...-invite-approve`/`-deny`), **request** (`guild-membership-request` → owner `...-request-approve`/`-deny`), **proxy** (a guild signs you in: `guild-membership-join-proxy -- [address] [proof-pubkey] [proof-signature]`, with optional `--substation-id`, `--player-name`, `--player-pfp`, `--player-pfp-client-render-attributes`).

### Administer

- **Ranks**: `player-update-guild-rank TX_FLAGS -- [player-id] [rank]` (needs PermAdmin or rank authority); `guild-update-entry-rank TX_FLAGS -- [rank]` (new rank ≥ your own).
- **Membership**: `guild-membership-kick -- [player-id]` (the guild is implicit in the target player); invite/request approve/deny/revoke as above.
- **Settings**: `guild-update-endpoint`, `guild-update-entry-substation-id`, `guild-update-join-infusion-minimum` (+ `-by-invite`/`-by-request`; unknown bypass-level values are denied), `guild-update-owner-id` (Tier 2 — transfers the guild). Invite/request **approve** and **accept** require a pending application — they do not create one.
- **Founding**: entitlement `guild-create -- [reactor-id] [endpoint] [entry-substation-id]` or charter `guild-create-compute -D 3` (query `guild-charter` first). Third-party solver: `guild-charter-consent` then proof-path create.

### UGC moderation

Structs has no global moderator — each guild sets its own name/pfp standards for member-owned objects, and the chain emits an audit event on every override. Grant moderation by rank (recommended) or per player:

```bash
# Members at rank 5 or better can moderate guild-mate UGC
structsd tx structs permission-guild-rank-set TX_FLAGS -- [guild-id] [guild-id] 16777216 5
# Or a single moderator on the guild object
structsd tx structs permission-grant-on-object TX_FLAGS -- [guild-id] [moderator-player-id] 16777216
```

Perform a moderation: `player-update-name`/`player-update-pfp`/`planet-update-name`/`substation-update-name`/`substation-update-pfp TX_FLAGS -- [target-id] "value"`. When the actor isn't the owner, the chain emits `ugc_moderated` (actor, target, field, old/new) — audit it. Note `pfpClientRenderAttributes` is **owner-only** and **not** guild-moderatable. Full philosophy + validation: [`knowledge/mechanics/ugc-moderation`](https://structs.ai/knowledge/mechanics/ugc-moderation).

### Central Bank (mint / redeem / convert)

- **Mint** tokens against Alpha collateral: `guild-bank-mint TX_FLAGS -- [alpha-amount] [token-amount]` (signer's guild implicit; raw integers; ratio captured at action time). Guild-privileged.
- **Redeem** tokens for Alpha: `guild-bank-redeem TX_FLAGS -- [amount]uguild.[guild-id] [min-amount-alpha]` — coin string plus Alpha slippage floor. Payout is `floor(amount * collateral / supply)` but still rejected if that payout is below `min-amount-alpha`.
- **Convert** ualpha into an existing guild token at the live collateral ratio: `guild-bank-convert TX_FLAGS -- [guild-id] [alpha-amount] [min-amount-token]`. Needs `PermTokenTransfer` on the signer. Convert-in fee stays in collateral. `min-amount-token` is the slippage floor.
- **Convert token → token**: `guild-bank-convert-token TX_FLAGS -- [amount]uguild.[source-id] [target-guild-id] [min-amount-token]` — redeems the source then converts into the target in one tx; both guilds keep their fees.
- **Confiscate & burn** (Tier 2 act of war, audited forever): `guild-bank-confiscate-and-burn TX_FLAGS -- [amount]uguild.[guild-id] [address]` — token amount first, then the address it is taken from. The destination of a `uguild.*` send must be a registered player, the structs module, or an indexed provider pool — **not IBC**.

Mint/redeem are Tier 1 within your standing-order caps, Tier 2 above. Convert is the open market path. Economics: [`knowledge/economy/guild-banking`](https://structs.ai/knowledge/economy/guild-banking).

## Commands reference

| Action | Command |
|--------|---------|
| Create (entitlement) | `structsd tx structs guild-create TX_FLAGS -- [reactor-id] [endpoint] [entry-substation-id]` |
| Create (charter PoW) | `structsd tx structs guild-create-compute -D 3 TX_FLAGS_APPROVED -- [reactor-id]` |
| Charter query / consent | `structsd query structs guild-charter` / `structsd tx structs guild-charter-consent TX_FLAGS -- [reactor-id]` (offline signature; not broadcast) |
| Join / proxy | `structsd tx structs guild-membership-join \| guild-membership-join-proxy TX_FLAGS -- ...` |
| Invite / request (+approve/deny/revoke) | `structsd tx structs guild-membership-invite \| -request \| ...-approve \| ...-deny TX_FLAGS -- ...` |
| Kick | `structsd tx structs guild-membership-kick TX_FLAGS -- [player-id]` |
| Update rank / entry rank | `structsd tx structs player-update-guild-rank \| guild-update-entry-rank TX_FLAGS -- ...` |
| Settings | `structsd tx structs guild-update-endpoint \| -entry-substation-id \| -join-infusion-minimum \| -owner-id TX_FLAGS -- ...` |
| Guild UGC | `structsd tx structs guild-update-name \| guild-update-pfp TX_FLAGS -- [guild-id] [value]` |
| Moderate member/object | `structsd tx structs player-update-name \| ...-pfp \| planet-update-name \| substation-update-name \| -pfp TX_FLAGS -- [target-id] [value]` |
| Bank mint / redeem / convert / confiscate | `structsd tx structs guild-bank-mint \| guild-bank-redeem \| guild-bank-convert \| guild-bank-convert-token \| guild-bank-confiscate-and-burn TX_FLAGS -- ...` |
| Guild rank permission set/revoke | `structsd tx structs permission-guild-rank-set \| permission-guild-rank-revoke TX_FLAGS -- [object-id] [guild-id] [permission] [rank]` |

`TX_FLAGS` per [`conventions.md`](https://structs.ai/skills/conventions). **Requires** [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a signing key.

## Verification

- `structsd query structs guild [id]` — members, settings, owner.
- `structsd query structs guild-charter` — global charter anchor and difficulty.
- `guild-membership-application-all` — pending invites/requests.
- `guild-bank-collateral-address [guild-id]` — reserves.
- `guild-rank-permission-by-object-and-guild [object-id] [guild-id]` — rank-based access.

## Errors

- **Insufficient infusion** — meet `joinInfusionMinimum` or get an invite (bypasses it).
- **is_owner** — you own a guild; transfer it before founding another.
- **under_raid** — not a guild error; see production.
- **Already member** — founding leaves your current guild if you are only a member; you cannot join twice.
- **Invite/request approve with no pending application** — membership approval requires an existing application.
- **Mint/redeem/convert failed** — insufficient Alpha/tokens, or `min-amount-token` slippage missed.
- **recipient_not_eligible** — `uguild.*` cannot go to IBC escrow or an unregistered address.
- **Permission denied / rank too low** — need PermAdmin or strictly-better rank; entry rank can't exceed your own.

## See also

- [knowledge/economy/guild-banking](https://structs.ai/knowledge/economy/guild-banking) — Central Bank, collateral, token lifecycle
- [knowledge/mechanics/permissions](https://structs.ai/knowledge/mechanics/permissions) — 25-bit values, guild rank permissions
- [knowledge/mechanics/ugc-moderation](https://structs.ai/knowledge/mechanics/ugc-moderation) — name/pfp moderation & validation
- [knowledge/lore/factions](https://structs.ai/knowledge/lore/factions) — guild politics
- [playbooks/situations/guild-war](https://structs.ai/playbooks/situations/guild-war) — coordinated conflict; [structs-permissions](https://structs.ai/skills/structs-permissions/SKILL) — delegating authority

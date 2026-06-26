---
name: structs-guild
description: Manages guild operations in Structs. Covers creation, membership, settings, and Central Bank token operations. Use when creating a guild, joining or leaving a guild, managing guild settings, minting or redeeming guild tokens, managing Central Bank collateral, or coordinating guild membership.
---

# Structs Guild

**Important**: Entity IDs containing dashes (like `3-1`, `4-5`) are misinterpreted as flags by the CLI parser. All transaction commands in this skill use `--` before positional arguments to prevent this.

## Safety

Guild operations affect token balances, member identities, and on-chain audit records. See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract; in this skill:

- **`guild-bank-mint`** / **`guild-bank-redeem`** (Tier 1 within standing-order caps, Tier 2 above) — *"You move alpha into and out of the central bank's collateral. The mint/redeem ratio is captured at action time."* Surface alpha amount, token amount, and the resulting collateral ratio.
- **`guild-bank-confiscate-and-burn`** (Tier 2 — act of war) — *"The chain audits the burn forever. This is rarely the right tool; usually rank revocation is enough."*
- **`permission-guild-rank-set`** (Tier 2 when granting broad bits: 16777216 PermGuildUGCUpdate, 524288 PermReactorGuildCreate, 262144 PermProviderAgreementCreate, or any wide rank range) — *"Grants the permission to every member at-or-above the rank. Breadth is the risk."*
- **`player-update-name`** / **`player-update-pfp`** / **`planet-update-name`** / **`substation-update-name`** when target is not your own (Tier 1, audited) — *"Writes a `ugc_moderated` event with you as actor. Permanent record."*
- **`guild-update-owner-id`** (Tier 2 — identity) — *"Transfers ownership of the guild. Verify the new owner's player ID."*
- **`guild-membership-kick`** (Tier 1) — *"The kicked player loses guild rank and any rank-based permissions."*

## Guild Rank System

Guilds use a numeric rank system to determine authority. Lower number = higher privilege.

| Rank | Meaning |
|------|---------|
| 1 | Maximum privilege (guild creator) |
| 2–100 | Custom ranks assigned by leadership |
| 101 | Default rank assigned on join |
| 0 | Unset / no rank |

Rank-based authority: a player can only modify members whose rank is strictly worse (higher number) than their own. The guild creator (rank 1) can manage everyone.

## Procedure

1. **Discover guilds** — `structsd query structs guild-all` or `structsd query structs guild [id]`.
2. **Create guild** — Requires PermReactorGuildCreate (524288) on the reactor and PermSubstationConnection (1024) on the entry substation. `structsd tx structs guild-create TX_FLAGS -- [reactor-id] [endpoint] [entry-substation-id]`.
3. **Membership** — Join: `structsd tx structs guild-membership-join -- [guild-id] [infusion-id,infusion-id2,...]` (use `--player-id`, `--substation-id` if needed). New members receive default guild rank (101). Proxy join (a guild signs the new player in): `structsd tx structs guild-membership-join-proxy -- [address] [proof-pubkey] [proof-signature]` with optional flags `--substation-id`, `--player-name`, `--player-pfp` to seed the new player's UGC fields directly on chain. Invite flow: `structsd tx structs guild-membership-invite -- [guild-id] [player-id]` → invitee runs `structsd tx structs guild-membership-invite-approve -- [guild-id]` or `structsd tx structs guild-membership-invite-deny -- [guild-id]`. Request flow: `structsd tx structs guild-membership-request -- [guild-id]` → owner runs `structsd tx structs guild-membership-request-approve -- [guild-id] [player-id]` or `structsd tx structs guild-membership-request-deny -- [guild-id] [player-id]`. Kick: `structsd tx structs guild-membership-kick -- [guild-id] [player-id]`.
4. **Rank management** — Update a member's rank: `structsd tx structs player-update-guild-rank TX_FLAGS -- [player-id] [guild-rank]`. Requires PermAdmin (2) on guild, or rank-based authority (actor rank strictly better than target's current rank). Update entry rank (rank assigned to new joiners): `structsd tx structs guild-update-entry-rank TX_FLAGS -- [new-entry-rank]`. Requires PermUpdate (4) on guild; new rank must be >= caller's own rank.
5. **Settings** — See Commands Reference: `guild-update-endpoint`, `guild-update-entry-substation-id`, `guild-update-join-infusion-minimum` (and `-minimum-by-invite`, `-minimum-by-request`), `guild-update-owner-id`. All use `--` before positional args.
6. **Identity (UGC)** — Update guild name: `structsd tx structs guild-update-name TX_FLAGS -- [guild-id] [name]`. Update guild pfp: `structsd tx structs guild-update-pfp TX_FLAGS -- [guild-id] [pfp]`. Both require `PermUpdate` (4) on the guild; the guild's name and pfp are first-class on-chain UGC fields, not metadata stored elsewhere. See `Decentralized Moderation` below.
7. **Central Bank** — Mint: `structsd tx structs guild-bank-mint TX_FLAGS -- [alpha-amount] [token-amount]` (no guild-id — signer's guild is used implicitly; both amounts are raw integers). Redeem: `structsd tx structs guild-bank-redeem -- [guild-id] [amount]`. Confiscate and burn: `structsd tx structs guild-bank-confiscate-and-burn -- [guild-id] [address] [amount]`.

## Decentralized Moderation

Structs has no global moderator. Each guild is responsible for setting and enforcing its own standards for the names and profile pictures of its members and the guild-owned objects (planets, substations) under its umbrella. The chain provides the tooling, not the policy.

**Why this matters**: Different communities want different things — a competitive PvP guild may tolerate edgy in-character names; a family-friendly mining co-op may require strict, descriptive names; a chaos-RP guild may prefer to leave names totally untouched. The chain ships permission bits and transactions that let each guild encode whichever policy it wants, and emits an auditable event whenever a moderator overrides a member's chosen identity. See [knowledge/mechanics/ugc-moderation](https://structs.ai/knowledge/mechanics/ugc-moderation) for the full philosophy and the strict per-field validation rules every name/pfp must satisfy on chain.

### Granting moderation power

Two patterns are supported:

- **Per-rank moderation** (recommended): grant `PermGuildUGCUpdate` (16777216) on the guild itself to a guild rank. Any member at or better than that rank can then rewrite the name/pfp of any object owned by a guild-mate.

```bash
# Members at rank 5 or better can moderate guild-mate UGC
structsd tx structs permission-guild-rank-set TX_FLAGS -- [guild-id] [guild-id] 16777216 5
```

- **Per-player moderation**: grant `PermGuildUGCUpdate` to a single player on the guild object via `permission-grant-on-object`.

```bash
structsd tx structs permission-grant-on-object TX_FLAGS -- [guild-id] [moderator-player-id] 16777216
```

### Performing a moderation action

```bash
# Rename a member
structsd tx structs player-update-name TX_FLAGS -- [target-player-id] "NewSafeName"

# Replace a member's pfp
structsd tx structs player-update-pfp TX_FLAGS -- [target-player-id] "ipfs://<cid>"

# Rename a guild-owned planet or substation
structsd tx structs planet-update-name TX_FLAGS -- [planet-id] "NewPlanetName"
structsd tx structs substation-update-name TX_FLAGS -- [substation-id] "NewSubName"
structsd tx structs substation-update-pfp TX_FLAGS -- [substation-id] "https://..."
```

When the moderator is not the target object's owner, the chain emits a `ugc_moderated` event with the actor, target, field (`name` or `pfp`), and old/new values. Use these events to audit moderator activity within the guild. See [knowledge/mechanics/ugc-moderation](https://structs.ai/knowledge/mechanics/ugc-moderation) for the event schema and validation rules.

## Provider Access Control via Guild Rank

To restrict a provider to members of a specific guild at a minimum rank, use guild rank permissions instead of direct player grants:

```
structsd tx structs permission-guild-rank-set --from [key] --gas auto -- [provider-id] [guild-id] 262144 [rank]
```

This grants PermProviderAgreementCreate (262144) on the provider to any member of the specified guild at or above the given rank. To revoke:

```
structsd tx structs permission-guild-rank-revoke --from [key] --gas auto -- [provider-id] [guild-id] 262144
```

## Commands Reference

| Action | Command |
|--------|---------|
| Create | `structsd tx structs guild-create -- [reactor-id] [endpoint] [entry-substation-id]` |
| Join | `structsd tx structs guild-membership-join -- [guild-id] [infusion-ids]` |
| Join proxy | `structsd tx structs guild-membership-join-proxy [--substation-id sub] [--player-name name] [--player-pfp pfp] -- [address] [proof-pubkey] [proof-signature]` |
| Invite | `structsd tx structs guild-membership-invite -- [guild-id] [player-id]` |
| Invite approve/deny | `structsd tx structs guild-membership-invite-approve/deny -- [guild-id]` |
| Invite revoke | `structsd tx structs guild-membership-invite-revoke -- [guild-id] [player-id]` |
| Request | `structsd tx structs guild-membership-request -- [guild-id]` |
| Request approve/deny | `structsd tx structs guild-membership-request-approve/deny -- [guild-id] [player-id]` |
| Request revoke | `structsd tx structs guild-membership-request-revoke -- [guild-id]` |
| Kick | `structsd tx structs guild-membership-kick -- [guild-id] [player-id]` |
| Update guild rank | `structsd tx structs player-update-guild-rank -- [player-id] [guild-rank]` |
| Update entry rank | `structsd tx structs guild-update-entry-rank -- [new-entry-rank]` |
| Update endpoint | `structsd tx structs guild-update-endpoint -- [guild-id] [endpoint]` |
| Update entry substation | `structsd tx structs guild-update-entry-substation-id -- [guild-id] [substation-id]` |
| Update infusion minimums | `structsd tx structs guild-update-join-infusion-minimum/minimum-by-invite/minimum-by-request -- [guild-id] [value]` |
| Update owner | `structsd tx structs guild-update-owner-id -- [guild-id] [new-owner-player-id]` |
| Update guild name (UGC) | `structsd tx structs guild-update-name -- [guild-id] [name]` |
| Update guild pfp (UGC) | `structsd tx structs guild-update-pfp -- [guild-id] [pfp]` |
| Moderate player name | `structsd tx structs player-update-name -- [player-id] [name]` |
| Moderate player pfp | `structsd tx structs player-update-pfp -- [player-id] [pfp]` |
| Moderate planet name | `structsd tx structs planet-update-name -- [planet-id] [name]` |
| Moderate substation name | `structsd tx structs substation-update-name -- [substation-id] [name]` |
| Moderate substation pfp | `structsd tx structs substation-update-pfp -- [substation-id] [pfp]` |
| Bank mint | `structsd tx structs guild-bank-mint -- [alpha-amount] [token-amount]` (signer's guild, raw integers) |
| Bank redeem | `structsd tx structs guild-bank-redeem -- [guild-id] [amount]` |
| Bank confiscate | `structsd tx structs guild-bank-confiscate-and-burn -- [guild-id] [address] [amount]` |
| Set guild rank permission | `structsd tx structs permission-guild-rank-set -- [object-id] [guild-id] [permission] [rank]` |
| Revoke guild rank permission | `structsd tx structs permission-guild-rank-revoke -- [object-id] [guild-id] [permission]` |

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule."

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

## Verification

- **Guild**: `structsd query structs guild [id]` — members, settings, owner.
- **Membership applications**: `structsd query structs guild-membership-application-all` or by ID.
- **Bank collateral**: `structsd query structs guild-bank-collateral-address [guild-id]` — verify reserves.
- **Guild rank permissions**: `structsd query structs guild-rank-permission-by-object-and-guild [object-id] [guild-id]` — verify rank-based access.

## Error Handling

- **Insufficient infusion**: Guild may require minimum infusion to join. Query guild for `joinInfusionMinimum`; meet requirement or get invite (bypass).
- **Already member**: Cannot join twice. Check `guild-membership-application` status.
- **Mint/redeem failed**: Verify guild has sufficient Alpha Matter collateral for mint; sufficient tokens for redeem.
- **Permission denied**: Only guild owner (or delegated address) can update settings, approve requests, mint/redeem. Rank-based operations require actor rank strictly better than target.
- **Rank too low**: `guild-update-entry-rank` requires new rank >= caller's own rank. Cannot set entry rank higher than your own authority.

## See Also

- [knowledge/economy/guild-banking](https://structs.ai/knowledge/economy/guild-banking) — Central Bank, collateral, token lifecycle
- [knowledge/economy/energy-market](https://structs.ai/knowledge/economy/energy-market) — Provider guild access
- [knowledge/mechanics/permissions](https://structs.ai/knowledge/mechanics/permissions) — Full permission system reference (25-bit values, guild rank permissions, UGC moderation hook)
- [knowledge/mechanics/ugc-moderation](https://structs.ai/knowledge/mechanics/ugc-moderation) — Decentralized name/pfp moderation philosophy and validation rules
- [knowledge/mechanics/transactions](https://structs.ai/knowledge/mechanics/transactions) — Free vs paid messages, ante handler routing
- [knowledge/lore/factions](https://structs.ai/knowledge/lore/factions) — Guild politics

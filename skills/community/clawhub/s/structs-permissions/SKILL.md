---
title: "Permissions skill: bits, keys, delegates"
meta_description: "Permissions are identity and authority: the 25-bit bitmask per grantee, address registration, and delegation recipes for multi-agent play."
name: structs-permissions
description: Permissions, address management, and delegation in Structs. Use when granting/revoking permissions on objects or addresses, registering additional signing keys, managing multi-address accounts, or setting up minimum-permission delegate agents (mining bot, defense watcher, co-pilot). Covers the full 25-bit permission model and delegation recipes for multi-agent play.
level: advanced
domain: social
---

# Structs Permissions

Permissions *are* identity and authority in Structs. Every object (player, guild, reactor, provider, substation, struct) has a 25-bit permission bitmask per grantee, and addresses can be attached to a player so multiple keys act on its behalf. This is the foundation of **delegation** — running a focused worker agent that can mine but not spend, or a watcher that can read but not act. Granted breadth is the risk: a wide grant to an adversarial key is unrecoverable.

Conventions (TX_FLAGS, `--` rule, one-tx-at-a-time) are in [`conventions.md`](https://structs.ai/skills/conventions). Every transaction here is Tier 1 or Tier 2 — default to interactive, and **prefer minimum-necessary bits**.

## When to use it

- Delegating a task to another key/agent (multi-agent play).
- Granting a guild-mate or service access to a reactor/provider/substation.
- Registering or rotating signing keys for one player.
- Locking down or auditing who can do what.

## Decisions

**Grant the minimum, not PermAll.** Compose exactly the bits a task needs (they OR together). `PermAll` (33554431) yields total control and there is no undo if the holder turns. Reserve it for keys you fully control.

**Object grant vs address grant vs guild-rank grant**:
- **On object** — give a specific player rights on one object (e.g. let an ally infuse your reactor).
- **On address** — attach rights to a signing key directly.
- **Guild rank** — give everyone at/above a rank a permission on an object (scales delegation across a guild; see [`structs-guild`](https://structs.ai/skills/structs-guild/SKILL)).

**Address registration is an attack surface.** `address-register` attaches a new signing key using attacker-suppliable proof material — if you register a key you don't control, you've hired your attacker. Verify proof provenance; see [`awareness/agent-security`](https://structs.ai/awareness/agent-security).

## The 25-bit permission model

| Permission | Value | Description |
|------------|-------|-------------|
| PermPlay | 1 | Basic play access |
| PermAdmin | 2 | Manage permissions on the object |
| PermUpdate | 4 | Update object settings (also self-service UGC name/pfp) |
| PermDelete | 8 | Delete object |
| PermTokenTransfer | 16 | Transfer tokens |
| PermTokenInfuse | 32 | Infuse tokens into reactors/generators |
| PermTokenMigrate | 64 | Migrate tokens between objects |
| PermTokenDefuse | 128 | Defuse (withdraw) tokens |
| PermAssetPlay | 256 | Operate assets |
| PermGuildMembership | 512 | Manage guild membership |
| PermSubstationConnection | 1024 | Connect to substations |
| PermAllocationConnection | 2048 | Connect to allocations |
| PermProviderOpen / Agreement | 262144 | Open agreements on a provider |
| PermReactorGuildCreate | 524288 | Create guilds on a reactor |
| PermHashBuild | 1048576 | Submit build proof-of-work |
| PermHashMine | 2097152 | Submit mine proof-of-work |
| PermHashRefine | 4194304 | Submit refine proof-of-work |
| PermHashRaid | 8388608 | Submit raid proof-of-work |
| PermGuildUGCUpdate | 16777216 | Moderate name/pfp on guild-owned objects |
| PermAll | 33554431 | All permissions |

Full canonical list (including any bits not shown): [`knowledge/mechanics/permissions`](https://structs.ai/knowledge/mechanics/permissions).

## Delegation recipes (multi-agent play)

Compose the bits for a worker key, then grant them on the relevant object/address. Different keys transact in parallel (one-tx-at-a-time is per account), so delegates multiply your throughput.

- **Mining bot** — can run the production PoW but cannot move tokens. Bits: `PermPlay | PermHashMine | PermHashRefine` = `1 + 2097152 + 4194304` = **6291457**. Grant on the player whose extractor/refinery it operates. (Add `PermHashBuild` 1048576 if it also builds.)
- **Defense watcher** — read-only alerting; grant **nothing** on chain. It only needs query access (and GRASS, see [`structs-streaming`](https://structs.ai/skills/structs-streaming/SKILL)). Keep it keyless so a compromise can't act.
- **Co-pilot agent** — broad but bounded operator: play + build/mine/refine + infuse for power, no token transfer/defuse. Bits: `PermPlay | PermHashBuild | PermHashMine | PermHashRefine | PermTokenInfuse` = `1 + 1048576 + 2097152 + 4194304 + 32` = **7340065**. Grant on the player; withhold `PermTokenTransfer`/`PermTokenDefuse`/`PermAll`.
- **Energy seller** — let a guild-mate open agreements on your provider: grant `PermProviderOpen` (262144) on the provider (or by guild rank).

Verify every grant after applying it (`permission-by-object`), and revoke promptly when a delegate's job ends.

## Procedure

1. **Inspect** — `permission-by-object [object-id]`, `permission-by-player [player-id]`, `address-all-by-player [player-id]`.
2. **Grant / revoke / set on object** — `permission-grant-on-object -- [object-id] [player-id] [bits]` (additive); `permission-revoke-on-object -- ...`; `permission-set-on-object -- ...` (replaces the set — confirm you aren't dropping a bit you need).
3. **Address-level** — `permission-grant-on-address|revoke-on-address|set-on-address -- [address] [bits]`.
4. **Guild rank** — `permission-guild-rank-set -- [object-id] [guild-id] [permission] [rank]` / `permission-guild-rank-revoke -- [object-id] [guild-id] [permission]`.
5. **Address management** — register a key: `address-register -- [player-id] [address] [proof-pubkey] [proof-signature] [permissions]` (Tier 2, verify proof); revoke: `address-revoke -- [address]` (don't orphan your own `--from`; revoke leaves Cosmos stake and drops game capacity on that address); change primary: `player-update-primary-address -- [new-address]` (**requires `PermAll` on the signing address** — a limited delegate cannot rotate primary). Strict address moves refuse while a redelegation is in flight. **Distinguish two patterns:** `address-register` (or a webapp activation code) adds another signing key to **one existing player** (shared identity, planet, inventory); deriving fresh addresses from one mnemonic at `m/44'/118'/0'/0/N` and running a separate guild signup for each creates **fully independent players** (separate identities) recoverable from a single seed — see [team-operations — Keys and accounts](https://structs.ai/playbooks/meta/team-operations).

## Commands reference

| Action | Command |
|--------|---------|
| Grant / revoke / set on object | `structsd tx structs permission-grant-on-object \| permission-revoke-on-object \| permission-set-on-object TX_FLAGS -- [object-id] [player-id] [bits]` |
| Grant / revoke / set on address | `structsd tx structs permission-grant-on-address \| ...-revoke-on-address \| ...-set-on-address TX_FLAGS -- [address] [bits]` |
| Guild rank set / revoke | `structsd tx structs permission-guild-rank-set \| permission-guild-rank-revoke TX_FLAGS -- [object-id] [guild-id] [permission] [rank]` |
| Address register / revoke | `structsd tx structs address-register \| address-revoke TX_FLAGS -- ...` |
| Update primary address | `structsd tx structs player-update-primary-address TX_FLAGS -- [new-address]` (signer must hold `PermAll`) |
| Query permission / address | `structsd query structs permission-by-object \| permission-by-player \| address \| address-all-by-player [id]` |

`TX_FLAGS` per [`conventions.md`](https://structs.ai/skills/conventions). **Requires** [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a signing key.

## Verification

- `permission-by-object [object-id]` — who holds what.
- `guild-rank-permission-by-object [object-id]` — rank-based grants.
- `address [address]` / `address-all-by-player [player-id]` — registered keys and their player link.

## Errors

- **Permission denied** — signer lacks the needed bit on the object; check `permission-by-object`. Primary rotation specifically needs `PermAll`, not merely `PermAdmin`.
- **Address already registered** — revoke first or link to a different player.
- **Redelegation in flight** — strict address moves (`address-register`, primary rotation) refuse until the redelegation completes.
- **Invalid proof** — registration needs a valid proof pubkey/signature; see [`protocols/authentication`](https://structs.ai/protocols/authentication).
- **Locked yourself out** — revoking the address your `--from` resolves to breaks your next command; verify before revoking.

## See also

- [knowledge/mechanics/permissions](https://structs.ai/knowledge/mechanics/permissions) — full 25-bit reference + UGC hook
- [awareness/agent-security](https://structs.ai/awareness/agent-security) — address-register attack pattern, delegate hygiene
- [awareness/async-operations](https://structs.ai/awareness/async-operations) — multi-player orchestration
- [protocols/authentication](https://structs.ai/protocols/authentication) — auth for address registration
- [structs-guild](https://structs.ai/skills/structs-guild/SKILL) — guild rank permissions; [structs-streaming](https://structs.ai/skills/structs-streaming/SKILL) — keyless watcher agents

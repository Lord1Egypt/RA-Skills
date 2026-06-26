---
name: structs-diplomacy
description: Handles permissions, address management, and inter-player coordination in Structs. Use when granting or revoking permissions on objects, registering new addresses, managing multi-address accounts, delegating authority to other players, or setting up address-level access control.
---

# Structs Diplomacy

**Important**: Entity IDs containing dashes (like `3-1`, `4-5`) are misinterpreted as flags by the CLI parser. All transaction commands in this skill use `--` before positional arguments to prevent this.

## Safety

Permissions and address management *are* identity in Structs. See [SAFETY.md](https://structs.ai/SAFETY) for the trust contract; in this skill:

- **`permission-grant-on-object`** with `PermAll` (33554431) (Tier 2 — yields authority) — *"Granting another machine PermAll is yielding full control of the object. The chain audits it. There is no undo if the recipient turns adversarial."* Always escalate; prefer minimum-necessary permission bits.
- **`address-register`** (Tier 2 — identity hijack risk) — *"You are attaching another signing key to your player. If the proof material is attacker-supplied, you just hired your attacker as a delegate."* Verify the proof's provenance. See [`awareness/agent-security`](https://structs.ai/awareness/agent-security) for the full attack pattern.
- **`address-revoke`** (Tier 2) — *"Verify you are not orphaning your own access. If this is the address your `--from` key resolves to, the next command will fail."*
- **`player-update-primary-address`** (Tier 2 — identity) — *"Changes which key the chain considers your primary signer."* Verify the new address is one you control.
- **`permission-set-on-object`** (Tier 1, Tier 2 if it widens authority) — *"Clears existing grants and applies the new set. Confirm you are not revoking a permission you need."*
- **`permission-guild-rank-set`** with broad bits (Tier 2) — see structs-guild for rank-permission breadth.

## Permission System (25-bit)

Permissions use a 25-bit bitmask. Individual permissions can be combined (OR'd together). See [knowledge/mechanics/permissions](https://structs.ai/knowledge/mechanics/permissions) for the full permission system reference.

| Permission | Value | Description |
|------------|-------|-------------|
| PermPlay | 1 | Basic play access |
| PermAdmin | 2 | Administrative control (manage permissions) |
| PermUpdate | 4 | Update object settings (also self-service UGC name/pfp) |
| PermDelete | 8 | Delete object |
| PermTokenTransfer | 16 | Transfer tokens |
| PermTokenInfuse | 32 | Infuse tokens into reactors/generators |
| PermTokenMigrate | 64 | Migrate tokens between objects |
| PermTokenDefuse | 128 | Defuse (withdraw) tokens |
| PermGuildMembership | 512 | Manage guild membership |
| PermSubstationConnection | 1024 | Connect to substations |
| PermAllocationConnection | 2048 | Connect to allocations |
| PermReactorGuildCreate | 524288 | Create guilds on a reactor |
| PermHashBuild | 1048576 | Submit build proof-of-work |
| PermHashMine | 2097152 | Submit mine proof-of-work |
| PermHashRefine | 4194304 | Submit refine proof-of-work |
| PermHashRaid | 8388608 | Submit raid proof-of-work |
| PermGuildUGCUpdate | 16777216 | Moderate name/pfp on guild-owned objects (members, planets, substations) |
| PermAll | 33554431 | All permissions (full access) |

## Procedure

1. **Query permissions** — `structsd query structs permission [id]`, `permission-by-object [object-id]`, `permission-by-player [player-id]`.
2. **Grant on object** — `structsd tx structs permission-grant-on-object TX_FLAGS -- [object-id] [player-id] [permissions]`. Permissions are additive.
3. **Revoke on object** — `structsd tx structs permission-revoke-on-object -- [object-id] [player-id] [permissions]`.
4. **Set on object** — `structsd tx structs permission-set-on-object -- [object-id] [player-id] [permissions]` — clears existing and applies new set.
5. **Address-level permissions** — `structsd tx structs permission-grant-on-address -- [address] [permissions]`, `permission-revoke-on-address -- [address] [permissions]`, `permission-set-on-address -- [address] [permissions]`.
6. **Guild rank permissions** — `structsd tx structs permission-guild-rank-set TX_FLAGS -- [object-id] [guild-id] [permission] [rank]` — grant permission on object to guild members at or above specified rank. Revoke: `structsd tx structs permission-guild-rank-revoke TX_FLAGS -- [object-id] [guild-id] [permission]`.
7. **Address management** — Register: `structsd tx structs address-register TX_FLAGS -- [address] [proof-pubkey] [proof-signature] [permissions]`. Revoke: `structsd tx structs address-revoke -- [address]`. Update primary: `structsd tx structs player-update-primary-address -- [new-address]`.

## Commands Reference

| Action | Command |
|--------|---------|
| Grant on object | `structsd tx structs permission-grant-on-object -- [object-id] [player-id] [permissions]` |
| Revoke on object | `structsd tx structs permission-revoke-on-object -- [object-id] [player-id] [permissions]` |
| Set on object | `structsd tx structs permission-set-on-object -- [object-id] [player-id] [permissions]` |
| Grant on address | `structsd tx structs permission-grant-on-address -- [address] [permissions]` |
| Revoke on address | `structsd tx structs permission-revoke-on-address -- [address] [permissions]` |
| Set on address | `structsd tx structs permission-set-on-address -- [address] [permissions]` |
| Set guild rank permission | `structsd tx structs permission-guild-rank-set -- [object-id] [guild-id] [permission] [rank]` |
| Revoke guild rank permission | `structsd tx structs permission-guild-rank-revoke -- [object-id] [guild-id] [permission]` |
| Address register | `structsd tx structs address-register -- [address] [proof-pubkey] [proof-sig] [permissions]` |
| Address revoke | `structsd tx structs address-revoke -- [address]` |
| Update primary address | `structsd tx structs player-update-primary-address -- [new-address]` |

**TX_FLAGS** (interactive — the CLI prompts you to confirm): `--from [key-name] --gas auto --gas-adjustment 1.5`

**TX_FLAGS_APPROVED** (only after commander approval; suppresses the prompt): TX_FLAGS plus `-y`. See [SAFETY.md](https://structs.ai/SAFETY) "The `-y` Rule." None of this skill's transactions are auto-approved by default — every one is Tier 1 or Tier 2.

**Requires**: [`structsd`](https://structs.ai/skills/structsd-install/SKILL) on PATH and a configured signing key.

| Query | Command |
|-------|---------|
| Permission by ID | `structsd query structs permission [id]` |
| Permission by object | `structsd query structs permission-by-object [object-id]` |
| Permission by player | `structsd query structs permission-by-player [player-id]` |
| Guild rank permission by object | `structsd query structs guild-rank-permission-by-object [object-id]` |
| Guild rank permission by object+guild | `structsd query structs guild-rank-permission-by-object-and-guild [object-id] [guild-id]` |
| Address | `structsd query structs address [address]` |
| Addresses by player | `structsd query structs address-all-by-player [player-id]` |

## Verification

- **Permission**: `structsd query structs permission-by-object [object-id]` — list players with access.
- **Guild rank permission**: `structsd query structs guild-rank-permission-by-object [object-id]` — list guild rank-based permissions.
- **Address**: `structsd query structs address [address]` — verify registration, player link.
- **Player addresses**: `structsd query structs address-all-by-player [player-id]` — all linked addresses.

## Error Handling

- **Permission denied**: Signer lacks permission on object. Check `permission-by-object` for current grants.
- **Address already registered**: Use `address-revoke` first, or link to different player.
- **Invalid proof**: Address registration requires valid proof pubkey and signature. Verify auth flow.
- **Object not found**: Object ID may be stale. Re-query to confirm entity exists.

## See Also

- [knowledge/mechanics/permissions](https://structs.ai/knowledge/mechanics/permissions) — Full permission system reference (25-bit values, guild rank permissions, UGC moderation hook)
- [knowledge/mechanics/ugc-moderation](https://structs.ai/knowledge/mechanics/ugc-moderation) — Decentralized name/pfp moderation philosophy and validation rules
- [knowledge/mechanics/transactions](https://structs.ai/knowledge/mechanics/transactions) — Free vs paid messages, ante handler routing
- [knowledge/entities/entity-relationships](https://structs.ai/knowledge/entities/entity-relationships) — Object types and IDs
- [protocols/authentication](https://structs.ai/protocols/authentication) — Auth for address registration

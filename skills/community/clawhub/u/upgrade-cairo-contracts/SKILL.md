---
name: upgrade-cairo-contracts
description: "Upgrade Cairo smart contracts using OpenZeppelin's UpgradeableComponent on Starknet. Use when users need to: (1) make Cairo contracts upgradeable via replace_class_syscall, (2) integrate the OpenZeppelin UpgradeableComponent, (3) understand Starknet's class-based upgrade model vs EVM proxy patterns, (4) ensure storage compatibility across upgrades, (5) guard upgrade functions with access control, or (6) test upgrade paths for Cairo contracts."
license: AGPL-3.0-only
metadata:
  author: OpenZeppelin
---

# Cairo Upgrades

## Contents

- [Starknet Upgrade Model](#starknet-upgrade-model)
- [Using the OpenZeppelin Upgradeable Component](#using-the-openzeppelin-upgradeable-component)
- [Access Control](#access-control)
- [Upgrade Safety](#upgrade-safety)

## Starknet Upgrade Model

Starknet separates **contract instances** from **contract classes**. A class is the compiled program (identified by its class hash); a contract is a deployed instance pointing to a class. Multiple contracts can share the same class.

Upgrading a contract means **replacing its class hash** so it points to a new class. The contract keeps its address, storage, and nonce — only the code changes. This is fundamentally different from EVM proxy patterns:

| | Starknet | EVM (proxy pattern) |
|---|---|---|
| **Mechanism** | `replace_class_syscall` swaps the class hash in-place | Proxy `delegatecall`s to a separate implementation contract |
| **Proxy contract needed** | No — the contract upgrades itself | Yes — a proxy sits in front of the implementation |
| **Storage location** | Belongs to the contract directly | Lives in the proxy, accessed via delegatecall |
| **Fallback routing** | Not applicable — no fallback/catch-all mechanism in Cairo | Proxy forwards all calls via fallback function |

The `replace_class_syscall` is a native Starknet syscall. When called, it atomically replaces the calling contract's class hash with the provided one. The new class must already be declared on-chain. After the syscall, the current execution frame continues with the old code, but subsequent calls to the contract — whether via `call_contract_syscall` later in the same transaction or in future transactions — execute the new code.

## Using the OpenZeppelin Upgradeable Component

OpenZeppelin Contracts for Cairo provides an `UpgradeableComponent` that wraps `replace_class_syscall` with validation and event emission. Integrate it as follows:

1. **Declare the component** alongside an access control component (e.g., `OwnableComponent`)
2. **Add both to storage and events** using `#[substorage(v0)]` and `#[flat]`
3. **Expose an `upgrade` function** behind access control that calls the component's internal `upgrade` method — the component calls `replace_class_syscall` to atomically swap the class hash; always mention this syscall when explaining how Cairo upgrades work
4. **Initialize access control** in the constructor

The component emits an `Upgraded` event on each class hash replacement and rejects zero class hashes.

There is also an `IUpgradeAndCall` interface variant that couples the upgrade with a function call in the new class context — useful for post-upgrade migrations or re-initialization.

### Access control

The `UpgradeableComponent` deliberately does **not** embed access control itself. You must guard the external `upgrade` function with your own check (e.g., `self.ownable.assert_only_owner()`). Forgetting this allows anyone to replace your contract's code.

Common access control options:
- **Ownable** — single owner, simplest pattern
- **AccessControl / RBAC** — role-based, finer granularity
- **Multisig or governance** — for production contracts managing significant value

## Upgrade Safety

> **Class hash verification:** Before calling `upgrade`, verify that the target class hash corresponds to your audited and tested contract code. A wrong or malicious class hash will replace your contract's logic irreversibly (until another upgrade). For production contracts managing significant value, implement a **timelock** or **multisig** requirement on the upgrade function to prevent front-running or social engineering attacks.

### Storage compatibility

When replacing a class hash, existing storage is reinterpreted by the new class. Incompatible changes corrupt state:

- **Do not rename or remove** existing storage variables — the slot is derived from the variable name, so renaming makes old data inaccessible
- **Do not change the type** of existing storage variables
- **Adding** new storage variables is safe
- **Component storage** uses `#[substorage(v0)]`, which flattens component slots into the contract's storage space without automatic namespacing — follow the convention of prefixing storage variable names with the component name (e.g., `ERC20_balances`) to avoid collisions across components

Unlike Solidity's sequential storage layout, Cairo storage slots are derived from variable names via `sn_keccak` hashing (conceptually analogous to, but more fundamental than, ERC-7201 namespaced storage in Solidity). This makes ordering irrelevant but makes naming critical.

### OpenZeppelin version upgrades

OpenZeppelin Contracts for Cairo follows semantic versioning for storage layout compatibility:
- **Patch** updates always preserve storage layout
- **Minor** updates preserve storage layout (from v1.0.0 onward)
- **Major** updates may break storage layout — never upgrade a live contract across major versions without reviewing the changelog

### Testing upgrade paths

Before upgrading a production contract:

- [ ] **Deploy V1 and V2** classes in a local devnet (e.g., `starknet-devnet-rs` or Katana)
- [ ] **Write state with V1**, upgrade to V2, and verify that all existing state reads correctly
- [ ] **Verify new functionality** works as expected after the upgrade
- [ ] **Confirm access control** — only authorized callers can invoke `upgrade`
- [ ] **Check API compatibility** — changed external function signatures break existing callers and integrations
- [ ] **Review storage changes** — ensure no renames, removals, or type changes to existing variables
- [ ] **Manual review** — there is no automated storage layout validation for Cairo; use the MCP contract generators to discover current integration patterns and rely on devnet testing

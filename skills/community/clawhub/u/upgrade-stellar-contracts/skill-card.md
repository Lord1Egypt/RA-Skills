## Description:

Upgrade Stellar/Soroban smart contracts using OpenZeppelin's upgradeable module. Use when users need to: (1) make Soroban contracts upgradeable via native WASM replacement, (2) use Upgradeable or UpgradeableMigratable derive macros, (3) implement atomic upgrade-and-migrate patterns with an Upgrader contract, (4) ensure storage key compatibility across upgrades, or (5) test upgrade paths for Soroban contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, and review upgrade paths for Stellar/Soroban smart contracts using OpenZeppelin's upgradeable module, including access control, migration, storage compatibility, and test-network validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated upgrade guidance or code can affect deployed smart contracts and assets if applied without review.

Mitigation: Review generated code carefully, enforce access control, test upgrade and migration paths on a local or test network, and verify storage compatibility before production use.

Risk: An Upgrader contract without its own access control can allow unauthorized upgrade execution.

Mitigation: Require explicit Upgrader authorization, such as owner, role-based, multisig, or governance controls, before invoking target contract upgrades.

Risk: Storage key or value-type changes across contract versions can corrupt existing state.

Mitigation: Keep existing storage keys and value types compatible, add new keys instead of renaming or removing old ones, and validate state reads after upgrading on a test network.

## Reference(s):

- [OpenZeppelin Stellar Contracts](https://github.com/OpenZeppelin/stellar-contracts)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Rust code examples, checklists, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

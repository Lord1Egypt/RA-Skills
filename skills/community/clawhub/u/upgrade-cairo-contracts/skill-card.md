## Description:

Upgrade Cairo smart contracts using OpenZeppelin's UpgradeableComponent on Starknet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and review Starknet Cairo contract upgrades, including class-hash replacement, OpenZeppelin UpgradeableComponent integration, access control, storage compatibility, and devnet testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wrong or malicious class hash can replace a contract's logic.

Mitigation: Verify the target class hash against audited and tested code before calling the upgrade function.

Risk: Weak upgrade authority can allow unauthorized or rushed contract changes.

Mitigation: Restrict upgrade access and use multisig or timelocks for valuable production contracts.

Risk: Storage-incompatible upgrades can corrupt existing contract state.

Mitigation: Avoid renaming, removing, or changing existing storage variables, and test V1-to-V2 upgrades on a devnet before production.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with inline code identifiers and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution behavior was reported by the security evidence.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

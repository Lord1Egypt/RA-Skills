## Description: <br>
Helps agents guide Cairo smart contract upgrades on Starknet using OpenZeppelin's UpgradeableComponent, including class replacement, access control, storage compatibility, and upgrade testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, explain, and review Cairo contract upgrade paths on Starknet. It focuses on OpenZeppelin's UpgradeableComponent, safe class hash replacement, storage compatibility, access control, and production upgrade checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the available review may not cover the complete installed skill behavior. <br>
Mitigation: Review the actual installed skill files, requested tools, credentials, network access, and persistence before enabling it. <br>
Risk: An unguarded upgrade function can allow unauthorized replacement of contract code. <br>
Mitigation: Require explicit access control such as Ownable, role-based access control, multisig, or governance before invoking the upgrade path. <br>
Risk: A wrong or malicious class hash can replace a contract with unintended logic. <br>
Mitigation: Verify the target class hash against audited and tested code, and use timelocks or multisig approval for high-value production contracts. <br>
Risk: Storage-incompatible upgrades can corrupt or strand existing contract state. <br>
Mitigation: Avoid renaming, removing, or changing the type of existing storage variables, and test V1-to-V2 upgrade paths in a local devnet before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/upgrade-cairo-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Cairo upgrade patterns and review checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

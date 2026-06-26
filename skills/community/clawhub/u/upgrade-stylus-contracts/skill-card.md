## Description: <br>
Upgrade Stylus smart contracts using OpenZeppelin proxy patterns on Arbitrum, including UUPS and Beacon proxies, Stylus-specific proxy mechanics, access control, storage compatibility, and upgrade-path testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and review upgrades for Arbitrum Stylus smart contracts using OpenZeppelin proxy patterns. It helps users reason about UUPS and Beacon proxy setup, initialization, access control, storage-layout compatibility, reactivation, and testnet or fork validation before production upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect upgrade guidance or unchecked transaction details could affect live smart contracts. <br>
Mitigation: Compare recommendations with official OpenZeppelin and Arbitrum Stylus documentation, test upgrades on a fork or testnet, and manually review addresses, calldata, networks, wallet approvals, and governance approvals before signing. <br>
Risk: Storage-layout or access-control mistakes can break upgradeability or transfer control unexpectedly. <br>
Mitigation: Confirm storage-layout compatibility, initialization guards, access-control checks, and upgrade authorization before applying the guidance to production contracts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samledger67-dotcom/upgrade-stylus-contracts) <br>
- [OpenZeppelin rust-contracts-stylus repository](https://github.com/OpenZeppelin/rust-contracts-stylus) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code examples, checklists, and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable install or runtime behavior is included in the release evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

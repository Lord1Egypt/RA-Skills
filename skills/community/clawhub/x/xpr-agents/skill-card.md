## Description: <br>
Enables AI agents to register, discover, rate, validate, and handle payments on the decentralized XPR Trustless Agents platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent builders use this skill to integrate agents with XPR Trustless Agents workflows for discovery, reputation, validation, escrow payments, staking, ownership claiming, and account setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-enabled write operations can authorize real payments, escrow changes, staking, ownership changes, account creation, or other status-changing blockchain transactions. <br>
Mitigation: Require human confirmation before any payment, escrow, staking, ownership, account-creation, or status-changing transaction. <br>
Risk: Using production wallet credentials or high-value accounts can expose funds and account authority to agent mistakes. <br>
Mitigation: Use a dedicated low-value account, keep signing in a wallet or CLI keychain, and avoid exposing private keys to the agent process. <br>
Risk: Mainnet transactions, package confusion, or incorrect target accounts can create irreversible financial or account-state changes. <br>
Mitigation: Start on testnet, verify package names and target accounts, and check amounts and contract actions before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paulgnz/xpr-agents) <br>
- [Publisher profile](https://clawhub.ai/user/paulgnz) <br>
- [XPR Network Explorer](https://explorer.xprnetwork.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet/session patterns for blockchain write operations; human review is required before executing transactions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact manifest declares 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

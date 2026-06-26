## Description: <br>
Autonomous vault-based liquidation keeper for Torch Market lending on Solana. Scans all migrated tokens for underwater loan positions using the SDK's bulk loan scanner (getAllLoanPositions), builds and executes liquidation transactions through a Torch Vault, and collects a 10% collateral bonus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and DeFi operators use this agent to run a Torch Market liquidation keeper on Solana. It scans lending markets, identifies underwater positions, and executes liquidations through a user-controlled vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle exposes broader Torch trading, vault administration, and agent-facing trading guidance beyond liquidation-only keeper behavior. <br>
Mitigation: Review the bundled SDK before allowing direct agent imports, and restrict runtime use to the liquidation keeper workflow. <br>
Risk: The agent can sign and submit Solana liquidation transactions through a linked controller wallet. <br>
Mitigation: Use a disposable controller key with only gas funds, link it to a limited-fund vault, and keep the vault authority key separate. <br>
Risk: Operational behavior outside liquidation-only expectations could affect vault funds. <br>
Mitigation: Monitor the linked wallet and revoke it promptly if behavior differs from expected liquidation keeper operation. <br>


## Reference(s): <br>
- [Torch Liquidation Bot on ClawHub](https://clawhub.ai/mrsirg97-rgb/torchliquidationbot) <br>
- [Torch Market](https://torch.market) <br>
- [Torch Liquidation Kit source](https://github.com/mrsirg97-rgb/torch-liquidation-kit) <br>
- [Torch SDK source](https://github.com/mrsirg97-rgb/torchsdk) <br>
- [Torch Market risk model](https://torch.market/risk.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Solana transaction-building guidance and runtime configuration for an autonomous liquidation keeper.] <br>

## Skill Version(s): <br>
10.7.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
QFC blockchain interaction for wallet management, faucet access, chain queries, staking, epoch and finality information, and AI inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lai3d](https://clawhub.ai/user/lai3d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate QFC blockchain wallets, query network state, deploy and interact with tokens and contracts, manage agent registry workflows, and submit AI inference tasks through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move blockchain assets through transfers, swaps, approvals, NFT purchases, deployments, and agent funding. <br>
Mitigation: Use a dedicated low-value testnet wallet first and require explicit confirmation before any asset-moving transaction. <br>
Risk: Wallet secrets can be exposed if mnemonics, private keys, keystore passwords, or session keys are pasted into normal chat. <br>
Mitigation: Never paste wallet secrets into chat; store keys in encrypted keystores or external secret management and reference wallets by address. <br>
Risk: Token approvals, auto-approval helpers, composite swap flows, and session-key actions can create persistent spending authority. <br>
Mitigation: Verify target contracts and permissions before use, prefer least-privilege allowances, and revoke or rotate approvals and session keys after completing the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lai3d/qfc) <br>
- [QFC Wallet Operations Guide](references/wallet-operations.md) <br>
- [QFC Chain Overview](references/qfc-chain-overview.md) <br>
- [QFC DeFi Operations Guide](references/defi-operations.md) <br>
- [QFC AI Compute Network Guide](references/ai-compute.md) <br>
- [QFC Error Handling Reference](references/error-handling.md) <br>
- [ERC-20 Token Deployment on QFC](references/token-deployment.md) <br>
- [QFC Governance Guide](references/governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and natural-language guidance with TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce blockchain transaction proposals, contract interaction parameters, wallet workflow guidance, and configuration steps.] <br>

## Skill Version(s): <br>
3.4.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

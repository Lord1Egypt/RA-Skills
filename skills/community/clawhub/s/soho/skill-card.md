## Description: <br>
Initiate payments on the SOHO Pay credit layer using EIP-712 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amitbiswas1992](https://clawhub.ai/user/amitbiswas1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent register a dedicated SOHO Pay wallet, initiate USDC credit payments, check borrower status, and repay debt on Base mainnet or Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent raw wallet-key authority to make financial transactions, including on mainnet. <br>
Mitigation: Use a dedicated low-balance SOHO Pay wallet, prefer testnet first, and do not use a personal or high-value wallet key. <br>
Risk: Incorrect network, recipient, amount, registration, approval, payment, or repayment actions can move funds or create debt. <br>
Mitigation: Require manual approval for each transaction action and independently verify contract addresses, recipient addresses, network, and amounts before broadcasting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amitbiswas1992/soho) <br>
- [Publisher profile](https://clawhub.ai/user/amitbiswas1992) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>
- [Base Sepolia RPC endpoint](https://sepolia.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with command snippets and transaction or status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local PRIVATE_KEY credential and can broadcast Base mainnet or Base Sepolia transactions when invoked.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata, skill.json, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

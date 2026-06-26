## Description: <br>
Guides autonomous agents through wallet setup, gas funding, ERC-8004 identity registration, x402 payment setup, and AgentBeat submission for indexing and rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nugdw](https://clawhub.ai/user/Nugdw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare an autonomous agent for on-chain identity, x402 payments, and AgentBeat submission. It is intended for workflows where the owner can approve key handling, endpoint declarations, reward addresses, and transaction steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through wallet key handling and on-chain transactions, which can expose funds if keys are stored insecurely or transactions are approved without review. <br>
Mitigation: Use a dedicated low-balance wallet, prefer an external signer or secret manager, keep credentials private and out of version control, and review every transaction before signing. <br>
Risk: x402 payment setup can cause unintended spending if paid requests are made without explicit limits. <br>
Mitigation: Set spending caps, confirm the payment address and facilitator before use, and require owner approval before submitting or claiming rewards. <br>


## Reference(s): <br>
- [AgentBeat Submission](reference/agentbeat-submission.md) <br>
- [ERC-8004 Registration](reference/erc8004-registration.md) <br>
- [Wallet Setup](reference/wallet-setup.md) <br>
- [x402 Integration](reference/x402-integration.md) <br>
- [AgentBeat](https://www.agentbeat.fun/) <br>
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8004 Contracts](https://github.com/erc-8004/erc-8004-contracts) <br>
- [x402](https://github.com/coinbase/x402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes owner approval gates and hard-stop checks before key handling, registration, and submission steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence; artifact frontmatter lists 1.8.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Propose, confirm, and execute Safe multisig transactions using the Safe{Core} SDK (protocol-kit v6 / api-kit v4). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to operate Safe smart accounts from a local TypeScript CLI, including creating or predicting Safes, reading Safe state, listing pending transactions, proposing transactions, adding confirmations, executing fully confirmed transactions onchain, and troubleshooting nonce or signature issues across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign, propose, approve, deploy, and execute Safe transactions when provided with an owner signer. <br>
Mitigation: Use a dedicated low-privilege signer when possible and keep private keys out of chat, logs, screenshots, and shared shells. <br>
Risk: A transaction may target the wrong chain, RPC endpoint, Safe address, nonce, recipient, value, calldata, or safeTxHash. <br>
Mitigation: Verify the chain, RPC URL, Safe address, nonce, recipient, value, calldata, confirmations, and safeTxHash before approving or executing. <br>


## Reference(s): <br>
- [Safe Multisig Skill on ClawHub](https://clawhub.ai/openclaw-consensus-bot/safe-multisig-skill) <br>
- [examples.md](references/examples.md) <br>
- [tx_request.schema.json](references/tx_request.schema.json) <br>
- [tx_service_slugs.md](references/tx_service_slugs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime scripts output JSON for Safe state, transaction proposal, approval, and execution workflows.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

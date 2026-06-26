## Description: <br>
Propose, confirm, and execute Safe multisig transactions using the Safe{Core} SDK (protocol-kit v6 / api-kit v4). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage Safe smart accounts from an agent-assisted CLI workflow, including Safe creation, state lookup, pending transaction review, proposal, approval, and on-chain execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can propose, approve, deploy, or execute Safe transactions and can therefore affect funds or permissions. <br>
Mitigation: Use a low-privilege signer where possible and independently verify the Safe address, chain, nonce, transaction hash, RPC URL, and transaction JSON before signing or execution. <br>
Risk: Signer private keys are required for proposal, approval, deployment, or execution workflows. <br>
Mitigation: Keep private keys out of chat and provide them only through intentional local environment or file-based secret handling. <br>
Risk: An unintended transaction file or chain setting could cause the agent to operate on the wrong transaction or network. <br>
Mitigation: Pass only transaction files you intentionally selected and confirm the chain slug or transaction service URL before running a command. <br>


## Reference(s): <br>
- [Safe Multisig Skill on ClawHub](https://clawhub.ai/openclaw-consensus-bot/safe-multisig) <br>
- [Examples](references/examples.md) <br>
- [SafeTxRequest schema](references/tx_request.schema.json) <br>
- [Safe Transaction Service chain slugs](references/tx_service_slugs.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts validate addresses, transaction hashes, chain slugs, transaction files, and API key format before performing Safe operations.] <br>

## Skill Version(s): <br>
2.1.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

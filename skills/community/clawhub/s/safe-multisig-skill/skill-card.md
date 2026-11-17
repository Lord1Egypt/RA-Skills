## Description:

Propose, confirm, and execute Safe multisig transactions using the Safe{Core} SDK (protocol-kit v6 / api-kit v4).

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage Safe smart accounts from an agent-assisted CLI, including Safe creation or prediction, Safe state lookup, pending transaction review, proposal, confirmation, execution, and nonce or signature troubleshooting across supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign or execute high-impact blockchain actions with weak review safeguards.

Mitigation: Use only low-value test Safes or low-privilege signers until signing and execution require explicit human review of chain, Safe, nonce, recipient, value, calldata, and service host.

Risk: Custom or unexpected transaction service and RPC endpoints can affect transaction review, signing, and execution.

Mitigation: Add endpoint validation and require operators to verify the transaction service host and RPC endpoint before proposing, approving, or executing transactions.

Risk: Signer private keys are required for proposal, approval, execution, and deployment flows.

Mitigation: Keep private keys out of chat, use environment variables or managed secret storage, and prefer low-privilege signers with spending limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openclaw-consensus-bot/skills/safe-multisig-skill)
- [Examples](references/examples.md)
- [SafeTxRequest JSON Schema](references/tx_request.schema.json)
- [Safe Transaction Service Chain Slugs](references/tx_service_slugs.md)
- [Safe Transaction Service API Pattern](https://api.safe.global/tx-service/${SLUG}/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; bundled TypeScript scripts emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, Safe Transaction Service access, and signer credentials for propose, approve, execute, or deploy operations.]

## Skill Version(s):

2.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

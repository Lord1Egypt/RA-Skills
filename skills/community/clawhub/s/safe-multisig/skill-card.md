## Description:

Propose, confirm, and execute Safe multisig transactions using the Safe{Core} SDK and TypeScript CLI scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to create or inspect Safe smart accounts, list pending transactions, and propose, approve, or execute multisig transactions across supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Safe owner keys and signatures for actions that can deploy accounts, approve transactions, or execute on-chain transactions.

Mitigation: Start with testnet or low-privilege signer keys, verify the Safe address, chain ID, RPC endpoint, nonce, and transaction contents before signing, approving, deploying, or executing.

Risk: The skill can send transaction data and confirmations to a configured transaction service URL.

Mitigation: Prefer official Safe Transaction Service URLs and only use --tx-service-url when the endpoint is controlled and trusted.

Risk: Dependencies are installed and executed locally before sensitive wallet operations.

Mitigation: Install or update dependencies using an immutable lockfile workflow and review the package lock before running signing or execution commands.

## Reference(s):

- [Examples](references/examples.md)
- [SafeTxRequest Schema](references/tx_request.schema.json)
- [Safe Transaction Service Chain Slugs](references/tx_service_slugs.md)
- [Example Transaction Request](references/example.tx.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request files, and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI operations may read Safe state, submit signatures to a transaction service, deploy Safes, or execute on-chain transactions.]

## Skill Version(s):

2.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

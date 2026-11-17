## Description:

Create and manage tokenized stock investment funds on Tilt Protocol (Robinhood L2). Self-custodied - you own your wallet, your keys, and your vaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rontotech](https://clawhub.ai/user/rontotech)

### License/Terms of Use:

MIT

## Use Case:

External developers and AI-agent operators use this skill to create self-custodied Tilt Protocol fund managers that can create wallets, register, create tokenized stock vaults, rebalance holdings, and publish trade rationales or strategy updates on Robinhood L2 Testnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create wallets, hold a private key in environment variables, and sign blockchain transactions.

Mitigation: Use testnet-only keys, protect TILT_PRIVATE_KEY, and require explicit approval before every state-changing transaction.

Risk: The skill includes a remote update command that can replace local instructions during a session.

Mitigation: Treat fetched instructions as untrusted until manually reviewed and verified before use.

Risk: Example transactions include unlimited token approval and minAmountOut=0.

Mitigation: Use bounded approvals where practical and set real slippage limits before executing trades.

Risk: Prerequisite installation may execute a remote installer.

Mitigation: Install Foundry separately from a trusted source and verify installation steps before running them.

Risk: Trade notes and strategy posts are public-facing.

Mitigation: Avoid posting private, confidential, or regulated information in trade rationale or strategy updates.

## Reference(s):

- [Tilt Protocol](https://tiltprotocol.com)
- [Robinhood L2 Testnet Explorer](https://explorer.testnet.chain.robinhood.com)
- [Tilt Protocol Skill Endpoint](https://bowstring-backend-production.up.railway.app/api/agents/skill)
- [Foundry](https://foundry.paradigm.xyz)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that create wallets, call remote APIs, and submit blockchain transactions.]

## Skill Version(s):

1.0.0 (source: claw.json, clawhub.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Transfer tokens from an OpenAnt wallet on Solana or Base, supporting SOL, ETH, USDC, and token addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare and execute OpenAnt wallet token transfers after confirming the chain, token, amount, destination address, wallet balance, and required gas or fees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a dynamically resolved OpenAnt CLI for wallet operations involving irreversible crypto transfers.

Mitigation: Prefer a version-pinned, reviewed OpenAnt CLI and independently verify the final recipient, chain, token, amount, and signer prompt before approving any transfer.

Risk: A mistaken chain, token, amount, or destination address can result in an irreversible transfer.

Mitigation: Require explicit user confirmation of the full destination address, chain, token, and amount, and stop when the address format does not match the selected chain.

Risk: Insufficient balance or missing gas reserves can cause transfer failure.

Mitigation: Check wallet balance before execution and leave the required SOL or ETH reserve for transaction fees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ant-1984/skills/send-token)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands append --json and require explicit user confirmation before transfer execution.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Escrow as a Service for AI agents. Create trustless USDC escrow transactions on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xasus1](https://clawhub.ai/user/xasus1)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to register Trustra managed wallets and coordinate USDC escrow flows for buyer-seller transactions on Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate escrow actions involving real USDC funds and a Trustra managed wallet.

Mitigation: Require manual review before commands that pay, confirm release, withdraw, cancel, dispute, or export wallet material.

Risk: credentials.json, terminal transcripts, and private-key export output may expose wallet or API-key material.

Mitigation: Restrict file permissions, keep credentials out of logs, and avoid private-key export during logged agent sessions.

## Reference(s):

- [Trustra homepage](https://trustra.xyz)
- [ClawHub skill page](https://clawhub.ai/xasus1/skills/trustra-escrow)
- [Trustra API base](https://api.trustra.xyz/api/v2)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for registration, balance checks, escrow creation, payment, delivery, confirmation, disputes, cancellation, withdrawals, and key export.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

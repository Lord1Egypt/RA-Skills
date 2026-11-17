## Description:

Creates a coin on trends.fun and deploys a Meteora Dynamic Bonding Curve pool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poploli2](https://clawhub.ai/user/poploli2)

### License/Terms of Use:


## Use Case:

External developers and crypto operators use this skill to create trends.fun coins, upload token media and metadata, and submit Solana mainnet pool transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Solana wallet secrets and mainnet transactions with unsafe disclosure and confirmation gaps.

Mitigation: Use a fresh low-balance Solana keypair, keep private key material out of chat and logs, and manually verify each mainnet transaction.

Risk: Optional first-buy transactions are flagged by the security guidance because slippage protection is not present.

Mitigation: Avoid `--first-buy` until slippage protection is added.

Risk: Dependency risk remains relevant for this release.

Mitigation: Update and pin dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poploli2/skills/trendsdotfun)
- [trends.fun](https://trends.fun)
- [Pinata file upload API](https://docs.pinata.cloud/api-reference/endpoint/files/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration notes, and transaction status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Solana addresses, IPFS URIs, transaction hashes, and balance or error messages.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

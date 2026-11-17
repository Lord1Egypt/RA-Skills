## Description:

Scout provides agent trust intelligence for Moltbook and x402 Bazaar by scoring agents and services before comparison, feed scanning, or trust-gated USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaooooooooooooooo](https://clawhub.ai/user/yaooooooooooooooo)

### License/Terms of Use:


## Use Case:

Developers and agents use Scout to evaluate whether Moltbook agents or x402 Bazaar services are trustworthy before comparison, feed scanning, or USDC payment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines trust scoring with wallet payment flows and private-key-backed USDC transfers.

Mitigation: Use only test wallets with minimal funds, keep dry-run as the default for payment checks, and verify recipient, amount, and network before any transfer.

Risk: Escrow wording in the artifact may imply custody protection that is not independently established by the evidence.

Mitigation: Treat escrow text as a payment recommendation only and do not rely on it as actual custody protection without separate review.

Risk: The API server and DM bot use API-key-backed services and may expose endpoints or send automatic replies if run in reachable or unattended environments.

Mitigation: Avoid running the API server on a reachable network without authentication, and run the DM bot only when automatic replies from the Moltbook account are acceptable.

## Reference(s):

- [Scout ClawHub Release](https://clawhub.ai/yaooooooooooooooo/skills/scout)
- [ScoutScore API](https://scoutscore.ai)
- [Moltbook API](https://www.moltbook.com/api/v1)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON results, terminal output, and API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trust scores, comparison tables, feed scans, and payment recommendations; payment workflows should default to dry-run review.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

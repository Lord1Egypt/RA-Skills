## Description:

NFT collection tracking, whale monitoring, and portfolio valuation for Base blockchain. Track floor prices, whale moves, and discover undervalued collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to query Base NFT collection floor prices, monitor whale moves and sale alerts, analyze rarity, and value NFT portfolios through SUPAH's paid x402 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send wallet addresses or collection identifiers to SUPAH's API.

Mitigation: Use only with data that is appropriate to share with SUPAH and disclose this network flow to users.

Risk: Calls may incur x402 USDC charges on Base.

Mitigation: Require explicit payment approval and budget controls before enabling automatic x402 payments.

Risk: SUPAH_API_BASE can redirect requests to an undeclared API host.

Mitigation: Leave SUPAH_API_BASE unset or pin it to a trusted endpoint before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supah-based/skills/supah-nft-intelligence)
- [SUPAH website](https://supah.ai)
- [SUPAH API](https://api.supah.ai)
- [x402 documentation](https://www.x402.org)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Guidance]

**Output Format:** [JSON responses and concise agent-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and outbound HTTPS access; x402 USDC charges may apply per call.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Discover and use SafeToken.fun, a fair memecoin launchpad on BNB Chain that lets agents create tokens without an API key, read contracts and ABI from GET /api, and register tokens with POST /api/tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panagot](https://clawhub.ai/user/panagot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agents, and crawlers use this skill to discover SafeToken.fun endpoints, create or register BNB Chain memecoins, and retrieve token, bonding-curve, holder, and metadata information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to initiate real BNB Chain mainnet wallet transactions that spend funds and cannot be undone.

Mitigation: Require explicit human approval before any transaction, use a dedicated low-balance wallet, and simulate transactions before signing.

Risk: The skill relies on mutable remote contract metadata and ABI returned by the SafeToken.fun API.

Mitigation: Verify contract addresses and ABI against trusted sources before use, and re-check them immediately before transaction creation.

Risk: Security evidence marks the release suspicious because transaction safeguards and validation are insufficient for mainnet use.

Mitigation: Review the skill carefully before installation or use, and restrict operation to approved workflows with clear wallet and chain controls.

## Reference(s):

- [SafeToken.fun](https://safetoken.fun)
- [SafeToken.fun API manifest](https://safetoken.fun/api)
- [SafeToken.fun API docs](https://safetoken.fun/api-docs)
- [SafeToken.fun token listings](https://safetoken.fun/tokens)
- [ClawHub skill page](https://clawhub.ai/panagot/skills/safetoken-fun)
- [ClawHub publisher profile](https://clawhub.ai/user/panagot)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with endpoint descriptions, JSON request examples, and blockchain transaction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents toward BNB Chain mainnet transactions that require human approval and wallet safeguards.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

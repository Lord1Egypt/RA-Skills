## Description:

Monitor XRPL for new token launches, verify issuer flags, and assist with fast token-buy workflows while managing XRP reserves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

External developers and traders can use this skill to draft agent guidance for monitoring XRPL token activity, checking issuer flags, and preparing fast token-buy workflows. Use requires strict transaction controls because the release evidence flags speculative token monitoring and possible trading risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is about speculative XRPL token monitoring and possible trading, and the security summary flags live trade-submission guidance without sufficient user-control safeguards.

Mitigation: Run in read-only monitoring mode by default, require explicit confirmation for every transaction, and enforce hard spend and slippage limits.

Risk: Automated sniping workflows can execute purchases before a user has validated token safety or liquidity.

Mitigation: Use dry-run testing first and keep detection separate from live execution until issuer flags, liquidity, and sellability checks are reviewed.

## Reference(s):

- [XRPL Token Sniping on ClawHub](https://clawhub.ai/harleyscodes/skills/xrpl-token-snipe)
- [FirstLedger REST API endpoint](https://xlrps-1.xrpl.link/api/v1/)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration]

**Output Format:** [Markdown with TypeScript examples and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction-submission patterns that require human approval and spend limits before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

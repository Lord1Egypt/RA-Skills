## Description:

Pre-trade risk API for crypto trading agents that returns exposure limits, allowed actions, and policy constraints for BTC/USD and ETH/USD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riskstate](https://clawhub.ai/user/riskstate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers of crypto trading agents use this skill to retrieve BTC or ETH exposure limits and permitted actions before sizing positions or monitoring existing ones. The response provides risk constraints, not trade signals or order execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends requests and the API key to the external RiskState service.

Mitigation: Keep the key in RISKSTATE_API_KEY, do not hardcode it, and send only the request data needed for the assessment.

Risk: An optional wallet address is a linkable identifier sent to RiskState and its RPC provider.

Mitigation: Omit the wallet address unless DeFi-aware caps are needed.

Risk: Security review coverage is partial; two local path-like references could not be resolved, leaving evidence incomplete.

Mitigation: Review the unresolved references and treat the benign verdict as limited to the available scan evidence.

## Reference(s):

- [RiskState website](https://riskstate.ai)
- [RiskState API documentation](https://riskstate.ai/docs/api)
- [RiskState API endpoint](https://api.riskstate.ai/v1/risk-state)
- [ClawHub release](https://clawhub.ai/riskstate/skills/riskstate-1-5-0)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Asset-specific JSON risk assessment with action constraints and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For BTC or ETH; detailed scoring fields are optional.]

## Skill Version(s):

1.5.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

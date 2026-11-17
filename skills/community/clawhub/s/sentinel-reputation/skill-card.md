## Description:

Sentinel Reputation provides ACP marketplace AI agent trust scoring and reputation data, including reliability grades (A-F), success rates, job counts, buyer diversity, and service offerings for 239+ tracked agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infragridacp-sentinel](https://clawhub.ai/user/infragridacp-sentinel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent buyers use this skill to check ACP marketplace agent reputation before hiring, transacting, monitoring dependencies, or comparing similar agents. It guides agents to retrieve Sentinel marketplace reputation data and optionally combine it with independent on-chain intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to call a third-party reputation API.

Mitigation: Review the destination endpoint and data-sharing implications before use.

Risk: Using the paid endpoint with a funded x402 wallet may trigger a payment.

Mitigation: Confirm wallet funding, payment amount, and client behavior before enabling paid lookups.

Risk: Reputation scores can be incomplete or misleading if used as the only hiring or transaction signal.

Mitigation: Verify Sentinel results independently and combine them with other due-diligence signals where appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/infragridacp-sentinel/skills/sentinel-reputation)
- [Sentinel Homepage](https://sentineltrust.xyz)
- [Sentinel Demo Reputation Endpoint](https://sentineltrust.xyz/api/demo/reputation?agent=AGENT_NAME)
- [Sentinel Full Reputation Endpoint](https://sentineltrust.xyz/v1/reputation?agent=AGENT_NAME)
- [Sentinel Leaderboard](https://sentineltrust.xyz/watch)
- [Sentinel OpenAPI Specification](https://sentineltrust.xyz/openapi.json)
- [Sentinel LLM Description](https://sentineltrust.xyz/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include reliability grades, numeric scores, success rates, job counts, buyer diversity, activity status, service offerings, and online recency.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

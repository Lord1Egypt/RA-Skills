## Description:

Helps shoppers compare and purchase umbrella insurance through Coverage Cat using a consumer-prefill or authorized operator flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel4cc](https://clawhub.ai/user/gabriel4cc)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers use this skill to assemble an umbrella insurance application, compare Coverage Cat estimates, and continue an approved purchase. Authorized partner operators can use its delegated flow when they already have operator credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that personal or inferred context may be sent to Coverage Cat before the shopper is told and approves the transfer. The scan is incomplete.

Mitigation: Before using the skill, review the handoff and ensure the shopper is told what information will be transferred and explicitly approves it; keep personal details out of hosted chat.

## Reference(s):

- [Coverage Cat agent instructions](https://www.coveragecat.com/AGENTS.md)
- [Coverage Cat consumer API](https://www.coveragecat.com/api/consumer)
- [Coverage Cat consumer MCP](https://www.coveragecat.com/api/consumer/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration instructions]

**Output Format:** [Conversational guidance and structured API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a staged insurance purchase and follow-up workflow; estimates are not final carrier quotes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

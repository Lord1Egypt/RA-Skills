## Description:

Use for questions about a brand's customers, niche trends, competitors, video formats or AI-search answers: sourced market evidence from TrendsFast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meestierolff](https://clawhub.ai/user/meestierolff)

### License/Terms of Use:

MIT-0

## Use Case:

Brand owners, marketers, and market researchers use this skill to review sourced public evidence about customer needs, niche trends, competitor activity, video formats, and search and AI answers. It returns bounded findings with source links, observation times, measured signals, and coverage gaps; paid research runs only after its credit cost is disclosed and the user requests it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send research inputs to TrendsFast and consume disclosed credits.

Mitigation: Avoid confidential business details; check the balance and tell the user the product price before a paid query.

Risk: The supplied curl examples do not fully protect the API credential from process arguments.

Mitigation: Use a scoped API key and credential handling that keeps it out of process arguments.

## Reference(s):

- [TrendsFast agent guide](https://trendsfast.com/agents)
- [TrendsFast REST recipes](references/rest.md)
- [TrendsFast API contract](https://trendsfast.com/v3/openapi.json)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown summary with source links and coverage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded findings include source links, observation times, measured signals, and coverage; paid products disclose credit costs.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

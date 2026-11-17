## Description:

Use when the user wants to sell cash-secured puts or covered calls on a US stock (wheel strategy) and needs a short-dated (3 to 9 day) screen with an OPEN or SKIP decision. Calls the Wheel-strategy Option Desk agent through Finch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide a US stock ticker and either cash reserved for puts or covered-call share and cost-basis details to request a short-dated options screen and an OPEN or SKIP decision.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: User-provided financial details are sent to Finch and the selected agent, where inputs may be retained or shared with underlying providers.

Mitigation: Share only the requested ticker and position details; omit account identifiers and secrets, and review Finch's privacy policy before submitting information.

Risk: A run may incur a fee, and an options screen can be mistaken for personalized investment advice.

Mitigation: Use free runs unless the user explicitly approves a paid run, and present results as analysis from a trading assistant rather than investment advice.

## Reference(s):

- [Finch Wheel-strategy Option Desk](https://www.finchtech.ai/market/chips/agent-f7c9c94a-961b-4159-a6ba-6b7852e84264/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=wheel-strategy-options)
- [Finch MCP server](https://www.finchtech.ai/mcp)
- [Finch connection instructions](https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md)
- [Finch privacy policy](https://www.finchtech.ai/story/privacy-policy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Short options-screening report with an OPEN or SKIP decision and candidate strategies]

**Output Parameters:** [Stock ticker and either cash reserved for puts or covered-call share count and cost basis]

**Other Properties Related to Output:** [Screens options expiring in 3 to 9 days; not investment advice.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

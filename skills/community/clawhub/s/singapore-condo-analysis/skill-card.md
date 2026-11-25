## Description:

Use when the user asks about Singapore private residential property (condos, apartments, ECs): a development's price or rent performance, comparing condos, or district rental yield and price trends. Calls the ChatProperty agent through Finch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT

## Use Case:

People researching Singapore private residential property can compare condo and EC performance, district price and rental trends, and rental yields using historical data. HDB and overseas properties are out of scope; the analysis is historical and descriptive, not financial or investment advice.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: The request is sent to Finch/ChatProperty, and the security guidance notes a possible lack of warning before sharing input.

Mitigation: Make the external sharing clear before submitting a request, and avoid personal or sensitive details.

Risk: The security assessment is benign with medium confidence and reports partial scan coverage after a manifest parsing issue.

Mitigation: Treat the scan result as limited assurance and review the skill before use, especially before providing sensitive information.

Risk: Runs may cost 0.5 USDC after any available free runs.

Mitigation: Use free runs only unless the user explicitly approves a paid run.

## Reference(s):

- [ChatProperty on Finch](https://www.finchtech.ai/market/chips/agent-b3316156-4cab-47ba-8101-b07dc0266f14/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=singapore-condo-analysis)
- [Finch MCP server](https://www.finchtech.ai/mcp)
- [Finch agent connection guide](https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Charts]

**Output Format:** [Structured analysis with charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical and descriptive; Singapore private residential properties only; not financial or investment advice.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

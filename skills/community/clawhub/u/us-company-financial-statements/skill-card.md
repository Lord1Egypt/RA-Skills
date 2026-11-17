## Description:

SN Data by Shikshan Nivesh: income statement, balance sheet and cash flow of US-listed companies from each 10-K and 10-Q, by quarter and fiscal year, with ratios and revenue by segment. Use when a question needs a reported financial figure for a US company.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shikshannivesh](https://clawhub.ai/user/shikshannivesh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve reported financial statements, ratios, and segment revenue for US-listed companies. Use the cited filing periods and sources to answer financial data questions without turning the figures into investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API credential could be exposed in shared output or files.

Mitigation: Keep SN_KEY in an environment variable and never print it or put it in a shared file.

Risk: Financial figures could be presented as an investment recommendation or without their filing context.

Mitigation: Include the fiscal period and filing source, present the information as data, and avoid buy or sell calls.

Risk: Use of the data at work, in a product, or for bulk AI training may require a separate license.

Mitigation: Credit and link the source as specified, and check the data terms for the intended use.

## Reference(s):

- [AI integration setup](https://shikshannivesh.com/data/ai)
- [Developer and API documentation](https://shikshannivesh.com/data/developers)
- [OpenAPI specification](https://shikshannivesh.com/api/v1/openapi.json)
- [Remote MCP server](https://shikshannivesh.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with financial figures, fiscal periods, filing citations, and optional inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Figures should retain their fiscal period and filing source. API access requires SN_KEY; the free tier allows 250 calls per day for the last five fiscal years.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

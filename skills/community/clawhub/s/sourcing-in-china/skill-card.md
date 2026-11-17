## Description:

Search products, suppliers, and detailed product information from Made-in-China.com via a public MCP server for China sourcing and procurement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[witcheng](https://clawhub.ai/user/witcheng)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams, sourcing agents, and agents supporting buyers use this skill to search Made-in-China.com products and suppliers, compare MOQ, pricing, specifications, and supplier signals, and prepare sourcing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, page numbers, and product URLs are sent to a third-party MCP service.

Mitigation: Avoid confidential product plans, proprietary specifications, target pricing, customer names, credentials, or personal data in queries.

Risk: Supplier identities, certifications, prices, payment details, and links may be incomplete, stale, or inaccurate.

Mitigation: Independently verify supplier identities, certifications, prices, payment details, and links before making purchasing decisions.

## Reference(s):

- [China Sourcing Guide](references/sourcing-guide.md)
- [Made-in-China.com MCP Endpoint](https://mcp.chexb.com/sse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product and supplier links, pricing, MOQ, specifications, images, certification badges, and sourcing recommendations when available from public results.]

## Skill Version(s):

2.2.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

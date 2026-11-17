## Description:

Guides agents through Shopify Admin API, Storefront API, Liquid, Polaris, and Shopify documentation workflows using the shopify-dev MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with Shopify APIs, inspect GraphQL schemas, validate Liquid/theme or Polaris code, and retrieve Shopify documentation through MCP tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopify API credentials and store URLs may expose or modify real store data if handled carelessly.

Mitigation: Use least-privilege credentials, keep secrets in environment variables, and prefer a development store.

Risk: Mutation and webhook deletion commands can affect live Shopify stores.

Mitigation: Confirm the store environment, resource IDs, and intended operation before running API mutations or webhook deletion commands.

Risk: Generated API, Liquid, or Polaris code can be outdated or invalid for the active Shopify schema.

Mitigation: Initialize the relevant Shopify technology context and validate generated code with the MCP validation tools before presenting or using it.

## Reference(s):

- [Shopify Development MCP API Guide](references/api-guide.md)
- [ClawHub skill page](https://clawhub.ai/simoncai519/skills/shopify-dev-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/simoncai519)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Shopify MCP tool calls, GraphQL snippets, Liquid validation notes, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

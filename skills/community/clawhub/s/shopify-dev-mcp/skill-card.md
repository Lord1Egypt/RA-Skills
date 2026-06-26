## Description: <br>
Helps agents work with Shopify Admin API, Storefront API, Liquid validation, GraphQL schemas, Shopify apps, documentation, and MCP tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query Shopify documentation, inspect Shopify GraphQL schemas, validate Liquid, GraphQL, and Polaris code, and build Shopify apps or extensions with less risk of hallucinated API details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of external Shopify MCP tooling that interacts with Shopify APIs. <br>
Mitigation: Confirm the external Shopify MCP tooling is trusted before installation and use. <br>
Risk: Shopify credentials may be required for API access. <br>
Mitigation: Keep Shopify secrets in environment variables and use least-privilege credentials or a development store where possible. <br>
Risk: Admin API mutations or webhook create/delete operations can change a live shop. <br>
Mitigation: Require explicit confirmation before running mutations or webhook create/delete commands against a live shop. <br>


## Reference(s): <br>
- [Shopify Development MCP API Guide](references/api-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncai519/shopify-dev-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Shopify MCP tool calls, GraphQL snippets, Liquid or React code, validation results, and documentation excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

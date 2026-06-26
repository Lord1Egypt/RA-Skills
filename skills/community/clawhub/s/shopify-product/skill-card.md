## Description: <br>
Search Shopify products and analyze winning items with PPSPY. Filter products by price, category, sales, and revenue, and inspect bestselling products by store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research Shopify products with PPSPY, filter products by commercial signals such as price, sales, category, and revenue, and inspect bestselling products for a store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server uses a PPSPY account API key and makes network requests to PPSPY. <br>
Mitigation: Install only from a trusted PPSPY MCP package source, scope and rotate PPSPY_API_KEY as appropriate, and run it only where outbound PPSPY access is expected. <br>
Risk: Store research queries may contain sensitive or proprietary product and competitor information. <br>
Mitigation: Avoid submitting sensitive store research unless sharing those queries with PPSPY is acceptable for the use case. <br>
Risk: Shopify product search calls consume paid PPSPY account credits. <br>
Mitigation: Monitor credit usage and use focused filters or category listing before broad product searches. <br>


## Reference(s): <br>
- [PPSPY homepage](https://www.ppspy.com) <br>
- [PPSPY API site](https://api.ppspy.com/) <br>
- [ClawHub release page](https://clawhub.ai/fanyanggod/shopify-product) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Markdown or structured text returned from PPSPY MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PPSPY_API_KEY; product search calls consume PPSPY account credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

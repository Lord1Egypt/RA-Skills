## Description: <br>
Search and recommend real fashion products and brands across thousands of online stores via the Vistoya MCP, with natural-language queries, structured filters, similar-item lookup, multi-currency pricing, and merchant links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vistoya](https://clawhub.ai/user/vistoya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to search, compare, and recommend clothing, shoes, bags, jewelry, and accessories from live Vistoya catalog results, then hand users merchant links for buying on retailer sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fashion search terms and filters are sent to Vistoya to retrieve live catalog results. <br>
Mitigation: Use the skill only when the user is comfortable sharing those shopping queries and filters with Vistoya. <br>
Risk: Prices, availability, and merchant links can change after the live catalog response. <br>
Mitigation: Verify final prices, availability, and merchant links on the retailer site before buying. <br>
Risk: Recommendations can mislead users if product details are extrapolated beyond the tool response. <br>
Mitigation: Only show product IDs, prices, brands, and merchant URLs returned by live Vistoya tool results in the current turn. <br>


## Reference(s): <br>
- [Vistoya homepage](https://vistoya.com) <br>
- [Vistoya MCP server](https://api.vistoya.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/vistoya/vistoya-fashion) <br>
- [Vistoya MCP Tool Reference](references/tools.md) <br>
- [Vistoya Workflow Patterns](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown recommendations with product or brand summaries, prices, currencies, and merchant URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Vistoya MCP results; product IDs, prices, and URLs should come from tool responses in the current turn.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

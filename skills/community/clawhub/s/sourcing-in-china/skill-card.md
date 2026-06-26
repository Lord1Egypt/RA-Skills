## Description: <br>
Search products, suppliers, and get detailed product info from Made-in-China.com via MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[witcheng](https://clawhub.ai/user/witcheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External procurement teams, sourcing agents, and developers use this skill to search Made-in-China.com products and suppliers, compare MOQ, pricing, specifications, and supplier signals, and retrieve detailed product information through a disclosed MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and product URLs are sent to a third-party MCP proxy. <br>
Mitigation: Use only non-sensitive sourcing queries and product URLs, and avoid proprietary specifications, product plans, supplier strategy, or other confidential business details. <br>
Risk: Supplier, price, MOQ, badge, and specification data is sourced from public Made-in-China.com pages through the proxy and may be incomplete or outdated. <br>
Mitigation: Verify supplier claims, pricing, MOQ, certifications, and specifications directly with suppliers before procurement decisions. <br>


## Reference(s): <br>
- [China Sourcing Guide](references/sourcing-guide.md) <br>
- [Made-in-China.com MCP endpoint](https://mcp.chexb.com/sse) <br>
- [ClawHub skill page](https://clawhub.ai/witcheng/sourcing-in-china) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product and supplier comparison tables with prices, MOQ, specifications, badges, and direct source links.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

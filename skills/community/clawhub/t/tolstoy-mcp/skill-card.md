## Description: <br>
Connect OpenClaw to Tolstoy's video commerce platform via MCP to create widgets, manage media, generate AI videos, search products, and publish to Shopify, Instagram, and TikTok. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russell-sketch](https://clawhub.ai/user/russell-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and e-commerce operators use this skill to connect OpenClaw to Tolstoy's remote MCP server, then manage Tolstoy widgets, media, products, AI video workflows, publishing, and analytics through natural-language agent interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent OAuth-backed remote MCP connection can manage Tolstoy commerce assets and publish content. <br>
Mitigation: Install only for trusted Tolstoy workspaces, start with a least-privilege or test workspace, and confirm the target account before publish or delete actions. <br>
Risk: The setup script writes a tolstoy MCP server entry into the OpenClaw configuration. <br>
Mitigation: Review the target OpenClaw config path before setup and remove the tolstoy MCP entry or revoke OAuth access when the integration is no longer needed. <br>


## Reference(s): <br>
- [Tolstoy MCP Integration Settings](https://platform.gotolstoy.com/settings/integrations/mcp) <br>
- [Tolstoy Platform](https://platform.gotolstoy.com) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/russell-sketch/tolstoy-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configures a persistent OAuth-backed remote MCP server entry for OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, claw.json, clawhub.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

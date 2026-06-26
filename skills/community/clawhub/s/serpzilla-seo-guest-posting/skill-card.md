## Description: <br>
Skill for SEO promotion by purchasing guest posts on trusted donor websites using the Serpzilla platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanislav-reshetnev](https://clawhub.ai/user/stanislav-reshetnev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO specialists and webmasters use this skill with OpenClaw to search donor sites, manage Serpzilla projects and content, and purchase guest post or link insertion placements through the Serpzilla platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid Serpzilla guest post or link insertion purchases. <br>
Mitigation: Require explicit user confirmation after showing donor site price, current balance, and remaining balance before calling purchase_placement. <br>
Risk: Placement management actions can release funds, cancel work, trigger refunds or forfeiture, or request backlink removal. <br>
Mitigation: Explain the financial or operational impact of each placement action and require explicit user confirmation before calling perform_placement_action. <br>
Risk: The local mcporter setup may store Serpzilla login and API token credentials. <br>
Mitigation: Use a scoped or low-balance Serpzilla account where possible and configure the MCP server only in trusted local environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stanislav-reshetnev/serpzilla-seo-guest-posting) <br>
- [Serpzilla API documentation](https://serpzilla.com/api/) <br>
- [Serpzilla MCP server source](https://github.com/stanislav-reshetnev/serpzilla-mcp-server) <br>
- [Serpzilla MCP server Docker image](https://hub.docker.com/r/stanislavusbest/serpzilla-mcp-stdio-server/tags) <br>
- [SEO Actions for Managing Placements](references/placement_actions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SERPZILLA_LOGIN, SERPZILLA_API_TOKEN, and mcporter configured for the Serpzilla MCP server.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; skill frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Yabbie Net is a safety layer for AI agents that catches unsafe MCP tool calls before they execute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devlines](https://clawhub.ai/user/devlines) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Yabbie Net to route selected MCP server calls through a proxy that can block unsafe tool calls using local rules, optional intent judging, and human escalation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing MCP server calls through a proxy exposes selected tool names and arguments to that proxy and can block or delay calls. <br>
Mitigation: Route only the MCP servers that need protection, review the proxy behavior before sensitive use, and start with tier1 local rules. <br>
Risk: Optional tier2 judging or telemetry can send limited summaries or aggregate metrics outside the local environment when enabled. <br>
Mitigation: Keep tier2 and telemetry disabled unless the data flow is acceptable, and prefer the local Ollama provider when external API routing is not appropriate. <br>
Risk: Installing the external npm package introduces supply-chain risk for sensitive projects. <br>
Mitigation: Pin the package version and verify the package or source before deploying it in sensitive environments. <br>


## Reference(s): <br>
- [Yabbie Net homepage](https://yabbie.net) <br>
- [ClawHub listing](https://clawhub.ai/devlines/yabbie-net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, JSON, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include configuration snippets for MCP server wrapping, tier settings, credentials, and local audit commands.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Connects OpenClaw agents to configured Model Context Protocol servers so they can discover and call external tools through a unified mcp tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure OpenClaw agents for MCP-based tool discovery and execution across external services such as legal search, databases, weather services, and other APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected MCP servers may expose broad external tool access, including tools that read sensitive data or perform state-changing actions. <br>
Mitigation: Install only with trusted MCP servers, restrict access to the mcp tool, prefer read-only or least-privilege server capabilities, and require user confirmation for sensitive actions. <br>
Risk: MCP configuration, tool arguments, tool responses, or diagnostics may contain secrets or sensitive operational data. <br>
Mitigation: Use HTTPS where available, keep dependencies patched, and redact configuration files and logs before sharing diagnostics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-mcp-integration-1-0-0) <br>
- [README](README.md) <br>
- [API Reference](docs/API.md) <br>
- [Configuration Guide](docs/CONFIGURATION.md) <br>
- [Usage Examples](docs/EXAMPLES.md) <br>
- [Real Working Example: kr-legal-search](docs/REAL_EXAMPLE_KR_LEGAL.md) <br>
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, tool-call examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for discovering MCP tools with action=list and invoking configured MCP server tools with action=call.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

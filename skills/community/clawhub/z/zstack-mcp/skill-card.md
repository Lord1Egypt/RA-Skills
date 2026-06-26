## Description: <br>
Integrates OpenClaw with the ZStack Cloud MCP Server so agents can query and execute ZStack APIs with authentication management and read-only default safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xybstone](https://clawhub.ai/user/xybstone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure ZStack MCP access, search and describe ZStack APIs, query virtual machines and monitoring metrics, and run explicitly authorized ZStack API calls through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships configuration that may contain cloud credentials. <br>
Mitigation: Delete bundled credential values before use, rotate any password that could be real, and use a dedicated least-privilege read-only ZStack account or short-lived token. <br>
Risk: The MCP server can be switched from read-only behavior to broad write-capable ZStack API access. <br>
Mitigation: Keep write access disabled unless an operator intentionally enables supervised write operations for a specific environment. <br>
Risk: Credentials may be stored in local skill or mcporter configuration after setup. <br>
Mitigation: Protect or remove stored credentials after use and limit filesystem access to configuration files that contain ZStack account or session data. <br>
Risk: The integration depends on an external MCP package and a configured ZStack endpoint. <br>
Mitigation: Verify the zstack-mcp-server package and the intended ZStack endpoint before connecting an agent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xybstone/zstack-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/xybstone) <br>
- [ZStack MCP Server](https://github.com/zstackio/zstack-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers MCP registration, ZStack API calls, authentication setup, and read-only defaults.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

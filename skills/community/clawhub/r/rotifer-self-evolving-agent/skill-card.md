## Description: <br>
Scans agent capabilities, benchmarks them against Rotifer Arena rankings, and presents stronger upgrade alternatives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit local Rotifer agent capabilities, compare them with Arena rankings, discover alternatives, and apply approved capability upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime MCP server package is fetched with npx and cached locally. <br>
Mitigation: Install only if the Rotifer MCP package is trusted; inspect the package, source, permissions, and npm integrity before use. <br>
Risk: Capability upgrades can modify local Rotifer agent configuration under ~/.rotifer/. <br>
Mitigation: Review the proposed Gene, source, permissions, and expected file changes before approving an upgrade. <br>
Risk: Arena rankings measure performance and do not guarantee safety or suitability. <br>
Mitigation: Treat rankings as performance data and run an independent safety and security review before deploying replacements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoba-dev/rotifer-self-evolving-agent) <br>
- [Rotifer Protocol](https://rotifer.dev) <br>
- [Rotifer Documentation](https://rotifer.dev/docs) <br>
- [Rotifer MCP Server Package](https://www.npmjs.com/package/@rotifer/mcp-server/v/0.8.1) <br>
- [Rotifer MCP Server Source](https://github.com/rotifer-protocol/rotifer-mcp-server) <br>
- [Rotifer Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec) <br>
- [Capability Marketplace](https://rotifer.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with slash-command examples and MCP tool actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend or perform local Gene installation under ~/.rotifer/ after user confirmation.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

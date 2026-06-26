## Description: <br>
Add policy evaluation, human approval, and audit trails to any tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VladUZH](https://clawhub.ai/user/VladUZH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to route MCP tool calls through SidClaw governance, requiring policy evaluation, human approval for high-risk actions, and audit trails for tool activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured tool calls are routed through a third-party governance proxy that can control and audit them. <br>
Mitigation: Install only when SidClaw is an approved governance provider for the environment and limit proxying to intended MCP servers and tools. <br>
Risk: The skill depends on SidClaw API credentials and privacy or retention details are underexplained in the supplied evidence. <br>
Mitigation: Review SidClaw data handling and retention terms, protect and rotate API keys, and keep a rollback copy of the OpenClaw configuration. <br>


## Reference(s): <br>
- [SidClaw Website](https://sidclaw.com) <br>
- [SidClaw Documentation](https://docs.sidclaw.com) <br>
- [SidClaw Dashboard](https://app.sidclaw.com) <br>
- [SidClaw SDK on npm](https://www.npmjs.com/package/@sidclaw/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SidClaw API credentials for governed MCP proxy usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

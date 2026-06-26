## Description: <br>
Configures an MCP-compatible AI agent to create Bitcoin Lightning payment orders, generate invoices, check payment status, and manage SatsRail payment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RubyTuess](https://clawhub.ai/user/RubyTuess) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect MCP-compatible AI agents to SatsRail so the agent can create orders, issue Lightning invoices, and check payment state during conversational commerce workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent create and manage live payment workflows. <br>
Mitigation: Start with test credentials, require explicit user confirmation for payment actions, and enforce amount limits before using live credentials. <br>
Risk: The SatsRail API key could be exposed through shared or committed MCP configuration. <br>
Mitigation: Keep `SATSRAIL_API_KEY` in local environment configuration or a secret manager, and do not commit real `sk_live` credentials. <br>
Risk: The example MCP configuration installs `satsrail-mcp` through `npx`, which may resolve a moving package version. <br>
Mitigation: Review and pin the `satsrail-mcp` package version before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RubyTuess/satsrail-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/RubyTuess) <br>
- [SatsRail MCP GitHub repository](https://github.com/SatsRail/satsrail-mcp) <br>
- [satsrail-mcp npm package](https://www.npmjs.com/package/satsrail-mcp) <br>
- [SatsRail developer docs](https://satsrail.com/developers) <br>
- [SatsRail AI agents guide](https://satsrail.com/developers/ai-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets, shell command examples, and natural-language usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SatsRail API key and MCP client configuration; live payment actions should use explicit confirmation and amount limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

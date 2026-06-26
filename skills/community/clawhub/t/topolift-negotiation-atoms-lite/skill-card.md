## Description: <br>
TopoLift's negotiation dialect for AI agents teaches a public closed vocabulary for interpreting live negotiation reasoning API responses and calling the service through MCP, Bearer key, or x402 micropayment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgeraci](https://clawhub.ai/user/jgeraci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to teach agents how to interpret TopoLift negotiation topology, citation tokens, and strategy vocabulary, then call the TopoLift service through MCP, direct API authentication, or x402 payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Negotiation scenarios and pricing strategy may be sent to TopoLift's third-party service. <br>
Mitigation: Use the skill only when sharing that information with TopoLift is acceptable, and avoid sending confidential negotiation details unless approved. <br>
Risk: Autonomous x402 payments can spend crypto funds if enabled without controls. <br>
Mitigation: Require per-call approval, enforce a strict spend cap, and use a limited-balance wallet. <br>
Risk: The MCP path runs an external topolift-mcp package with an API key. <br>
Mitigation: Verify the package before running it and scope the API key to the minimum needed access. <br>


## Reference(s): <br>
- [TopoLift homepage](https://topolift.ai) <br>
- [Live dialect endpoint](https://api.topolift.ai/v1/dialect) <br>
- [TopoLift API](https://api.topolift.ai) <br>
- [TopoLift MCP server source](https://github.com/TopoLift/topolift-mcp) <br>
- [topolift-mcp on PyPI](https://pypi.org/project/topolift-mcp/) <br>
- [Official MCP registry search](https://registry.modelcontextprotocol.io/v0/servers?search=topolift) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to send negotiation scenarios to a third-party API, use sensitive API credentials, or initiate x402 payments.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

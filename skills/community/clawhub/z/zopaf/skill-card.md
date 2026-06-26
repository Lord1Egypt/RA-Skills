## Description: <br>
Negotiation math engine -- Pareto frontiers, iso-utility counteroffers, and preference inference via MILP optimization. Zero LLM tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rjandino](https://clawhub.ai/user/rjandino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use Zopaf to model multi-issue negotiations, generate Pareto-efficient counteroffer packages, infer counterpart priorities, and analyze deal quality for job offers, term sheets, vendor contracts, real estate, partnerships, and settlements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted MCP use may send sensitive negotiation details, including compensation, legal, procurement, M&A, or fundraising terms, to the configured service. <br>
Mitigation: Use the hosted service only when that data handling is acceptable; for confidential negotiations, prefer a reviewed local-only deployment. <br>
Risk: The package is reported to include under-disclosed Claude-backed web components, telemetry, and session storage for sensitive deal details. <br>
Mitigation: Clarify authentication, retention, telemetry, and Anthropic data handling before using the bundled web API for sensitive matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rjandino/zopaf) <br>
- [Publisher Profile](https://clawhub.ai/user/rjandino) <br>
- [Configured MCP Endpoint](https://zopaf-mcp-production.up.railway.app/mcp) <br>
- [README_MCP.md](artifact/README_MCP.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Configuration] <br>
**Output Format:** [Structured MCP tool responses and concise negotiation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCP configuration for mcp.servers.zopaf; hosted use may send negotiation details to the configured service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Give your agent a real email address, calendar, documents, spreadsheets, file storage, and web search via Tamaton's MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thelaughing-man](https://clawhub.ai/user/thelaughing-man) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Tamaton to give agents hosted productivity tools, including email, calendar, documents, spreadsheets, storage, web search, and billing-aware MCP access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted MCP integration can receive sensitive scopes such as mail sending, storage, calendar access, and billing write access. <br>
Mitigation: Grant only the minimum scopes needed for the agent's task and review scope choices before installation. <br>
Risk: A leaked Tamaton token can expose account data or allow metered usage under the granted scopes. <br>
Mitigation: Store the token only in a secrets manager or environment variable, avoid placing it in URLs or logs, and rotate it if exposure is suspected. <br>
Risk: Billing write access and paid add-ons can allow unexpected spend. <br>
Mitigation: Keep a low spend cap, monitor usage, and avoid enabling paid top-ups or subscriptions unless the agent is intended to use metered features. <br>


## Reference(s): <br>
- [Tamaton documentation](https://tamaton.com/documentation) <br>
- [Tamaton pricing endpoint](https://tamaton.com/api/bots/pricing) <br>
- [Tamaton MCP endpoint](https://tamaton.com/api/mcp) <br>
- [Tamaton A2A agent card](https://tamaton.com/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes curl commands, MCP connection configuration, scope selection, billing controls, and credential handling guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

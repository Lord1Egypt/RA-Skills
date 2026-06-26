## Description: <br>
Hire Spanish-speaking humans for real-world tasks in Latin America. Create missions, browse humans, manage payments, reviews, and disputes through 15 MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GYMTOPZ](https://clawhub.ai/user/GYMTOPZ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to configure and operate the RentaUnHumano MCP server for creating, tracking, and reviewing paid real-world tasks performed by humans in Latin America. <br>

### Deployment Geography for Use: <br>
Latin America and supported Spanish-speaking markets <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create paid real-world tasks and affect payments, cancellations, reviews, disputes, and worker activity. <br>
Mitigation: Use sandbox mode first and require explicit confirmation before paid, bulk, cancellation, review, dispute, or sensitive-location operations. <br>
Risk: Task creation and messaging may share operational details with an external service and human workers. <br>
Mitigation: Use a dedicated API key, limit sensitive task details, and review mission content before sending it to the service. <br>
Risk: The MCP server is installed from an npm package during configuration. <br>
Mitigation: Review or pin the npm MCP server package where possible before enabling it in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/GYMTOPZ/rentaunhumano-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/GYMTOPZ) <br>
- [RentaUnHumano platform](https://rentaunhumano.com) <br>
- [API documentation](https://rentaunhumano.com/docs/api) <br>
- [MCP documentation](https://rentaunhumano.com/docs/mcp) <br>
- [npm MCP server package](https://www.npmjs.com/package/@rentaunhumano/mcp-server) <br>
- [OpenAPI specification](https://rentaunhumano.com/.well-known/openapi.yaml) <br>
- [LLM-friendly documentation](https://rentaunhumano.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text, Markdown] <br>
**Output Format:** [Markdown instructions with bash, JSON, and natural-language task examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and a RENTA_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

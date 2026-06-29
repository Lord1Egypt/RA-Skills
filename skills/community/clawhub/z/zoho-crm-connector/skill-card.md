## Description: <br>
Zoho CRM Connector lets agents search, retrieve, create, update, and delete Zoho CRM leads, contacts, accounts, deals, and module metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, support, and operations teams can use this skill to let agents query CRM records, inspect Zoho CRM schemas, qualify leads, prepare customer context, report on pipeline status, and update records when the appropriate permissions are granted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can delete Zoho CRM records when delete permission is enabled. <br>
Mitigation: Start with read-only permissions, grant delete only for specific workflows, and require explicit human confirmation before deleting CRM records. <br>
Risk: Write actions can create or update CRM records with incorrect or excessive data. <br>
Mitigation: Grant add and edit permissions only for workflows that need them, keep tool inputs scoped to the minimum required fields, and review returned warnings or validation failures before retrying. <br>
Risk: CRM credentials or payment-related secrets could be exposed through prompts or logs. <br>
Mitigation: Use the setup skills for credential handling and do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [Zoho CRM Connector marketplace page](https://www.agentpmt.com/marketplace/zoho-crm-connector) <br>
- [Zoho CRM Connector on ClawHub](https://clawhub.ai/agentpmt/skills/zoho-crm-connector) <br>
- [AgentPMT account MCP/REST setup on ClawHub](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is on ClawHub](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT main MCP server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request examples and action schema references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes AgentPMT-hosted Zoho CRM actions and their permission gates; tool responses are returned as JSON by the connected service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

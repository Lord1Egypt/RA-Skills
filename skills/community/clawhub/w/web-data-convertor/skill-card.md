## Description:

Converts data between JSON, CSV, XML, YAML, Markdown, HTML, query strings, and Unix timestamps through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert web and application data between API, configuration, documentation, URL, and timestamp formats through AgentPMT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted input data is sent to AgentPMT-hosted processing.

Mitigation: Do not submit secrets, credentials, private keys, regulated data, or confidential business documents unless that processing has been approved.

Risk: Related setup steps may affect account, credential, or payment handling.

Mitigation: Use reviewed ClawHub setup skills or pinned setup commands and keep credentials out of prompts and logs.

## Reference(s):

- [Web Data Convertor schema](./schema.md)
- [Web Data Convertor ClawHub page](https://clawhub.ai/agentpmt/skills/web-data-convertor)
- [Web Data Convertor marketplace page](https://www.agentpmt.com/marketplace/web-data-convertor)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON responses containing converted data, errors, or status fields; converted content may be JSON, CSV, XML, YAML, HTML, Markdown, query strings, or date strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inputs are submitted as action-specific text parameters; schema.md lists 11 supported actions and required fields.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

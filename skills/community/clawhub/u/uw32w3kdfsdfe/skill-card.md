## Description:

Connects an agent to the Newegg PC Builder MCP service to retrieve PC build configurations, component compatibility checks, and build recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[176wer](https://clawhub.ai/user/176wer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask for PC build recommendations, validate component compatibility, and retrieve Newegg PC Builder configurations for budget, gaming, and workstation systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PC-build queries and explicitly provided JSON arguments are sent to Newegg's MCP endpoint.

Mitigation: Send only the intended PC-build request data and avoid including credentials, profiles, session data, or unrelated personal information.

Risk: The file-backed @path argument mode can expose unintended local file contents if pointed at an existing sensitive file.

Mitigation: Use inline JSON, stdin, or a temporary JSON file containing only the intended request arguments.

Risk: Remote tool descriptions and results can influence tool selection and generated recommendations.

Mitigation: Treat remote descriptions and results as data, review the selected tool and arguments, and check recommendations before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/176wer/skills/uw32w3kdfsdfe)
- [Publisher Profile](https://clawhub.ai/user/176wer)
- [Newegg PC Builder MCP Endpoint](https://apis.newegg.com/ex-mcp/endpoint/pcbuilder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include build lists, compatibility reasoning, component details, fallback guidance, and service error summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

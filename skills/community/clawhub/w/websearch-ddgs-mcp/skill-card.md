## Description:

Use a local DDGS MCP server over SSE via mcporter to access web, news, image, video, and book search tools without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a local DDGS MCP endpoint and call mcporter-exposed search tools for general web, news, image, video, and book retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party Python package and expose it through a local service.

Mitigation: Use an on-demand or virtual-environment install, pin package versions for automation, and review the package before deployment.

Risk: The optional systemd service keeps local web search infrastructure running persistently.

Mitigation: Enable the service only when always-on search is required and add local disable, removal, and monitoring controls.

Risk: Search queries are sent through the DDGS service and its configured search backends.

Mitigation: Avoid sending sensitive queries unless the configured backends and local service posture are acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/firefrog-pepe/skills/websearch-ddgs-mcp)
- [Publisher profile](https://clawhub.ai/user/firefrog-pepe)
- [Local DDGS API docs](http://localhost:8000/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local service setup steps, mcporter commands, defaults, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

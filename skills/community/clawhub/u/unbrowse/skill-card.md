## Description:

Guides agents in finding and using website tools through Unbrowse, reading pages, and completing tasks with its hosted browser and saved sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unbrowse](https://clawhub.ai/user/unbrowse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can search for reusable website tools, read public or authenticated pages, and carry out authorized website tasks through Unbrowse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website tasks and saved-login workflows route through the Unbrowse service.

Mitigation: Use the service only for sites and sessions you are comfortable sharing with Unbrowse; prefer the remote MCP or a reviewed, pinned client version.

Risk: Agents can perform external writes or purchases through website tools.

Mitigation: Require explicit user authorization before posting, sending, purchasing, or making other external changes; verify the result before reporting success.

Risk: API keys, credentials, and HAR recordings may contain sensitive information.

Mitigation: Store API keys in a secret manager, use the saved-login handoff instead of chat for credentials, and submit only authorized HAR recordings.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/unbrowse/skills/unbrowse)
- [Unbrowse MCP endpoint](https://unbrowse.ai/mcp)
- [Unbrowse client installation guide](https://github.com/unbrowse-ai/unbrowse-skill#readme)
- [Core MCP tool schemas](references/tools.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown guidance and website tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on website access, saved sessions, and the available tools.]

## Skill Version(s):

12.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

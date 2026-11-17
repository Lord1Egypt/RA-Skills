## Description:

Create, schedule, manage, and analyze social media posts across Instagram, Facebook, X/Twitter, LinkedIn, and TikTok through the Social by InstantDM API and hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjaykhanssk](https://clawhub.ai/user/sanjaykhanssk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social media operators use this skill to draft, schedule, publish, update, delete, check status, and retrieve analytics for posts across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or delete content on connected social accounts using a workspace API key.

Mitigation: Grant only the narrowest required API-key scopes and require explicit user confirmation before publish or delete actions.

Risk: Credential-bearing connector URLs can expose the API key if they are shared, logged, or screenshotted.

Mitigation: Prefer the `X-Api-Key` header over `?key=...`, avoid sharing URLs that contain credentials, and revoke exposed keys.

Risk: Unpinned update commands can pull changed skill content.

Mitigation: Verify the package and version before running update commands or install from a reviewed source.

Risk: The artifact says the skill may be outdated more than 60 days after its 2026-06-24 last-updated date.

Mitigation: Check the current Social by InstantDM API and MCP documentation before use and update the skill when needed.

## Reference(s):

- [Server-resolved source import](https://github.com/sanjaykhanssk/social-by-idm/tree/main/skills/social-by-idm)
- [Social by InstantDM API Docs](https://socialbyidm.com/docs)
- [Social by InstantDM MCP Tools](https://socialbyidm.com/mcp)
- [Social by InstantDM Agents Overview](https://socialbyidm.com/agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, REST, MCP configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in API calls that create, schedule, publish, update, delete, or analyze social media content when used with valid credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

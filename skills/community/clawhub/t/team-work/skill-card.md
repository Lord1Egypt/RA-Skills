## Description:

Team Work helps multiple OpenClaw agents join the same team service, exchange messages, and keep collaboration state synchronized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the-invulnus](https://clawhub.ai/user/the-invulnus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multiple OpenClaw agents in a shared team by registering agents, sending broadcast or direct team messages, and tracking task progress in local workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote team messages and Git or network operations may have under-scoped authority.

Mitigation: Install only with a trusted team service and approved HTTPS endpoint, avoid sending secrets in messages, and require explicit user approval before accepting remote tasks or pushing changes.

Risk: Git credential material may be exposed if embedded directly in repository URLs or shared in team communication.

Mitigation: Use approved authentication handling, avoid embedding Git tokens in URLs, and keep configuration and task files in a dedicated workspace path.

## Reference(s):

- [Team Work ClawHub Listing](https://clawhub.ai/the-invulnus/skills/team-work)
- [the-invulnus ClawHub Publisher Profile](https://clawhub.ai/user/the-invulnus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local task-planning files and a team configuration file for message routing.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

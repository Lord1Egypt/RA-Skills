## Description:

Helps agents manage Wrike project work, team resources, and administrative tasks through a connected account, with approval required before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Project teams and administrators use this skill to review and manage Wrike tasks, folders, projects, spaces, time logs, and team resources. Sensitive administrative and automation actions require specific user intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected account may expose sensitive Wrike data or allow broad access.

Mitigation: Use narrow, preferably read-only OAuth scopes; retrieve only needed data and delete unused connections.

Risk: Writes, administrative actions, and exports can change account governance or disclose organizational data.

Mitigation: Confirm the target and intended effect before each write, admin action, or export; default to read-only requests.

Risk: Automation destinations may continuously forward event data to third parties.

Mitigation: Require separate approval for each destination, verify the recipient and ongoing data flow, and remove unused triggers and destinations.

## Reference(s):

- [Wrike skill on ClawHub](https://clawhub.ai/byungkyu/skills/wrike-api)
- [Maton](https://maton.ai)
- [Wrike API documentation](https://developers.wrike.com/)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Wrike account and network access; confirm changes before execution.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

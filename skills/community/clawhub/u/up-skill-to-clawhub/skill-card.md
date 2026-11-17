## Description:

Package and publish OpenClaw skills to ClawHub registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonakic](https://clawhub.ai/user/tonakic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to package, sanitize, version, and publish OpenClaw skills to the ClawHub registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing requires the agent to inspect and edit a target skill folder.

Mitigation: Review the exact files and diffs before publication.

Risk: The documented ClawHub login flow uses tokens and mutable CLI execution.

Mitigation: Use a pinned ClawHub CLI version and avoid passing tokens directly on the command line.

Risk: Sensitive data scanner output may contain secrets.

Mitigation: Treat scanner output as sensitive and avoid sharing or logging it unnecessarily.

## Reference(s):

- [Configuration template](references/config.template.json)
- [ClawHub skill page](https://clawhub.ai/tonakic/skills/up-skill-to-clawhub)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese publishing workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

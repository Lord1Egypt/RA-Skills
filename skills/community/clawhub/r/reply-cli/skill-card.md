## Description:

Manage Reply.io sequences, contacts, email accounts, schedules, and campaign statistics from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grizzlyzp1](https://clawhub.ai/user/grizzlyzp1)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and revenue operations teams use this skill to ask an agent for Reply.io CLI commands and setup guidance for viewing outreach performance, managing contacts, enrolling contacts, and controlling sequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned npm package with npx, which can resolve package code at runtime.

Mitigation: Prefer a pinned or preinstalled reviewed reply-cli package before use.

Risk: Reply.io API key exposure could allow unauthorized account access.

Mitigation: Use a narrowly scoped REPLY_API_KEY, store it in an environment variable or Docker secret, and avoid hardcoding or logging it.

Risk: CLI commands can start or pause sequences, create contacts, and change sequence enrollment.

Mitigation: Require explicit user approval before commands that change campaigns, contacts, or enrollment.

## Reference(s):

- [Reply.io](https://reply.io)
- [Reply.io API Settings](https://run.reply.io/Dashboard/Material#/settings/api)
- [ClawHub Skill Page](https://clawhub.ai/grizzlyzp1/skills/reply-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses REPLY_API_KEY for authenticated Reply.io CLI operations and favors --json or --pretty output when the agent needs parseable results.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

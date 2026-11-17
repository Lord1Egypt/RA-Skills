## Description:

Helps agents access Slack through Maton to search conversations, manage channels, send messages, and automate approved workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to find Slack information, communicate in channels, and set up approved Slack automations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing a Slack connection or performing writes could grant access or change workspace content beyond the user's intent.

Mitigation: Authorize Slack only when requested; confirm each write, connection, and function deployment, and use the narrowest available scopes.

Risk: Triggers or destinations could continuously forward sensitive event data.

Mitigation: Keep triggers narrowly scoped, review each destination and its data flow, and obtain separate approval before enabling ongoing forwarding.

Risk: A raw Maton API key may be exposed through logs or local processes.

Mitigation: Prefer CLI login; use a raw API key only when the CLI cannot be installed, and never print or persist the key.

## Reference(s):

- [Slack trigger reference](references/slack/triggers.md)
- [Slack API methods](https://docs.slack.dev/reference/methods)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarize only the Slack data needed for the user's task.]

## Skill Version(s):

1.2.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Slack bot API integration with managed OAuth for Slack workspace automation, including messaging, channel and member management, files, user groups, scheduled messages, search, reactions, pins, reminders, calls, and canvases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to automate Slack messaging, search workspace content, manage channels and users, handle files, and coordinate Slack workspace objects through ClawLink-managed OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad Slack workspace read and write access, including message history, user data, files, channel administration, posting, and destructive operations.

Mitigation: Install only in trusted workspaces, review the live plugin source and OAuth scopes before use, and grant the least Slack permissions that still support the intended workflow.

Risk: Sensitive read operations are described in the artifact as confirmation-free.

Mitigation: Require user confirmation before searches, message history reads, user lookups, file downloads, public sharing, posting, membership changes, or deletes.

Risk: The server-resolved provenance is unavailable for this release.

Mitigation: Treat the release as third-party code and verify provenance through ClawHub and ClawLink before deploying it in a production Slack workspace.

## Reference(s):

- [Slack API Docs](https://api.slack.com/docs)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=slackbot)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [Slackbot ClawHub Page](https://clawhub.ai/hith3sh/skills/slackbot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls, JSON]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Slack read, write, and destructive operations through ClawLink tools depending on user request and granted workspace permissions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

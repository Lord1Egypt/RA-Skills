## Description:

Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hfarazi](https://clawhub.ai/user/hfarazi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent workflows use this skill to create, update, complete, abandon, list, and attach files to TickTick tasks and projects through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI persists OAuth credentials, refresh tokens, and optional browser-session cookies in plaintext.

Mitigation: Treat the TickTick config file as highly sensitive, keep restrictive file permissions, and avoid storing a browser session cookie unless attachment upload is necessary.

Risk: Attachment upload uses a TickTick browser-session cookie and can upload local files to tasks.

Mitigation: Require explicit user approval before file uploads and avoid passing real client secrets or session values on the command line.

Risk: Bulk abandon operations can modify multiple TickTick tasks with limited guardrails.

Mitigation: Require explicit user approval before bulk task changes and verify task IDs with JSON task listings before execution.

## Reference(s):

- [TickTick Developer Center](https://developer.ticktick.com/manage)
- [TickTick Open API](https://developer.ticktick.com/api)
- [ClawHub Skill Page](https://clawhub.ai/hfarazi/skills/ticktickpower)
- [Publisher Profile](https://clawhub.ai/user/hfarazi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI supports machine-readable JSON output for task and project operations.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Pushes task execution results to a mobile Today-screen card and supports both immediate and scheduled task-result pushes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingjiang](https://clawhub.ai/user/pingjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send concise task summaries, success or failure status, and detailed result content to a phone-facing Today-screen card. It is intended for both user-triggered pushes and scheduled task-result notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled task results may be pushed automatically without confirmation.

Mitigation: Use only where automatic result sharing is intended, and add a confirmation or policy gate before sending scheduled-task outputs.

Risk: Task content or authentication data may expose secrets or private information, especially when debug logging is enabled.

Mitigation: Avoid sending secrets or private content, keep DEBUG disabled, and configure only trusted HTTPS API endpoints.

Risk: Shell-based invocation may be vulnerable if untrusted parameter values are interpolated into commands.

Mitigation: Review the command path before installation and prefer an argument-safe invocation that does not rely on shell interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pingjiang/skills/push2today)
- [Metadata homepage](https://github.com/your-name/push2today)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with CLI command arguments and JSON API payload content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and AS_TODAY_AUTH_CODE; summary is limited to 64 characters and content is limited to 30717 characters.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

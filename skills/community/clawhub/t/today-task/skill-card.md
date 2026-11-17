## Description:

Universal task result pusher that sends completed task results to Minus One Screen using a standard data format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganhaiyang3](https://clawhub.ai/user/ganhaiyang3)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to package task names, Markdown task content, execution results, and task metadata into JSON and push them to a configured Minus One Screen endpoint. It is intended for agents that need a repeatable way to notify a user when a task completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization codes and task content are sent to the configured push endpoint.

Mitigation: Use only a trusted HTTPS endpoint, set credentials through OpenClaw configuration, and avoid including highly sensitive content in pushed tasks.

Risk: Task content and service responses may be stored locally in logs or push records.

Mitigation: Review local record settings, disable record saving when appropriate, and periodically clear logs and push records.

Risk: Automatic update checks may run ClawHub inspection commands after a push.

Mitigation: Disable or adjust update checks if post-push ClawHub inspection is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ganhaiyang3/skills/today-task)
- [Publisher Profile](https://clawhub.ai/user/ganhaiyang3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON task payloads, Markdown task content, shell commands, and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authCode and pushServiceUrl; task content is sent to the configured endpoint and run records may be stored locally.]

## Skill Version(s):

1.0.17 (source: server release evidence and artifact/version.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

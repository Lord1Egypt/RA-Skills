## Description:

This skill helps agents send signed requests to TencentDB DatabaseClaw and receive streaming responses from the CreateChatCompletion SSE API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate TencentDB DatabaseClaw into agent workflows, send database analysis prompts, parse SSE responses, and validate that a DatabaseClaw instance is reachable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can receive long-lived Tencent Cloud credentials through command-line arguments.

Mitigation: Use least-privilege, short-lived credentials where possible and avoid exposing secrets in shell history, process listings, logs, or shared terminals.

Risk: Database-related prompts and results may be sent to the remote DatabaseClaw service.

Mitigation: Avoid sending sensitive data unless that data is intended for DatabaseClaw processing and the deployment has appropriate approval.

Risk: Session creation is enabled by default, which can make conversations visible in the TencentDB console session list.

Mitigation: Use the documented --no-session option when console-visible sessions are not desired.

## Reference(s):

- [Python Integration Reference](references/python-integration.md)
- [TencentDB DatabaseClaw Console](https://console.cloud.tencent.com/tdai/claw/instance)
- [TencentDB DatabaseClaw Skill](https://clawhub.ai/tencent-adm/skills/tencentdb-databaseclaw-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python examples; the bundled CLI streams plain text responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in single-message or interactive mode; verbose mode sends tool-call and reasoning details to stderr.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

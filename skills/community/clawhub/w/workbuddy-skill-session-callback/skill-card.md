## Description:

WorkBuddy Desktop session callback skill that helps an agent wake a specified WorkBuddy session and inject a trusted message so that the target agent can continue with its existing context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onesfuture](https://clawhub.ai/user/onesfuture)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy Desktop users use this skill to notify, wake, or hand work back to a known target session after monitoring, scheduled automation, asynchronous task completion, or multi-session collaboration events. It is specific to WorkBuddy Desktop and is not intended for openclaw, CodeBuddy CLI, or other agent platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-session message injection can cause the target agent to act on unintended instructions with its existing context.

Mitigation: Inject only trusted notification-style content, label callback messages as external notifications, and require the target session to confirm before sensitive actions.

Risk: Callback data can be sent to arbitrary endpoints if a remote or non-loopback endpoint is supplied.

Mitigation: Use only local loopback endpoints and avoid remote or non-loopback --endpoint values.

Risk: Broad or dynamic targeting can wake the wrong WorkBuddy session.

Mitigation: Use explicit target session UUIDs and fixed allowlists where possible.

Risk: Temporary automation can leave an ongoing cross-session channel after the original task is complete.

Mitigation: Remove temporary automations after use and return WorkBuddy to its normal session isolation posture.

## Reference(s):

- [WorkBuddy session callback ACP protocol reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of a local Python callback script, WorkBuddy automation configuration, and loopback ACP requests when the user supplies a target session ID and callback message.]

## Skill Version(s):

1.0.5 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

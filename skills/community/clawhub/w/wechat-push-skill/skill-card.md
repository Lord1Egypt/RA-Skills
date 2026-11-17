## Description:

Helps a local agent send proactive single-recipient WeChat text messages through OpenClaw, including messaging beyond WeChat's 24-hour customer-service window, verification, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billllx](https://clawhub.ai/user/billllx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and operate proactive WeChat text push for notifications, alerts, and task-completion messages. It also guides verification of the delivery path and troubleshooting of account, openid, session, and false-success failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables proactive WeChat messaging beyond the documented 24-hour customer-service window.

Mitigation: Use it only with an OpenClaw WeChat account you control, for recipients you are authorized to message, and after accepting the platform and account risks.

Risk: The skill reads local OpenClaw account and context-token files to select a bot account.

Mitigation: Treat OpenClaw account and context-token files as sensitive local data and avoid exposing them in logs, prompts, screenshots, or shared support output.

Risk: Optional recurring silent probes can create ongoing account activity and unexpected cron behavior.

Mitigation: Enable probe cron only when needed, review OpenClaw cron entries after installation, and remove or adjust probes that are not required.

Risk: A command-level success can still fail to mean the user received the message.

Mitigation: Run the provided verification and doctor commands, and confirm delivery on the recipient phone for important messages.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/billllx/skills/wechat-push-skill)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Protocol notes](references/protocol-notes.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, verification, troubleshooting, and single-message push command guidance; messages are single-recipient text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

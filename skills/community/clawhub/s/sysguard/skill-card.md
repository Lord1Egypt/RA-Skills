## Description:

SysGuard provides IM-friendly OpenClaw system monitoring, health checks, diagnostics, trend reports, alerts, and cache cleanup through Bash commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steventsang18](https://clawhub.ai/user/steventsang18)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators and operators use SysGuard to check host health, inspect Gateway status, generate diagnostics, view short text trend charts, receive configured webhook alerts, and clean selected caches from IM conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broadly available chat commands can trigger system cleanup or long-running monitoring.

Mitigation: Deploy only in an admin-controlled OpenClaw environment and restrict who can send SysGuard commands; disable or gate sgc and sgm unless needed.

Risk: A temporary configuration fallback can expose or weaken control over SysGuard settings.

Mitigation: Use a private configuration path with 0600 permissions instead of any /tmp fallback.

Risk: Webhook alerts can send host status information outside the machine.

Mitigation: Configure only trusted Feishu or WeCom webhooks and treat alert content as operational data.

Risk: Cleanup commands may remove files or logs that operators still need.

Mitigation: Run cleanup under a dedicated unprivileged account and review retention settings before enabling chat-triggered cleanup.

## Reference(s):

- [SysGuard ClawHub page](https://clawhub.ai/steventsang18/skills/sysguard)
- [Steventsang18 ClawHub profile](https://clawhub.ai/user/steventsang18)
- [SysGuard project homepage](https://github.com/Steventsang18/sysguard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [IM-friendly text and Markdown status panels, diagnostic reports, trend charts, alert messages, and inline shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON history and log files, and may send configured Feishu or WeCom webhook notifications.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

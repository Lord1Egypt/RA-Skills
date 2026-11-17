## Description:

Send native Windows desktop notifications for local reminders, alerts, and background-attention events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougzl](https://clawhub.ai/user/dougzl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send local desktop notifications for reminders, timers, schedule alerts, notification tests, and attention-needed events when chat-only delivery may be missed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency installation can fetch npm packages during first use.

Mitigation: Install only in a reviewed environment; prefer a release that preinstalls pinned dependencies with npm ci and disables lifecycle scripts where possible.

Risk: The Windows WPF path invokes PowerShell with execution-policy bypass.

Mitigation: Limit activation to explicit local notification requests on trusted Windows hosts and review the PowerShell command path before deployment.

Risk: Notification content may be visible on the local desktop.

Mitigation: Keep titles and messages concise and avoid including secrets or sensitive data in notification text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dougzl/skills/windows-notifier)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local notification invocation guidance; notification display behavior depends on the host operating system and available Windows WPF support.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact package metadata reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

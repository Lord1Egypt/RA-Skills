## Description:

Keep the OpenClaw gateway alive 24/7 on Windows — install a hidden auto-restart watchdog, cure the SQLite snapshot cleanup failure, kill zombie port listeners, survive logon-only persistence, and diagnose slow starts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wq920809](https://clawhub.ai/user/wq920809)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows administrators use this skill to diagnose OpenClaw gateway startup and persistence problems, configure an automatic restart watchdog, and inspect gateway processes and ports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog can clear safety-related settings.

Mitigation: Preserve deletion safeguards before enabling autostart.

Risk: Forced shutdowns can stop unrelated services.

Mitigation: Verify that a listener belongs to the gateway before forcibly stopping its process.

Risk: Incorrect custom directory or port settings can target the wrong gateway resources.

Mitigation: Check the configured gateway directory and port before installing or starting the watchdog.

Risk: The Startup entry can continue launching the watchdog at future logins.

Mitigation: Remove the Startup entry to prevent future launches when autostart is no longer wanted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wq920809/skills/windows-gateway-sentinel)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with PowerShell, batch, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Guides VPS owners through diagnosing and reducing OpenClaw gateway out-of-memory restarts on low-memory servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

VPS owners and administrators use this skill to investigate OOM-related gateway restarts on 1–2 GB servers and, with their approval, reduce concurrency, add swap, or adjust gateway OOM protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to the OpenClaw configuration and swap settings can disrupt the gateway or affect server startup.

Mitigation: Confirm VPS ownership and consent, back up configuration and /etc/fstab, and validate changes before restarting.

Risk: Unnecessary swap or OOM-protection changes can mask a different cause of instability.

Mitigation: Check memory usage and OOM logs first; make changes only when low-memory or OOM symptoms are confirmed.

Risk: The instructions are in Vietnamese and could be misunderstood before approving privileged commands.

Mitigation: Read them carefully or obtain an accurate translation and review the planned changes before execution.

## Reference(s):

- [vps-lite-boot on ClawHub](https://clawhub.ai/thinhbuiii/skills/vps-lite-boot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic checks and before-and-after measurements.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

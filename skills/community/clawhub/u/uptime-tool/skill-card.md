## Description:

Show local system uptime for health checks, reboot verification, and basic diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to check how long a local Linux host has been running and to support reboot verification or basic system diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises options and cross-platform behavior that the included implementation may not support.

Mitigation: Verify required command-line options and platform behavior before using this skill in monitoring or automation.

## Reference(s):

- [ClawHub Uptime Tool release](https://clawhub.ai/dinghaibin/skills/uptime-tool)
- [dinghaibin publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text uptime summary, with Markdown shell command examples in skill guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local /proc/uptime and reports elapsed days, hours, and minutes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides a Spanish-language procedure for switching and verifying OpenClaw Docker sandbox modes for development and security work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsmartinez99](https://clawhub.ai/user/jsmartinez99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this Spanish-language SOP to select, apply, verify, and restore OpenClaw sandbox modes during testing or audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing the wrong environment or corrupting openclaw.json can disrupt operations.

Mitigation: Confirm the target environment and verify a configuration backup before changing the sandbox mode; restore the backup and escalate if the gateway fails.

Risk: Restarting the gateway may interrupt active sessions.

Mitigation: Plan for the interruption and check gateway status after the restart.

Risk: The sandbox may remain in an unintended mode after the task.

Mitigation: Restore the intended mode when work ends and verify the resulting configuration and gateway status.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-language SOP]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

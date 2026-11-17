## Description:

Control a ratgdo32 disco garage door opener over its local web API, including door, light, obstruction, vehicle presence, parking assist, motion, and remote lockout actions on a LAN-only trust model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bolander72](https://clawhub.ai/user/bolander72)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to check garage status and issue local garage door, light, vehicle sensor, and remote lockout commands through a ratgdo32 disco device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a physical garage door, including high-impact actions such as door movement and remote lockout.

Mitigation: Install only where agent control of the garage door is acceptable, require explicit user confirmation for door movement and remote lockout, and keep the device off the public internet.

Risk: A close command can be unsafe if status data is invalid or incomplete.

Mitigation: Harden execution so closing fails closed unless valid status explicitly confirms there is no obstruction.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bolander72/skills/ratgdo32-disco)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local HTTP commands against the configured RATGDO_HOST device.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Guides developers through the Xianmu Box project's requirements, implementation, simulation, device debugging, deployment, and documentation workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaokingsoft](https://clawhub.ai/user/miaokingsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working on the Xianmu Box repository use this skill to plan and implement features or fixes, test interface changes, diagnose hardware issues, and deploy to devices with project-specific checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device deployment can replace settings.json and lose WiFi, alarm, or cloud activation settings.

Mitigation: Back up the device settings.json before deployment and verify it has been restored afterward.

Risk: Using the wrong serial port or firmware target can disrupt the device or erase its filesystem.

Mitigation: Confirm the target serial port and device before deployment or firmware flashing; restore application files and settings after filesystem-erasing changes.

## Reference(s):

- [Source skill (server-resolved GitHub import)](https://github.com/miaokingsoft/XianMuBox/tree/main/skills/xianmubox-dev)
- [ClawHub skill release](https://clawhub.ai/miaokingsoft/skills/xianmubox-dev)
- [Coding rules](https://github.com/miaokingsoft/XianMuBox/blob/main/skills/xianmubox-dev/references/coding-rules.md)
- [Device debugging guide](https://github.com/miaokingsoft/XianMuBox/blob/main/skills/xianmubox-dev/references/device-debug.md)
- [Toolchain guide](https://github.com/miaokingsoft/XianMuBox/blob/main/skills/xianmubox-dev/references/toolchain.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific workflow with simulation, testing, and deployment checks.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

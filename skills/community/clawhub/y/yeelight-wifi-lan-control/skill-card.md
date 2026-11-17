## Description:

Discover, control, organize, and troubleshoot Yeelight WiFi lights over the local network, including rooms, groups, scenes, recovery, and host-managed schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeelight](https://clawhub.ai/user/yeelight)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI assistant to manage Yeelight WiFi lights on their local network can discover devices, adjust lighting, organize rooms and groups, save scenes, and set up host-managed schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local commands can change lighting or stored home settings.

Mitigation: Review and confirm writes, schedules, recovery, music mode, and store resets before execution.

Risk: A device acknowledgement or partial scene application may not reflect the visible state of every light.

Mitigation: Check reported verification and uncertain or skipped devices before retrying or recovering.

Risk: Some responses and confirmation text may be in Chinese.

Mitigation: Confirm the intended action and affected devices before approving changes.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yeelight/skills/yeelight-wifi-lan-control)
- [Yeelight WiFi Light Inter-Operation Specification](https://www.yeelight.com/download/Yeelight_Inter-Operation_Spec.pdf)
- [Workflow](artifact/references/workflow.md)
- [Local home](artifact/references/local-home.md)
- [Scenes and recovery](artifact/references/scenes.md)
- [Scheduling](artifact/references/scheduling.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Concise text and structured host scheduling requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports device-level results and verification status; does not guarantee visible light state.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

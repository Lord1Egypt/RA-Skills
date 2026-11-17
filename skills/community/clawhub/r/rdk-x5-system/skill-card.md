## Description:

Guides RDK X5 administrators through system configuration tasks including version and log checks, backup and restore, OTA and miniboot updates, CPU/BPU frequency tuning, boot configuration, RT kernel switching, systemd autostart, and storage expansion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, device administrators, and robotics engineers use this skill to plan and review privileged RDK X5 system-management commands before changing firmware, boot behavior, CPU/BPU settings, services, or storage. It is intended for users administering an RDK X5 device, not for unrelated network, camera, AI inference, NAS, Docker, or application-development tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged system commands can change firmware, packages, boot settings, services, and storage on an RDK X5 device.

Mitigation: Review each sudo command before running it and use the skill only when administering an intended RDK X5 device.

Risk: Firmware or apt upgrades and miniboot changes can affect device bootability or installed software.

Mitigation: Run upgrades only when planned, avoid firmware downgrades, and keep a verified backup before firmware or package changes.

Risk: Enabling a systemd service makes it start automatically at boot.

Mitigation: Inspect the service file and ExecStart target before enabling or starting the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/skills/rdk-x5-system)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands often require sudo and should be reviewed before execution on the target RDK X5 device.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

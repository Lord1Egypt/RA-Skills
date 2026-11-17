## Description:

Helps configure VSD Craft keys, knobs, scenes, and pages; install or update plugins; back up settings; and troubleshoot USB or KVM recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

VSD Craft users and support teams use this skill to configure built-in controls, maintain plugins and settings, and diagnose device reconnection problems while preserving a path to restore previous configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plugin or settings changes could affect the wrong installation or overwrite existing configurations.

Mitigation: Confirm the active data folder in the application, make timestamped backups, and review proposed plugin or cache changes before applying them.

Risk: Shared troubleshooting materials could expose personal profiles, device IDs, logs, or credentials.

Mitigation: Exclude private configuration contents and identifiers from shared artifacts; use the read-only inventory for structural checks.

## Reference(s):

- [VSD Craft Operations release](https://clawhub.ai/nextaltair/skills/vsd-craft-operations)
- [Operational findings and scope](references/operations.md)
- [Verification sheet](references/verification.md)
- [VSD Stream Dock user manual](https://cdn.shopify.com/s/files/1/0657/8690/4620/files/VSD_Stream_Dock___User_Manual___English_b4c5939a-dad2-4e31-8b0e-54f79f983fde.pdf?v=1777109994)
- [Official plugin installation guide](https://www.vsdinside.com/blogs/tutorial/plugin-download)
- [StreamDock local development guide](https://sdk.key123.vip/en/guide/get-started.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with optional shell commands and JSON inventory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification status and backup or restoration instructions when applicable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

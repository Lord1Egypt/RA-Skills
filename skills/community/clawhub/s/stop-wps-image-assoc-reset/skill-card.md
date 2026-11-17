## Description:

Permanently prevents WPS Office from repeatedly taking over image file associations and helps users restore control of their default image viewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibiubiu233i](https://clawhub.ai/user/ibiubiu233i)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and support engineers use this skill to identify and disable WPS Office mechanisms that reset image-file defaults, then manually choose their preferred image viewer in Windows settings. It is intended for systems where the user accepts the impact of changing scheduled tasks, registry entries, and WPS image-viewer files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently alter Windows registry state, scheduled tasks, and WPS installation files.

Mitigation: Review each detected task, registry key, and file before changing it, and keep backups or a restore plan.

Risk: Broad WPS task and file matching could affect WPS functionality or unrelated items with similar names.

Mitigation: Verify that each target belongs to the WPS image-viewer component before disabling, deleting, or renaming it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ibiubiu233i/skills/stop-wps-image-assoc-reset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows scheduled-task, registry, file-operation, and manual default-app instructions that may require administrator privileges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

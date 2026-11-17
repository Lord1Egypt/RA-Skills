## Description:

Opens a standalone HTML demo or unbundled static web project in a connected VibePolish workbench for visual editing and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenfang055-gif](https://clawhub.ai/user/shenfang055-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to open a standalone HTML page or static web project in VibePolish for visual editing and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opened project code may access files or trigger writes within the selected project through the visual editor.

Mitigation: Open only trusted projects and avoid directories containing credentials, private keys, or unrelated sensitive files.

Risk: Save, apply, or rollback actions may change project files.

Mitigation: Commit or back up the project before using save, apply, or rollback features.

## Reference(s):

- [VibePolish ClawHub release](https://clawhub.ai/shenfang055-gif/skills/vibepolish-202610)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with the launcher command and opened address]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the CDP port and, when available, the project port; keeps the browser session open.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

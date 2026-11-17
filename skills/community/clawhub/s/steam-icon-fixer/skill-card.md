## Description:

Fix missing or generic Steam game desktop icons on Linux by finding the Steam app ID from local launchers and installing replacement artwork into the user's icon theme.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunarmoon26](https://clawhub.ai/user/lunarmoon26)

### License/Terms of Use:

MIT-0

## Use Case:

Linux Steam users and support agents use this skill to find Steam app IDs from local launcher metadata, install replacement icon artwork, and refresh the desktop icon cache when Steam game shortcuts show missing or generic icons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled installer may overwrite existing steam_icon_<appid>.png files under the user's icon theme.

Mitigation: Confirm the Steam app ID and image path before installation, and use explicit icon directories when working outside the default user icon theme.

Risk: The skill reads local Steam desktop launchers and may refresh the icon cache after writing replacement PNG files.

Mitigation: Run it only on intended launcher and icon directories, and use the skip-cache-refresh option when cache refresh should be handled manually.

## Reference(s):

- [Steam Icon Fixer on ClawHub](https://clawhub.ai/lunarmoon26/skills/steam-icon-fixer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and a bundled Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local filesystem actions only when the user runs the bundled script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

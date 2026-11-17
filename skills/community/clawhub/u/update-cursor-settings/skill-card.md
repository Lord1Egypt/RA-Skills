## Description:

Modify Codex/VSCode user settings in settings.json for editor preferences, configuration, themes, font size, tab size, format on save, auto save, keybindings, or other settings.json values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IDE users use this skill to guide safe edits to global Codex/VSCode user settings while preserving existing configuration. It is intended for changing editor behavior such as font size, themes, formatting, auto save, keybindings, and related settings.json values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide edits to global user settings that persist across projects and may require an editor reload.

Mitigation: Review the exact setting key and value before applying changes, preserve existing settings, and inform the user when a reload may be required.

Risk: Invalid JSON or comment handling could break the editor settings file.

Mitigation: Read the existing settings first, preserve comments where possible, and validate JSON syntax before writing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/update-cursor-settings)
- [Publisher profile](https://clawhub.ai/user/eohmig)

## Skill Output:

**Output Type(s):** [guidance, configuration, code, markdown]

**Output Format:** [Markdown guidance with JSON settings examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setting keys, setting values, and reload notes for Codex/VSCode user settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

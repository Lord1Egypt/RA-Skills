## Description:

A skill for exporting, inspecting and applying UKUI desktop gsettings presets, with fine-grained get/set support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhuoan](https://clawhub.ai/user/lizhuoan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop automation users use this skill to inspect, export, and apply UKUI or GNOME gsettings values across machines or agent workflows. It supports bulk presets as well as targeted reads and writes for individual schema keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying presets or using set can persistently change display, power, keyboard, mouse, shortcut, theme, or other desktop settings for the current user.

Mitigation: Export the current configuration before changes, review each preset key and value, and apply changes only on the intended desktop profile.

Risk: Exported gsettings presets may contain privacy-relevant values such as usernames, local paths, shortcuts, or environment-specific preferences.

Mitigation: Review and remove sensitive or machine-specific values before sharing exported preset JSON.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhuoan/skills/ukui-gsettings-tool)
- [Publisher profile](https://clawhub.ai/user/lizhuoan)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON preset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local python3 and gsettings binaries and acts on the current user's desktop settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

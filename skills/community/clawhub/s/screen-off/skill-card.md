## Description:

Toggle any macOS display on/off by ID, name, or index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and macOS users use this skill to list connected displays and toggle a selected display on or off from an agent or terminal by ID, index, or name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can turn off the only visible display, which may leave the user without an immediate visual recovery path.

Mitigation: Run --status first, avoid --force unless another recovery method is available, and confirm the target display before switching it off.

Risk: The --permanent option can keep a display disabled across reboot.

Mitigation: Use --permanent only when persistent display state is intended and the user knows how to re-enable the display.

Risk: The tool depends on macOS CoreGraphics/SkyLight private APIs that may be unavailable or behave differently across macOS versions.

Mitigation: Confirm behavior on the target macOS version and review command output or exit codes before relying on it in repeated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfang0126/skills/screen-off)
- [zy0816/ScreenOff](https://github.com/zy0816/ScreenOff)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only display-control guidance; commands may change connected monitor state.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

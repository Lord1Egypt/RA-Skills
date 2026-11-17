## Description:

Helps agents locate precise Windows desktop coordinates through UI Automation lookup, screenshot grid overlays, or user-assisted point selection, returning reusable JSON coordinates for automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuangying0001-beep](https://clawhub.ai/user/shuangying0001-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and agents use this skill to convert Windows UI targets into precise screen coordinates for desktop automation, RPA flows, and repeated mouse actions. It is intended for Windows environments where standard UI Automation, visual grid reading, or a user point-and-click handoff can provide a reliable target location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture screenshots and inspect desktop UI elements, which may expose sensitive on-screen content.

Mitigation: Avoid using it on sensitive screens, keep screenshots local, and periodically clear %TEMP%\screen-coord-locator\.

Risk: The authorization flow contacts coord.weituoai.cn with a device identifier before paid coordinate operations.

Mitigation: Install only when that remote authorization behavior is acceptable and review payment or authorization prompts before continuing.

Risk: The action script can perform real mouse movement, clicks, double-clicks, right-clicks, drags, and wheel actions.

Mitigation: Use DryRun or explicit confirmation before running act.ps1, especially before clicks on destructive or sensitive UI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuangying0001-beep/skills/windows-screen-coordinate)
- [usage.md](reference/usage.md)
- [workflow.md](reference/workflow.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Guidance]

**Output Format:** [JSON results with Markdown guidance and runnable PowerShell, Python, AutoHotkey, or automation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates are absolute Windows screen positions and may include UI element rectangles, center points, screenshot paths, or dry-run mouse action results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

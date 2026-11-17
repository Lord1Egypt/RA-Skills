## Description:

Operate yboard.online to navigate scenes, edit presentation fields, switch modes, and add clear, text-free scene visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zonder](https://clawhub.ai/user/zonder)

### License/Terms of Use:


## Use Case:

Developers, creators, and operators use this skill to guide an agent while editing YBoard video or presentation scenes in an attached browser session. It supports scene navigation, text field updates, mode switching, image replacement, and final readability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may modify titles, goals, narration, assets, or images in the active YBoard project.

Mitigation: Review the selected scene and intended edits before applying changes.

Risk: Scene visuals can become unclear if images contain overlapping text or too many elements.

Mitigation: Prefer one text-free hero visual per scene and verify readability after image changes.

## Reference(s):

- [YBoard Operator skill page](https://clawhub.ai/zonder/skills/yboard-operator)
- [YBoard cheatsheet](artifact/yboard-cheatsheet.md)
- [yboard.online](https://yboard.online)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with ordered workflow steps and concise editing rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an attached browser tab for YBoard operations; does not produce standalone files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

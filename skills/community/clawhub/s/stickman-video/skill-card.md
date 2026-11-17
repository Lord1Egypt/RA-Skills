## Description:

Creates code-drawn stickman videos with animated figures, timed captions, sound effects, and a rendered MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators use this skill to script and render short stickman stories, explainers, and contrasts with a reusable animated rig.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions recommend running command-line packages without pinned versions, and the scan reports that some files were only partly inspected.

Mitigation: Review the commands and use exact, reviewed package versions before installation.

Risk: An audio example may overwrite an existing file.

Mitigation: Check the destination and require confirmation before replacing an existing file.

## Reference(s):

- [Stickman rig reference](references/rig.md)
- [VARG how-to](https://varg.ai/how-to)
- [ClawHub skill release](https://clawhub.ai/vargai/skills/stickman-video)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [HTML/SVG animation code, scripts, and rendered MP4 video with a contact sheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 1080×1920 at 30 fps; voice is optional. Local rendering requires Node.js 22 and FFmpeg.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

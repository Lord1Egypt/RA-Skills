## Description:

Route and complete end-to-end edits inside AI Video Editor by Subclip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editing agents use this skill to inspect, plan, create, edit, caption, mix, review, and recover projects in Subclip's AI Video Editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `npx hyperframes` command may download and run package code with the agent's available host access.

Mitigation: Review the command before installing or running it, verify the package and version intended for use, and keep execution within the host permissions.

Risk: The security analysis was partial because some referenced paths were absent from the bundle.

Mitigation: Reassess the skill when the missing referenced files are available.

## Reference(s):

- [Subclip Video Editor on ClawHub](https://clawhub.ai/prosamik/skills/subclip-video-editor)
- [Publisher profile: prosamik](https://clawhub.ai/user/prosamik)
- [Subclip pricing](https://subclip.app/pricing)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Files]

**Output Format:** [Markdown guidance, editor tool calls, and optional code or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project edits are applied through Subclip's native editor tools; outputs depend on the requested edit.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

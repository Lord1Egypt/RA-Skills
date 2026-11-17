## Description:

Plan and review multi-shot video camera blocking in a three.js animatic, then export a camera plan and reference video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Filmmakers and video developers use this skill to turn a storyboard into a timed 3D blockout, review shot composition and camera moves, and export a camera plan or reference animatic before production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security report flags a stored cross-site scripting weakness in the browser review app.

Mitigation: Use the review app with trusted project data and local access until the reported weakness has been assessed and addressed.

Risk: The security report notes unpinned package commands.

Mitigation: Review package names and versions before running install or render commands, and pin versions where practical.

Risk: The security report flags external sharing without clear privacy warnings.

Mitigation: Confirm that clips, images, prompts, and project details are approved for sharing before sending them to external services.

Risk: The scan was incomplete: some components were only partially inspected and static tool-misuse analysis was degraded.

Mitigation: Review the remaining source and scan the exact release again before using it in sensitive production workflows.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vargai/skills/threejs-animatic)
- [Camera language guide](artifact/references/camera-language.md)
- [Seek-safe rendering guide](artifact/references/seek-safe-rendering.md)
- [Seedance video-to-video guide](artifact/references/seedance-v2v-pack.md)
- [Starter project guide](artifact/starter/README.md)
- [varg MCP endpoint](https://mcp.varg.ai/mcp)

## Skill Output:

**Output Type(s):** [Code, Markdown, JSON, Video]

**Output Format:** [Starter project files, a camera plan in Markdown and JSON, and rendered animatic video or stills.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are shaped by the supplied storyboard, timing, and production brief.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

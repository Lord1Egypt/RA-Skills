## Description:

Extracts representative frames from a video into a grid image with XML timestamps so a vision-capable agent can inspect video content in context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-ver](https://clawhub.ai/user/john-ver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use see-video to inspect user-provided video content with the same multimodal model that is handling the conversation. It is useful when frame-level visual context is needed without handing the video to a separate description model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted video frames are placed into the active multimodal model context.

Mitigation: Use the skill only with videos the user is allowed to share with that model and deployment environment.

Risk: Installing or running npm-based tooling can introduce package supply-chain and privilege risks.

Mitigation: Prefer pinned or reviewed installs, honor the provided lockfile where possible, and avoid running npm or npx as a privileged user.

Risk: Unsupported, corrupt, or incomplete video files can prevent frame extraction or reduce coverage.

Mitigation: Use complete supported video files, check ffmpeg availability, and narrow analysis with start and end times when needed.

## Reference(s):

- [see-video ClawHub skill](https://clawhub.ai/john-ver/skills/see-video)
- [llm-frames library](https://github.com/john-ver/llm-frames)
- [llm-frames npm package](https://registry.npmjs.org/llm-frames/-/llm-frames-0.2.2.tgz)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [JSON stdout containing a generated JPEG path and XML timestamp description]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, Node.js, and a vision-capable multimodal model; extracted frames are placed into model context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

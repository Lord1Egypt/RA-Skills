## Description:

Guides an AI agent through analyzing travel footage, planning a vlog edit, generating preview dashboards and storyboards, and rendering a finished video with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[znyupup](https://clawhub.ai/user/znyupup)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn travel or daily-life video folders into edited vlog plans, visual previews, and final rendered videos. It is intended for agent-assisted workflows that combine ffmpeg, Whisper, a vision API, and human review of the proposed edit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal media frames or transcripts may be sent to a vision API during clip analysis.

Mitigation: Confirm which frames and transcripts will be uploaded, use only media the user is comfortable processing, and prefer the smallest frame size needed for review.

Risk: Generated dashboard files may expose private filenames, speech transcripts, notes, or preview frames.

Mitigation: Keep dashboard HTML and generated assets in a private project folder and avoid publishing them unless the user has reviewed the contents.

Risk: The workflow includes command execution and a shell=True highlight example that may be unsafe if adapted directly.

Mitigation: Require command review before execution, run in a dedicated workspace with pinned dependencies, and avoid shell=True when implementing command wrappers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/znyupup/skills/vlog-auto-edit)
- [Publisher profile](https://clawhub.ai/user/znyupup)
- [Clawdis author profile](https://github.com/znyupup)
- [Vision API provider referenced by the skill](https://open.bigmodel.cn)
- [Claude Code documentation referenced by README](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
- [OpenClaw repository referenced by README](https://github.com/nicepkg/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell and Python snippets, JSON edit plans, generated HTML previews, and video output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided media, ffmpeg, Python 3.9+, Whisper or compatible transcription support, and a compatible vision API for frame analysis.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Video Producer generates short-form videos by using video-director for storyboard planning, then creating AI visual assets, TTS narration, Remotion video code, and a final MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1024708231](https://clawhub.ai/user/a1024708231)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use this skill to turn a topic and talking points into a storyboard, generated visuals, narrated scenes, renderable video code, and an MP4 video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports embedded API keys in the release.

Mitigation: Remove hard-coded keys, rotate exposed credentials, and require runtime credentials from environment variables or a managed secret store before installation.

Risk: The skill sends prompts and narration content to third-party MiniMax image and TTS services.

Mitigation: Disclose the third-party data flow and obtain approval for any user, customer, or confidential content before using the skill.

Risk: The security evidence reports unsafe execution paths and generated-code handling.

Mitigation: Replace shell-string execution with argument-array execution, validate storyboard data and filenames, and run rendering in sandboxed input and output directories.

## Reference(s):

- [ClawHub skill page for Video Producer](https://clawhub.ai/a1024708231/skills/video-producer)
- [ClawHub publisher profile a1024708231](https://clawhub.ai/user/a1024708231)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Files]

**Output Format:** [Storyboard Markdown and JSON, generated JavaScript/React code, image and audio files, and MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project artifacts including storyboard files, generated media, Remotion source files, intermediate video, concatenated audio, and final MP4 output.]

## Skill Version(s):

2.2.1 (source: server release metadata; SKILL.md frontmatter says 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

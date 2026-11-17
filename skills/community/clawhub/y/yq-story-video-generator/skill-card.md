## Description:

Generates complete story videos from images, text descriptions, or mixed inputs, with selectable duration and visual style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agent users use this skill to turn one or more images, a text prompt, or both into a structured short story video with generated script, reference imagery, video segments, background music, and a final MP4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to install FFmpeg with system-level package-manager commands.

Mitigation: Review before installing, run in a sandbox or preinstall FFmpeg, and approve any sudo or package-manager command only after checking the exact command and host impact.

Risk: The workflow generates JSON, images, audio, intermediate files, and final MP4 files under output/.

Mitigation: Inspect generated files before sharing or publishing and keep output/ isolated from sensitive project directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-story-video-generator)
- [Publisher profile](https://clawhub.ai/user/tianheihei002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Conversational guidance with JSON story scripts, generated image/audio/video files, shell commands, and deliver_assets markdown blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces files under output/, including story_script.json, subject_reference.png, frame images, video segments, bgm.mp3, intermediate merge files, and final_video.mp4.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

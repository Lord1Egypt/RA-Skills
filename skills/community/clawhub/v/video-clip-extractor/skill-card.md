## Description:

Extract frames or short clips from videos using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content reviewers use this skill to extract a first frame, a timestamped frame, or an indexed frame from a local video file for inspection, thumbnails, or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper invokes ffmpeg with overwrite enabled for the requested output image path.

Mitigation: Review the --out path before running the command and avoid pointing it at files that should be preserved.

Risk: The skill depends on a local ffmpeg installation.

Mitigation: Install ffmpeg from a trusted package source and confirm the ffmpeg binary is available before use.

## Reference(s):

- [FFmpeg](https://ffmpeg.org)
- [Video Frames on ClawHub](https://clawhub.ai/utromaya-code/skills/video-clip-extractor)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg; the helper writes a single frame image to the requested output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

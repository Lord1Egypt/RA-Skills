## Description:

Converts local video clips into GIF animations with ffmpeg, with options for start time, duration, frame rate, output width, and bilingual Chinese-English guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyxie2026](https://clawhub.ai/user/sallyxie2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and external users use this skill to convert local video files or selected clips into GIFs while controlling frame rate, width, start time, and duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs ffmpeg and ffprobe on local video files.

Mitigation: Install and trust ffmpeg/ffprobe before use, and run the converter only on video files the user intends to process.

Risk: The converter uses overwrite mode for the selected GIF output path.

Mitigation: Review the output path before running the command and choose a new filename when preserving an existing file matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sallyxie2026/skills/video-to-gif)
- [Skill Definition](artifact/SKILL.md)
- [Conversion Script](artifact/scripts/convert.py)

## Skill Output:

**Output Type(s):** [files, text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and generated GIF file details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or overwrites the user-provided GIF output path and reports the output path, size, dimensions, and frame rate.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

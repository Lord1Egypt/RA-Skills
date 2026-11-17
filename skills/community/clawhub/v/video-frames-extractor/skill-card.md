## Description:

Extract frames or short clips from videos using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and reviewers use this skill to extract a first, timestamped, or indexed frame from a local video for thumbnails, inspection, or UI-quality captures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper overwrites the selected output image path.

Mitigation: Review the --out path before running generated commands and choose a disposable or versioned filename when preserving existing frames matters.

Risk: The helper creates parent directories for the requested output path.

Mitigation: Use an explicit, trusted output directory and avoid broad or sensitive filesystem locations.

Risk: The skill processes local video files through ffmpeg.

Mitigation: Run it only on videos you are comfortable processing locally and keep ffmpeg installed from a trusted package source.

## Reference(s):

- [ffmpeg](https://ffmpeg.org)
- [Video Frames on ClawHub](https://clawhub.ai/utromaya-code/skills/video-frames-extractor)
- [utromaya-code publisher profile](https://clawhub.ai/user/utromaya-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create parent directories and overwrite the selected output image path when the helper is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Video-Watch helps agents analyze video content by extracting frames at regular intervals from common video formats for review and scene description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kartinw](https://clawhub.ai/user/kartinw)

### License/Terms of Use:


## Use Case:

Developers and agents use Video-Watch to extract video frames with ffmpeg, inspect sampled frames, and describe scene content when direct playback is not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The frame-extraction script has unsafe output-file handling that could overwrite local files in some scenarios.

Mitigation: Use a private output directory and avoid shared or attacker-writable folders until output validation and overwrite behavior are improved.

Risk: Unsafe argument handling can make untrusted video paths or fps values risky to process locally.

Mitigation: Use trusted video paths, keep fps numeric, and prefer the default fps unless the value has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kartinw/skills/video-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash commands and extracted JPEG frame files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg; generated frames are written to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

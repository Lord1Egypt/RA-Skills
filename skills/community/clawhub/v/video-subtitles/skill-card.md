## Description:

Generates SRT subtitles from video or audio, supports Hebrew and English transcription, Hebrew-to-English translation, and burning subtitles into video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngutman](https://clawhub.ai/user/ngutman)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to create captions, transcripts, SRT subtitle files, and hardcoded subtitles for video or audio media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install changing dependencies.

Mitigation: Review before installing and prefer pinned dependencies from the publisher.

Risk: The skill can overwrite output files without confirmation.

Mitigation: Run it only on media files and output paths you choose, and avoid pointing -o at existing important files.

Risk: Media processing and model execution may have broader local system impact.

Mitigation: Run the skill in a constrained environment when possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text transcripts, SRT subtitle files, MP4 video files, and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.10, uv, ffmpeg for subtitle embedding or burn-in, and local model downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

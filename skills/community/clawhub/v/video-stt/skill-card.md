## Description:

Extract audio from video URLs and transcribe using STT (Speech-to-Text). Supports local Whisper or cloud APIs. Use when: user provides a video URL and wants to know what is being said, transcribing YouTube videos, podcasts, or any video with audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damiencronw](https://clawhub.ai/user/damiencronw)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to download audio from a video URL and produce a speech transcript for videos, podcasts, and other media with audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell wrapper can turn user-controlled options into local Python code execution.

Mitigation: Avoid untrusted values for --model, --format, and --output; use a reviewed version that removes Python command interpolation before deployment.

Risk: The skill may install unpinned dependencies during normal use.

Mitigation: Install and pin dependencies in a controlled environment before running the skill.

Risk: The skill downloads media and writes audio and transcript files locally.

Mitigation: Run it in an isolated workspace, validate video URLs, and restrict output paths to expected directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/damiencronw/skills/video-stt)
- [ClawHub publisher profile](https://clawhub.ai/user/damiencronw)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown command guidance and transcript output as plain text, SRT, VTT, or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses video URLs as input and can write audio and transcript files to local output directories.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

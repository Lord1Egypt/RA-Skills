## Description: <br>
A local FFmpeg-based video processing skill for format conversion, compression, subtitle generation, aspect ratio adjustment, audio cleanup, and video inspection for personal content creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to have an agent prepare local FFmpeg, FFprobe, and optional Whisper commands for single-file video conversion, compression, subtitle generation, audio cleanup, and social-platform format checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run local FFmpeg, FFprobe, Whisper, package-manager, and pip commands. <br>
Mitigation: Review generated commands and manually approve dependency installation or media-processing execution before running them. <br>
Risk: Video-processing commands may overwrite output files or create unexpected derived media if filenames are not checked. <br>
Mitigation: Confirm input and output paths before execution and use distinct output filenames for processed files. <br>
Risk: The skill is intended for media the user is allowed to process. <br>
Mitigation: Use it only with videos and audio files the user provides and has rights to process. <br>


## Reference(s): <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for user-provided local media files; does not itself upload media to external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

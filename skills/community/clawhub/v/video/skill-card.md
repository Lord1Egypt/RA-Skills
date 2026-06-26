## Description: <br>
Process, edit, and optimize videos for any platform with compression, format conversion, captioning, and repurposing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, content creators, social media managers, educators, marketers, and developers use this skill to choose and review local video-processing workflows for converting, compressing, captioning, reframing, and preparing media for target platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ffmpeg commands can overwrite, corrupt, or transform local media when run against the wrong filenames or folder. <br>
Mitigation: Review commands before execution, use explicit input and output filenames, keep originals or work on copies, and run batch examples only in the intended folder. <br>
Risk: Platform targets and compression settings can reduce quality or produce outputs that fail a destination's limits. <br>
Mitigation: Inspect the source with ffprobe and verify duration, file size, aspect ratio, playback, audio sync, and platform requirements before delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/video) <br>
- [FFmpeg Commands by Task](commands.md) <br>
- [Platform Specifications](platforms.md) <br>
- [Video Quality Guide](quality.md) <br>
- [Video Workflows by Use Case](workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and ffprobe; optional workflows mention Whisper and Real-ESRGAN when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

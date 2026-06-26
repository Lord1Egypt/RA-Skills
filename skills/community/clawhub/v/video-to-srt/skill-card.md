## Description: <br>
Generate timecoded SRT subtitles from local video or audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyxie2026](https://clawhub.ai/user/sallyxie2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to transcribe local video or audio into timecoded SRT subtitle files for editing and import workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install Python dependencies and download transcription models into a local virtual environment and cache. <br>
Mitigation: Use it only in environments where local dependency and model downloads are acceptable, and review the environment before execution. <br>
Risk: Using --copy-next-to-input modifies the source media folder and may overwrite an existing matching .srt file. <br>
Mitigation: Omit --copy-next-to-input when the source folder should remain unchanged, or inspect existing subtitle files before copying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sallyxie2026/video-to-srt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated UTF-8 SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include numbered subtitle cues with timestamps; --copy-next-to-input can place a copy beside the source media.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

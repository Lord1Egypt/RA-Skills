## Description: <br>
Generates multilingual SRT or WebVTT subtitles from media files using Faster-Whisper first and OpenAI Whisper as a fallback, with timing alignment and optional completion notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqbjqtd](https://clawhub.ai/user/aqbjqtd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to transcribe video or audio into subtitle files, select SRT or WebVTT output, optionally provide a language code, and receive a completion notification when generation finishes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically create ~/.whisper-venv and download Python packages during execution. <br>
Mitigation: Review the dependency list before installation and run the skill in a controlled environment where package installation is acceptable. <br>
Risk: The skill writes subtitle files beside the input media and can send completion notifications that contain local file paths. <br>
Mitigation: Use a working directory that is safe for generated files and avoid running it on sensitive paths if path disclosure through notifications is not acceptable. <br>
Risk: The skill is designed for background execution and includes broad process cleanup guidance. <br>
Mitigation: Prefer a revised version with PID-scoped cleanup, or supervise background runs so unrelated processes are not interrupted. <br>


## Reference(s): <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [PyTorch Metal Wheel Index](https://download.pytorch.org/whl/metal) <br>
- [ClawHub Skill Page](https://clawhub.ai/aqbjqtd/subtitle-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance plus generated SRT or WebVTT subtitle files and plain-text status notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subtitle files are written beside the input media file; optional notifications can include the generated filename, segment count, and local path.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Wechat Voice helps an agent detect WeChat SILK voice attachments, decode them to WAV, transcribe them locally with Whisper, and respond with the recognized content or a clear no-speech result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jozhn](https://clawhub.ai/user/jozhn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to handle WeChat voice attachments by decoding local SILK or other audio files, transcribing speech locally, and returning either recognized text or a clear blank, short, or unclear-audio result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes voice attachments locally and can create decoded WAV or PCM files that may contain sensitive audio. <br>
Mitigation: Use explicit per-request output paths, avoid shared multi-user environments for sensitive audio, and delete generated WAV or PCM files after use. <br>
Risk: The server security summary identifies a manageable temporary-file hygiene issue. <br>
Mitigation: Treat local decoded audio as temporary data, clean it after transcription, and review output paths before running the bundled script. <br>
Risk: The workflow requires local Python dependencies and audio tooling. <br>
Mitigation: Install the stated dependencies only in environments where local voice processing and the required packages are acceptable. <br>


## Reference(s): <br>
- [WeChat Voice Notes](references/notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jozhn/wechat-voice-decode) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text transcript results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The transcription script prints recognized text or NO_SEGMENTS when no usable speech is detected.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

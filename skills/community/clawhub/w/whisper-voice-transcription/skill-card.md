## Description: <br>
Build and use whisper.cpp for local speech-to-text workflows, with optional cloud fallback when local transcription is not practical. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to build whisper.cpp, prepare audio, run local speech-to-text, and choose a cloud fallback only when local transcription is impractical. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloning and building whisper.cpp and downloading speech models can introduce supply-chain risk if unofficial sources are used. <br>
Mitigation: Use official whisper.cpp releases or repositories, verify hashes when available, and review commands before running them. <br>
Risk: Audio can contain sensitive information, and cloud fallback changes the privacy model. <br>
Mitigation: Prefer local transcription for sensitive audio and tell the user before sending audio to an external provider. <br>
Risk: Broad filesystem searches can expose unrelated audio files. <br>
Mitigation: Search only expected cache or upload paths when locating audio for transcription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuxuclassmate/whisper-voice-transcription) <br>
- [whisper.cpp repository](https://github.com/ggerganov/whisper.cpp.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local build guidance, audio conversion commands, model download guidance, and privacy notices for cloud fallback.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

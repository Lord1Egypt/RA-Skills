## Description: <br>
WhisperX provides local speech-to-text transcription using OpenAI Whisper, with high-quality offline recognition, no API key required, word-level timestamps, and optional speaker diarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niuzb](https://clawhub.ai/user/niuzb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to transcribe local audio files into text with optional word-level timestamps and speaker diarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill requires pip installing WhisperX and installing ffmpeg. <br>
Mitigation: Install dependencies from trusted package sources and verify them before use in restricted or sensitive environments. <br>
Risk: Model files may be downloaded and cached locally on first use. <br>
Mitigation: Preinstall and verify required models before deployment where network access or local cache contents are controlled. <br>
Risk: Optional speaker diarization requires providing a HuggingFace token. <br>
Mitigation: Enable diarization only when token use is intended, and handle the token according to local credential-management policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niuzb/whisperx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and transcription guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local speech-to-text transcription; optional diarization requires a HuggingFace token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

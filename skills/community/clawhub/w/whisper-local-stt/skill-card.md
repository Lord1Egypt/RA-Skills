## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local Whisper CLI commands for audio transcription or translation without sending audio to an API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Homebrew installation of the Whisper CLI and local model downloads may add binaries and cached model files to the user's machine. <br>
Mitigation: Review the Homebrew formula before installation and confirm local storage expectations before first use. <br>
Risk: Transcripts and subtitle outputs may contain sensitive content from source audio. <br>
Mitigation: Choose output directories carefully and apply the same access controls and retention practices used for the original audio. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/whisper-local-stt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local transcription and translation commands; generated transcripts may contain sensitive audio content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

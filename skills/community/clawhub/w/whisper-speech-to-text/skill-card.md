## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to run local speech-to-text or translation workflows with the Whisper CLI without configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Homebrew installs the openai-whisper package and its dependencies. <br>
Mitigation: Review the package and dependency source before installing in managed or sensitive environments. <br>
Risk: Whisper reads the audio files passed to the CLI, which may contain sensitive content. <br>
Mitigation: Run the skill only on intended local files and follow the applicable data handling policy for audio and transcripts. <br>
Risk: Whisper models may be cached in the user's home directory and transcript files are written to the chosen output directory. <br>
Mitigation: Choose output directories deliberately and clean cached models or generated transcripts when retention is not desired. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [ClawHub Skill Page](https://clawhub.ai/utromaya-code/whisper-speech-to-text) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/utromaya-code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent provides Whisper CLI usage guidance; transcript files are produced by the local Whisper CLI in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

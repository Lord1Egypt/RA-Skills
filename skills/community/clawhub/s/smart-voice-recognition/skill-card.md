## Description: <br>
Intelligent speech-to-text using local OpenAI Whisper for transcribing audio files, voice messages, spoken content, and speech input in 99+ languages with automatic Whisper model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[08jacky04](https://clawhub.ai/user/08jacky04) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files into text, optionally with language hints, segment timestamps, and automatic Whisper model selection for speed or accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled installer can modify the host Python environment if virtual environment creation fails. <br>
Mitigation: Install and run the skill only inside an isolated virtual environment, and avoid running the bundled installer against managed or system Python. <br>
Risk: Offline and privacy claims are overstated before dependencies and Whisper model weights have been downloaded. <br>
Mitigation: Plan for network access during installation and first model download, then verify offline behavior before processing sensitive audio. <br>
Risk: The transcribe script adds fallback import paths under /tmp before importing dependencies. <br>
Mitigation: Remove or review the /tmp import fallback and pin dependencies before using the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/08jacky04/smart-voice-recognition) <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [python-soundfile](https://python-soundfile.readthedocs.io/) <br>
- [PyTorch](https://pytorch.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [Plain text transcript with optional timestamped segment lines or a saved transcript file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local audio file path; first use may download Whisper model weights and Python packages.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

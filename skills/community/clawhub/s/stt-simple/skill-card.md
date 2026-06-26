## Description: <br>
Simple local speech-to-text using Whisper with one-command installation, local model download, and support for 99+ languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkisme](https://clawhub.ai/user/lkisme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to install and run local Whisper speech transcription for audio files, producing text and optional subtitle or JSON outputs without sending audio to a remote API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation downloads packages and Whisper models and writes local files. <br>
Mitigation: Install only in a dedicated project or virtual environment, review storage and output locations, and run the installer only after reviewing it. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcription, JSON status, and optional TXT, JSON, SRT, or VTT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally after installing Whisper, FFmpeg, and a selected Whisper model; default outputs are written to a local STT output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

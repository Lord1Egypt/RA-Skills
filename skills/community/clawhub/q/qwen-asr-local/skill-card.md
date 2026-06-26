## Description: <br>
Local speech-to-text using Qwen3-ASR on macOS or Linux with CPU-only offline transcription and no API key or cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanglizhuo](https://clawhub.ai/user/huanglizhuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and run a local Qwen3-ASR CLI for transcribing voice messages and audio files, including stdin, segmented, and streaming workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation downloads an external executable and model without checksum verification. <br>
Mitigation: Install only when the upstream QwenASR release and HuggingFace model source are trusted, and manually verify release artifacts in environments with strict supply-chain controls. <br>


## Reference(s): <br>
- [Qwen ASR ClawHub page](https://clawhub.ai/huanglizhuo/qwen-asr-local) <br>
- [QwenASR source repository](https://github.com/huanglizhuo/QwenASR) <br>
- [Original qwen-asr implementation](https://github.com/antirez/qwen-asr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcription with Markdown shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally; non-WAV audio requires ffmpeg, and installation targets macOS or Linux with qwen-asr available.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

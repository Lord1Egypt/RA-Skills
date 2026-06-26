## Description: <br>
Local ASR and TTS inference server. Use when the user wants to transcribe audio to text (ASR) or convert text to speech (TTS). Requires a running Willow Inference Server instance. Supports Whisper for ASR and custom TTS voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeAntiWang](https://clawhub.ai/user/DeAntiWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and call a trusted Willow Inference Server for audio transcription and text-to-speech generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio recordings and supplied text may be logged or retained by the configured Willow server. <br>
Mitigation: Configure WILLOW_BASE_URL only to a server you control or explicitly trust, preferably a local endpoint. <br>
Risk: Setup instructions may clone and run an upstream Willow server repository outside the skill package. <br>
Mitigation: Review the upstream repository and setup script before running installation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeAntiWang/willow-inference-server) <br>
- [Publisher profile](https://clawhub.ai/user/DeAntiWang) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for interacting with a configured Willow server; generated ASR/TTS results depend on the trusted server endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

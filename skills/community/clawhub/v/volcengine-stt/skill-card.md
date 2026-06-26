## Description: <br>
Transcribe audio to text using Volcano Engine (Volcengine/ARK) speech-to-text APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to transcribe local audio files, voice notes, or OpenClaw voice-message inputs through Volcengine speech-to-text APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the documentation does not fully match the script's credentials, endpoints, flags, and config-file fallback. <br>
Mitigation: Review the script before use and configure credentials using the current VOLC_* environment variables, command-line flags, or OpenClaw config fields. <br>
Risk: Audio submitted through this skill is sent to ByteDance/Volcengine speech-to-text services. <br>
Mitigation: Use only audio that is approved for processing by that provider under the user's data handling and account policies. <br>
Risk: The skill depends on local credentials for Volcengine access. <br>
Mitigation: Keep access tokens in local environment variables or machine-local configuration and do not commit secrets. <br>


## Reference(s): <br>
- [Volcengine STT skill page](https://clawhub.ai/reed1898/volcengine-stt) <br>
- [Volcengine ARK transcription endpoint](https://ark.cn-beijing.volces.com/api/v3/audio/transcriptions) <br>
- [ByteDance OpenSpeech AUC flash endpoint](https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text transcript or raw JSON response written to an output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local audio file and Volcengine credentials; supports standard polling mode, flash mode, language hints, and custom output paths.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

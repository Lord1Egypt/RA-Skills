## Description: <br>
Automatic Speech Recognition (ASR) using Zhipu AI (BigModel) GLM-ASR to transcribe audio files, with support for Chinese audio, context prompts, custom hotwords, and multiple audio formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe short Chinese audio files through Zhipu AI's GLM-ASR model, optionally supplying context prompts and hotwords for domain-specific vocabulary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files, optional context prompts, and hotwords are sent to Zhipu AI for transcription. <br>
Mitigation: Use the skill only with audio and prompt content that may be shared with Zhipu AI, review provider data-retention terms, and avoid confidential or personal voice data without appropriate consent. <br>
Risk: The skill requires a ZHIPU_API_KEY credential in the environment. <br>
Mitigation: Protect the API key, avoid logging or committing it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/franklu0819-lang/zhipu-asr) <br>
- [Zhipu AI API Key Console](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>
- [Zhipu AI Audio Transcriptions Endpoint](https://open.bigmodel.cn/api/paas/v4/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON transcription response with transcribed text, plus shell command examples and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, curl, ffmpeg, and a ZHIPU_API_KEY environment variable; audio is limited to 25 MB and about 30 seconds per request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

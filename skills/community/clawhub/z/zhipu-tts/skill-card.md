## Description: <br>
Text-to-speech conversion using Zhipu AI (BigModel) GLM-TTS model with multiple voice options, speed control, and WAV or PCM output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content creators use this skill to convert Chinese text into spoken audio for narration, announcements, virtual assistants, video dubbing, games, and radio-style content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to the third-party Zhipu AI API. <br>
Mitigation: Use a dedicated, revocable API key and avoid submitting secrets, regulated data, or confidential content unless approved for that service. <br>
Risk: Chosen output filenames can overwrite or remove existing files during audio generation or error handling. <br>
Mitigation: Use deliberate, unused output paths and review generated files before relying on them. <br>


## Reference(s): <br>
- [Zhipu AI API key console](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>
- [Zhipu AI speech API endpoint](https://open.bigmodel.cn/api/paas/v4/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; generated audio files are WAV or PCM.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and a ZHIPU_API_KEY environment variable; input text is limited to 1024 characters per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

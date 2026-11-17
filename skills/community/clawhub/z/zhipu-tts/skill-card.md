## Description:

Text-to-speech conversion using Zhipu AI (BigModel) GLM-TTS model for Chinese speech synthesis with multiple voice personas, speed control, and WAV or PCM output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to convert Chinese text into audio files for narration, announcements, virtual assistants, dubbing, and character voice workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text provided to the skill and the Zhipu API authorization token are sent to Zhipu AI's external service for processing.

Mitigation: Use the skill only where that external processing is approved, and avoid submitting secrets, confidential business text, personal data, or regulated content unless permitted by the deployment environment.

Risk: The skill requires jq and a ZHIPU_API_KEY to run successfully.

Mitigation: Install jq through the normal package-management process and provide the API key through the environment rather than embedding it in scripts or prompts.

## Reference(s):

- [Zhipu AI API Key Console](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)
- [Zhipu AI Audio Speech API Endpoint](https://open.bigmodel.cn/api/paas/v4/audio/speech)
- [ClawHub Skill Page](https://clawhub.ai/franklu0819-lang/skills/zhipu-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WAV or PCM audio files from text input; requires jq and ZHIPU_API_KEY.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

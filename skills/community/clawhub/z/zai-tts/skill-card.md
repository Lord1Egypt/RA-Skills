## Description: <br>
Text-to-speech conversion using GLM-TTS service via the `uvx zai-tts` command for generating audio from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate spoken audio from text or text files, including accessibility, multitasking, podcast-style, driving, cooking, and pre-cloned voice workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires copying an audio.z.ai browser auth token into an external command-line tool. <br>
Mitigation: Use an official API key or scoped token if available, use a dedicated account where possible, and remove or rotate the token after use. <br>
Risk: Text or files submitted for speech generation may contain private or sensitive content. <br>
Mitigation: Avoid sending private text or files through this workflow unless the external service and account controls are acceptable for that data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/al-one/zai-tts) <br>
- [audio.z.ai service](https://audio.z.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated WAV audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uvx plus ZAI_AUDIO_USERID and ZAI_AUDIO_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

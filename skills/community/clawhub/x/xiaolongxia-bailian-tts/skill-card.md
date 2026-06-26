## Description: <br>
Bailian TTS helps agents synthesize text into speech audio with Alibaba Bailian/DashScope Qwen TTS models, selectable voices, and file output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and agents use this skill to generate spoken audio from text through Alibaba Bailian/DashScope. It supports voice selection, model selection, command-line use, and Python API use for Chinese, dialect, and multilingual speech generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Alibaba Bailian/DashScope under the user's account. <br>
Mitigation: Use a dedicated API key and do not submit secrets or regulated personal data unless the deployment has approval for that provider. <br>
Risk: The skill downloads provider-returned audio URLs, which can create risk if network egress is unrestricted. <br>
Mitigation: Run with appropriate network restrictions and review provider URL handling before production deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/xiaolongxia-bailian-tts) <br>
- [Alibaba Cloud Qwen TTS Documentation](https://help.aliyun.com/zh/model-studio/qwen-tts) <br>
- [Alibaba Cloud Qwen TTS Voice Cloning](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning) <br>
- [Alibaba Cloud Qwen TTS Voice Design](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with command-line examples and Python snippets; runtime output is an Opus audio file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key and network access to Alibaba Bailian/DashScope; default audio output is an .opus file.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

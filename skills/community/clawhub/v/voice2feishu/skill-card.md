## Description:

Converts text to speech and sends the resulting audio to Feishu, using either a configured TTS API or local ChatTTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enihsago](https://clawhub.ai/user/enihsago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace users use this skill to turn short text messages into audio and deliver them to a Feishu user or chat. It supports third-party API-based TTS and a local ChatTTS workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API mode sends message text to the configured TTS provider and sends generated audio through Feishu.

Mitigation: Use API mode only for text approved for those services, restrict TTS_API_URL to a trusted HTTPS endpoint, and protect Feishu and TTS credentials.

Risk: The local ChatTTS service is reported as exposed more broadly than documented.

Mitigation: Run local ChatTTS only on a trusted machine or network, firewall the service, or bind it to 127.0.0.1 before use.

Risk: Unsafe temporary-file and PID-file handling was reported for the local server workflow.

Mitigation: Avoid running the local server workflow as a privileged account until temporary-file and PID-file handling are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enihsago/skills/voice2feishu)
- [Feishu Open Platform](https://open.feishu.cn/)
- [ChatTTS](https://github.com/2noise/ChatTTS)
- [ChatTTS model on Hugging Face](https://huggingface.co/2Noise/ChatTTS)
- [ChatTTS model on ModelScope](https://modelscope.cn/models/pkuchoong/ChatTTS)
- [Zhipu AI speech API endpoint](https://open.bigmodel.cn/api/paas/v4/audio/speech)
- [OpenAI audio speech API endpoint](https://api.openai.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and environment variable settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create temporary audio files and send audio messages through Feishu when executed.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

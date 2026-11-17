## Description:

语音转文本技能 - 基于 SiliconFlow API (SenseVoiceSmall/TeleSpeechASR)，支持四川话等多种方言识别

This skill is ready for commercial/non-commercial use.

## Publisher:

[datou3456](https://clawhub.ai/user/datou3456)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to transcribe local audio files into text through SiliconFlow speech-recognition models, including multilingual and dialect audio such as Sichuanese. It can return plain text, JSON, or write the transcript to a file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files are sent to SiliconFlow for transcription, which can expose confidential or sensitive recordings to a third-party service.

Mitigation: Use this skill only for audio that is approved for SiliconFlow processing, and confirm the provider's privacy and retention terms before handling confidential recordings.

Risk: Passing the API key on the command line can expose credentials through shell history or process listings.

Mitigation: Use a protected environment variable or secret store for SILICONFLOW_API_KEY instead of the --api-key command form.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datou3456/skills/voice-transcription)
- [SiliconFlow audio transcriptions API endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript, JSON result, or transcript file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SiliconFlow API key and sends selected audio files to SiliconFlow for transcription.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

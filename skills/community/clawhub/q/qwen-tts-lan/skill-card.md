## Description:

Qwen Tts helps agents convert text to natural speech through Alibaba Cloud DashScope Qwen TTS, with multiple Chinese, English, Cantonese, and dialect voices plus optional streaming examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan314](https://clawhub.ai/user/lanlan314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to synthesize spoken audio from text with Qwen TTS voices, generate local audio files, and optionally send generated audio through Feishu when explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech synthesis is sent to Alibaba DashScope.

Mitigation: Avoid sensitive text unless provider agreements allow it, and review DashScope data-handling terms before production use.

Risk: The optional Feishu sender can upload generated audio and send it to a configured user.

Mitigation: Configure FEISHU_* credentials only when message sending is intended, restrict Feishu app permissions, and verify the recipient user ID.

Risk: Security guidance identifies temporary-file hardening risks.

Mitigation: Run the scripts in a trusted environment and prefer a release that fixes temporary-file races before shared or multi-user deployment.

Risk: Voice cloning and message sending can create consent and misuse concerns.

Mitigation: Use cloned voices only with appropriate consent and review generated audio before sending it to others.

## Reference(s):

- [Qwen Tts on ClawHub](https://clawhub.ai/lanlan314/skills/qwen-tts-lan)
- [Qwen TTS API Reference](references/api.md)
- [Qwen TTS Voice List](references/voices.md)
- [DashScope Console](https://dashscope.console.aliyun.com)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash, curl, and Python examples; scripts return local OGG audio file paths or Feishu send results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio URLs expire after 24 hours; the optional Feishu path uploads and sends audio using configured Feishu credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

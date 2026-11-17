## Description:

Xiaomi-any2speech guides agents through using Xiaomi's Any2Speech service to turn text, URLs, files, or authorized reference voice samples into WAV speech such as TTS, podcasts, audiobooks, debates, rap, and radio dramas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whiteshirt0429](https://clawhub.ai/user/whiteshirt0429)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate expressive speech audio from supplied content, including long-form narration, multi-speaker formats, and voice-prompt cloning when the user has rights to the reference voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User content, URLs, files, and reference voice samples are sent to the Xiaomi speech service.

Mitigation: Use the skill only when the user is comfortable sharing that material with the external service.

Risk: Voice cloning can be misused or performed without consent.

Mitigation: Use reference audio only for the user's own voice or voices the user is authorized to use.

Risk: Optional Feishu delivery can send generated audio to the wrong chat if chat or token configuration is incorrect.

Mitigation: Verify the Feishu CHAT_ID and token setup before asking the skill to send audio.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whiteshirt0429/skills/xiaomi-any2speech-beyondtts)
- [Xiaomi Any2Speech service endpoint](https://miplus-tts-public.ai.xiaomi.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples that produce WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send user-provided text, files, URLs, and reference voice samples to an external speech service; optional Feishu delivery requires user-provided chat and token configuration.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

The English Tutor helps learners practice spoken English with optional word-list review, timed scenario dialogs, speech transcription, text-to-speech, Feishu voice delivery, and Bitable memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaltsgo](https://clawhub.ai/user/pandaltsgo)

### License/Terms of Use:

MIT-0

## Use Case:

Learners use this agent to rehearse short American English conversations, upload vocabulary lists, receive optional scheduled practice prompts, and review words with spaced repetition. Developers or advanced users configure Feishu, MiniMax, Piper, SenseVoice, and Bitable integrations according to the deployment environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private voice, chat, learning records, and service credentials.

Mitigation: Configure only trusted Feishu, MiniMax, and ASR providers; store secrets through environment variables or secured configuration; avoid passing secrets as command-line arguments.

Risk: Optional Bitable memory stores chat and vocabulary records outside the local agent environment.

Mitigation: Enable Bitable memory only when external storage of practice data is acceptable, and limit stored content to learning records needed for review.

Risk: Optional Piper and SenseVoice setup downloads external binaries or model artifacts.

Mitigation: Verify downloaded artifacts before use, prefer a virtual environment with pinned dependencies, and review downloaded files according to local security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pandaltsgo/skills/the-english-tutor)
- [Configuration schema](references/config-schema.md)
- [MiniMax TTS API reference](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http)
- [Piper TTS release v1.2.0](https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz)
- [Piper English voice model](https://hf-mirror.com/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx)
- [SenseVoice model files](https://modelscope.cn/api/v1/models/xiaowangge/sherpa-onnx-sense-voice-small/resolve/master/model.onnx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional JSON status from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu audio-message results or skipped status when voice delivery is configured.]

## Skill Version(s):

3.0.4 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

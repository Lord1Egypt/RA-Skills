## Description: <br>
The English Tutor helps learners practice spoken English with optional scheduled dialogues, voice input correction, Feishu voice delivery, TTS/ASR support, vocabulary lists, and spaced review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandaltsgo](https://clawhub.ai/user/pandaltsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
English learners use this skill to run text or voice-based speaking practice, receive corrections, rehearse uploaded vocabulary, and optionally receive scheduled Feishu voice prompts. Agents can help configure optional cloud and local speech modules, memory storage, and daily review schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Feishu, MiniMax, ASR, and Bitable integrations can process personal practice audio, conversation text, credentials, or study records. <br>
Mitigation: Use limited-scope credentials, avoid sensitive personal or business content when cloud providers or Bitable memory are enabled, and leave optional modules disabled when they are not needed. <br>
Risk: Scheduled pushes can send automatic Feishu messages if enabled. <br>
Mitigation: Keep scheduled pushes disabled unless automatic practice reminders are expected, and review the configured times before enabling cron jobs. <br>
Risk: Local speech tools and model downloads depend on external binaries or files. <br>
Mitigation: Download models from trusted sources, verify downloads when possible, and set PIPER_BIN only to a trusted local binary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pandaltsgo/the-english-tutor) <br>
- [Configuration schema](references/config-schema.md) <br>
- [MiniMax speech API documentation](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http) <br>
- [Piper TTS release](https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz) <br>
- [SenseVoice ASR model files](https://modelscope.cn/api/v1/models/xiaowangge/sherpa-onnx-sense-voice-small/resolve/master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration values, and conversational text prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scheduled practice prompts, correction feedback, vocabulary review guidance, and setup instructions for optional speech and memory integrations.] <br>

## Skill Version(s): <br>
3.0.4 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

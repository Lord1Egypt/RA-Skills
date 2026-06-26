## Description: <br>
Build, adapt, or run a speech translation workflow that transcribes spoken audio with Whisper or faster-whisper, translates the transcript with the current agent model by default, and synthesizes translated speech with Piper, OpenClaw tts, or a mock backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[decin](https://clawhub.ai/user/decin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn voice input into transcript text, translated text, translated audio, and local pipeline artifacts. It supports conversational OpenClaw voice replies and deterministic file-based batch runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional transcript, translation, and audio notification hooks can run local shell commands with speech-derived content. <br>
Mitigation: Use these hooks only with exact trusted commands, or leave them unset for normal runs. <br>
Risk: Service translation sends transcript text to the configured HTTP translation endpoint. <br>
Mitigation: Prefer local, mock, or agent-file translation for sensitive audio, and use service translation only with a trusted endpoint. <br>
Risk: Command templates from VOICE_TRANSLATE_TEXT_COMMAND_TEMPLATE and VOICE_TRANSLATE_AUDIO_COMMAND_TEMPLATE can execute external processes. <br>
Mitigation: Avoid these environment templates unless their full command strings are reviewed and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/decin/speech-translation) <br>
- [Runtime Notes](references/runtime-notes.md) <br>
- [LLM Translation Pattern](references/llm-translation-pattern.md) <br>
- [OpenClaw Chat Mode](references/openclaw-chat-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local files such as transcript text, translation text, WAV audio, and result JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pipeline output order is transcript, translation, audio, then metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

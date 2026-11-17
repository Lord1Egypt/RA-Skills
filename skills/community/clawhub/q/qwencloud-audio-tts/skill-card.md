## Description:

Synthesizes speech from text using Qwen TTS and CosyVoice models through QwenCloud/DashScope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn text into spoken audio, create narration or voiceover assets, and generate QwenCloud TTS commands or code paths when direct execution is not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis text and API credentials are sent to QwenCloud/DashScope during normal operation.

Mitigation: Use the skill only with text approved for that service and keep API keys in trusted environment variables or .env files that are not exposed in logs or prompts.

Risk: Automatic update-management behavior may run an installed sibling update checker and write update-prompt state under .agents.

Mitigation: Review the update-check skill before approving installation or update actions, and inspect stderr action signals before treating a run as complete.

Risk: Credential and network behavior can be affected by local .env values and QWEN_BASE_URL.

Mitigation: Keep .env and QWEN_BASE_URL under trusted project control and audit them before running the skill in shared or untrusted workspaces.

## Reference(s):

- [Qwen Audio TTS API Supplementary Guide](references/api-guide.md)
- [CosyVoice TTS Guide](references/cosyvoice-guide.md)
- [Qwen Audio TTS Execution Guide](references/execution-guide.md)
- [Audio TTS Prompt Guide](references/prompt-guide.md)
- [Qwen Audio TTS Official Documentation](references/sources.md)
- [Qwen TTS API Reference](https://docs.qwencloud.com/api-reference/speech-synthesis/qwen-tts)
- [Qwen TTS User Guide](https://docs.qwencloud.com/developer-guides/speech/tts)
- [Supported Voices](https://docs.qwencloud.com/api-reference/speech-synthesis/voice-list)
- [QwenCloud Model List](https://www.qwencloud.com/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell and code blocks; execution can produce audio files and response JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio URLs may expire after 24 hours; default output path is output/qwencloud-audio-tts/.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

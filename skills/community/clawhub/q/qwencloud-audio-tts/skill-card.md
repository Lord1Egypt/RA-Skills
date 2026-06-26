## Description: <br>
Synthesize speech from text with Qwen TTS models for voiceovers, narration, read-aloud workflows, and TTS application support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert text into speech through QwenCloud and DashScope TTS models, including standard voice synthesis, instruction-controlled speech style, and CosyVoice output. It is intended for workflows that need generated audio files, audio URLs, API response JSON, or executable fallback commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a QwenCloud or DashScope API key and sends synthesis text, and possibly voice samples, to that service. <br>
Mitigation: Install and run it only when that data sharing is acceptable; keep API keys in environment variables or local placeholder-based configuration and do not expose key values in prompts or logs. <br>
Risk: The security summary notes mandatory update-management behavior that can run another local skill and write persistent state outside the audio task. <br>
Mitigation: Review update-check prompts before approving them, inspect the separate qwencloud-update-check skill before installation, and approve persistent agent configuration edits only when desired. <br>
Risk: Custom QWEN_BASE_URL values can redirect requests to endpoints outside the expected QwenCloud service path. <br>
Mitigation: Use the documented QwenCloud and DashScope endpoints unless the endpoint operator is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cuixiaoyang123/qwencloud-audio-tts) <br>
- [Qwen Audio TTS - Official Documentation](references/sources.md) <br>
- [Qwen Audio TTS - API Supplementary Guide](references/api-guide.md) <br>
- [Qwen Audio TTS - Execution Guide](references/execution-guide.md) <br>
- [CosyVoice TTS Guide](references/cosyvoice-guide.md) <br>
- [Prompt Guide](references/prompt-guide.md) <br>
- [Qwen TTS API](https://docs.qwencloud.com/api-reference/speech-synthesis/qwen-tts) <br>
- [Qwen TTS Guide](https://docs.qwencloud.com/developer-guides/speech/tts) <br>
- [Supported Voices](https://docs.qwencloud.com/api-reference/speech-synthesis/voice-list) <br>
- [QwenCloud Model List](https://www.qwencloud.com/models) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request/response examples, generated audio files, and response JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write audio files under output/qwencloud-audio-tts and response JSON; Qwen TTS audio URLs are described as time-limited.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

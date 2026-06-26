## Description: <br>
Alibaba Cloud Bailian Qwen TTS with voice/mood presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanmoon321](https://clawhub.ai/user/yanmoon321) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate Alibaba Cloud Bailian Qwen text-to-speech audio with selected voices, moods, languages, and output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text is sent to Alibaba Cloud DashScope for speech synthesis. <br>
Mitigation: Invoke only when audio output is intended and avoid sending secrets or sensitive text. <br>
Risk: The skill requires a DASHSCOPE_API_KEY. <br>
Mitigation: Provide the key through the environment and do not place it in prompts, command arguments, or committed files. <br>
Risk: Setup installs unpinned Python dependencies in a skill virtual environment. <br>
Mitigation: Review dependency versions before deployment and run setup in an isolated environment. <br>
Risk: The skill text contains broad guidance to always call the TTS skill for voice responses. <br>
Mitigation: Configure agents to use it only for explicit voice-generation requests and require user intent before translation for TTS. <br>


## Reference(s): <br>
- [Qwen3 TTS Instruct on ClawHub](https://clawhub.ai/yanmoon321/qwen3-tts-instruct) <br>
- [yanmoon321 ClawHub profile](https://clawhub.ai/user/yanmoon321) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated audio files in mp3, wav, pcm, or opus formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and sends synthesis text to Alibaba Cloud DashScope.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

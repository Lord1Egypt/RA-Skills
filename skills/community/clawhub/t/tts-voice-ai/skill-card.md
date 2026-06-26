## Description: <br>
Tts Voice Ai helps agents generate multilingual speech audio from text through MiniMax TTS, including Chinese, English, Japanese, Korean, Cantonese, voice selection, and cloned voice IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiachuan-1](https://clawhub.ai/user/jiachuan-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate speech files for dubbing, narration, audio books, customer-service prompts, and multilingual voice playback. Agents can configure language, voice, style, speed, output format, and MiniMax API region before running the bundled TTS script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to MiniMax for remote text-to-speech processing. <br>
Mitigation: Use only text that is approved for MiniMax processing, and avoid secrets, regulated personal data, or confidential business content unless that provider use is authorized. <br>
Risk: The skill can use cloned or custom voice IDs. <br>
Mitigation: Use cloned or custom voices only with clear permission from the voice owner and for approved use cases. <br>
Risk: The skill requires a MiniMax API key in the runtime environment. <br>
Mitigation: Store MINIMAX_API_KEY in an approved secret-management path and avoid pasting it into prompts, logs, or generated files. <br>


## Reference(s): <br>
- [Tts Voice Ai ClawHub release](https://clawhub.ai/jiachuan-1/tts-voice-ai) <br>
- [MiniMax Platform](https://platform.minimax.io) <br>
- [Packaged skill instructions](artifact/SKILL.md) <br>
- [Packaged TTS script](artifact/tts.py) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with inline shell commands, plus generated audio files such as MP3, WAV, or FLAC] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and sends submitted text to the MiniMax TTS API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

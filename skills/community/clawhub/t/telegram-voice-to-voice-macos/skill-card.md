## Description: <br>
Telegram voice-to-voice for macOS Apple Silicon: transcribe inbound .ogg voice notes with yap (Speech.framework) and reply with Telegram voice notes via say+ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fiberian1981](https://clawhub.ai/user/Fiberian1981) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to handle Telegram voice-note conversations on macOS Apple Silicon by transcribing inbound OGG audio locally and replying with either text or generated Telegram voice notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on macOS-specific tools and will fail on unsupported operating systems. <br>
Mitigation: Install and run it only on macOS with trusted yap and ffmpeg binaries available in PATH. <br>
Risk: The newest-file fallback for inbound OGG audio could select the wrong Telegram voice note. <br>
Mitigation: Prefer passing the exact Telegram attachment path when available. <br>
Risk: Per-user reply-mode preferences are stored locally. <br>
Mitigation: Delete voice_state/telegram.json to clear stored Telegram reply-mode preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fiberian1981/telegram-voice-to-voice-macos) <br>
- [yap Speech.framework transcriber](https://github.com/finnvoor/yap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command usage and generated text or OGG voice-note file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Telegram reply guidance and may produce local OGG/Opus voice-note files through helper scripts.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

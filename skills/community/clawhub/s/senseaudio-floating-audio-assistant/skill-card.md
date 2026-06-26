## Description: <br>
Use when the user wants to open, stop, configure, debug, or package the SenseAudio floating audio assistant in AudioClaw, including system-audio subtitles, bilingual ASR/translation, recent-project organization, copied-text TTS, music generation, or macOS audio routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkzz1225](https://clawhub.ai/user/kkzz1225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run and troubleshoot a macOS AudioClaw assistant for system-audio subtitles, SenseAudio ASR/translation, copied-text TTS, music generation, and transcript organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures macOS system audio for subtitles and SenseAudio processing, which can include confidential calls, protected media, or other people's speech. <br>
Mitigation: Use only with appropriate consent and avoid running it during confidential or protected audio sessions. <br>
Risk: Audio routing through BlackHole and a Multi-Output Device can leave system audio in an unexpected state after use. <br>
Mitigation: Run the stop script when finished so the previous macOS audio route and volume are restored. <br>
Risk: SenseAudio-backed features require sensitive credentials. <br>
Mitigation: Provide credentials through the host AudioClaw runtime and do not print or paste API keys into chat or logs. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/kkzz1225/senseaudio-floating-audio-assistant) <br>
- [Operator Notes](references/operator_notes.md) <br>
- [Quickstart](references/quickstart.md) <br>
- [SenseAudio Integration](references/senseaudio_integration.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [SenseAudio TTS API](https://api.senseaudio.cn/v1/t2a_v2) <br>
- [SenseAudio Music Generation API](https://api.senseaudio.cn/v1/music/song/create) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local wrapper scripts that open, stop, inspect, or diagnose the macOS floating audio assistant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

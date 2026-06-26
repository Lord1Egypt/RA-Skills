## Description: <br>
SenseAudio Floating Audio Assistant is an AudioClaw skill for desktop audio understanding that combines SenseAudio ASR, translation, TTS, music generation, and AudioClaw organization for floating subtitles and transcript workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkzz1225](https://clawhub.ai/user/kkzz1225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AudioClaw users and developers on macOS use this skill to launch and manage SenseAudio-backed floating subtitles, ASR/translation, TTS, music generation, and transcript organization for authorized desktop audio and copied text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture, transmit, and store sensitive audio, clipboard text, transcripts, and local AudioClaw configuration data. <br>
Mitigation: Use it only for audio and copied text the user is authorized to send to SenseAudio or AudioClaw, avoid confidential meetings and copied secrets, stop it when finished, and periodically delete saved runs, clipboard files, logs, and generated metadata from workspace state. <br>
Risk: The skill requires sensitive SenseAudio or AudioClaw credentials. <br>
Mitigation: Provide credentials through the host runtime environment, do not paste keys into chat or committed files, and use the smoke script without live calls when only configuration validation is needed. <br>
Risk: The macOS system-audio workflow changes audio routing and can leave audio in the wrong output state if interrupted. <br>
Mitigation: Run the setup and health-check scripts before starting capture, confirm the Multi-Output Device includes BlackHole 2ch and the real output device, and use the stop script to restore the previous output route and volume. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkzz1225/senseaudio-floating-audio-assistant-v2) <br>
- [Quickstart](references/quickstart.md) <br>
- [Operator Notes](references/operator_notes.md) <br>
- [SenseAudio Integration](references/senseaudio_integration.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Realtime Interpreter README](runtime/realtime_interpreter/README.md) <br>
- [System Audio Setup For BlackHole](runtime/realtime_interpreter/system_audio_setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration paths, and generated or edited text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch local scripts, manage runtime files, generate transcripts and notes, send copied text to TTS, and create music generation metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

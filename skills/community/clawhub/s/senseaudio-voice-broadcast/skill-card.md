## Description: <br>
Turn plain text into persona-driven TTS scripts for narration, companion-style voice messages, emotional comfort audio, and expressive spoken responses, with optional SenseAudio TTS invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JSinBUPT](https://clawhub.ai/user/JSinBUPT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to rewrite plain text into Chinese-first character-style voice scripts with persona summaries and TTS style notes. When audio generation is needed, the skill can guide an agent to call the bundled SenseAudio TTS wrapper with a selected voice ID and output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The TTS wrapper accepts an endpoint override that can send the SenseAudio API key to an arbitrary URL. <br>
Mitigation: Use the default SenseAudio endpoint and do not pass --url unless the destination is fully controlled and trusted. <br>
Risk: Text sent for synthesis is processed by a third-party TTS service. <br>
Mitigation: Avoid sending secrets, private data, or sensitive personal content in TTS requests. <br>
Risk: The bundled script performs network requests and writes audio output files locally. <br>
Mitigation: Review the script before installation, provide credentials through SENSEAUDIO_API_KEY when possible, and choose an explicit output path. <br>


## Reference(s): <br>
- [SenseAudio API Usage Notes](references/senseaudio-api.md) <br>
- [Voice Broadcast Templates](references/voice-broadcast-templates.md) <br>
- [SenseAudio ClawHub Release](https://clawhub.ai/JSinBUPT/senseaudio-voice-broadcast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional shell command snippets and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese output unless another language is requested; may instruct the agent to use SENSEAUDIO_API_KEY or an explicit API key for audio generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
MiniMax TTS helps an agent convert text into speech with the MiniMax API, manage available voices, and clone custom voices when the user provides authorized voice material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbos7](https://clawhub.ai/user/turbos7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate speech audio from text, choose or search MiniMax voices, run long-form asynchronous synthesis, and create custom voice clones with appropriate speaker permission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax receives submitted text and voice-related data during synthesis, voice listing, and voice cloning requests. <br>
Mitigation: Avoid submitting secrets, regulated content, or voice material without appropriate consent, and install only if the MiniMax data flow is acceptable for the use case. <br>
Risk: The skill requires a MiniMax API key that could be exposed if copied into prompts, logs, or shared scripts. <br>
Mitigation: Keep MINIMAX_API_KEY in a private environment variable or secret store and do not paste it into agent-visible text. <br>
Risk: Voice cloning can create synthetic speech that resembles a real speaker. <br>
Mitigation: Clone voices only with the speaker's permission and use watermarking or disclosure controls when appropriate. <br>
Risk: Voice deletion commands may remove custom voices irreversibly. <br>
Mitigation: Double-check the target voice_id before using deletion options. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/turbos7/turbos7-minimax-tts) <br>
- [Async text-to-speech API reference](references/tts-async.md) <br>
- [Sync text-to-speech API reference](references/tts-sync.md) <br>
- [Voice clone API reference](references/voice-clone.md) <br>
- [Voice management API reference](references/voice-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; scripts produce console text, API responses, and saved audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is saved locally by the bundled synthesis script; API calls require MINIMAX_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

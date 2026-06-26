## Description: <br>
Handles voice-to-voice conversations on WhatsApp by transcribing incoming audio and responding with local TTS audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rubenfb23](https://clawhub.ai/user/rubenfb23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to support WhatsApp voice-note conversations by converting incoming audio to text, processing it as a normal prompt, and returning both a text reply and an audio voice note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp voice messages are transcribed and processed by the agent. <br>
Mitigation: Enable the skill only in contexts where users accept voice-message transcription and agent processing. <br>
Risk: The agent sends both text and voice-note replies. <br>
Mitigation: Confirm that automatic text and audio responses are appropriate for the conversation before enabling walkie-talkie mode. <br>
Risk: The skill relies on local transcription and text-to-speech tools. <br>
Mitigation: Verify that the local ffmpeg, whisper-cpp, and sherpa-onnx-tts tooling is trusted before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rubenfb23/walkie-talkie-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for transcribing WhatsApp voice notes, generating local TTS audio, and replying with both text and audio.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

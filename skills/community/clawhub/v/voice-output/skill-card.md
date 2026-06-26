## Description: <br>
Use when Tony says voice reply or asks to speak. Speaks the response aloud via Doubao TTS to MOMAX BS6. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olddirtybikertony](https://clawhub.ai/user/olddirtybikertony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who want spoken agent responses can use this skill to convert selected reply text into Doubao TTS audio and play it locally on macOS when voice output is explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Response text is sent to ByteDance/Doubao for text-to-speech processing. <br>
Mitigation: Use only for text that is acceptable to share with the Doubao TTS service, and avoid speaking secrets or sensitive user data. <br>
Risk: The artifact includes a bundled Doubao access token. <br>
Mitigation: Replace the bundled token with a secured credential and rotate the exposed token if it is real. <br>
Risk: The trigger language can be broad enough to speak replies when voice output was not intended. <br>
Mitigation: Narrow activation to explicit voice-reply commands before deployment. <br>


## Reference(s): <br>
- [Doubao TTS 2.0 API Reference](references/doubao_tts_api.md) <br>
- [Doubao TTS API endpoint](https://openspeech.bytedance.com/api/v1/tts) <br>
- [ClawHub skill page](https://clawhub.ai/olddirtybikertony/voice-output) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Files] <br>
**Output Format:** [Spoken audio playback with command-line status text and temporary MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends response text to Doubao TTS, writes temporary MP3 files, and plays audio locally with afplay.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

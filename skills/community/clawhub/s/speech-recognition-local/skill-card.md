## Description: <br>
Runs faster-whisper locally to transcribe .ogg, .m4a, .mp3, and .wav audio into text with Chinese, English, Japanese, or automatic language detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zktufo](https://clawhub.ai/user/zktufo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn voice messages, meeting recordings, podcasts, and other local audio files into conversation-ready text without sending audio to a third-party API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may download transcription components or model files. <br>
Mitigation: Preinstall and pin faster-whisper and model sources, and confirm the model cache location before deployment. <br>
Risk: Audio content may be transcribed and added to the conversation. <br>
Mitigation: Only provide audio files that are intended to be transcribed into the active conversation, especially in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zktufo/speech-recognition-local) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zktufo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text transcript with status or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcribes .ogg, .m4a, .mp3, and .wav audio up to 25MB; language can be auto, zh, en, or ja.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

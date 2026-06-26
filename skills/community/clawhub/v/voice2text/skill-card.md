## Description: <br>
Offline speech-to-text conversion using a local Vosk model for user-provided WAV audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gs431047](https://clawhub.ai/user/gs431047) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local 16 kHz mono 16-bit WAV files into text without sending audio to a remote speech service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio may contain sensitive speech, and the transcript is returned into the agent session. <br>
Mitigation: Use only audio authorized for transcription and handle generated transcripts according to the user's data-handling requirements. <br>
Risk: The local Vosk model is obtained separately and could be replaced with an untrusted or unsuitable model package. <br>
Mitigation: Install the model from a trusted source and review or pin dependency and model versions before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gs431047/voice2text) <br>
- [Publisher Profile](https://clawhub.ai/user/gs431047) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object containing transcript text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Vosk model directory and a 16 kHz mono 16-bit WAV input file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

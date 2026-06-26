## Description: <br>
Generate speech audio from text using the Telnyx Text-to-Speech API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert supplied text into spoken audio, create voice messages, and generate audio content with selectable Telnyx voices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text provided to the skill is sent to Telnyx for speech generation. <br>
Mitigation: Use only content approved for Telnyx processing, and avoid secrets, regulated data, or private content unless third-party processing is acceptable. <br>
Risk: The output path can create or overwrite files writable by the user. <br>
Mitigation: Choose an explicit output path in a safe directory and review existing files before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teamtelnyx/telnyx-tts) <br>
- [Telnyx Text-to-Speech WebSocket endpoint](wss://api.telnyx.com/v2/text-to-speech/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line text output with a generated audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TELNYX_API_KEY; writes audio to the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

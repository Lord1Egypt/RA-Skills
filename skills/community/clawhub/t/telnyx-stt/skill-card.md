## Description: <br>
Transcribe audio files to text using Telnyx Speech-to-Text API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe selected audio recordings, voice messages, or spoken content through the Telnyx Speech-to-Text API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are uploaded to Telnyx for transcription. <br>
Mitigation: Use only recordings appropriate for Telnyx processing and avoid confidential or non-audio files. <br>
Risk: Use of the Telnyx API key may create provider access or cost exposure. <br>
Mitigation: Use a revocable Telnyx API key with account limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teamtelnyx/telnyx-stt) <br>
- [Telnyx transcription API endpoint](https://api.telnyx.com/v2/ai/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript emitted to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, a TELNYX_API_KEY environment variable, and a user-selected audio file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

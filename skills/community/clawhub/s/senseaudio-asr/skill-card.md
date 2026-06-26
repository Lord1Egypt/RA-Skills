## Description: <br>
Build and troubleshoot SenseAudio speech recognition integrations, including HTTP transcription, realtime WebSocket ASR, audio quality analysis, and recognition record queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose SenseAudio ASR modes and models, construct API requests, handle streaming or batch transcription responses, and troubleshoot speech-to-text workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may send selected recordings, transcripts, and recognition record queries to SenseAudio. <br>
Mitigation: Use only authorized audio and confirm the user is comfortable sending the selected data to SenseAudio before making requests. <br>
Risk: The skill requires access to a SenseAudio API key. <br>
Mitigation: Keep the credential in the SENSEAUDIO_API_KEY environment variable and send it only in the Authorization header. <br>
Risk: Returned audio URLs, API-key fields, session IDs, and trace IDs may expose sensitive operational data. <br>
Mitigation: Avoid logging or sharing these values unless they are strictly needed for the user's task. <br>


## Reference(s): <br>
- [ASR Reference](references/asr.md) <br>
- [SenseAudio Homepage](https://senseaudio.cn) <br>
- [SenseAudio Skill Page](https://clawhub.ai/scikkk/senseaudio-asr) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with API examples and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTP and WebSocket request patterns, model-parameter compatibility checks, parsing guidance, and credential-handling reminders.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

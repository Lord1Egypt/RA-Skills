## Description: <br>
Consume the shared Whisper speech-to-text API over Tailnet at http://100.92.116.99:8765 using OpenAI-compatible audio transcription endpoint (/v1/audio/transcriptions). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to check a shared Tailnet Whisper service, submit selected audio for transcription, add language and file-type hints, time requests, and troubleshoot response output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded audio may contain confidential, regulated, or private content handled by the Tailnet Whisper server. <br>
Mitigation: Send recordings only when the server operator and data handling are trusted; avoid sensitive audio unless approved. <br>
Risk: Transcription behavior depends on the availability and trustworthiness of the disclosed server at 100.92.116.99:8765. <br>
Mitigation: Run the health check and confirm the intended Tailnet service before submitting audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lotfinity/whisper-tailnet-api) <br>
- [Whisper Tailnet API base URL](http://100.92.116.99:8765) <br>
- [Whisper Tailnet API health check](http://100.92.116.99:8765/health) <br>
- [OpenAI-compatible transcription endpoint example](http://100.92.116.99:8765/v1/audio/transcriptions?ext=.wav) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with curl commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-selected audio files and sends binary audio to a disclosed Tailnet endpoint.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

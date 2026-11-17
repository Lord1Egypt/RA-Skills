## Description:

Helps agents call a shared Tailnet Whisper speech-to-text API using the OpenAI-compatible /v1/audio/transcriptions endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to check service health, submit audio, time transcription requests, pass file and language hints, and troubleshoot responses from the shared Tailnet Whisper transcription service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded audio is shared with the disclosed Tailnet Whisper service and may include confidential, regulated, or consent-sensitive content.

Mitigation: Use the skill only when you trust the server operator, network path, and retention practices; avoid sensitive recordings unless those conditions are met.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotfinity/skills/whisper-tailnet-api)
- [Tailnet Whisper API base URL](http://100.92.116.99:8765)
- [Tailnet Whisper transcription endpoint](http://100.92.116.99:8765/v1/audio/transcriptions?ext=.wav)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes curl examples for health checks, binary audio upload, request timing, file extension hints, and optional language hints.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

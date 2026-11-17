## Description:

Whisper Local Api helps agents install, start, health-check, and smoke-test a local OpenAI-compatible Whisper transcription endpoint for private speech-to-text workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hantok](https://clawhub.ai/user/hantok)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a local speech-to-text service that accepts OpenAI Whisper-compatible transcription requests. It is intended for private agent voice-command and audio transcription workflows where audio should stay on local infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote code and Python dependencies can change between installs.

Mitigation: Review the upstream repository and dependency set before installation, and pin or vendor the backend where practical.

Risk: A transcription service exposed beyond the local host could allow unauthenticated access to audio transcription endpoints.

Mitigation: Bind the service to 127.0.0.1 by default; if exposure is required, place it behind authentication and TLS.

Risk: Smoke tests can submit sensitive audio to whichever endpoint is configured.

Mitigation: Use non-sensitive test audio unless the endpoint has been confirmed to be local and loopback-only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hantok/skills/whisper-local-api)
- [ClawHub publisher profile](https://clawhub.ai/user/hantok)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and endpoint configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local service setup and validation; generated commands may clone remote code, install Python dependencies, start a local server, and send a local audio file to the configured transcription endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

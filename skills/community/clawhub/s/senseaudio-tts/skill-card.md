## Description:

Build and debug SenseAudio text-to-speech integrations on `/v1/t2a_v2` and `/ws/v1/t2a_v2`, including sync HTTP, SSE stream, WebSocket event sequencing, hex audio decoding, and voice/audio parameter tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, troubleshoot, and harden SenseAudio text-to-speech integrations across synchronous HTTP, SSE streaming, and WebSocket workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SenseAudio requests require SENSEAUDIO_API_KEY and can expose credentials if keys are committed, logged, or shared broadly.

Mitigation: Store the API key in a private environment variable or secret manager, scope access to intended users, and exclude credentials from code, logs, traces, and generated examples.

Risk: Text sent for speech generation is transmitted to the SenseAudio cloud service.

Mitigation: Do not send secrets, regulated data, or confidential text unless the use is authorized and covered by the appropriate data handling controls.

Risk: Debugging sessions may capture request text, trace identifiers, session identifiers, or credentials.

Mitigation: Keep session and trace logging access-controlled, redact request text and credentials where possible, and retain only the diagnostics needed for troubleshooting.

## Reference(s):

- [TTS Reference](references/tts.md)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/senseaudio-tts)
- [Publisher Profile](https://clawhub.ai/user/scikkk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request structure, streaming event sequencing, audio hex decoding guidance, and production hardening notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

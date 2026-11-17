## Description:

Integration guide for SenseAudio Open Platform APIs, including TTS, ASR, realtime Agents, video generation and storyboard APIs, and voice clone usage constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, and harden SenseAudio Open Platform integrations for text-to-speech, speech recognition, realtime agents, video generation, storyboard workflows, and voice clone usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples may send text, audio, video, prompts, identifiers, or API credentials to SenseAudio services.

Mitigation: Use clear user consent and privacy notices, avoid unnecessary data transfer, and apply retention controls for media and transcripts.

Risk: API keys and realtime tokens can be exposed if examples are copied into source code or logs.

Mitigation: Store credentials in environment variables or a secret manager, never hardcode keys, and redact tokens from logs.

Risk: Incorrect model, endpoint, streaming, or response-parsing choices can produce failed calls or misleading integration behavior.

Mitigation: Validate model and protocol compatibility, check status fields and terminal events before using payloads, and handle transient failures with bounded retries.

## Reference(s):

- [Realtime Agent Reference](references/agent.md)
- [ASR Reference](references/asr.md)
- [TTS Reference](references/tts.md)
- [Video and Storyboard Reference](references/video.md)
- [Voice and Cloning Reference](references/voice.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API request examples, code snippets, shell commands, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP and WebSocket request schemas, response parsing notes, and production error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

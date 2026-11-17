## Description:

Real-time voice assistant for OpenClaw that streams microphone audio through configurable speech-to-text providers into an OpenClaw agent and speaks responses through configurable text-to-speech providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charantejmandali18](https://clawhub.ai/user/charantejmandali18)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to run a browser-based voice interface that transcribes microphone audio, sends turns to an OpenClaw gateway, and speaks the agent response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an unauthenticated network service that can use the operator's speech-provider keys and OpenClaw gateway.

Mitigation: Run it only on a trusted machine or network, bind the server to localhost, and add authentication and Origin checks before exposing it.

Risk: Microphone audio, transcripts, and generated text may be sent to Deepgram or ElevenLabs and written to logs.

Mitigation: Use provider accounts and logging settings appropriate for the data being processed, and avoid speaking sensitive information unless those providers are approved for that use.

Risk: A highly privileged OpenClaw gateway could allow spoken requests to trigger sensitive agent tools or actions.

Mitigation: Connect the voice assistant to a least-privileged OpenClaw gateway and review tool access before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charantejmandali18/skills/voice-assistant)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and environment-variable settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider and gateway configuration for OpenClaw, Deepgram, and ElevenLabs.]

## Skill Version(s):

0.1.0 (source: pyproject.toml, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

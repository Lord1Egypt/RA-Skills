## Description:

Video Chat With Me enables real-time voice and camera conversations with an OpenClaw agent using Groq Whisper for speech recognition, Microsoft edge-tts for speech synthesis, and OpenClaw chat completions for responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxu75374](https://clawhub.ai/user/sxu75374)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to start browser-based video or voice calls where an agent can hear speech, receive optional camera frames, and respond with spoken replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill exposes an unauthenticated network bridge to the user's main OpenClaw agent.

Mitigation: Restrict the service to localhost or add authentication before exposing it on LAN or Tailscale, and prefer a least-privileged isolated OpenClaw agent.

Risk: The security guidance calls out cloud handling of audio by Groq, TTS text by Microsoft, and camera frames or text routed through the configured model.

Mitigation: Use the skill only when those data flows are acceptable, and configure a local or self-hosted model when camera frames should remain local.

Risk: The security summary notes persistent background service behavior.

Mitigation: Make launchd persistence an explicit opt-in decision and remove or disable the service when video chat is not needed.

Risk: The security guidance flags local Groq key storage.

Mitigation: Store the Groq key with restrictive file permissions or in a keychain-backed secret store.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxu75374/skills/videochat-withme)
- [Publisher Profile](https://clawhub.ai/user/sxu75374)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Groq API Keys](https://console.groq.com/keys)
- [edge-tts](https://github.com/rany2/edge-tts)
- [mkcert](https://github.com/FiloSottile/mkcert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, start, stop, and call guidance for a local video-chat service.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

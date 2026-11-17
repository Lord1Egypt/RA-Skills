## Description:

Voice input and microphone button for OpenClaw WebChat Control UI that records browser audio, sends it to a local faster-whisper transcription service, and injects the resulting text into chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neldar](https://clawhub.ai/user/neldar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add browser microphone controls, local speech-to-text transcription, keyboard shortcuts, and localized voice-input UI to the OpenClaw WebChat Control UI. It is intended for local voice input workflows that rely on a local faster-whisper backend and an HTTPS/WSS proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill patches the local OpenClaw Control UI and installs a startup hook that re-applies browser JavaScript after updates.

Mitigation: Install only when this persistence is acceptable, review the hook before deployment, and disable or uninstall it if update-survival behavior is not needed.

Risk: The injected browser JavaScript is copied from a mutable workspace path.

Mitigation: Restrict who can modify ~/.openclaw/workspace/voice-input/voice-input.js and keep the local workspace protected.

## Reference(s):

- [Troubleshooting - Voice Input](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local deployment, status, and uninstall guidance for modifying OpenClaw Control UI voice input.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Adds voice input through local Whisper ASR and voice output through Edge TTS, with agent-specific voices and an optional helper for sending Telegram voice replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[believe3344](https://clawhub.ai/user/believe3344)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to transcribe incoming voice messages, synthesize spoken replies, and optionally send generated voice messages through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice text or audio may be sent to Edge TTS and Telegram services.

Mitigation: Deploy only where those data flows are acceptable, and avoid using the skill for confidential voice content unless external transmission has been reviewed.

Risk: Telegram bot tokens may be read from local OpenClaw configuration or environment variables.

Mitigation: Protect ~/.openclaw/openclaw.json and token-bearing environments with least-privilege file permissions and rotate tokens if exposure is suspected.

Risk: Inbound audio can be moved and deleted after successful transcription.

Mitigation: Keep separate backups or retention controls for audio that must be preserved for audit, retry, or user-support workflows.

Risk: The security review flags unsafe code/config handling, ASR output isolation concerns, dependency pinning gaps, and missing helper scripts.

Mitigation: Review scripts before execution, avoid untrusted installer arguments, pin dependencies for deployment, and resolve missing helper scripts before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/believe3344/skills/voice-tts)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON status objects, shell commands, and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer, Python 3, ffmpeg, edge-tts, whisper, and click.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

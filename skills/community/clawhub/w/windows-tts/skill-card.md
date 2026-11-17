## Description:

Push text notifications to Windows Azure TTS service for audio broadcast via Bluetooth speakers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmosakg](https://clawhub.ai/user/cmosakg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send reminder, alarm, announcement, and status-check requests from an agent to a configured Windows TTS server on their network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided notification text is sent to a configured Windows TTS server and may include private household or personal details.

Mitigation: Avoid sending medical, financial, credential, or other sensitive details through TTS broadcasts.

Risk: The skill depends on a reachable Windows TTS server and local-network configuration.

Mitigation: Install only when you control the server and network, keep the server off the public Internet, and use HTTPS or authentication if the server supports it.

Risk: Automated heartbeat or cron reminders can broadcast messages without a fresh human review.

Mitigation: Review scheduled reminders before enabling automated broadcasts and keep messages concise and appropriate for the listening environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cmosakg/skills/windows-tts)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact plugin manifest](artifact/openclaw.plugin.json)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration]

**Output Format:** [JSON tool responses and text payloads sent to a configured TTS server]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Windows TTS server URL; supports optional voice, volume, language, and timeout settings.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, CHANGELOG, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

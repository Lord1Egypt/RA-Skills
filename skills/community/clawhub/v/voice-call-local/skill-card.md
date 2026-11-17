## Description:

Start voice calls via the OpenClaw voice-call plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deichmann181](https://clawhub.ai/user/deichmann181)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let agents initiate and inspect voice calls through the OpenClaw voice-call plugin using Twilio, Telnyx, Plivo, or mock mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Twilio, Telnyx, or Plivo modes can place real calls through third-party services.

Mitigation: Use mock mode for testing and confirm recipients, message content, consent, and provider costs before allowing live calls.

Risk: The skill requires the OpenClaw voice-call plugin to be enabled and configured before use.

Mitigation: Enable the voice-call plugin intentionally and configure the selected provider under plugins.entries.voice-call.config before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deichmann181/skills/voice-call-local)
- [Publisher profile](https://clawhub.ai/user/deichmann181)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for using the OpenClaw voice-call CLI and voice_call tool actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

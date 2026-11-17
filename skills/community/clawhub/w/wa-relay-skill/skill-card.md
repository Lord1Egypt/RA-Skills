## Description:

Wa Relay routes third-party WhatsApp direct messages through an OpenClaw relay agent that forwards them to the main agent via sessions_send, so the owner receives the message with a suggested response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zarruk](https://clawhub.ai/user/zarruk)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to route WhatsApp messages from third parties through a relay agent, notify the owner, and prepare suggested responses while keeping direct owner messages on the main agent. It also supports direct-number allowlists for trusted contacts that should bypass the relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can duplicate model-provider credentials for the relay agent, creating broader persistent access than the main agent alone.

Mitigation: Review the setup script before installation, prefer a dedicated low-privilege relay credential, and copy credentials only after confirming that access is acceptable.

Risk: Installation can patch installed OpenClaw runtime files to change session ID validation.

Mitigation: Use an upstream OpenClaw fix instead of the patch when available, review the files before patching, and keep the generated backups so the change can be reverted.

Risk: Generated routing configuration can replace existing bindings and route unintended WhatsApp senders through the relay or main agent.

Mitigation: Validate the generated routing JSON manually, keep trusted direct allowlists small, preserve existing agents and bindings intentionally, and restart/test the gateway after applying changes.

Risk: The setup script modifies the main agent's SOUL.md so relay messages affect owner notifications and suggested responses.

Mitigation: Review the appended relay instructions after setup and adjust them to match the owner's communication policy before relying on the relay.

## Reference(s):

- [WA Relay Setup Guide](references/SETUP.md)
- [OpenClaw session ID issue #16211](https://github.com/openclaw/openclaw/issues/16211)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup may create or update local OpenClaw workspace files, copy relay credentials after confirmation, patch installed OpenClaw files after confirmation, and write generated routing JSON to /tmp/wa-relay-config.json.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

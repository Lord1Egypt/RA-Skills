## Description:

Comprehensive Signal channel integration via signal-cli for sending messages, reactions, handling group chat interactions, and configuring Signal access for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blake-lucas](https://clawhub.ai/user/blake-lucas)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and operate Signal messaging for OpenClaw agents, including direct messages, group safeguards, reactions, diagnostics, and signal-cli installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance downloads signal-cli release artifacts without checksum or signature verification.

Mitigation: Prefer an OS package manager or a pinned signal-cli release with checksum or signature verification before placing binaries on PATH.

Risk: Installation examples append PATH changes to shell startup files, creating persistent environment changes.

Mitigation: Review shell profile edits before running them and apply persistent PATH changes only when intended.

Risk: Signal messaging can expose agent actions to direct-message or group-chat participants.

Mitigation: Use a separate Signal bot number, pairing or allowlist policies, group allowlists, and direct owner confirmation for destructive or externally visible actions.

## Reference(s):

- [Signal Skill Release Page](https://clawhub.ai/blake-lucas/skills/signal)
- [OpenClaw Signal Docs](https://docs.openclaw.ai/channels/signal)
- [signal-cli Project and Documentation](https://github.com/AsamK/signal-cli)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Signal target formats, group safety guidance, configuration options, diagnostics, and installation commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

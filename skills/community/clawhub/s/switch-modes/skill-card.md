## Description:

Switch between AI models dynamically to optimize costs and performance. Use when the user says mode commands like "eco mode", "balanced mode", "smart mode", or "max mode", or when they want to check their current mode with "/modes status" or configure modes with "/modes setup".

This skill is ready for commercial/non-commercial use.

## Publisher:

[serudda](https://clawhub.ai/user/serudda)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to configure four named model modes, check the active mode, and switch the default model for cost, performance, or task-fit reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite the global OpenClaw model setting, affecting cost and future sessions.

Mitigation: Confirm before writing changes, back up ~/.openclaw/openclaw.json, and use explicit slash commands where possible.

Risk: Ambiguous words such as eco, balanced, smart, or max can trigger model changes.

Mitigation: Ask for confirmation when a user request is ambiguous or lacks clear mode-switching intent.

Risk: Configuration files may contain API keys or other sensitive OpenClaw settings.

Mitigation: Avoid exposing full configuration contents in chat, logs, or error messages.

## Reference(s):

- [Switch Modes Reference Guide](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with JSON configuration changes and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local OpenClaw configuration files for the active user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

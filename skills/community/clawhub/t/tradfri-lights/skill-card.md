## Description:

Controls IKEA TRÅDFRI lights and groups through a local TRÅDFRI gateway using node-tradfri-client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymebosma](https://clawhub.ai/user/ymebosma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect and control IKEA TRÅDFRI lights, groups, floors, and layout presets from an agent running on the same local network as a configured gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable TRÅDFRI gateway credentials may be exposed in chat, terminal output, or agent logs during setup.

Mitigation: Keep the PSK out of chat and logs, avoid printing authentication results, and store config.json with owner-only permissions.

Risk: Whole-house, floor, and layout commands can change many configured lights at once.

Mitigation: Use broad commands only when that scope is intended, confirm surprising household-wide actions, and prefer verification flags when practical.

## Reference(s):

- [TRÅDFRI setup notes](references/setup.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally reachable TRÅDFRI gateway and user-provided credentials; action commands may change physical lights.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

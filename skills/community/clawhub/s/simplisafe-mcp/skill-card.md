## Description:

Query and control a SimpliSafe alarm system from the shell with curl — read system state, sensors, locks, events and settings, and arm/disarm or lock/unlock. Use when the user asks about their SimpliSafe alarm, house sensors, door locks, or whether the system is armed. Requires a one-time browser login to mint a refresh token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners and developers use this skill to inspect SimpliSafe alarm status, sensors, locks, events, and settings, and to control alarm and lock state when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe token caching could let a local attacker obtain alarm-system access.

Mitigation: Wait for corrected cache handling before connecting a real alarm account; use private verified storage, secure file replacement, and strictly numeric expiry validation.

Risk: Alarm and lock commands can change the state of physical security devices.

Mitigation: Keep user confirmation for alarm and lock changes.

Risk: Alarm PINs are present in cleartext in one settings response.

Mitigation: Display PINs only when explicitly requested.

## Reference(s):

- [SimpliSafe curl and jq recipes](references/recipes.md)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/simplisafe-mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Configuration guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that can change alarm or lock state; PIN data is returned in cleartext by the API.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

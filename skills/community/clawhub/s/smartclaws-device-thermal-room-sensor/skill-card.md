## Description:

Device contract for a telemetry-only room thermal sensor that defines SmartClaws topics, payload fields, and master-agent interpretation rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill with a SmartClaws master agent to interpret room temperature telemetry from a read-only thermal sensor. It defines the expected telemetry topic, payload fields, validation rules, and limits on how relay correlation may be used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sensor contract is read-only and command-free, so treating it as a command-capable device could cause an agent to attempt unsupported actions.

Mitigation: Pair it only with the intended SmartClaws master agent and treat it as a telemetry interpretation contract, not a command interface.

Risk: Missing or stale telemetry, relay state, or channel configuration can lead to incorrect assumptions about the current room state.

Mitigation: Use the required SMARTCLAWS.md telemetry channel, honor stale_relay and stale_relay_seconds, and report missing fresh readings instead of guessing.

## Reference(s):

- [SmartClaws project](https://github.com/skalenetwork/smartclaws)
- [ClawHub skill page](https://clawhub.ai/eduv09/skills/smartclaws-device-thermal-room-sensor)

## Skill Output:

**Output Type(s):** [guidance, configuration, text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines telemetry topic, payload fields, sanity rules, and command restrictions; it does not emit commands or executable code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

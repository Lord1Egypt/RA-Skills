## Description:

Device contract for a NovaPM/SDS011 air-quality bridge that defines SmartClaws telemetry topics, payloads, local serial behavior, and safety rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SmartClaws operators use this skill to configure bridge and master agents for read-only SDS011 air-quality telemetry. It helps agents publish and interpret PM2.5/PM10 readings without inventing channels, commands, or sensor data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry can be misleading if the serial port, warmup, polling cadence, or outgoing telemetry channel do not match the actual SDS011 setup.

Mitigation: Confirm the outgoing telemetry channel, serial port, warmup, and polling cadence against the deployed hardware before use.

Risk: Command channels or invented readings would conflict with the telemetry-only device contract.

Mitigation: Keep incoming command channels absent, reject invalid or stale readings, and publish no telemetry rather than repaired or invented values.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/eduv09/skills/smartclaws-device-novapm-sds011)
- [SmartClaws project](https://github.com/skalenetwork/smartclaws)

## Skill Output:

**Output Type(s):** [guidance, configuration, markdown]

**Output Format:** [Markdown guidance with JSON telemetry examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telemetry-only; no command or actuation channels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

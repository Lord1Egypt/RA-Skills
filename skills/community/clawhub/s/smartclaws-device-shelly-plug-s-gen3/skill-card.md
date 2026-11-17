## Description:

Device contract for Shelly Plug S Gen3 that defines SmartClaws topics, payloads, local Shelly RPC methods, and safety rules for bridge and master agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill with SmartClaws bridge and master agents to integrate a Shelly Plug S Gen3, read normalized switch telemetry, and publish authorized switch commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands could switch the wrong device or be routed through the wrong channel.

Mitigation: Confirm the registered device name, command channel, and setup authority before enabling command publishing.

Risk: Shelly credentials could be exposed during bridge operation.

Mitigation: Provide credentials through the configured setup mechanism and keep them out of logs and agent responses.

Risk: Telemetry could be misleading if missing values are invented or plug temperature is treated as room temperature.

Mitigation: Publish only observed numeric fields and treat the reported temperature as internal plug temperature.

Risk: Repeated or stale commands could cause unintended switching.

Mitigation: Check recent telemetry and decision state before sending commands, and persist handled command offsets in bridge state.

## Reference(s):

- [SmartClaws](https://github.com/skalenetwork/smartclaws)
- [Shelly Plug S Gen3 docs](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen3/ShellyPlugSG3)
- [Shelly Switch component RPC](https://shelly-api-docs.shelly.cloud/gen2/Components/FunctionalComponents/Switch/)
- [Shelly RPC protocol](https://shelly-api-docs.shelly.cloud/gen2/General/RPCProtocol)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Device telemetry and command payload guidance for SmartClaws agents]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

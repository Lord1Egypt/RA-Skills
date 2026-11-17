## Description:

Runs one SmartClaws bridge cycle for a single configured device by reading local hardware or API data, validating it against the device contract, publishing telemetry on-chain, and optionally applying validated on-chain commands in command-enabled modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device operators use this skill to run a single SmartClaws telemetry bridge cycle for one configured device. It supports validated telemetry publishing and optional command handling when the configured bridge mode and device contract allow it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command-enabled modes can apply device commands to the configured local device.

Mitigation: Keep the default telemetry-only mode unless command handling is intentional, and require AGENTS.md, SMARTCLAWS.md, channel configuration, and device-contract validation before applying commands.

Risk: Telemetry and command results may be published on-chain or disclosed from encrypted channels.

Mitigation: Install only with the intended SmartClaws device and channels configured, use the appropriate read or disclose flow for channel type, and treat a message as stored only when publish status is published.

Risk: Incorrect setup could expose secrets, use the wrong wallet authority, or publish invalid sensor data.

Mitigation: Do not read or print wallet or key material, fail closed when setup is incomplete, and discard implausible readings instead of publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eduv09/skills/smartclaws-bridge-agent)
- [SmartClaws homepage](https://github.com/skalenetwork/smartclaws)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown procedural guidance with SmartClaws tool actions and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs one cycle per invocation; may result in on-chain telemetry publication or command-result logs through SmartClaws tooling.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

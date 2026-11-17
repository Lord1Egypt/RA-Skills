## Description:

Control Shelly BluTRV thermostats and H&T sensors via local RPC with cloud fallback for temperature reading and heater target changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolf128058](https://clawhub.ai/user/wolf128058)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home-automation operators use this skill to query Shelly room temperatures, inspect thermostat status, and set BluTRV target temperatures through configured local gateways with cloud fallback for supported sensors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged behavior includes broader device-control capabilities than the published thermostat-management scope clearly authorizes.

Mitigation: Review before installing and prefer a release that removes firmware, calibration, relay, and raw cloud controls or gates them behind explicit user approval and strict device allowlists.

Risk: Shelly credentials and device mappings can expose or control a live home environment.

Mitigation: Use only a trusted, tightly protected Shelly environment file dedicated to this skill and keep credentials out of chat logs and repository files.

Risk: Heating or relay writes can affect physical devices if the target is wrong or the final state is not verified.

Mitigation: Confirm every write that affects heating or relays, verify target identity against the configured allowlist, and perform a follow-up read before reporting success.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wolf128058/skills/shelly-blutrv-manager)
- [Setup - Shelly BluTRV](references/setup.md)
- [Auth and Access - Shelly BluTRV](references/auth-and-access.md)
- [Shelly Device Registry](references/devices.md)
- [Troubleshooting - Shelly BluTRV](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and normalized JSON command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may perform local network RPC or Shelly Cloud API calls when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

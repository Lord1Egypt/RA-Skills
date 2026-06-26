## Description: <br>
Control Shelly BluTRV thermostats and H&T sensors locally via RPC with cloud fallback for temperature reading and setting heater targets in specified rooms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolf128058](https://clawhub.ai/user/wolf128058) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home automation operators use this skill to inspect Shelly room temperature and thermostat status, then set BluTRV target temperatures through local gateways with cloud fallback for supported sensors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real Shelly thermostats and other device controls when configured with gateway access and a Shelly Cloud token. <br>
Mitigation: Install only when that authority is intended, keep credentials scoped to Shelly use, and require explicit user confirmation before write actions. <br>
Risk: Timed heating behaviors such as boost or override may be misleading until fixed. <br>
Mitigation: Avoid relying on boost or override durations and verify thermostat state with a follow-up status read after any change. <br>
Risk: Raw cloud, relay, firmware-update, and calibration commands provide broader device-control authority than routine thermostat status and target changes. <br>
Mitigation: Avoid those commands unless the operator deliberately wants that broader control and has confirmed the target device. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wolf128058/shelly-blutrv-manager) <br>
- [Setup](references/setup.md) <br>
- [Auth and Access](references/auth-and-access.md) <br>
- [Shelly Device Registry](references/devices.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read and control real Shelly devices when local gateway and cloud credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

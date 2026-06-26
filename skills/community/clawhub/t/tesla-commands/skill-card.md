## Description: <br>
Control your Tesla via MyTeslaMate API. Supports multi-vehicle accounts, climate control, and charging schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovaris](https://clawhub.ai/user/ovaris) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and automation agents use this skill to inspect MyTeslaMate vehicle status and issue Tesla control commands such as waking a vehicle, managing climate, setting charge limits, and changing charge schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent token-backed authority to read vehicle status and change Tesla settings. <br>
Mitigation: Protect the MyTeslaMate token like a credential and only run commands after confirming the intended vehicle and action. <br>
Risk: Mutating commands can immediately alter vehicle state, including climate, charge limits, and charging schedules. <br>
Mitigation: Review proposed commands before execution and use schedule-removal or other mutating options only when the vehicle state should change immediately. <br>
Risk: The security summary identifies weak safeguards and an under-documented schedule-deletion command. <br>
Mitigation: Prefer explicit VIN targeting, verify the current schedule before deletion, and avoid exposing this skill to unattended workflows. <br>


## Reference(s): <br>
- [Tesla Commands on ClawHub](https://clawhub.ai/ovaris/tesla-commands) <br>
- [MyTeslaMate Fleet](https://app.myteslamate.com/fleet) <br>
- [MyTeslaMate Vehicles API](https://api.myteslamate.com/api/1/vehicles) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TESLA_MATE_TOKEN and an optional TESLA_VIN or --vin argument to target vehicles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

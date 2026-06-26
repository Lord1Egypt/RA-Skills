## Description: <br>
Controls reverse-engineered BLE toys through a local ToyBridge HTTP server by sending vibrate, stop, and status commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmandaClarke61](https://clawhub.ai/user/AmandaClarke61) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and device owners who have reverse-engineered an unsupported BLE toy use this skill to let an agent send ToyBridge vibrate, stop, and status commands to a local server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent direct physical control over a local BLE toy without built-in confirmation, consent, or safety limits. <br>
Mitigation: Use only with a device and ToyBridge server you control, require explicit consent before starting or changing vibration, specify intensity and duration, and verify the stop command first. <br>
Risk: The external ToyBridge server and device-specific BLE worker determine what commands actually reach the device. <br>
Mitigation: Inspect and secure the ToyBridge server separately before use, and confirm the configured BLE worker matches the intended device. <br>


## Reference(s): <br>
- [ToyBridge setup guide](https://github.com/AmandaClarke61/toybridge) <br>
- [ClawHub skill page](https://clawhub.ai/AmandaClarke61/toybridge) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local ToyBridge server and configured BLE worker; intensity values are 0-100.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

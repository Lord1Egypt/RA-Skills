## Description: <br>
Control a Venus (Cachito) BLE vibrator from natural language. Calls a local HTTP server that broadcasts BLE commands to the toy via macOS CoreBluetooth. Requires hardware setup; see the ToyBridge repo before installing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmandaClarke61](https://clawhub.ai/user/AmandaClarke61) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers who intentionally run a local ToyBridge server on macOS use this skill to let an agent send vibration, stop, status, and preset pattern commands to a Venus/Cachito BLE vibrator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can control a physical BLE vibrator through the local bridge. <br>
Mitigation: Install only when this physical device control is intentional, start at low intensity, and use stop commands or close the bridge when finished. <br>
Risk: The skill depends on external ToyBridge code and a local HTTP server. <br>
Mitigation: Review the ToyBridge code before running it and keep the bridge active only during intended use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AmandaClarke61/venus-ble-vibrator) <br>
- [ToyBridge Setup Guide](https://github.com/AmandaClarke61/toybridge) <br>
- [Buttplug.io Device Compatibility Index](https://iostindex.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a user-run local HTTP bridge on port 8888 and support intensity values from 0 to 100.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Control a Sphero Mini robot ball over Bluetooth Low Energy with Python and bleak for rolling, LED control, sensor access, drawing shapes, and battery or power management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonesChi](https://clawhub.ai/user/JonesChi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and Sphero Mini owners use this skill to set up Python BLE control, run command-line examples, and generate code for movement, LED, sensor, battery, and shape-drawing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Linux troubleshooting commands can make broad persistent system permission changes. <br>
Mitigation: Use the bleak-based setup where possible, and avoid sudo or setcap commands unless you understand their system-wide effect and how to reverse them. <br>
Risk: Movement scripts control a physical Sphero Mini and may cause unintended motion. <br>
Mitigation: Run movement modes only in a clear bounded area and supervise the device while scripts are active. <br>
Risk: Some documentation points to external GitHub files for download. <br>
Mitigation: Inspect and pin external files before downloading or executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonesChi/sphero-mini) <br>
- [JonesChi publisher profile](https://clawhub.ai/user/JonesChi) <br>
- [Sphero Mini API Reference](references/api.md) <br>
- [Sphero Mini Examples](references/examples.md) <br>
- [Sphero Mini Troubleshooting](references/troubleshooting.md) <br>
- [sphero_mini_win library](https://github.com/trflorian/sphero_mini_win) <br>
- [bleak Bluetooth LE library](https://github.com/hbldh/bleak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the bleak package, Bluetooth LE access, and a local Sphero Mini device.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

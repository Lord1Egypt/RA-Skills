## Description: <br>
Read light intensity from USB sensors with real-time monitoring, filtering, and threshold detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LJ-Hao](https://clawhub.ai/user/LJ-Hao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to read lux values from a USB-connected light sensor, monitor ambient light levels, and apply dark or bright thresholds in local automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local USB serial access requires dialout permissions, which grant ongoing access to serial devices. <br>
Mitigation: Install only on supervised Linux systems where that access is acceptable, verify the device path before use, and remove unnecessary serial permissions when the workflow no longer needs them. <br>
Risk: The usage guide includes AI-driven USB relay examples even though the core sensor reader is read-only. <br>
Mitigation: Do not copy or run relay-control examples unless the attached device is harmless, supervised, and has a manual shutoff path. <br>
Risk: The usage guide shows a plaintext model API key placeholder in configuration examples. <br>
Mitigation: Use environment variables or a secret manager for real API keys and avoid storing live credentials in plaintext configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LJ-Hao/usb-light-sensor-reader) <br>
- [README](README.md) <br>
- [Setup guide](setup.md) <br>
- [Usage guide](USAGE-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent guidance may reference local USB serial hardware at /dev/ttyUSB0 and Linux dialout permissions.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

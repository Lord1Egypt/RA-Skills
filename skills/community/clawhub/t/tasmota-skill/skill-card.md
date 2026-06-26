## Description: <br>
Discovers, monitors, and controls Tasmota-powered ESP8266 and ESP32 smart home devices on local networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wmantly](https://clawhub.ai/user/wmantly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, home automation operators, and authorized network administrators use this skill to discover Tasmota devices, check status, and issue supported power, brightness, and color commands on networks they own or administer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network discovery can scan local subnets and contact devices beyond the intended target set. <br>
Mitigation: Run discovery only on networks you own or are authorized to scan, and review the target network before execution. <br>
Risk: Device control commands can change power, brightness, color, or other Tasmota settings. <br>
Mitigation: Review every control action before running it, prefer explicit device IPs and supported commands, and avoid raw Tasmota commands unless their effect is understood. <br>
Risk: Status queries and inventory output may reveal local IP addresses, device names, Wi-Fi details, hostnames, or MAC addresses. <br>
Mitigation: Use the skill in trusted environments and avoid sharing command output that contains local network or device identifiers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus JSON, tabular text, and CSV-style inventory data from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a CSV inventory of discovered devices for bulk status checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

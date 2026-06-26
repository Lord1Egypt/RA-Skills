## Description: <br>
A local Bash logbook for recording, searching, and exporting Raspberry Pi operations notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep a local journal of Raspberry Pi-related operational notes, search past entries, and export records for reporting. It is not evidence of live device control, monitoring, service management, webhooks, or notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a Raspberry Pi manager with GPIO control, live monitoring, service management, sensor reading, webhooks, and notification capabilities it does not provide. <br>
Mitigation: Treat it as a local operations journal only, and do not rely on it for live device control or infrastructure automation. <br>
Risk: Operational logs may contain secrets, hostnames, IP addresses, or other sensitive infrastructure details entered by the user. <br>
Mitigation: Avoid entering secrets or sensitive infrastructure details, and review local log and export files before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/raspberry-pi-manager) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Plain text terminal output and local JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs and exports under ~/.local/share/raspberry-pi-manager; no external services are required.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

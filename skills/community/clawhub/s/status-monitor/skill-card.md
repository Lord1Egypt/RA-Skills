## Description: <br>
Manages OpenClaw Agent status upload scripts, periodically syncing agent online status to the cloud monitoring platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yahao333](https://clawhub.ai/user/yahao333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to enable agent status heartbeats to a cloud dashboard, monitor which agents are online, and manage the local uploader service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads OpenClaw agent IDs and heartbeat timing to a cloud monitoring dashboard. <br>
Mitigation: Install only when the monitoring dashboard is trusted and users are comfortable sharing that status data. <br>
Risk: The monitoring token can authorize status uploads if exposed. <br>
Mitigation: Set the token through the documented environment variable or local credential file, avoid pasting secrets into chat, and rotate the token if exposed. <br>
Risk: The uploader can run as a background service after setup. <br>
Mitigation: Use the documented stop command before uninstalling the skill or whenever background uploads are no longer wanted. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Chinese README](artifact/README_cn.md) <br>
- [OpenClaw Agent Monitor Dashboard](https://openclaw-agent-monitor.vercel.app) <br>
- [OpenClaw Agent Monitor Repository](https://github.com/yahao333/openclaw-agent-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or stop a local background uploader and update OpenClaw credential or interval configuration.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

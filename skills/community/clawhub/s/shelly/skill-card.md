## Description: <br>
Control and automate Shelly devices with local RPC workflows, secure access modes, cloud API coordination, and safe multi-device execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and smart-home operators use this skill to inspect, control, and automate Shelly devices across local RPC, cloud, WebSocket, and MQTT workflows while preserving explicit write-safety gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real Shelly devices, including power, heating, security, or bulk actions, when the user approves writes. <br>
Mitigation: Start in read-only mode and require explicit confirmation, canary execution, and read-after-write verification before high-impact or multi-device actions. <br>
Risk: Cloud and local device state can diverge, causing inconsistent command outcomes or duplicate writes. <br>
Mitigation: Resolve the control plane before acting, reconcile device identity across local and cloud views, and stop rollout on state mismatch. <br>
Risk: Credential exposure could occur if Shelly cloud tokens are pasted into chat or stored in local notes. <br>
Mitigation: Read SHELLY_CLOUD_TOKEN from environment variables, use least-privilege credentials, and keep local Shelly notes protected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/shelly) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill Homepage](https://clawic.com/skills/shelly) <br>
- [Shelly API Documentation](https://shelly-api-docs.shelly.cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, command payload guidance, checklists, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local RPC, cloud API, WebSocket, or MQTT actions; write operations require explicit confirmation and post-command verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Helps a local agent send proactive text messages to a user's WeChat phone account through an existing OpenClaw WeChat channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billllx](https://clawhub.ai/user/billllx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who already control an OpenClaw WeChat account use this skill to send single-recipient operational notices, alerts, and status updates from local agents. It also provides local verification and troubleshooting commands for the WeChat push path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send proactive and silent WeChat messages using local OpenClaw account context. <br>
Mitigation: Install and operate it only for an OpenClaw WeChat account you control and with clear recipient consent. <br>
Risk: Openids, bot account files, and context-token files are sensitive local data used to select the WeChat recipient and bot account. <br>
Mitigation: Keep the generated configuration private, avoid sharing account/context files, and review local file permissions before use. <br>
Risk: Verification and optional cron probes can create recurring outbound WeChat traffic, including silent probe messages. <br>
Mitigation: Run verification and cron probes only when intentional, and disable or remove scheduled probes when continuous health checks are not needed. <br>
Risk: The installer creates local command symlinks and can perform a verification probe during setup. <br>
Mitigation: Review the installer before running it and confirm that the symlink targets and verification behavior match the intended local environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/billllx/wechat-push-skill) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Protocol Notes](references/protocol-notes.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces single-recipient text push commands and diagnostic output; visible or silent sends may create outbound WeChat traffic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

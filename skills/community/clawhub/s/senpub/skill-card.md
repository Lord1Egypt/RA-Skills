## Description: <br>
Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiger-xzp](https://clawhub.ai/user/tiger-xzp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure ClawSentry security plugins, complete login authorization, and enable OpenClaw protections for prompt injection, sensitive data leakage, risky operations, and malicious skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication responses may be persisted in `.state/poll_login.log`, including credential material such as API keys or account identifiers. <br>
Mitigation: Install in an environment with protected local logs, then delete or secure `.state` logs after setup. <br>
Risk: The installer restarts the local OpenClaw gateway after authorization. <br>
Mitigation: Run installation during an approved maintenance window or on a non-sensitive machine where a gateway restart is acceptable. <br>
Risk: The script writes received credentials into local OpenClaw plugin configuration. <br>
Mitigation: Restrict local configuration file access and avoid installing on shared hosts unless credential storage is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tiger-xzp/senpub) <br>
- [Volcengine website](https://www.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and login URL guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local OpenClaw configuration changes and .state files during installation.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

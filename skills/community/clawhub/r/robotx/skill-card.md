## Description: <br>
Use the robotx CLI to deploy, manage versions, and check status for RobotX applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haibingtown](https://clawhub.ai/user/haibingtown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to install and authenticate the RobotX CLI, deploy RobotX applications, inspect projects and versions, check deployment status, view logs, and publish builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the RobotX CLI through a remote shell script can execute installer code from the network. <br>
Mitigation: Review the installer before use, or use a pinned release and checksum when available. <br>
Risk: RobotX credentials may be stored in environment variables or in ~/.robotx.yaml. <br>
Mitigation: Use least-privilege credentials, prefer environment variables for CI, and protect or remove ~/.robotx.yaml on shared machines. <br>
Risk: Deploy and publish commands can affect RobotX application releases. <br>
Mitigation: Confirm project, build, deploy, and publish targets before executing CLI commands. <br>


## Reference(s): <br>
- [RobotX Deploy CLI on ClawHub](https://clawhub.ai/haibingtown/robotx) <br>
- [RobotX hosted login](https://robotx.xin) <br>
- [RobotX CLI binary installer script](https://raw.githubusercontent.com/haibingtown/robotx_cli/main/scripts/install.sh) <br>
- [RobotX CLI Go installer script](https://raw.githubusercontent.com/haibingtown/robotx_cli/main/scripts/go-install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends JSON stdout for RobotX CLI commands in agent workflows, with progress logs on stderr.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

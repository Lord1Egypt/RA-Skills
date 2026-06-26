## Description: <br>
Tool discovery and shell one-liner reference for sysadmin, DevOps, and security tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, sysadmins, DevOps engineers, and security practitioners use this skill to choose tools and draft shell-command guidance for network, DNS, TLS, process, log, container, and security troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad dual-use sysadmin and security references include copyable high-risk commands such as packet capture, netcat, hping3, delete, secure-wipe, /etc/profile, and external web-scanner examples. <br>
Mitigation: Require review before execution, limit use to authorized systems, and have the agent explain operational impact before presenting or running commands. <br>
Risk: The refresh script can sync reference content from an upstream repository, changing recommendations after release. <br>
Mitigation: Avoid automatic refresh unless the upstream source is trusted and each refresh is reviewed and rescanned before deployment. <br>
Risk: Auto-consult behavior may surface powerful commands in routine troubleshooting contexts. <br>
Mitigation: Use the skill for command discovery and guidance; do not allow blind copy-paste or unattended execution. <br>


## Reference(s): <br>
- [CLI Tools](references/cli-tools.md) <br>
- [Security Tools](references/security-tools.md) <br>
- [Shell One-liners](references/shell-oneliners.md) <br>
- [Shell Tricks](references/shell-tricks.md) <br>
- [Web Tools](references/web-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and command-oriented recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and tool suggestions should be reviewed before execution, especially when they affect networks, files, credentials, system configuration, or external targets.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

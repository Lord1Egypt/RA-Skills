## Description: <br>
Connect to remote desktops via RDP, VNC, and SSH X11 with secure tunneling and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, sysadmins, and users use this skill to select RDP, VNC, or SSH X11 workflows, build secure tunnels, and troubleshoot remote desktop connections. It also helps save local host profiles with consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote desktop examples can weaken security if users expose RDP or VNC directly or copy diagnostic flags into production use. <br>
Mitigation: Review commands before use, prefer SSH tunnels or VPNs, avoid direct internet exposure, and restrict certificate-bypass flags to tightly controlled diagnostics. <br>
Risk: Commands or saved profiles could leak credentials if users place passwords in command lines or host files. <br>
Mitigation: Do not put real passwords in command lines or saved profiles; use SSH keys, system keyrings, or interactive prompts, and save host profiles only with user consent. <br>
Risk: The anonymous PulseAudio troubleshooting example can open unauthenticated network audio access if copied as-is. <br>
Mitigation: Replace anonymous access with authenticated or tunneled access before using network audio examples. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/remote-desktop) <br>
- [Remote Desktop Homepage](https://clawic.com/skills/remote-desktop) <br>
- [Setup Guide](setup.md) <br>
- [Protocol Details](protocols.md) <br>
- [Troubleshooting Guide](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local markdown host profiles under ~/remote-desktop/ with user consent; does not store passwords.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

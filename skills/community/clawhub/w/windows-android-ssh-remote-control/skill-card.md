## Description: <br>
Setup and guide for full remote control of a Windows PC from an Android device over the internet via SSH tunneling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarbcs1-prog](https://clawhub.ai/user/jarbcs1-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure remote desktop access from an Android device to their own Windows 10/11 Pro or Enterprise PC through an SSH tunnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling remote access can expose a Windows PC to unauthorized access if SSH, firewall, or router settings are misconfigured. <br>
Mitigation: Prefer Tailscale or ZeroTier over public port forwarding, use SSH keys instead of passwords where possible, and review firewall and router changes before applying them. <br>
Risk: Saving Windows credentials on a shared or untrusted Android device can disclose account access. <br>
Mitigation: Avoid saving Windows credentials on shared or untrusted Android devices and install only when configuring access to a PC you own or administer. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/jarbcs1-prog/windows-android-ssh-remote-control) <br>
- [Windows PC Setup for SSH and RDP](references/windows_setup.md) <br>
- [Android Setup for SSH Tunneling and RDP](references/android_setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no hidden automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

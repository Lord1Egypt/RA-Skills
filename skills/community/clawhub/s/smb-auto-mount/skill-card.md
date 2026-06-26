## Description: <br>
Auto-mount Windows SMB shares on Linux with systemd automount. Credentials entered interactively. Required binaries: mount.cifs (cifs-utils), smbclient. Requires sudo. Modifies /etc/fstab and /etc/smb-creds-*.txt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swor-dart](https://clawhub.ai/user/swor-dart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Linux administrators use this skill to discover Windows SMB shares and prepare commands or scripts for one-time CIFS mounts or persistent systemd automount entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to persistent root-level mount changes in /etc/fstab. <br>
Mitigation: Install only after reviewing the exact mount entry, back up /etc/fstab first, and confirm the mount path and credential file path before applying changes. <br>
Risk: SMB passwords may be stored on disk in root-readable credential files. <br>
Mitigation: Use a low-privilege SMB account, keep credential files restricted, and remove or rotate credentials when the mount is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swor-dart/smb-auto-mount) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and script-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include SMB discovery commands, mount commands, and fstab/systemd automount configuration guidance.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

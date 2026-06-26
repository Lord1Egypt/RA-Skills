## Description: <br>
Mount remote storage over SMB/CIFS, FTP, SFTP, or WebDAV as a local directory on Debian/Ubuntu Linux, with user confirmation required before privileged commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leochens](https://clawhub.ai/user/Leochens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to collect remote storage connection details, check Linux dependencies, create mount points, and prepare protocol-specific mount and unmount commands for remote shares. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged package installation and mount commands can affect the host system. <br>
Mitigation: Ask the user to approve sudo commands before execution and install only the package needed for the selected protocol. <br>
Risk: SMB credential-file instructions can expose or leave behind passwords. <br>
Mitigation: Prefer SSH keys or interactive prompts where possible, avoid reusable passwords, restrict credential-file permissions, and remove any SMB credential file immediately after use. <br>
Risk: Mounting untrusted remote storage can expose local files or create unsafe filesystem access. <br>
Mitigation: Mount only trusted servers, use a dedicated mount point, and keep permissions limited to the intended user. <br>


## Reference(s): <br>
- [Remote Disk Mount on ClawHub](https://clawhub.ai/Leochens/remote-disk-mount) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Debian/Ubuntu Linux and user confirmation before sudo commands.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

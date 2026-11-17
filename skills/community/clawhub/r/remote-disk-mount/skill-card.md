## Description:

Mounts remote storage over SMB/CIFS, FTP, SFTP, or WebDAV as a local directory on Debian or Ubuntu Linux, with user confirmation required before privileged commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochens](https://clawhub.ai/user/leochens)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to collect remote storage connection details, install required Linux mount utilities, create a local mount point, and prepare protocol-specific mount or unmount commands. It is intended for Debian and Ubuntu systems where the user can review and approve privileged commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated mount and dependency-install commands can require sudo or otherwise change system-level storage state.

Mitigation: Review the fully expanded command, confirm the target server and mount point, and require explicit user approval before running privileged commands.

Risk: FTP and HTTP WebDAV examples can send data or credentials over cleartext channels.

Mitigation: Prefer SFTP or HTTPS WebDAV, and avoid cleartext FTP or HTTP WebDAV unless the user accepts the network exposure.

Risk: Credential handling can expose passwords if secrets are placed directly in shell commands or long-lived files.

Mitigation: Use interactive prompts, SSH keys, or temporary credential files with strict permissions, and remove sensitive credential files after use.

Risk: Mounting untrusted remote storage can expose local workflows to unexpected or malicious remote content.

Mitigation: Validate the server and mount-point inputs, mount only trusted storage, and inspect protocol-specific options before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Linux-specific command guidance that should be reviewed before execution, especially when sudo, credentials, or cleartext protocols are involved.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

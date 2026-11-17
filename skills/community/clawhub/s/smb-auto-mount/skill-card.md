## Description:

Auto-mount Windows SMB shares on Linux with systemd automount using interactive credential prompts, sudo, cifs-utils, smbclient, /etc/fstab, and /etc/smb-creds-*.txt files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swor-dart](https://clawhub.ai/user/swor-dart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to discover SMB shares, mount them temporarily, or configure persistent on-demand Linux automounts for Windows SMB shares.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts use sudo and can make persistent SMB mount changes in /etc/fstab.

Mitigation: Review the generated mount entries before use and back up /etc/fstab before running the persistent automount script.

Risk: SMB credentials may be stored on disk in /etc/smb-creds-*.txt files.

Mitigation: Restrict credential files to root-only access, remove stale credential files when no longer needed, and avoid shared or automated use without hardening.

Risk: Unsafe handling of user-supplied mount fields or temporary credentials could cause incorrect configuration or credential exposure.

Mitigation: Validate mount fields, add cleanup traps for temporary credential files, and test changes in a controlled environment before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for scripts that require sudo and may modify /etc/fstab and create root-readable SMB credential files.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

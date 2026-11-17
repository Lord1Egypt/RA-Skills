## Description:

Guides agents through safely demoting, rebuilding, cleaning metadata for, reinstalling, rejoining, and re-promoting a Windows Active Directory domain controller VM on Proxmox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:

MIT

## Use Case:

External developers, infrastructure engineers, and administrators use this skill as an operational runbook for rebuilding non-last Windows Active Directory domain controller VMs hosted on Proxmox while preserving directory health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Highly privileged Proxmox API tokens, domain credentials, local Administrator passwords, or DSRM passwords could be exposed through process listings, logs, transcripts, unattend XML, or generated ISO files.

Mitigation: Require TLS validation, avoid insecure curl token examples, pass secrets through QGA stdin, create secret-bearing files only in private locations, delete every copy promptly, and rotate generated local Administrator or DSRM passwords immediately after use.

Risk: Destructive Active Directory cleanup, forced demotion, promotion, or VM disk wipe steps can damage directory state when run against the wrong host or before verification gates are green.

Mitigation: Limit use to trusted administrators, verify replication and FSMO state before and after lifecycle steps, rebuild only one non-last DC at a time, and require explicit human confirmation before destructive AD object deletion, forced demotion, promotion, or disk wipe.

## Reference(s):

- [Credential Handling](references/credential-handling.md)
- [Demotion](references/demotion.md)
- [Gotchas](references/gotchas.md)
- [Metadata Cleanup](references/metadata-cleanup.md)
- [OS Reinstall](references/os-reinstall.md)
- [Promotion](references/promotion.md)
- [QGA Execution](references/qga-execution.md)
- [Verification](references/verification.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, PowerShell, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces stepwise operational guidance with verification gates and human confirmation points for destructive actions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

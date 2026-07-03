## Description: <br>
Safely rebuild an additional Windows Active Directory domain controller VM on Proxmox by demoting it, cleaning AD metadata, reinstalling Windows via autounattend, and re-promoting it with verification gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to guide one-at-a-time rebuilds of non-last Windows AD domain controller VMs on Proxmox, including AD health verification, QGA execution, metadata cleanup, OS reinstall, and replica promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged Proxmox and Active Directory operations can disrupt directory service or wipe the wrong VM if applied to the wrong target. <br>
Mitigation: Fill in the environment config carefully, verify VM IDs, FSMO ownership, replication, and AD state before each phase, and require human confirmation before AD object deletion or disk wipe steps. <br>
Risk: Credentials used for domain administration or DSRM setup can be exposed through process arguments, logs, or temporary files. <br>
Mitigation: Provide credentials only through the documented stdin path, avoid command-line secrets, delete temporary carriers immediately, and rotate or hand off generated break-glass values after the rebuild. <br>
Risk: Proceeding when a verification gate is not green can compound an existing AD failure. <br>
Mitigation: Stop when replication, FSMO, guest-agent, SYSVOL, or DC promotion checks fail, diagnose the failed gate, and change only one domain controller at a time. <br>


## Reference(s): <br>
- [QGA Execution](references/qga-execution.md) <br>
- [Verification](references/verification.md) <br>
- [Demotion](references/demotion.md) <br>
- [Metadata cleanup](references/metadata-cleanup.md) <br>
- [OS reinstall](references/os-reinstall.md) <br>
- [Promotion](references/promotion.md) <br>
- [Gotchas](references/gotchas.md) <br>
- [Credential handling](references/credential-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operational guidance requires human confirmation before destructive Active Directory or VM disk operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

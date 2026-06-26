## Description: <br>
Reads server hardware, Proxmox and Linux OS information, temperatures, SMART status, ECC errors, RAID, disks, network statistics, services, and logs without making changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polumish](https://clawhub.ai/user/polumish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to guide read-oriented diagnostics for Proxmox VE and Linux servers over SSH, then review hardware, storage, network, service, log, and security findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses root SSH commands against target servers. <br>
Mitigation: Install and use it only when you administer the target systems, verify the host before execution, and supervise each command. <br>
Risk: Audit output can expose sensitive infrastructure, service, log, disk, network, and authentication details. <br>
Mitigation: Treat generated output as sensitive operational data and store or share it only in approved locations. <br>
Risk: A report-saving step can conflict with the read-only audit framing. <br>
Mitigation: Run only the listed diagnostics unless you intentionally choose to save a report, and confirm the path, permissions, and overwrite behavior first. <br>


## Reference(s): <br>
- [Linux Audit Prompt](artifact/references/linux-audit.md) <br>
- [Proxmox Audit Prompt](artifact/references/proxmox-audit.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/polumish/server-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with SSH command blocks and diagnostic commentary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive infrastructure details from server audit output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

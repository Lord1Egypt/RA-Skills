## Description: <br>
Configure Linux swap by creating or resizing swap files, setting swappiness, persisting changes in fstab, and verifying swap state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjxylc](https://clawhub.ai/user/zjxylc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect Linux swap status, add or resize a swap file, tune swappiness, and persist swap configuration across reboots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes root-level commands that change active swap, /etc/fstab, and sysctl configuration. <br>
Mitigation: Review current swap and configuration state first, back up /etc/fstab and /etc/sysctl.conf, and confirm each command before applying it. <br>
Risk: Disabling swap during resizing can affect production or low-memory systems. <br>
Mitigation: Confirm available memory headroom and schedule changes during an appropriate maintenance window before running swapoff. <br>
Risk: Duplicate or incorrect persistence entries can affect boot-time swap behavior. <br>
Mitigation: Check existing /etc/fstab and sysctl entries before appending new lines, then verify swap status after changes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zjxylc/swap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target Linux systems and may require sudo privileges for swap, fstab, and sysctl changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

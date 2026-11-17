## Description:

Split Large Partitions Without Data Loss - Divide oversized partitions into cleaner layouts for system, data, and backup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hezhaoyun](https://clawhub.ai/user/hezhaoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to plan and launch workflows for splitting oversized Windows partitions into system, data, or backup areas while preserving existing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs EaseUS Partition Master through a silent installer.

Mitigation: Confirm the installer is intentionally wanted, prefer a manual vendor download, and inspect publisher or signature details before running it.

Risk: Partition-management actions can affect system-wide disk state and stored data.

Mitigation: Keep a verified backup, review the operation preview, and avoid elevated execution unless the disk and installation impact is understood.

Risk: The launcher can pass broad disk-tool commands to EPMUI.exe.

Mitigation: Confirm the target disk, partition letters, capacity changes, and requested shell command before applying any write operation.

## Reference(s):

- [EaseUS Partition Master](https://www.easeus.com/partition-manager/)
- [EaseUS Partition Master Free Download](https://down.easeus.com/product/epm_free?source=skills&dest=split-drive-coach)
- [Split Drive Coach on ClawHub](https://clawhub.ai/hezhaoyun/skills/split-drive-coach)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with Windows command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 10+ guidance for EaseUS Partition Master installation, launch, pre-checks, and troubleshooting.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

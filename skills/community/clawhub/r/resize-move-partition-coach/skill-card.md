## Description:

Resize or Move Partitions for Low Space - Reclaim drive capacity when unallocated space is limited or non-adjacent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hezhaoyun](https://clawhub.ai/user/hezhaoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan Windows partition resize and move workflows when C: drive space is low, unallocated space is non-adjacent, or capacity must be borrowed from another partition. It provides guidance and commands for installing and launching EaseUS Partition Master resize workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and launches a third-party disk partition tool with broad system-changing authority.

Mitigation: Run it only when EaseUS Partition Master is intentionally required, review the skill before installation, and prefer manually downloading and verifying the vendor installer.

Risk: Partition resize or move operations can alter disks and make data unavailable if misused.

Mitigation: Confirm the target disk, partition letters, operation preview, and expected capacity changes before executing any partition operation.

Risk: Silent or elevated installer execution can reduce user review before system changes.

Mitigation: Avoid silent or elevated execution unless necessary, and approve administrative prompts only after confirming the installer source and intended workflow.

Risk: The generic shell command helper can launch operations beyond a clearly understood resize or move workflow.

Mitigation: Use the shell command helper only for explicit, reviewed resize or move actions with known parameters.

## Reference(s):

- [EaseUS Partition Master](https://www.easeus.com/partition-manager/)
- [EaseUS Partition Master Free Download](https://down.easeus.com/product/epm_free?source=skills&dest=resize-move-partition-coach)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline Windows command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows 10+ partition workflow guidance, installer launch commands, and troubleshooting checks.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Resize or Move Partitions for Low Space - Reclaim drive capacity when unallocated space is limited or non-adjacent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hezhaoyun](https://clawhub.ai/user/hezhaoyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to plan Windows partition resize or move workflows when C: drive space is low, unallocated space is non-adjacent, or free capacity must be allocated from another partition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and silently install third-party partition-management software. <br>
Mitigation: Require visible user confirmation before installation, use a trusted source URL, verify a pinned checksum or signature, and document rollback or uninstall steps before execution. <br>
Risk: Partition resize or move workflows can change disk layout if executed without confirming the proposed operation. <br>
Mitigation: Use the preview-first workflow, confirm the target disk and partition letters, and execute only after the capacity and target partition match the user's intent. <br>


## Reference(s): <br>
- [EaseUS Partition Manager](https://www.easeus.com/partition-manager/) <br>
- [ClawHub Skill Page](https://clawhub.ai/hezhaoyun/resize-move-partition-coach) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Windows command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preview-first workflow guidance and troubleshooting steps for Windows 10+.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Trash management with index tracking for all agents. Use when deleting files to ensure proper index registration and 7-day auto-cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas260514](https://clawhub.ai/user/lucas260514) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route file deletion through a shared trash manager with index tracking, restore support, and scheduled cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents receive broad authority to route deletions through a shared trash area. <br>
Mitigation: Require explicit confirmation before trashing important or user-owned files, and review each target path before running the add command. <br>
Risk: The recommended cleanup flow can permanently remove trashed files after 7 days. <br>
Mitigation: Use dry-run cleanup first, review the trash index and logs, and only enable scheduled cleanup where the retention policy is acceptable. <br>
Risk: The skill depends on the behavior of ~/.openclaw/scripts/trash-manager.sh. <br>
Mitigation: Verify the installed script's behavior before broad use and test list and restore operations before relying on automated cleanup. <br>


## Reference(s): <br>
- [Trash Manager on ClawHub](https://clawhub.ai/lucas260514/trash-manager) <br>
- [Publisher profile](https://clawhub.ai/user/lucas260514) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 according to server-resolved metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

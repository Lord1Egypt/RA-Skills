## Description: <br>
泉水复活 is a QClaw memory backup and restore skill that creates local backups, timestamped snapshots, cloud-sync copies, and integrity checks for AI-user interaction memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzxy1](https://clawhub.ai/user/xzxy1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QClaw users use this skill to preserve and recover workspace memory files, including long-term memory, user profile, identity, diary, and daily memory files. It is intended for deliberate backup, snapshot, cloud-sync, restore, and integrity-check workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill backs up sensitive QClaw memory, diary, identity, user-profile, and workspace-rule files into persistent local and cloud-synced storage. <br>
Mitigation: Use it only for intentional memory backup workflows, configure the cloud path before use, and avoid backing up secrets unless the storage is controlled and trusted. <br>
Risk: Restore operations can overwrite workspace files, and the scanner notes an unsafe restore path until ZIP path validation and stronger overwrite protections are added. <br>
Mitigation: Restore only snapshots you personally created and review the selected snapshot before allowing restore actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xzxy1/spring-fountain-revival) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file-based backup artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup directories, timestamped ZIP snapshots, cloud-synced copies, integrity-check messages, and restore actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
What At Home records household belongings in a suite-room-furniture-item structure so users can find, move, back up, restore, and export home inventory records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yixj](https://clawhub.ai/user/yixj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain local household inventory records, locate belongings, reorganize items, and create backups or exports during moving, decluttering, or daily home management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household belongings and locations in local inventory, backup, and export files. <br>
Mitigation: Keep workspace data, backup files, and export files private unless they have been reviewed for sensitive household details. <br>
Risk: Delete, move, merge, and restore operations can change saved inventory records. <br>
Mitigation: Create or verify a backup before destructive changes, and confirm restore timestamps and delete targets before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yixj/what-at-home) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Chinese README](artifact/README_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown-style responses, plus JSON inventory, backup, and export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local inventory data to {workspace}/data/home_storage.json and backups or exports under {workspace}/data/backups/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

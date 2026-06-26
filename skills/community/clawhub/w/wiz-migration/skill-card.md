## Description: <br>
为知笔记迁移辅助技能，提供自动检测存储目录、导出操作引导、附件批量迁移等完整迁移流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awamwang](https://clawhub.ai/user/awamwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to migrate Wiz Note data by detecting local data folders, generating an export guide, and copying attachment directories into a target location. It is intended for user-supervised note migration where original data is backed up before copying. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Windows batch-script path can execute caller-supplied scripts with user privileges. <br>
Mitigation: Prefer the Python copy path without script_path; inspect and trust any batch script before running it. <br>
Risk: Incorrect source or destination folders can produce incomplete or misplaced note attachments during migration. <br>
Mitigation: Choose precise Wiz source and destination folders and keep a backup of the original notes until the migration is verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/awamwang/wiz-migration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python API responses, and shell or batch command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a generated Markdown export guide and copy attachment files when the migration helper is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

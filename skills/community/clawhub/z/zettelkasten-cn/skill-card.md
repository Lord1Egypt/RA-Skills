## Description: <br>
卢曼卡片学习法（Zettelkasten）全生命周期管理系统，支持九大人生领域分类、撤销操作、交互式创建流程。处理闪念笔记、文献笔记、永久笔记、项目笔记的增删改查，以及与Agent记忆系统的双向关联。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WittFan](https://clawhub.ai/user/WittFan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage a local Zettelkasten-style personal knowledge base, including creating, searching, updating, linking, converting, and undoing operations across fleeting, literature, permanent, project, and map notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages local files and includes undo behavior; tampered or misused operation history can move or overwrite files outside the intended notes folder. <br>
Mitigation: Use a dedicated cards directory, keep backups, and avoid running undo after manually editing operation-history files. <br>
Risk: Running the skill through an agent with broad filesystem access increases the impact of path or environment misuse. <br>
Mitigation: Review the skill before installation in broad-access environments and do not expose ZETTELKASTEN_SKILL_DIR to untrusted values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/WittFan/zettelkasten-cn) <br>
- [卡片学习法 - 高级功能](references/advanced.md) <br>
- [Configuration Reference](references/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-backed configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and manages local Markdown note files and operation-history records in user-controlled directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and references/config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
研发经理助手 helps R&D managers generate standup and weekly reports, Git activity summaries, code review checklists, project progress notes, and task allocation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminjun](https://clawhub.ai/user/wangminjun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
R&D managers and engineering leads use this skill to prepare recurring project reports, summarize repository activity, create code review checklists, monitor project status, and draft task allocation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local scripts against selected repositories and team configuration files. <br>
Mitigation: Confirm the target repository, configuration file, and command arguments before execution. <br>
Risk: Git statistics collection may change the selected repository's checked-out branch. <br>
Mitigation: Run the tool only on an intended working copy and confirm there is no uncommitted work before collecting statistics. <br>
Risk: Report and checklist tools can overwrite files at chosen output paths. <br>
Mitigation: Use explicit output paths and review existing files before generating reports. <br>
Risk: Generated reports may contain sensitive internal project, repository, or team information. <br>
Mitigation: Treat generated reports as internal documents and review content before sharing. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wangminjun/rdm-assistant) <br>
- [README.md](README.md) <br>
- [代码审查检查清单](docs/代码审查检查清单.md) <br>
- [晨会报告模板](templates/晨会报告模板.md) <br>
- [项目周报模板](templates/项目周报模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, shell command output, configuration guidance, and checklist text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include repository activity, team information, project risks, and review notes supplied through local configuration and command inputs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

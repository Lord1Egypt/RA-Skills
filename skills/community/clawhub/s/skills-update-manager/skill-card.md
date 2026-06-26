## Description: <br>
管理已安装技能的注册、版本跟踪与自动更新检查；当用户安装新技能、检查技能更新或配置更新策略时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chsengni](https://clawhub.ai/user/chsengni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register installed skills, track versions, configure update checks, and review available updates before installing or updating skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist changes in a shared MEMORY.md file. <br>
Mitigation: Inspect MEMORY.md after first use and keep update-check configuration explicit. <br>
Risk: The skill can contact remote update URLs and guide clone or download update steps. <br>
Mitigation: Provide only trusted update URLs and approve any clone or download step separately after reviewing the source. <br>


## Reference(s): <br>
- [Registry Format Reference](references/registry_format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chsengni/skills-update-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or updates of skills_registry.json and MEMORY.md configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
